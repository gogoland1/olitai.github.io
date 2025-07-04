// 🌊 Dashboard CTD - JavaScript Principal
// Sistema interactivo de perfiles oceanográficos

class CTDDashboard {
    constructor() {
        this.currentProfile = null;
        this.environments = {};
        this.compositionChart = null;
        this.currentView = 'temperature';
        
        // Configuración de colores
        this.colors = {
            fjord: '#2E8B57',
            delta: '#8B4513', 
            coastal: '#4682B4',
            oceanic: '#191970',
            mixed: '#800080'
        };
        
        // Inicializar dashboard
        this.init();
    }
    
    async init() {
        console.log('🌊 Inicializando Dashboard CTD...');
        
        try {
            // Cargar información de ambientes
            await this.loadEnvironments();
            
            // Configurar event listeners
            this.setupEventListeners();
            
            // Cargar perfil inicial
            await this.updateProfile();
            
            // Inicializar gráfico de composición
            this.initCompositionChart();
            
            console.log('✅ Dashboard inicializado correctamente');
            
        } catch (error) {
            console.error('❌ Error inicializando dashboard:', error);
            this.showError('Error al inicializar el dashboard');
        }
    }
    
    async loadEnvironments() {
        const response = await fetch('/api/environments');
        this.environments = await response.json();
        console.log('📊 Ambientes cargados:', Object.keys(this.environments));
    }
    
    setupEventListeners() {
        // Sliders de ambiente
        document.querySelectorAll('.environment-slider').forEach(slider => {
            slider.addEventListener('input', (e) => {
                this.updateSliderValue(e.target);
                this.updateProfile();
            });
        });
        
        // Slider de profundidad
        document.getElementById('depthSlider').addEventListener('input', (e) => {
            document.getElementById('depthValue').textContent = e.target.value + 'm';
            this.updateProfile();
        });
        
        // Botones preset
        document.querySelectorAll('.preset-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const preset = e.target.dataset.preset;
                this.setPreset(preset);
            });
        });
        
        // Botón reset
        document.getElementById('resetBtn').addEventListener('click', () => {
            this.resetSliders();
        });
        
        // Botones de vista de perfil
        document.querySelectorAll('input[name="profileView"]').forEach(radio => {
            radio.addEventListener('change', (e) => {
                this.currentView = e.target.id.replace('View', '');
                this.updateProfilePlot();
            });
        });
    }
    
    updateSliderValue(slider) {
        const env = slider.dataset.env;
        const value = parseInt(slider.value);
        const valueSpan = document.getElementById(env + 'Value');
        
        valueSpan.textContent = value + '%';
        
        // Normalizar otros sliders para que sumen 100%
        this.normalizeSliders(env, value);
    }
    
    normalizeSliders(changedEnv, newValue) {
        const sliders = document.querySelectorAll('.environment-slider');
        const otherSliders = Array.from(sliders).filter(s => s.dataset.env !== changedEnv);
        
        const remainingValue = 100 - newValue;
        const otherCount = otherSliders.length;
        
        if (remainingValue >= 0 && otherCount > 0) {
            const valuePerOther = Math.floor(remainingValue / otherCount);
            const remainder = remainingValue % otherCount;
            
            otherSliders.forEach((slider, index) => {
                const value = valuePerOther + (index < remainder ? 1 : 0);
                slider.value = value;
                const env = slider.dataset.env;
                document.getElementById(env + 'Value').textContent = value + '%';
            });
        }
    }
    
    setPreset(preset) {
        const presets = {
            fjord: { fjord: 100, delta: 0, coastal: 0, oceanic: 0 },
            delta: { fjord: 0, delta: 100, coastal: 0, oceanic: 0 },
            coastal: { fjord: 0, delta: 0, coastal: 100, oceanic: 0 },
            oceanic: { fjord: 0, delta: 0, coastal: 0, oceanic: 100 }
        };
        
        const values = presets[preset];
        if (values) {
            Object.keys(values).forEach(env => {
                const slider = document.getElementById(env + 'Slider');
                const valueSpan = document.getElementById(env + 'Value');
                
                slider.value = values[env];
                valueSpan.textContent = values[env] + '%';
            });
            
            // Actualizar indicadores visuales
            document.querySelectorAll('.preset-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            document.querySelector(`[data-preset="${preset}"]`).classList.add('active');
            
            this.updateProfile();
        }
    }
    
    resetSliders() {
        const sliders = document.querySelectorAll('.environment-slider');
        sliders.forEach(slider => {
            slider.value = 25;
            const env = slider.dataset.env;
            document.getElementById(env + 'Value').textContent = '25%';
        });
        
        document.getElementById('depthSlider').value = 500;
        document.getElementById('depthValue').textContent = '500m';
        
        document.querySelectorAll('.preset-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        this.updateProfile();
    }
    
    async updateProfile() {
        try {
            this.showLoading(true);
            
            // Obtener valores actuales
            const weights = this.getCurrentWeights();
            const maxDepth = parseInt(document.getElementById('depthSlider').value);
            
            // Solicitar perfil mixto
            const response = await fetch('/api/mixed_profile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    fjord_weight: weights.fjord / 100,
                    delta_weight: weights.delta / 100,
                    coastal_weight: weights.coastal / 100,
                    oceanic_weight: weights.oceanic / 100,
                    max_depth: maxDepth
                })
            });
            
            this.currentProfile = await response.json();
            
            // Actualizar visualizaciones
            this.updateProfilePlot();
            this.updateStatistics();
            this.updateEnvironmentInfo();
            this.updateCompositionChart();
            this.updateTSPlot();
            
            this.showLoading(false);
            
        } catch (error) {
            console.error('❌ Error actualizando perfil:', error);
            this.showError('Error al actualizar el perfil');
            this.showLoading(false);
        }
    }
    
    getCurrentWeights() {
        return {
            fjord: parseInt(document.getElementById('fjordSlider').value),
            delta: parseInt(document.getElementById('deltaSlider').value),
            coastal: parseInt(document.getElementById('coastalSlider').value),
            oceanic: parseInt(document.getElementById('oceanicSlider').value)
        };
    }
    
    updateProfilePlot() {
        if (!this.currentProfile) return;
        
        const profile = this.currentProfile;
        const traces = [];
        
        // Crear trazas según la vista seleccionada
        if (this.currentView === 'temperature' || this.currentView === 'all') {
            traces.push({
                x: profile.temperature,
                y: profile.depths.map(d => -d),
                mode: 'lines',
                name: 'Temperatura (°C)',
                line: { color: '#dc3545', width: 3 },
                hovertemplate: '<b>Temperatura</b><br>%{x:.1f}°C<br>Profundidad: %{y:.0f}m<extra></extra>'
            });
        }
        
        if (this.currentView === 'salinity' || this.currentView === 'all') {
            traces.push({
                x: profile.salinity,
                y: profile.depths.map(d => -d),
                mode: 'lines',
                name: 'Salinidad (PSU)',
                line: { color: '#0dcaf0', width: 3 },
                yaxis: this.currentView === 'all' ? 'y' : 'y',
                xaxis: this.currentView === 'all' ? 'x2' : 'x',
                hovertemplate: '<b>Salinidad</b><br>%{x:.1f} PSU<br>Profundidad: %{y:.0f}m<extra></extra>'
            });
        }
        
        if (this.currentView === 'oxygen' || this.currentView === 'all') {
            traces.push({
                x: profile.oxygen,
                y: profile.depths.map(d => -d),
                mode: 'lines',
                name: 'Oxígeno (μmol/L)',
                line: { color: '#198754', width: 3 },
                yaxis: this.currentView === 'all' ? 'y' : 'y',
                xaxis: this.currentView === 'all' ? 'x3' : 'x',
                hovertemplate: '<b>Oxígeno</b><br>%{x:.0f} μmol/L<br>Profundidad: %{y:.0f}m<extra></extra>'
            });
        }
        
        // Configurar layout
        const layout = {
            title: `Perfil CTD - ${profile.dominant_environment}`,
            xaxis: { 
                title: this.getXAxisTitle(),
                side: 'top'
            },
            yaxis: { 
                title: 'Profundidad (m)',
                autorange: 'reversed'
            },
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { color: 'white' },
            showlegend: this.currentView === 'all',
            margin: { l: 60, r: 60, t: 80, b: 60 }
        };
        
        // Layout para vista múltiple
        if (this.currentView === 'all') {
            layout.xaxis2 = {
                title: 'Salinidad (PSU)',
                overlaying: 'x',
                side: 'top',
                position: 0.85
            };
            layout.xaxis3 = {
                title: 'Oxígeno (μmol/L)',
                overlaying: 'x',
                side: 'top',
                position: 0.95
            };
        }
        
        // Agregar líneas de referencia de profundidad
        const shapes = this.getDepthReferenceLines(profile.max_depth);
        layout.shapes = shapes;
        
        const config = {
            responsive: true,
            displayModeBar: true,
            modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
            displaylogo: false
        };
        
        Plotly.newPlot('profilesPlot', traces, layout, config);
    }
    
    getXAxisTitle() {
        const titles = {
            temperature: 'Temperatura (°C)',
            salinity: 'Salinidad (PSU)',
            oxygen: 'Oxígeno (μmol/L)',
            all: 'Variables Oceanográficas'
        };
        return titles[this.currentView] || 'Valor';
    }
    
    getDepthReferenceLines(maxDepth) {
        const references = [
            { depth: 50, label: '50m', color: 'rgba(255,255,255,0.3)' },
            { depth: 100, label: '100m', color: 'rgba(255,255,255,0.4)' },
            { depth: 200, label: '200m', color: 'rgba(255,255,255,0.3)' },
            { depth: 500, label: '500m', color: 'rgba(255,255,255,0.4)' },
            { depth: 1000, label: '1000m', color: 'rgba(255,255,255,0.3)' }
        ];
        
        return references
            .filter(ref => ref.depth < maxDepth)
            .map(ref => ({
                type: 'line',
                x0: 0,
                x1: 1,
                xref: 'paper',
                y0: -ref.depth,
                y1: -ref.depth,
                line: {
                    color: ref.color,
                    width: 1,
                    dash: 'dash'
                }
            }));
    }
    
    updateStatistics() {
        if (!this.currentProfile) return;
        
        const profile = this.currentProfile;
        
        // Calcular estadísticas
        const tempMean = this.calculateMean(profile.temperature);
        const salMean = this.calculateMean(profile.salinity);
        const oxyMean = this.calculateMean(profile.oxygen);
        
        // Estratificación (diferencia superficie-fondo)
        const tempStrat = profile.temperature[0] - profile.temperature[profile.temperature.length - 1];
        
        // Actualizar DOM
        document.getElementById('tempMean').textContent = tempMean.toFixed(1);
        document.getElementById('salMean').textContent = salMean.toFixed(1);
        document.getElementById('oxyMean').textContent = Math.round(oxyMean);
        document.getElementById('stratification').textContent = tempStrat.toFixed(1);
    }
    
    calculateMean(array) {
        return array.reduce((sum, val) => sum + val, 0) / array.length;
    }
    
    updateEnvironmentInfo() {
        if (!this.currentProfile) return;
        
        const profile = this.currentProfile;
        const weights = this.getCurrentWeights();
        
        // Ambiente dominante
        const dominantEnv = Object.keys(weights).reduce((a, b) => 
            weights[a] > weights[b] ? a : b
        );
        
        const envNames = {
            fjord: 'Fiordo Patagónico',
            delta: 'Delta de Río',
            coastal: 'Ambiente Costero',
            oceanic: 'Océano Abierto'
        };
        
        const envDescriptions = {
            fjord: 'Características de fiordo con aguas frías estratificadas y fuerte haloclina.',
            delta: 'Influencia fluvial con gradientes salinos pronunciados y alta variabilidad.',
            coastal: 'Ambiente costero con influencia terrestre y termoclina estacional.',
            oceanic: 'Masas de agua oceánicas con termoclina profunda y estructura vertical compleja.'
        };
        
        document.getElementById('dominantEnvName').textContent = envNames[dominantEnv];
        document.getElementById('dominantEnvDesc').textContent = 
            `Ambiente dominante (${weights[dominantEnv]}%): ${envDescriptions[dominantEnv]}`;
    }
    
    initCompositionChart() {
        const ctx = document.getElementById('compositionChart').getContext('2d');
        
        this.compositionChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Fiordo', 'Delta', 'Costero', 'Oceánico'],
                datasets: [{
                    data: [25, 25, 25, 25],
                    backgroundColor: [
                        this.colors.fjord,
                        this.colors.delta,
                        this.colors.coastal,
                        this.colors.oceanic
                    ],
                    borderWidth: 2,
                    borderColor: 'rgba(255, 255, 255, 0.8)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: 'white',
                            font: { size: 10 }
                        }
                    }
                }
            }
        });
    }
    
    updateCompositionChart() {
        if (!this.compositionChart) return;
        
        const weights = this.getCurrentWeights();
        this.compositionChart.data.datasets[0].data = [
            weights.fjord,
            weights.delta,
            weights.coastal,
            weights.oceanic
        ];
        this.compositionChart.update();
    }
    
    async updateTSPlot() {
        if (!this.currentProfile) return;
        
        const profile = this.currentProfile;
        
        const trace = {
            x: profile.salinity,
            y: profile.temperature,
            mode: 'markers+lines',
            name: 'Perfil T-S',
            marker: {
                color: profile.depths,
                colorscale: 'Viridis_r',
                size: 8,
                colorbar: {
                    title: 'Profundidad (m)',
                    titlefont: { color: 'white' },
                    tickfont: { color: 'white' }
                },
                showscale: true
            },
            line: { color: this.colors.mixed, width: 2 },
            hovertemplate: '<b>Diagrama T-S</b><br>' +
                         'Salinidad: %{x:.1f} PSU<br>' +
                         'Temperatura: %{y:.1f}°C<extra></extra>'
        };
        
        const layout = {
            title: 'Diagrama Temperatura-Salinidad',
            xaxis: { 
                title: 'Salinidad (PSU)',
                color: 'white'
            },
            yaxis: { 
                title: 'Temperatura (°C)',
                color: 'white'
            },
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { color: 'white' },
            margin: { l: 60, r: 60, t: 60, b: 60 }
        };
        
        const config = {
            responsive: true,
            displayModeBar: false
        };
        
        Plotly.newPlot('tsPlot', [trace], layout, config);
    }
    
    showLoading(show) {
        const elements = ['profilesPlot', 'tsPlot', 'statsContainer'];
        
        elements.forEach(id => {
            const element = document.getElementById(id);
            if (show) {
                element.style.opacity = '0.5';
                element.style.pointerEvents = 'none';
            } else {
                element.style.opacity = '1';
                element.style.pointerEvents = 'auto';
            }
        });
    }
    
    showError(message) {
        // Crear toast de error
        const toast = document.createElement('div');
        toast.className = 'alert alert-danger alert-dismissible fade show';
        toast.style.position = 'fixed';
        toast.style.top = '20px';
        toast.style.right = '20px';
        toast.style.zIndex = '9999';
        toast.innerHTML = `
            <i class="fas fa-exclamation-triangle"></i> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(toast);
        
        // Auto-remover después de 5 segundos
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 5000);
    }
}

// Inicializar dashboard cuando se carga la página
document.addEventListener('DOMContentLoaded', () => {
    window.ctdDashboard = new CTDDashboard();
});

// Funciones de utilidad globales
window.downloadProfile = function() {
    if (!window.ctdDashboard.currentProfile) {
        alert('No hay perfil disponible para descargar');
        return;
    }
    
    const profile = window.ctdDashboard.currentProfile;
    const weights = window.ctdDashboard.getCurrentWeights();
    
    const data = {
        timestamp: new Date().toISOString(),
        environment_weights: weights,
        max_depth: profile.max_depth,
        dominant_environment: profile.dominant_environment,
        profile_data: {
            depths: profile.depths,
            temperature: profile.temperature,
            salinity: profile.salinity,
            oxygen: profile.oxygen
        }
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ctd_profile_${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
};

// Exportar imagen del perfil
window.exportProfileImage = function() {
    Plotly.downloadImage('profilesPlot', {
        format: 'png',
        width: 1200,
        height: 800,
        filename: `ctd_profile_${new Date().toISOString().split('T')[0]}`
    });
};