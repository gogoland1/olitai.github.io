# 🌊 Simulador Oceánico 3D - Plotly Dash + Three.js

Una aplicación híbrida que combina **Plotly Dash** para análisis científico interactivo con **Three.js** para visualización 3D inmersiva de ecosistemas marinos.

## 🚀 Características Principales

### 📊 **Plotly Dash Backend**
- **Callbacks reactivos** para interactividad en tiempo real
- **Gráficos 3D científicos** con Plotly
- **Análisis de datos** oceanográficos
- **Dashboard modular** con controles especializados

### 🎮 **Three.js Frontend**
- **Renderizado 3D WebGL** de alta performance
- **Shaders personalizados** para atenuación espectral
- **Sistema de partículas** para organismos marinos
- **Física en tiempo real** (migración, hundimiento, fotosíntesis)

### 🌊 **Simulación Oceánica Realista**
- **Atenuación espectral** por tipo de agua (oceánico/costero/estuarino)
- **Migración vertical circadiana** del zooplancton
- **Loop microbiano** en zona profunda
- **DCM (Deep Chlorophyll Maximum)** dinámico

## 🛠️ Instalación

### Prerrequisitos
```bash
# Python 3.8+
python --version

# Node.js (opcional, para desarrollo)
node --version
```

### Instalar Dependencias
```bash
# Clonar proyecto
cd /mnt/d/proyectos_claude/olitai/ocean_simulator_3d

# Instalar dependencias Python
pip install -r requirements.txt

# O crear entorno virtual
python -m venv venv_ocean3d
source venv_ocean3d/bin/activate  # Linux/Mac
# venv_ocean3d\Scripts\activate   # Windows
pip install -r requirements.txt
```

## 🎯 Uso

### Opción 1: Aplicación Dash Completa
```bash
# Ejecutar servidor Dash
python app.py

# Abrir navegador en:
http://localhost:8050
```

### Opción 2: Demo Three.js Standalone
```bash
# Servir archivos estáticos (cualquier servidor HTTP)
python -m http.server 8080

# Abrir navegador en:
http://localhost:8080/index.html
```

### Opción 3: Integración Completa
1. Ejecutar `python app.py` en una terminal
2. Abrir `index.html` en otra pestaña
3. Usar botón "📊 Lanzar Aplicación Dash Completa"

## 🎮 Controles Interactivos

### **Panel Zona Fótica (0-100m)**
- **💡 Intensidad Lumínica:** Control de penetración solar
- **🌊 Tipo de Agua:** Oceánico (K=0.05) / Costero (K=0.15) / Estuarino (K=0.5)
- **🧪 Nutrientes:** N-P-Si concentrations (0-30 μM)
- **🌡️ Temperatura:** Rango realista (5-25°C)

### **Panel Zona Profunda (100-2000m)**
- **🦠 Actividad Microbiana:** Loop de remineralización
- **🔄 Remineralización:** Eficiencia de descomposición
- **⬇️ Flux de Carbono:** Bomba biológica (mg C/m²/día)
- **🌊 Migración Vertical:** Factor de migración nocturna

### **Controles Globales**
- **⏰ Hora del Día:** Ciclo circadiano (0-23h)
- **▶️ Play/Pause:** Control de animaciones
- **🔄 Reset:** Reiniciar simulación

## 🎨 Arquitectura Técnica

```
ocean_simulator_3d/
├── app.py                 # Servidor Dash principal
├── requirements.txt       # Dependencias Python
├── index.html            # Demo integrado
├── assets/
│   └── threejs_ocean.js  # Componente Three.js
└── README.md             # Este archivo
```

### **Flujo de Datos**
```
Usuario → Dash Callbacks → Python Analysis → JSON Data → Three.js Renderer → WebGL
```

### **Componentes Clave**

#### `app.py` - Servidor Dash
```python
@app.callback(
    Output('photic-zone-3d', 'figure'),
    [Input('time-slider', 'value'), ...]
)
def update_photic_zone_3d(time, water_type, ...):
    # Generar datos de organismos
    # Calcular parámetros oceanográficos
    # Retornar figura Plotly 3D
```

#### `threejs_ocean.js` - Renderizador 3D
```javascript
class ThreeJSOceanSimulator {
    updateSimulation(params) {
        // Actualizar shaders oceánicos
        // Migración vertical organismos
        // Atenuación espectral lumínica
    }
}
```

## 🌊 Modelos Científicos Implementados

### **Atenuación Lumínica**
```
I(z,λ) = I₀(λ) × e^(-K(λ) × z)
```
- **Oceánico:** K = 0.05 m⁻¹ (agua clara)
- **Costero:** K = 0.15 m⁻¹ (turbiedad moderada) 
- **Estuarino:** K = 0.5 m⁻¹ (alta turbiedad)

### **Migración Vertical**
```
Migration_factor = {
    0.8    si 20:00 ≤ hora ≤ 6:00  (noche)
    gradual si 18:00-20:00, 6:00-8:00
    0      si 8:00-18:00 (día)
}
```

### **Productividad Primaria**
```
PP = (Light/100) × (Nutrients/30) × (Temp/25) × Day_factor × 100
```

### **DCM (Deep Chlorophyll Maximum)**
```
DCM_depth = 60 + (15 - Nutrients) + (Upwelling/5)
```

## 🎯 Casos de Uso

### **Educación**
- **Oceanografía:** Visualizar procesos verticales marinos
- **Biología:** Migración y comportamiento organismos
- **Química:** Ciclos biogeoquímicos

### **Investigación**
- **Modelado ecosistémico:** Validar hipótesis ecológicas
- **Análisis de datos:** Explorar datasets oceanográficos
- **Simulaciones:** Escenarios de cambio climático

### **Divulgación**
- **Museos:** Instalaciones interactivas inmersivas
- **Documentales:** Visualizaciones científicas precisas
- **Web:** Contenido educativo engaging

## 🔧 Desarrollo

### **Agregar Nuevos Organismos**
```javascript
// En threejs_ocean.js
createNewOrganism() {
    const geometry = new THREE.SphereGeometry(radius);
    const material = new THREE.MeshPhongMaterial({ color });
    // Agregar comportamiento específico
}
```

### **Nuevos Parámetros Ambientales**
```python
# En app.py
@app.callback(...)
def update_with_new_param(new_param, ...):
    # Cálculos científicos
    # Actualizar visualización
```

### **Shaders Personalizados**
```glsl
// Vertex shader para efectos oceánicos
varying float vDepth;
void main() {
    vDepth = -position.y / max_depth;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}
```

## 🐛 Troubleshooting

### **Three.js no carga**
```javascript
// Verificar en consola del navegador
if (typeof THREE === 'undefined') {
    console.error('Three.js CDN no disponible');
}
```

### **Dash no inicia**
```bash
# Verificar puerto disponible
lsof -i :8050

# Cambiar puerto si necesario
app.run_server(debug=True, port=8051)
```

### **Performance lenta**
- Reducir número de organismos en `generate_organism_data()`
- Simplificar shaders en `createOcean()`
- Usar `renderer.setPixelRatio(1)` en dispositivos de alta resolución

## 🚀 Próximas Características

- [ ] **WebXR/VR**: Inmersión total con Oculus/HTC Vive
- [ ] **Datos reales**: Integración con APIs oceanográficas (COPERNICUS, NOAA)
- [ ] **Machine Learning**: Predicción de patrones ecológicos
- [ ] **Multijugador**: Exploración colaborativa
- [ ] **Export**: Generación de videos/imágenes científicas

## 📚 Referencias Científicas

- **Jerlov, N.G.** (1976). Marine Optics. Elsevier.
- **Kirk, J.T.O.** (2011). Light and Photosynthesis in Aquatic Ecosystems.
- **Longhurst, A.** (2007). Ecological Geography of the Sea.

## 🤝 Contribuciones

¡Contribuciones bienvenidas! Especialmente en:
- Nuevos modelos oceanográficos
- Optimizaciones de rendering
- Validación científica
- UX/UI improvements

## 📄 Licencia

MIT License - Ver archivo LICENSE para detalles.

---

**Desarrollado con ❤️ para la educación oceánica**