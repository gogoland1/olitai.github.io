#!/bin/bash

echo "🚀 Dashboard CTD - Ejecución Rápida"
echo "=================================="

# Verificar si virtual environment existe
if [ -d "venv_dashboard" ]; then
    echo "🔄 Activando virtual environment..."
    source venv_dashboard/bin/activate
    
    # Verificar que las dependencias estén instaladas
    if python -c "import flask, plotly, numpy" 2>/dev/null; then
        echo "✅ Dependencias verificadas"
        echo "🚀 Ejecutando Dashboard CTD..."
        echo "📍 El navegador se abrirá automáticamente en http://localhost:5000"
        echo "🛑 Para detener el dashboard, presiona Ctrl+C"
        echo ""
        python run_dashboard.py
    else
        echo "❌ Faltan dependencias. Ejecuta primero: ./dashboard_completo.sh"
    fi
else
    echo "❌ Virtual environment no encontrado."
    echo "💡 Ejecuta primero: ./dashboard_completo.sh"
fi