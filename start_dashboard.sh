#!/bin/bash

echo "🌊 Iniciando Dashboard CTD..."

# Crear virtual environment si no existe
if [ ! -d "venv_ctd" ]; then
    echo "📦 Creando virtual environment..."
    python3 -m venv venv_ctd
fi

# Activar virtual environment
echo "🔄 Activando virtual environment..."
source venv_ctd/bin/activate

# Verificar si flask está instalado
if ! python -c "import flask" 2>/dev/null; then
    echo "📦 Instalando dependencias..."
    pip install flask flask-cors plotly numpy matplotlib scipy pandas
fi

# Ejecutar dashboard
echo "🚀 Ejecutando Dashboard CTD..."
python run_dashboard.py