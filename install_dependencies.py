#!/usr/bin/env python3
"""
📦 Instalador de Dependencias - Dashboard CTD
Script para instalar automáticamente todas las dependencias necesarias
"""

import subprocess
import sys
import os

def install_package(package):
    """Instalar un paquete específico"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def check_package(package):
    """Verificar si un paquete está instalado"""
    try:
        __import__(package)
        return True
    except ImportError:
        return False

def main():
    """Función principal del instalador"""
    
    print("🌊" + "="*60)
    print("   INSTALADOR DE DEPENDENCIAS - DASHBOARD CTD")
    print("="*63)
    print()
    
    # Lista de dependencias básicas
    basic_deps = [
        ('numpy', 'numpy'),
        ('matplotlib', 'matplotlib'),
        ('scipy', 'scipy'),
        ('pandas', 'pandas')
    ]
    
    # Lista de dependencias web
    web_deps = [
        ('flask', 'Flask'),
        ('flask_cors', 'Flask-CORS'),
        ('plotly', 'plotly')
    ]
    
    print("🔍 Verificando dependencias básicas...")
    missing_basic = []
    for import_name, package_name in basic_deps:
        if check_package(import_name):
            print(f"✅ {package_name} - Instalado")
        else:
            print(f"❌ {package_name} - Faltante")
            missing_basic.append(package_name)
    
    print("\n🔍 Verificando dependencias web...")
    missing_web = []
    for import_name, package_name in web_deps:
        if check_package(import_name):
            print(f"✅ {package_name} - Instalado")
        else:
            print(f"❌ {package_name} - Faltante")
            missing_web.append(package_name)
    
    # Instalar dependencias faltantes
    all_missing = missing_basic + missing_web
    
    if not all_missing:
        print("\n🎉 ¡Todas las dependencias están instaladas!")
        print("✅ Listo para ejecutar el dashboard")
        return
    
    print(f"\n📦 Instalando {len(all_missing)} dependencias faltantes...")
    
    for package in all_missing:
        print(f"⏳ Instalando {package}...")
        if install_package(package):
            print(f"✅ {package} instalado correctamente")
        else:
            print(f"❌ Error instalando {package}")
    
    print("\n🔄 Verificación final...")
    
    # Verificar instalación
    all_deps = basic_deps + web_deps
    success_count = 0
    
    for import_name, package_name in all_deps:
        if check_package(import_name):
            print(f"✅ {package_name}")
            success_count += 1
        else:
            print(f"❌ {package_name}")
    
    print(f"\n📊 Resultado: {success_count}/{len(all_deps)} dependencias instaladas")
    
    if success_count == len(all_deps):
        print("🎉 ¡Instalación completada exitosamente!")
        print("🚀 Ejecutar dashboard: python run_dashboard.py")
    else:
        print("⚠️  Algunas dependencias fallaron")
        print("💡 Intenta instalación manual:")
        print("   pip install -r requirements_web.txt")

if __name__ == "__main__":
    main()