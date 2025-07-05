#!/bin/bash

echo "🌊 Dashboard CTD - Instalación y Ejecución Completa"
echo "=================================================="

# Función para verificar si un comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Limpiar virtual environment si existe
if [ -d "venv_dashboard" ]; then
    echo "🧹 Limpiando virtual environment existente..."
    rm -rf venv_dashboard
fi

# Crear nuevo virtual environment
echo "📦 Creando virtual environment..."
python3 -m venv venv_dashboard

# Activar virtual environment
echo "🔄 Activando virtual environment..."
source venv_dashboard/bin/activate

# Actualizar pip en el virtual environment
echo "⬆️ Actualizando pip..."
python -m pip install --upgrade pip

# Instalar dependencias en el virtual environment
echo "📦 Instalando dependencias en virtual environment..."
pip install flask flask-cors plotly numpy matplotlib scipy pandas

# Verificar instalación
echo "✅ Verificando instalación..."
python -c "import flask, plotly, numpy; print('✅ Todas las dependencias instaladas correctamente')"

# Ejecutar dashboard
echo "🚀 Ejecutando Dashboard CTD..."
echo "📍 El navegador se abrirá automáticamente en http://localhost:5000"
echo "🛑 Para detener el dashboard, presiona Ctrl+C"
echo ""

python run_dashboard.py