#!/bin/bash

echo "🌊 Dashboard CTD - Instalación y Ejecución Automática"
echo "=================================================="

# Intentar instalar dependencias con --user para evitar problemas de permisos
echo "📦 Instalando dependencias..."
pip3 install --user flask flask-cors plotly numpy matplotlib scipy pandas

# Ejecutar dashboard
echo "🚀 Ejecutando Dashboard CTD..."
python3 run_dashboard.py