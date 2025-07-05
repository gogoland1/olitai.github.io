// Three.js Ocean Simulator Component
class ThreeJSOceanSimulator {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.organisms = [];
        this.oceanMesh = null;
        this.lightSources = [];
        this.animationId = null;
        this.isAnimating = false;
        
        this.init();
    }
    
    init() {
        // Crear escena
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x001122);
        
        // Configurar cámara
        this.camera = new THREE.PerspectiveCamera(
            75,
            this.container.clientWidth / this.container.clientHeight,
            0.1,
            3000
        );
        this.camera.position.set(100, 50, 200);
        
        // Configurar renderer
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.container.appendChild(this.renderer.domElement);
        
        // Controles de órbita
        this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        
        // Crear océano base
        this.createOcean();
        
        // Configurar iluminación
        this.setupLighting();
        
        // Inicializar organismos
        this.createOrganisms();
        
        // Iniciar renderizado
        this.animate();
        
        // Responsividad
        window.addEventListener('resize', () => this.onWindowResize());
    }
    
    createOcean() {
        // Geometría del océano con gradiente vertical
        const geometry = new THREE.BoxGeometry(200, 2000, 200, 10, 100, 10);
        
        // Shader material para gradiente de profundidad
        const vertexShader = `
            varying vec3 vPosition;
            varying float vDepth;
            
            void main() {
                vPosition = position;
                vDepth = -position.y / 1000.0; // Normalizar profundidad
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }
        `;
        
        const fragmentShader = `
            uniform float time;
            uniform vec3 surfaceColor;
            uniform vec3 deepColor;
            uniform float lightAttenuation;
            
            varying vec3 vPosition;
            varying float vDepth;
            
            void main() {
                // Gradiente de color por profundidad
                vec3 color = mix(surfaceColor, deepColor, clamp(vDepth, 0.0, 1.0));
                
                // Atenuación de luz
                float lightFactor = exp(-lightAttenuation * vDepth);
                color *= lightFactor;
                
                // Transparencia variable
                float alpha = 0.3 + 0.4 * vDepth;
                
                gl_FragColor = vec4(color, alpha);
            }
        `;
        
        const material = new THREE.ShaderMaterial({
            uniforms: {
                time: { value: 0.0 },
                surfaceColor: { value: new THREE.Color(0x87CEEB) },
                deepColor: { value: new THREE.Color(0x000080) },
                lightAttenuation: { value: 0.05 }
            },
            vertexShader: vertexShader,
            fragmentShader: fragmentShader,
            transparent: true,
            side: THREE.DoubleSide
        });
        
        this.oceanMesh = new THREE.Mesh(geometry, material);
        this.oceanMesh.position.y = -1000; // Centrar verticalmente
        this.scene.add(this.oceanMesh);
    }
    
    setupLighting() {
        // Luz ambiental
        const ambientLight = new THREE.AmbientLight(0x404040, 0.3);
        this.scene.add(ambientLight);
        
        // Luz solar (direccional)
        const sunLight = new THREE.DirectionalLight(0xffffff, 1.0);
        sunLight.position.set(100, 100, 50);
        sunLight.castShadow = true;
        sunLight.shadow.mapSize.width = 2048;
        sunLight.shadow.mapSize.height = 2048;
        this.scene.add(sunLight);
        this.lightSources.push(sunLight);
        
        // Luces espectrales para atenuación
        const spectralColors = [
            { color: 0xff0000, intensity: 0.8, attenuation: 0.45 }, // Rojo
            { color: 0xff6500, intensity: 0.7, attenuation: 0.25 }, // Naranja
            { color: 0xffff00, intensity: 0.6, attenuation: 0.15 }, // Amarillo
            { color: 0x00ff00, intensity: 0.5, attenuation: 0.08 }, // Verde
            { color: 0x0000ff, intensity: 0.4, attenuation: 0.05 }, // Azul
        ];
        
        spectralColors.forEach((spec, index) => {
            const light = new THREE.PointLight(spec.color, spec.intensity, 1000);
            light.position.set(-80 + index * 40, 10, 0);
            this.scene.add(light);
            this.lightSources.push({ light, attenuation: spec.attenuation });
        });
    }
    
    createOrganisms() {
        this.organisms = [];
        
        // Crear diferentes tipos de organismos
        this.createPhytoplankton();
        this.createZooplankton();
        this.createBacteria();
        this.createFecalPellets();
    }
    
    createPhytoplankton() {
        const geometry = new THREE.SphereGeometry(0.5, 8, 6);
        const material = new THREE.MeshPhongMaterial({ 
            color: 0x22c55e,
            emissive: 0x002200,
            shininess: 100
        });
        
        for (let i = 0; i < 100; i++) {
            const mesh = new THREE.Mesh(geometry, material);
            
            // Distribución exponencial cerca de superficie
            const depth = -Math.random() * 100;
            mesh.position.set(
                (Math.random() - 0.5) * 180,
                depth,
                (Math.random() - 0.5) * 180
            );
            
            mesh.userData = {
                type: 'phytoplankton',
                originalY: depth,
                floatSpeed: Math.random() * 0.5 + 0.1,
                phase: Math.random() * Math.PI * 2
            };
            
            this.scene.add(mesh);
            this.organisms.push(mesh);
        }
    }
    
    createZooplankton() {
        const geometry = new THREE.ConeGeometry(1, 2, 6);
        const material = new THREE.MeshPhongMaterial({ 
            color: 0xf97316,
            shininess: 50
        });
        
        for (let i = 0; i < 50; i++) {
            const mesh = new THREE.Mesh(geometry, material);
            
            const depth = -Math.random() * 300 - 50;
            mesh.position.set(
                (Math.random() - 0.5) * 160,
                depth,
                (Math.random() - 0.5) * 160
            );
            
            mesh.userData = {
                type: 'zooplankton',
                originalY: depth,
                migrationSpeed: Math.random() * 2 + 1,
                phase: Math.random() * Math.PI * 2
            };
            
            this.scene.add(mesh);
            this.organisms.push(mesh);
        }
    }
    
    createBacteria() {
        const geometry = new THREE.SphereGeometry(0.2, 6, 4);
        const material = new THREE.MeshBasicMaterial({ 
            color: 0x8b5cf6,
            transparent: true,
            opacity: 0.7
        });
        
        for (let i = 0; i < 200; i++) {
            const mesh = new THREE.Mesh(geometry, material);
            
            const depth = -Math.random() * 1800 - 200;
            mesh.position.set(
                (Math.random() - 0.5) * 190,
                depth,
                (Math.random() - 0.5) * 190
            );
            
            mesh.userData = {
                type: 'bacteria',
                originalY: depth,
                wobbleSpeed: Math.random() * 1 + 0.5,
                phase: Math.random() * Math.PI * 2
            };
            
            this.scene.add(mesh);
            this.organisms.push(mesh);
        }
    }
    
    createFecalPellets() {
        const geometry = new THREE.CylinderGeometry(0.3, 0.5, 1.5, 6);
        const material = new THREE.MeshLambertMaterial({ 
            color: 0x78716c,
            transparent: true,
            opacity: 0.8
        });
        
        for (let i = 0; i < 75; i++) {
            const mesh = new THREE.Mesh(geometry, material);
            
            const depth = -Math.random() * 1500 - 100;
            mesh.position.set(
                (Math.random() - 0.5) * 170,
                depth,
                (Math.random() - 0.5) * 170
            );
            
            mesh.userData = {
                type: 'fecal_pellet',
                originalY: depth,
                sinkSpeed: Math.random() * 0.5 + 0.2,
                rotationSpeed: Math.random() * 0.1 + 0.05
            };
            
            this.scene.add(mesh);
            this.organisms.push(mesh);
        }
    }
    
    updateSimulation(params) {
        const { time, waterType, lightIntensity, nutrients, temperature } = params;
        
        // Actualizar shader del océano
        if (this.oceanMesh) {
            const attenuationCoeffs = {
                oceanic: 0.05,
                coastal: 0.15,
                estuarine: 0.5
            };
            
            this.oceanMesh.material.uniforms.lightAttenuation.value = attenuationCoeffs[waterType] || 0.05;
            this.oceanMesh.material.uniforms.time.value = time * 0.01;
        }
        
        // Actualizar posiciones de organismos
        const migrationFactor = this.calculateMigrationFactor(time);
        
        this.organisms.forEach(organism => {
            const userData = organism.userData;
            
            switch (userData.type) {
                case 'phytoplankton':
                    // Movimiento flotante
                    organism.position.y = userData.originalY + 
                        Math.sin(time * userData.floatSpeed + userData.phase) * 2;
                    
                    // Fotosíntesis activa durante el día
                    if (time >= 6 && time <= 18) {
                        organism.material.emissive.setHex(0x004400);
                    } else {
                        organism.material.emissive.setHex(0x002200);
                    }
                    break;
                    
                case 'zooplankton':
                    // Migración vertical
                    const migrationOffset = migrationFactor * userData.migrationSpeed * 50;
                    organism.position.y = userData.originalY + migrationOffset;
                    
                    // Rotación durante migración
                    organism.rotation.z = Math.sin(time * 0.1 + userData.phase) * 0.3;
                    break;
                    
                case 'bacteria':
                    // Movimiento errático
                    organism.position.x += Math.sin(time * userData.wobbleSpeed + userData.phase) * 0.1;
                    organism.position.z += Math.cos(time * userData.wobbleSpeed + userData.phase) * 0.1;
                    break;
                    
                case 'fecal_pellet':
                    // Hundimiento continuo
                    userData.originalY -= userData.sinkSpeed;
                    if (userData.originalY < -2000) {
                        userData.originalY = -100; // Resetear en superficie
                    }
                    organism.position.y = userData.originalY;
                    
                    // Rotación durante caída
                    organism.rotation.x += userData.rotationSpeed;
                    organism.rotation.z += userData.rotationSpeed * 0.5;
                    break;
            }
        });
        
        // Actualizar intensidad de luces espectrales
        this.lightSources.forEach((lightData, index) => {
            if (index > 0 && lightData.light) { // Saltar luz solar
                const depthFactor = Math.exp(-lightData.attenuation * 50);
                lightData.light.intensity = (lightIntensity / 100) * depthFactor;
            }
        });
    }
    
    calculateMigrationFactor(timeHour) {
        if (timeHour >= 20 || timeHour <= 6) {
            return 0.8; // Máxima migración nocturna
        } else if (timeHour >= 18 && timeHour < 20) {
            return (timeHour - 18) / 2 * 0.8; // Ascenso gradual
        } else if (timeHour > 6 && timeHour <= 8) {
            return (8 - timeHour) / 2 * 0.8; // Descenso gradual
        }
        return 0; // Día - posición normal
    }
    
    animate() {
        if (!this.isAnimating) return;
        
        this.animationId = requestAnimationFrame(() => this.animate());
        
        // Actualizar controles
        this.controls.update();
        
        // Renderizar escena
        this.renderer.render(this.scene, this.camera);
    }
    
    start() {
        this.isAnimating = true;
        this.animate();
    }
    
    stop() {
        this.isAnimating = false;
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
    }
    
    onWindowResize() {
        const width = this.container.clientWidth;
        const height = this.container.clientHeight;
        
        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(width, height);
    }
    
    dispose() {
        this.stop();
        
        // Limpiar geometrías y materiales
        this.organisms.forEach(organism => {
            organism.geometry.dispose();
            organism.material.dispose();
            this.scene.remove(organism);
        });
        
        if (this.oceanMesh) {
            this.oceanMesh.geometry.dispose();
            this.oceanMesh.material.dispose();
            this.scene.remove(this.oceanMesh);
        }
        
        // Limpiar renderer
        this.renderer.dispose();
        if (this.container.contains(this.renderer.domElement)) {
            this.container.removeChild(this.renderer.domElement);
        }
    }
}

// Función global para inicializar desde Dash
window.initThreeJSOcean = function(containerId) {
    if (window.oceanSimulator3D) {
        window.oceanSimulator3D.dispose();
    }
    
    // Esperar a que Three.js esté cargado
    if (typeof THREE === 'undefined') {
        console.error('Three.js no está cargado');
        return;
    }
    
    window.oceanSimulator3D = new ThreeJSOceanSimulator(containerId);
    window.oceanSimulator3D.start();
};

// Función para actualizar parámetros desde Dash
window.updateOceanParams = function(params) {
    if (window.oceanSimulator3D) {
        window.oceanSimulator3D.updateSimulation(params);
    }
};