#!/usr/bin/env python3
"""
🚀 Launcher para Dashboard CTD
Script para ejecutar el dashboard web con configuraciones optimizadas
"""

import os
import sys
import webbrowser
import time
import threading
from pathlib import Path

def check_requirements():
    """Verificar que estén instalados los requisitos"""
    try:
        import flask
        import numpy
        import plotly
        print("✅ Dependencias básicas encontradas")
        return True
    except ImportError as e:
        print(f"❌ Falta dependencia: {e}")
        print("📦 Instalar con: pip install -r requirements_web.txt")
        return False

def open_browser():
    """Abrir navegador después de un delay"""
    time.sleep(2)  # Esperar a que arranque el servidor
    webbrowser.open('http://localhost:5000')
    print("🌐 Dashboard abierto en el navegador")

def main():
    """Función principal del launcher"""
    
    print("🌊" + "="*60)
    print("     DASHBOARD CTD - AMBIENTES MARINOS")
    print("="*63)
    print("🎮 Sistema Interactivo de Perfiles Oceanográficos")
    print()
    
    # Verificar directorio de trabajo
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    print(f"📂 Directorio: {script_dir}")
    
    # Verificar dependencias
    if not check_requirements():
        return
    
    # Verificar archivos necesarios
    required_files = [
        'web_dashboard.py',
        'ctd_environments.py',
        'templates/ctd_dashboard.html',
        'static/css/dashboard.css',
        'static/js/dashboard.js'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Archivos faltantes:")
        for file in missing_files:
            print(f"   - {file}")
        return
    
    print("✅ Todos los archivos necesarios encontrados")
    
    # Configurar variables de entorno
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = '1'
    
    print("\n🚀 Iniciando servidor web...")
    print("📍 URL: http://localhost:5000")
    print("🛑 Para detener: Ctrl+C")
    print()
    
    # Abrir navegador en thread separado
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Importar y ejecutar Flask app
    try:
        from web_dashboard import app
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
        
    except KeyboardInterrupt:
        print("\n👋 Dashboard detenido por el usuario")
        
    except Exception as e:
        print(f"\n❌ Error ejecutando dashboard: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()