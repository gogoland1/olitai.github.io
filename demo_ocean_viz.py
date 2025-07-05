#!/usr/bin/env python3
"""
🌊 Demo Interactivo - Visualizaciones Oceanográficas Modulares
Ejemplo práctico de uso de los módulos de visualización
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Importar nuestros módulos
from ocean_viz_modules import (
    BathymetryVisualizer,
    CurrentFlowVisualizer, 
    MarineLifeVisualizer,
    HydrographicProfiler,
    TimeSeriesOceanVisualizer
)

def create_antarctic_scenario():
    """Crear escenario oceanográfico antártico realista"""
    
    print("🐧 Creando escenario oceanográfico antártico...")
    
    # 1. Batimetría de la Península Antártica
    bathy_viz = BathymetryVisualizer()
    X, Y, Z = bathy_viz.create_synthetic_bathymetry(nx=150, ny=150, region_type='continental_shelf')
    
    # Modificar para simular península antártica
    # Agregar plataforma de hielo y cañones submarinos
    ice_shelf_mask = (Y > 30) & (Z > -500)
    Z[ice_shelf_mask] = 0  # Plataforma de hielo flotante
    
    # Cañón submarino
    canyon_mask = (np.abs(X) < 10) & (Y < 0)
    Z[canyon_mask] -= 1000
    
    fig_bathy = bathy_viz.plot_3d_bathymetry(X, Y, Z, "Batimetría - Península Antártica")
    
    # 2. Corriente Circumpolar Antártica
    current_viz = CurrentFlowVisualizer()
    X_c, Y_c, U, V, speed = current_viz.generate_current_field(nx=80, ny=80, pattern='jet')
    
    # Modificar para simular corriente circumpolar
    U = U * 1.5  # Intensificar corriente hacia el este
    V = V * 0.3  # Reducir componente meridional
    speed = np.sqrt(U**2 + V**2)
    
    fig_currents, _ = current_viz.plot_vector_field(X_c, Y_c, U, V, speed, 
                                                   "Corriente Circumpolar Antártica")
    
    # 3. Krill Antártico (Euphausia superba)
    life_viz = MarineLifeVisualizer()
    X_krill, Y_krill, krill_density = life_viz.generate_species_distribution(
        nx=120, ny=120, species_type='zooplankton')
    
    # Concentrar krill cerca del borde de hielo
    ice_edge_y = 25
    distance_to_ice = np.abs(Y_krill - ice_edge_y)
    krill_enhancement = 3 * np.exp(-distance_to_ice/10)
    krill_density = krill_density * (1 + krill_enhancement)
    
    fig_krill, _ = life_viz.plot_species_hotspots(X_krill, Y_krill, krill_density, 
                                                 "Krill Antártico", threshold_percentile=80)
    
    # 4. Perfil CTD en Aguas Antárticas
    hydro_viz = HydrographicProfiler()
    depths, temp, sal, oxy = hydro_viz.generate_ctd_profile(max_depth=3000, station_type='polar')
    
    # Modificar para características antárticas específicas
    temp = np.clip(temp, -1.8, 4)  # Temperatura de congelación del agua de mar
    sal[depths < 100] += 0.2  # Agua más salina por formación de hielo
    oxy += 50  # Aguas bien oxigenadas
    
    fig_ts, _ = hydro_viz.plot_ts_diagram(temp, sal, depths, "Diagrama T-S - Aguas Antárticas")
    fig_profiles, _ = hydro_viz.plot_vertical_profiles(depths, temp, sal, oxy, 
                                                      "Estación CTD - Mar de Weddell")
    
    return {
        'bathymetry': fig_bathy,
        'currents': fig_currents,
        'krill': fig_krill,
        'ts_diagram': fig_ts,
        'profiles': fig_profiles
    }

def create_upwelling_scenario():
    """Crear escenario de surgencia costera (ej: Corriente de Humboldt)"""
    
    print("🌊 Creando escenario de surgencia costera...")
    
    # 1. Batimetría de margen continental
    bathy_viz = BathymetryVisualizer()
    X, Y, Z = bathy_viz.create_synthetic_bathymetry(nx=100, ny=100, region_type='continental_shelf')
    
    # Modificar para costa oeste sudamericana
    coastal_slope = X > -20
    Z[coastal_slope] = -50 * (X[coastal_slope] + 20) - 10
    Z = np.clip(Z, -4000, 0)
    
    fig_bathy_up = bathy_viz.plot_contour_bathymetry(X, Y, Z, "Batimetría - Margen Continental")
    
    # 2. Sistema de surgencia
    current_viz = CurrentFlowVisualizer()
    X_c, Y_c, U, V, speed = current_viz.generate_current_field(pattern='upwelling')
    
    fig_upwelling = current_viz.plot_interactive_currents(X_c, Y_c, U, V, speed, 
                                                         "Sistema de Surgencia Costera")
    
    # 3. Productividad primaria
    life_viz = MarineLifeVisualizer()
    X_phyto, Y_phyto, phyto_conc = life_viz.generate_species_distribution(
        species_type='phytoplankton')
    
    # Intensificar cerca de la costa (surgencia)
    coastal_distance = np.abs(X_phyto + 40)
    upwelling_factor = 5 * np.exp(-coastal_distance/15)
    phyto_conc = phyto_conc * (1 + upwelling_factor)
    
    fig_phyto, _ = life_viz.plot_species_hotspots(X_phyto, Y_phyto, phyto_conc,
                                                 "Fitoplancton", threshold_percentile=75)
    
    return {
        'bathymetry': fig_bathy_up,
        'upwelling': fig_upwelling,
        'phytoplankton': fig_phyto
    }

def create_climate_timeseries():
    """Crear series temporales climáticas oceánicas"""
    
    print("📊 Generando series temporales climáticas...")
    
    ts_viz = TimeSeriesOceanVisualizer()
    
    # Serie temporal de 5 años con múltiples variables
    df_climate = ts_viz.generate_ocean_timeseries(
        days=5*365, 
        variables=['sst', 'chlorophyll', 'wave_height', 'wind_speed']
    )
    
    # Agregar eventos climáticos extremos
    # Simular El Niño (años 2 y 4)
    elnino_years = [365, 3*365]
    for year_start in elnino_years:
        for i in range(year_start, min(year_start + 180, len(df_climate))):
            df_climate.loc[i, 'sst'] += 2.5  # Anomalía positiva de SST
            df_climate.loc[i, 'chlorophyll'] *= 0.6  # Reducción de productividad
    
    # La Niña (año 3)
    lanina_start = 2*365
    for i in range(lanina_start, min(lanina_start + 180, len(df_climate))):
        df_climate.loc[i, 'sst'] -= 1.5  # Anomalía negativa de SST
        df_climate.loc[i, 'chlorophyll'] *= 1.4  # Aumento de productividad
    
    fig_climate = ts_viz.plot_interactive_timeseries(
        df_climate, "Series Temporales Climáticas - Pacífico Tropical")
    
    # Matriz de correlación
    fig_corr = ts_viz.plot_correlation_matrix(
        df_climate, "Correlaciones entre Variables Oceánicas")
    
    return {
        'timeseries': fig_climate,
        'correlations': fig_corr
    }

def create_comprehensive_dashboard():
    """Crear dashboard comprehensive combinando múltiples escenarios"""
    
    print("🎮 Creando dashboard comprehensive...")
    
    # Crear figura con subplots
    fig = make_subplots(
        rows=3, cols=2,
        specs=[
            [{"type": "scene"}, {"type": "xy"}],
            [{"type": "xy"}, {"type": "xy"}],
            [{"type": "xy", "colspan": 2}, None]
        ],
        subplot_titles=[
            "Batimetría 3D", "Campo de Corrientes",
            "Distribución de Especies", "Perfil Hidrográfico",
            "Series Temporal Integrada"
        ],
        vertical_spacing=0.08
    )
    
    # 1. Batimetría 3D (seamount)
    bathy_viz = BathymetryVisualizer()
    X, Y, Z = bathy_viz.create_synthetic_bathymetry(nx=50, ny=50, region_type='seamount')
    
    fig.add_trace(
        go.Surface(x=X, y=Y, z=Z, colorscale='Blues_r', showscale=False),
        row=1, col=1
    )
    
    # 2. Campo de corrientes
    current_viz = CurrentFlowVisualizer()
    X_c, Y_c, U, V, speed = current_viz.generate_current_field(nx=30, ny=30, pattern='eddy')
    
    fig.add_trace(
        go.Contour(x=X_c[0,:], y=Y_c[:,0], z=speed, 
                  colorscale='Plasma', showscale=False),
        row=1, col=2
    )
    
    # 3. Distribución de especies
    life_viz = MarineLifeVisualizer()
    X_s, Y_s, conc = life_viz.generate_species_distribution(nx=60, ny=60, species_type='fish')
    
    fig.add_trace(
        go.Heatmap(x=X_s[0,:], y=Y_s[:,0], z=conc, 
                  colorscale='Viridis', showscale=False),
        row=2, col=1
    )
    
    # 4. Perfil hidrográfico
    hydro_viz = HydrographicProfiler()
    depths, temp, sal, oxy = hydro_viz.generate_ctd_profile(station_type='tropical')
    
    fig.add_trace(
        go.Scatter(x=temp, y=-depths, mode='lines', name='Temperatura',
                  line=dict(color='red', width=2)),
        row=2, col=2
    )
    
    # 5. Serie temporal
    ts_viz = TimeSeriesOceanVisualizer()
    df_ts = ts_viz.generate_ocean_timeseries(days=180)
    
    fig.add_trace(
        go.Scatter(x=df_ts['date'], y=df_ts['sst'], mode='lines',
                  name='SST', line=dict(color='orange', width=2)),
        row=3, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=df_ts['date'], y=df_ts['chlorophyll'], mode='lines',
                  name='Clorofila', line=dict(color='green', width=2),
                  yaxis='y2'),
        row=3, col=1
    )
    
    # Configurar layout
    fig.update_layout(
        height=1200,
        title_text="🌊 Dashboard Oceanográfico Comprehensive",
        showlegend=True
    )
    
    # Configurar ejes específicos
    fig.update_xaxes(title_text="Longitud (km)", row=1, col=2)
    fig.update_yaxes(title_text="Latitud (km)", row=1, col=2)
    
    fig.update_xaxes(title_text="Temperatura (°C)", row=2, col=2)
    fig.update_yaxes(title_text="Profundidad (m)", row=2, col=2)
    
    fig.update_xaxes(title_text="Fecha", row=3, col=1)
    fig.update_yaxes(title_text="SST (°C)", row=3, col=1)
    
    return fig

def main():
    """Función principal - menú interactivo"""
    
    print("🌊" + "="*60)
    print("   SISTEMA MODULAR DE VISUALIZACIONES OCEANOGRÁFICAS")
    print("="*63)
    print()
    print("Selecciona el escenario a visualizar:")
    print("1. 🐧 Escenario Antártico (Península + Krill)")
    print("2. 🌊 Surgencia Costera (Humboldt-like)")
    print("3. 📊 Series Temporales Climáticas")
    print("4. 🎮 Dashboard Comprehensive")
    print("5. 🧪 Demo Completo (todos los módulos)")
    print("0. ❌ Salir")
    print()
    
    try:
        choice = input("Ingresa tu opción (0-5): ").strip()
        
        if choice == '1':
            figs = create_antarctic_scenario()
            print("✅ Escenario antártico creado. Visualizaciones mostradas.")
            if 'bathymetry' in figs:
                figs['bathymetry'].show()
            plt.show()
            
        elif choice == '2':
            figs = create_upwelling_scenario()
            print("✅ Escenario de surgencia creado.")
            if 'upwelling' in figs:
                figs['upwelling'].show()
            plt.show()
            
        elif choice == '3':
            figs = create_climate_timeseries()
            print("✅ Series temporales climáticas creadas.")
            if 'timeseries' in figs:
                figs['timeseries'].show()
            if 'correlations' in figs:
                figs['correlations'].show()
                
        elif choice == '4':
            fig = create_comprehensive_dashboard()
            print("✅ Dashboard comprehensive creado.")
            fig.show()
            
        elif choice == '5':
            from ocean_viz_modules import demo_ocean_visualizations
            demo_ocean_visualizations()
            
        elif choice == '0':
            print("👋 ¡Hasta luego!")
            return
            
        else:
            print("❌ Opción inválida. Intenta de nuevo.")
            main()
            
    except KeyboardInterrupt:
        print("\n👋 ¡Hasta luego!")
        return
    except Exception as e:
        print(f"❌ Error: {e}")
        print("🔧 Verifica que tengas instaladas las dependencias:")
        print("   pip install numpy matplotlib plotly pandas scipy")

if __name__ == "__main__":
    main()