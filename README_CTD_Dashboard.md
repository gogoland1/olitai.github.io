# 🌊 Dashboard CTD - Ambientes Marinos

Sistema interactivo de visualización de perfiles CTD (Conductividad, Temperatura, Profundidad) para diferentes ambientes marinos, desarrollado como parte del proyecto OLITAI.

## ✨ Características

### 🏔️ Ambientes Marinos Soportados
- **Fiordo Patagónico** (0-100m): Aguas frías estratificadas con fuerte haloclina
- **Delta de Río** (0-50m): Gradiente salino pronunciado, alta variabilidad
- **Ambiente Costero** (0-500m): Influencia terrestre, termoclina estacional
- **Océano Abierto** (0-2000m): Masas de agua oceánicas, estructura vertical compleja

### 🎮 Funcionalidades Interactivas
- **Controles modulares**: Sliders para mezclar ambientes en tiempo real
- **Perfiles dinámicos**: Visualización de temperatura, salinidad y oxígeno
- **Diagramas T-S**: Análisis de masas de agua
- **Estadísticas**: Métricas oceanográficas en tiempo real
- **Presets**: Configuraciones rápidas por ambiente
- **Exportación**: Descarga de datos y gráficos

## 🚀 Instalación y Uso

### Requisitos del Sistema
- Python 3.8+
- Navegador web moderno
- 4GB RAM mínimo

### 1. Instalación
```bash
# Clonar o descargar archivos
cd olitai/

# Instalar dependencias
pip install -r requirements_web.txt
```

### 2. Ejecución Rápida
```bash
# Launcher automático (recomendado)
python run_dashboard.py

# O manual
python web_dashboard.py
```

### 3. Acceso
- **URL**: http://localhost:5000
- **Dashboard**: Se abre automáticamente en el navegador

## 📊 Estructura del Proyecto

```
olitai/
├── ctd_environments.py      # Motor de perfiles CTD
├── web_dashboard.py         # Backend Flask
├── run_dashboard.py         # Launcher principal
├── requirements_web.txt     # Dependencias
├── templates/
│   └── ctd_dashboard.html   # Frontend principal
├── static/
│   ├── css/
│   │   └── dashboard.css    # Estilos personalizados
│   └── js/
│       └── dashboard.js     # Lógica JavaScript
└── README_CTD_Dashboard.md  # Esta documentación
```

## 🎯 Guía de Uso

### Controles Principales

#### 🎛️ Sliders de Ambiente
- **Fiordo**: Características de aguas frías estratificadas
- **Delta**: Influencia fluvial con gradientes salinos
- **Costero**: Ambiente de transición tierra-mar
- **Oceánico**: Masas de agua profundas

#### 📏 Profundidad Máxima
- Rango: 50m - 2000m
- Afecta la resolución vertical del perfil

#### 🎨 Modos de Visualización
- **Temperatura**: Perfiles térmicos
- **Salinidad**: Distribución halina
- **Oxígeno**: Contenido de oxígeno disuelto
- **Todos**: Vista combinada

### Presets Rápidos
- **🏔️ Fiordo**: 100% características de fiordo
- **🌊 Delta**: 100% influencia fluvial
- **⚓ Costero**: 100% ambiente costero
- **🌍 Oceánico**: 100% océano abierto

## 🔬 Base Científica

### Modelos Implementados

#### Fiordo Patagónico
- **Termoclina**: Gradual, influenciada por agua dulce
- **Haloclina**: Muy pronunciada (5-35 PSU)
- **Oxígeno**: Alto en superficie, disminución gradual

#### Delta de Río
- **Estratificación**: Fuerte gradiente superficial
- **Salinidad**: 0.5-25 PSU (agua dulce a salobre)
- **Variabilidad**: Alta debido a flujos estacionales

#### Ambiente Costero
- **Termoclina**: Estacional (30-80m)
- **Surgencias**: Máximo subsuperficial de oxígeno
- **Influencia**: Terrestre y oceánica

#### Océano Abierto
- **Estructura**: Múltiples capas (superficial, termoclina, profunda)
- **Masas de agua**: Diferenciadas por T-S
- **Mínimo de oxígeno**: Zona de mínimo intermedio

## 🌐 API Endpoints

El dashboard incluye una API RESTful completa:

### Perfiles
- `GET /api/environments` - Información de ambientes
- `GET /api/profile/<environment>` - Perfil específico
- `POST /api/mixed_profile` - Perfil mixto personalizado

### Análisis
- `GET /api/statistics/<environment>` - Estadísticas detalladas
- `GET /api/ts_diagram` - Diagrama T-S comparativo
- `GET /api/comparison_plot` - Gráficos de comparación

### Ejemplo de Uso API
```python
import requests

# Obtener perfil costero
response = requests.get('http://localhost:5000/api/profile/coastal')
data = response.json()

# Crear perfil mixto
mixed_profile = requests.post('http://localhost:5000/api/mixed_profile', json={
    'fjord_weight': 0.3,
    'coastal_weight': 0.7,
    'max_depth': 300
})
```

## 🔧 Personalización

### Modificar Ambientes
Editar `ctd_environments.py`:
```python
def generate_custom_profile(self, max_depth=100):
    # Personalizar parámetros oceanográficos
    temp = custom_temperature_profile()
    sal = custom_salinity_profile()
    oxy = custom_oxygen_profile()
    return depths, temp, sal, oxy
```

### Agregar Nuevas Visualizaciones
Extender `dashboard.js`:
```javascript
updateCustomPlot() {
    // Nueva funcionalidad de visualización
}
```

### Estilos Personalizados
Modificar `dashboard.css`:
```css
.custom-environment {
    /* Nuevos estilos para ambientes */
}
```

## 📈 Métricas y Análisis

### Estadísticas Calculadas
- **Media, mín, máx**: Para cada variable
- **Estratificación**: Diferencias superficie-fondo
- **Termoclina**: Profundidad de máximo gradiente
- **Correlaciones**: Entre variables oceanográficas

### Índices Oceanográficos
- **Índice de estratificación térmica**
- **Gradiente halino superficial**
- **Saturación de oxígeno relativa**

## 🐛 Troubleshooting

### Problemas Comunes

#### Dashboard no se abre
```bash
# Verificar puerto
netstat -an | grep :5000

# Usar puerto alternativo
python web_dashboard.py --port 5001
```

#### Error de dependencias
```bash
# Reinstalar requisitos
pip install --upgrade -r requirements_web.txt

# Verificar versiones
python -c "import flask, numpy, plotly; print('OK')"
```

#### Perfiles no se actualizan
- Verificar conexión a localhost:5000
- Revisar consola del navegador (F12)
- Comprobar logs del servidor Flask

### Logs y Debug
```bash
# Ejecutar con debug detallado
FLASK_DEBUG=1 python web_dashboard.py

# Ver logs en tiempo real
tail -f flask.log
```

## 🚀 Despliegue

### Desarrollo Local
```bash
python run_dashboard.py
```

### Producción
```bash
# Usando Gunicorn (Linux/Mac)
gunicorn -w 4 -b 0.0.0.0:5000 web_dashboard:app

# Usando Waitress (Windows)
waitress-serve --port=5000 web_dashboard:app
```

### Docker (Opcional)
```dockerfile
FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements_web.txt
EXPOSE 5000
CMD ["python", "web_dashboard.py"]
```

## 🤝 Contribución

### Estructura de Desarrollo
1. **Fork** el proyecto
2. **Crear rama** para nueva funcionalidad
3. **Desarrollar** siguiendo estándares de código
4. **Testear** con múltiples navegadores
5. **Pull request** con descripción detallada

### Estándares de Código
- **Python**: PEP 8, docstrings completos
- **JavaScript**: ES6+, comentarios descriptivos
- **CSS**: BEM methodology, responsive design
- **HTML**: Semántico, accesible

## 📝 Changelog

### v1.0.0 (2024-07-04)
- ✨ Sistema base de perfiles CTD
- 🎮 Dashboard interactivo completo
- 🔧 API RESTful
- 📊 4 ambientes marinos implementados
- 🌐 Frontend responsive

### Roadmap v1.1.0
- 🗺️ Integración con mapas geográficos
- 📁 Importación de datos CTD reales
- 🔄 Comparación temporal
- 📱 Optimización móvil
- 🌍 Internacionalización

## 📄 Licencia

Proyecto desarrollado como parte de **OLITAI** - Sistema educativo de oceanografía interactiva.

---

## 🌊 Información del Proyecto

**Desarrollado por**: Equipo OLITAI  
**Contacto**: [GitHub OLITAI](https://github.com/olitai)  
**Documentación**: README_CTD_Dashboard.md  
**Última actualización**: Julio 2024

---

¡Explora los océanos desde tu navegador! 🌊🔬