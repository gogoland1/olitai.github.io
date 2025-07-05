#!/usr/bin/env python3
"""
🌊 Demo Rápido - Visualización Oceanográfica (VERSIÓN ARREGLADA)
Compatible con todas las versiones de matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Configurar estilo
plt.style.use('default')
plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 13,
    'figure.titlesize': 15
})

def create_bathymetry_simple():
    """Crear batimetría simple sin dependencias externas"""
    print("Creando batimetría...")
    
    # Generar grilla
    x = np.linspace(-50, 50, 100)
    y = np.linspace(-50, 50, 100)
    X, Y = np.meshgrid(x, y)
    
    # Monte submarino
    distance = np.sqrt(X**2 + Y**2)
    Z = -3000 + 2500 * np.exp(-distance**2 / 400)
    Z += np.random.normal(0, 50, Z.shape)
    
    # Visualizar
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Mapa de contornos
    contourf = ax1.contourf(X, Y, Z, levels=20, cmap='Blues_r')
    contours = ax1.contour(X, Y, Z, levels=10, colors='navy', alpha=0.6, linewidths=0.8)
    ax1.clabel(contours, inline=True, fontsize=8, fmt='%0.0f')
    
    cbar1 = plt.colorbar(contourf, ax=ax1, shrink=0.8)
    cbar1.set_label('Profundidad (m)', rotation=270, labelpad=15)
    
    ax1.set_xlabel('X (km)')
    ax1.set_ylabel('Y (km)')
    ax1.set_title('Monte Submarino - Vista en Planta')
    ax1.grid(True, alpha=0.3)
    ax1.set_aspect('equal')
    
    # Perfil transversal
    profile_y = Z[50, :]  # Corte en Y=0
    ax2.plot(x, profile_y, 'b-', linewidth=2, label='Perfil batimétrico')
    ax2.fill_between(x, profile_y, -4000, alpha=0.3, color='lightblue')
    
    ax2.set_xlabel('X (km)')
    ax2.set_ylabel('Profundidad (m)')
    ax2.set_title('Perfil Transversal del Monte')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Agregar referencias
    ax2.axhline(y=-200, color='gray', linestyle='--', alpha=0.5, label='Plataforma (200m)')
    ax2.axhline(y=-1000, color='gray', linestyle=':', alpha=0.5, label='Batisal (1000m)')
    
    plt.tight_layout()
    return fig

def create_ocean_currents():
    """Crear campo de corrientes oceánicas"""
    print("Generando corrientes oceánicas...")
    
    # Generar grilla para corrientes
    x = np.linspace(-100, 100, 40)
    y = np.linspace(-100, 100, 40)
    X, Y = np.meshgrid(x, y)
    
    # Giro subtropical (pattern circular)
    r = np.sqrt(X**2 + Y**2)
    theta = np.arctan2(Y, X)
    
    # Velocidad tangencial
    v_theta = 0.5 * np.exp(-r/60) * (r/30)
    U = -v_theta * np.sin(theta)  # Componente X
    V = v_theta * np.cos(theta)   # Componente Y
    
    # Calcular magnitud
    speed = np.sqrt(U**2 + V**2)
    
    # Visualizar
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Campo de velocidades como contornos
    contourf = ax.contourf(X, Y, speed, levels=20, cmap='viridis', alpha=0.8)
    
    # Vectores de corriente (submuestrear)
    skip = 2
    ax.quiver(X[::skip, ::skip], Y[::skip, ::skip], 
             U[::skip, ::skip], V[::skip, ::skip],
             angles='xy', scale_units='xy', scale=1.2,
             color='white', alpha=0.9, width=0.003)
    
    # Líneas de corriente (SIN alpha para compatibilidad)
    ax.streamplot(X, Y, U, V, color='white', density=1.5, linewidth=1.5)
    
    # Colorbar
    cbar = plt.colorbar(contourf, ax=ax, shrink=0.8)
    cbar.set_label('Velocidad (m/s)', rotation=270, labelpad=20)
    
    ax.set_xlabel('X (km)')
    ax.set_ylabel('Y (km)')
    ax.set_title('Giro Subtropical - Campo de Corrientes')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3, color='white', linewidth=0.5)
    
    return fig

def create_species_distribution():
    """Crear distribución de especies marinas"""
    print("Simulando distribución de especies...")
    
    # Generar grilla
    x = np.linspace(-100, 100, 80)
    y = np.linspace(-100, 100, 80)
    X, Y = np.meshgrid(x, y)
    
    # Fitoplancton (máximo en surgencia costera)
    upwelling_x = -70
    distance_upwelling = np.abs(X - upwelling_x)
    latitudinal_gradient = np.cos(Y * np.pi / 200)
    
    phytoplankton = (8 * np.exp(-distance_upwelling/15) * 
                    (1 + latitudinal_gradient) + 
                    np.random.exponential(1.5, X.shape))
    
    # Zooplancton (sigue fitoplancton con retraso espacial)
    zooplankton = (4 * np.exp(-np.abs(X + 60)/20) * 
                   np.exp(-Y**2/2000) + 
                   np.random.exponential(1, X.shape))
    
    # Peces (agregaciones en zonas productivas)
    center1 = np.sqrt((X - 20)**2 + (Y - 30)**2)
    center2 = np.sqrt((X + 30)**2 + (Y + 10)**2)
    
    fish = (2 * np.exp(-center1/18) + 
            1.5 * np.exp(-center2/25) +
            0.3 * np.random.exponential(0.8, X.shape))
    
    # Visualizar
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    species_data = [
        (phytoplankton, 'Fitoplancton', 'Greens'),
        (zooplankton, 'Zooplancton', 'Blues'),
        (fish, 'Peces', 'Oranges')
    ]
    
    for i, (data, title, cmap) in enumerate(species_data):
        row, col = i // 2, i % 2
        ax = axes[row, col]
        
        # Mapa de concentración
        im = ax.contourf(X, Y, data, levels=15, cmap=cmap, alpha=0.9)
        contours = ax.contour(X, Y, data, levels=8, colors='black', alpha=0.4, linewidths=0.6)
        
        cbar = plt.colorbar(im, ax=ax, shrink=0.7)
        cbar.set_label('Concentración', rotation=270, labelpad=15)
        
        ax.set_xlabel('X (km)')
        ax.set_ylabel('Y (km)')
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal')
    
    # Dashboard combinado
    ax_combined = axes[1, 1]
    ax_combined.clear()
    
    # Superponer las tres especies con transparencia
    ax_combined.contourf(X, Y, phytoplankton, levels=10, cmap='Greens', alpha=0.4)
    ax_combined.contourf(X, Y, zooplankton, levels=10, cmap='Blues', alpha=0.4)
    ax_combined.contourf(X, Y, fish, levels=10, cmap='Reds', alpha=0.4)
    
    ax_combined.set_xlabel('X (km)')
    ax_combined.set_ylabel('Y (km)')
    ax_combined.set_title('Ecosistema Marino Integrado')
    ax_combined.grid(True, alpha=0.3)
    ax_combined.set_aspect('equal')
    
    plt.tight_layout()
    return fig

def create_hydrographic_profile():
    """Crear perfil hidrográfico CTD"""
    print("Generando perfil hidrográfico...")
    
    # Generar datos de profundidad
    depths = np.linspace(0, 2000, 200)
    
    # Temperatura (termoclina típica)
    temp = 25 * np.exp(-depths/200) + 4 + 1.5*np.sin(depths/80)
    temp += np.random.normal(0, 0.2, len(depths))
    
    # Salinidad
    salinity = 35 + 1.2 * np.exp(-depths/400) - 0.3 * np.exp(-depths/50)
    salinity += np.random.normal(0, 0.05, len(depths))
    
    # Oxígeno disuelto
    oxygen = 250 - 120 * np.exp(-depths/150) + 60 * np.exp(-(depths-800)**2/150000)
    oxygen += np.random.normal(0, 3, len(depths))
    
    # Visualizar
    fig, axes = plt.subplots(1, 4, figsize=(16, 8), sharey=True)
    
    # Perfil de temperatura
    axes[0].plot(temp, -depths, 'r-', linewidth=2.5, label='Temperatura')
    axes[0].set_xlabel('Temperatura (°C)')
    axes[0].set_ylabel('Profundidad (m)')
    axes[0].set_title('Temperatura')
    axes[0].grid(True, alpha=0.3)
    axes[0].fill_betweenx(-depths, temp, alpha=0.3, color='red')
    
    # Perfil de salinidad
    axes[1].plot(salinity, -depths, 'b-', linewidth=2.5, label='Salinidad')
    axes[1].set_xlabel('Salinidad (PSU)')
    axes[1].set_title('Salinidad')
    axes[1].grid(True, alpha=0.3)
    axes[1].fill_betweenx(-depths, salinity, alpha=0.3, color='blue')
    
    # Perfil de oxígeno
    axes[2].plot(oxygen, -depths, 'g-', linewidth=2.5, label='Oxígeno')
    axes[2].set_xlabel('Oxígeno (μmol/L)')
    axes[2].set_title('Oxígeno Disuelto')
    axes[2].grid(True, alpha=0.3)
    axes[2].fill_betweenx(-depths, oxygen, alpha=0.3, color='green')
    
    # Diagrama T-S
    scatter = axes[3].scatter(salinity, temp, c=depths, cmap='viridis_r', 
                             s=15, alpha=0.8, edgecolors='black', linewidth=0.3)
    
    cbar = plt.colorbar(scatter, ax=axes[3], shrink=0.8)
    cbar.set_label('Profundidad (m)', rotation=270, labelpad=15)
    
    axes[3].set_xlabel('Salinidad (PSU)')
    axes[3].set_ylabel('Temperatura (°C)')
    axes[3].set_title('Diagrama T-S')
    axes[3].grid(True, alpha=0.3)
    
    # Agregar líneas de referencia de profundidad
    reference_depths = [0, -200, -500, -1000, -1500]
    for ax in axes[:3]:
        for depth in reference_depths[1:]:
            ax.axhline(y=depth, color='gray', linestyle='--', alpha=0.4, linewidth=0.8)
            ax.text(ax.get_xlim()[1]*0.95, depth-30, f'{abs(depth)}m', 
                   ha='right', va='bottom', fontsize=8, alpha=0.7)
    
    plt.suptitle('Perfil Hidrográfico CTD - Océano Atlántico', fontsize=16)
    plt.tight_layout()
    return fig

def create_time_series():
    """Crear serie temporal oceanográfica"""
    print("Generando series temporales...")
    
    # Generar fechas (1 año)
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(365)]
    days = np.arange(365)
    
    # SST con ciclo estacional
    sst = 20 + 5 * np.cos(2 * np.pi * days / 365) + np.random.normal(0, 0.8, 365)
    
    # Clorofila con blooms primaveral y otoñal
    spring_bloom = 3 * np.exp(-((days - 80)**2) / 300)
    fall_bloom = 2 * np.exp(-((days - 260)**2) / 200)
    chlorophyll = spring_bloom + fall_bloom + 0.5 + np.random.exponential(0.4, 365)
    
    # Altura de olas (mayor en invierno)
    wave_height = 2 + 1.2 * np.cos(2 * np.pi * (days - 300) / 365) + np.random.exponential(0.6, 365)
    
    # Visualizar
    fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)
    
    # SST
    axes[0].plot(dates, sst, 'r-', linewidth=1.5, alpha=0.8)
    axes[0].fill_between(dates, sst, alpha=0.3, color='red')
    
    # Línea de tendencia
    z = np.polyfit(days, sst, 1)
    trend = np.poly1d(z)(days)
    axes[0].plot(dates, trend, 'k--', linewidth=2, alpha=0.7, label=f'Tendencia: {z[0]:.3f}°C/año')
    
    axes[0].set_ylabel('SST (°C)')
    axes[0].set_title('Temperatura Superficial del Mar')
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()
    
    # Clorofila
    axes[1].plot(dates, chlorophyll, 'g-', linewidth=1.5, alpha=0.8)
    axes[1].fill_between(dates, chlorophyll, alpha=0.3, color='green')
    
    # Marcar blooms
    axes[1].axvline(x=dates[80], color='lightgreen', linestyle=':', alpha=0.7, label='Bloom Primaveral')
    axes[1].axvline(x=dates[260], color='darkgreen', linestyle=':', alpha=0.7, label='Bloom Otoñal')
    
    axes[1].set_ylabel('Clorofila-a (mg/m³)')
    axes[1].set_title('Clorofila-a (Productividad Primaria)')
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()
    
    # Altura de olas
    axes[2].plot(dates, wave_height, 'b-', linewidth=1.5, alpha=0.8)
    axes[2].fill_between(dates, wave_height, alpha=0.3, color='blue')
    
    axes[2].set_ylabel('Altura de Olas (m)')
    axes[2].set_xlabel('Fecha')
    axes[2].set_title('Altura Significativa de Olas')
    axes[2].grid(True, alpha=0.3)
    
    # Formatear fechas en eje X (compatible con versiones antiguas)
    try:
        import matplotlib.dates as mdates
        axes[2].xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        axes[2].xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    except:
        # Si falla, usar formato simple
        pass
    
    plt.suptitle('Series Temporales Oceanográficas - 2023', fontsize=16)
    plt.tight_layout()
    return fig

def create_additional_analysis():
    """Crear análisis adicional: correlaciones y estadísticas"""
    print("Generando análisis estadístico...")
    
    # Generar datos sintéticos para múltiples variables
    days = np.arange(365)
    
    # Variables oceanográficas
    sst = 20 + 5 * np.cos(2 * np.pi * days / 365) + np.random.normal(0, 0.8, 365)
    chlorophyll = 2 + 1.5 * np.cos(2 * np.pi * (days - 60) / 365) + np.random.exponential(0.5, 365)
    wind_speed = 8 + 3 * np.cos(2 * np.pi * (days - 300) / 365) + np.random.gamma(2, 1, 365)
    wave_height = 0.3 * wind_speed + np.random.normal(0, 0.5, 365)
    
    # Crear figura con múltiples análisis
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. Scatter plot SST vs Clorofila
    scatter = axes[0, 0].scatter(sst, chlorophyll, c=days, cmap='viridis', alpha=0.6, s=20)
    axes[0, 0].set_xlabel('SST (°C)')
    axes[0, 0].set_ylabel('Clorofila-a (mg/m³)')
    axes[0, 0].set_title('Relación SST vs Clorofila')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Línea de tendencia
    z = np.polyfit(sst, chlorophyll, 1)
    p = np.poly1d(z)
    axes[0, 0].plot(sorted(sst), p(sorted(sst)), "r--", alpha=0.8, 
                   label=f'Correlación: {np.corrcoef(sst, chlorophyll)[0,1]:.2f}')
    axes[0, 0].legend()
    
    # 2. Histograma de distribuciones
    axes[0, 1].hist(sst, bins=20, alpha=0.7, color='red', label='SST', density=True)
    axes[0, 1].hist(chlorophyll, bins=20, alpha=0.7, color='green', label='Clorofila', density=True)
    axes[0, 1].set_xlabel('Valor')
    axes[0, 1].set_ylabel('Densidad de Probabilidad')
    axes[0, 1].set_title('Distribuciones de Variables')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # 3. Análisis espectral (periodicidad)
    fft_sst = np.fft.fft(sst - np.mean(sst))
    freqs = np.fft.fftfreq(len(sst))
    power = np.abs(fft_sst)**2
    
    # Mostrar solo frecuencias positivas
    positive_freqs = freqs[:len(freqs)//2]
    positive_power = power[:len(power)//2]
    
    axes[1, 0].plot(1/positive_freqs[1:50], positive_power[1:50], 'b-', linewidth=2)
    axes[1, 0].set_xlabel('Período (días)')
    axes[1, 0].set_ylabel('Potencia Espectral')
    axes[1, 0].set_title('Análisis Espectral SST')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].set_xlim(0, 100)
    
    # Marcar ciclo anual
    axes[1, 0].axvline(x=365, color='red', linestyle='--', alpha=0.7, label='Ciclo Anual')
    axes[1, 0].legend()
    
    # 4. Box plot estacional
    # Dividir en estaciones
    seasons = ['Verano', 'Otoño', 'Invierno', 'Primavera']
    seasonal_data = []
    
    for i in range(4):
        start_day = i * 91
        end_day = (i + 1) * 91
        seasonal_sst = sst[start_day:end_day]
        seasonal_data.append(seasonal_sst)
    
    bp = axes[1, 1].boxplot(seasonal_data, labels=seasons, patch_artist=True)
    
    # Colorear boxes
    colors = ['orange', 'brown', 'lightblue', 'lightgreen']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    axes[1, 1].set_ylabel('SST (°C)')
    axes[1, 1].set_title('Variabilidad Estacional SST')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def main():
    """Función principal del demo"""
    
    print("="*60)
    print("     DEMO OCEANOGRÁFICO - VERSIÓN ARREGLADA")
    print("="*60)
    print("Solo requiere: numpy, matplotlib")
    print()
    
    # Crear todas las visualizaciones
    try:
        print("Iniciando generación de visualizaciones...")
        
        # 1. Batimetría
        fig1 = create_bathymetry_simple()
        
        # 2. Corrientes
        fig2 = create_ocean_currents()
        
        # 3. Especies marinas
        fig3 = create_species_distribution()
        
        # 4. Perfil hidrográfico
        fig4 = create_hydrographic_profile()
        
        # 5. Series temporales
        fig5 = create_time_series()
        
        # 6. Análisis adicional
        fig6 = create_additional_analysis()
        
        print("✅ Todas las visualizaciones creadas exitosamente!")
        print("Mostrando gráficos...")
        
        # Mostrar todos los gráficos
        plt.show()
        
        print("\nDemo completado!")
        print("Tip: Modifica los parámetros en las funciones para experimentar")
        print("Características técnicas:")
        print("- Batimetría con monte submarino realista")
        print("- Campo de corrientes con giro subtropical")  
        print("- Distribución de especies con hotspots")
        print("- Perfiles CTD con termoclina y diagrama T-S")
        print("- Series temporales con ciclos estacionales")
        print("- Análisis estadístico y espectral")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Verifica que tengas instalados: numpy, matplotlib")
        print("   Instalar con: pip install numpy matplotlib")

if __name__ == "__main__":
    main()