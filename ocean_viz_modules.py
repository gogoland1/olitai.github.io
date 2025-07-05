#!/usr/bin/env python3
"""
🌊 Módulos de Visualización Oceanográfica
Sistema modular para visualizaciones científicas del océano
"""

import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from scipy.interpolate import griddata
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class OceanVisualizationBase:
    """Clase base para todas las visualizaciones oceanográficas"""
    
    def __init__(self, figsize=(12, 8), style='scientific'):
        """
        Inicializar visualizador base
        
        Args:
            figsize: Tamaño de figura para matplotlib
            style: Estilo de visualización ('scientific', 'presentation', 'publication')
        """
        self.figsize = figsize
        self.style = style
        self.color_palettes = {
            'depth': ['#e8f4f8', '#71c7ec', '#2e86ab', '#0a4d68', '#1f2937'],
            'temperature': ['#3b82f6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444'],
            'salinity': ['#ddd6fe', '#a78bfa', '#8b5cf6', '#7c3aed', '#5b21b6'],
            'oxygen': ['#fca5a5', '#f87171', '#ef4444', '#dc2626', '#991b1b'],
            'chlorophyll': ['#f0fdf4', '#bbf7d0', '#4ade80', '#16a34a', '#15803d']
        }
        
        # Configurar estilo matplotlib
        plt.style.use('default')
        if style == 'scientific':
            plt.rcParams.update({
                'font.size': 11,
                'axes.labelsize': 12,
                'axes.titlesize': 14,
                'xtick.labelsize': 10,
                'ytick.labelsize': 10,
                'legend.fontsize': 10,
                'figure.titlesize': 16
            })
    
    def get_depth_colors(self, depths, max_depth=None):
        """Obtener colores según profundidad"""
        if max_depth is None:
            max_depth = np.max(depths)
        
        normalized_depths = np.array(depths) / max_depth
        colors = plt.cm.viridis_r(normalized_depths)
        return colors
    
    def add_bathymetry_reference(self, ax, region='global'):
        """Agregar líneas de referencia batimétrica"""
        reference_depths = {
            'global': [0, -200, -1000, -3000, -6000],
            'coastal': [0, -50, -100, -200, -500],
            'abyssal': [-1000, -2000, -4000, -6000, -8000]
        }
        
        depths = reference_depths.get(region, reference_depths['global'])
        for depth in depths[1:]:  # Skip surface
            ax.axhline(y=depth, color='gray', linestyle='--', alpha=0.3, linewidth=0.8)
            ax.text(ax.get_xlim()[1]*0.95, depth, f'{abs(depth)}m', 
                   ha='right', va='bottom', fontsize=8, alpha=0.7)

class BathymetryVisualizer(OceanVisualizationBase):
    """Visualizador de batimetría y topografía marina"""
    
    def create_synthetic_bathymetry(self, nx=100, ny=100, region_type='seamount'):
        """
        Crear datos sintéticos de batimetría
        
        Args:
            nx, ny: Resolución de la grilla
            region_type: Tipo de región ('seamount', 'trench', 'continental_shelf', 'abyssal_plain')
        """
        x = np.linspace(-50, 50, nx)
        y = np.linspace(-50, 50, ny)
        X, Y = np.meshgrid(x, y)
        
        if region_type == 'seamount':
            # Monte submarino
            center_x, center_y = 0, 0
            distance = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
            Z = -3000 + 2500 * np.exp(-distance**2 / 400)
            # Agregar ruido realista
            Z += np.random.normal(0, 50, Z.shape)
            
        elif region_type == 'trench':
            # Fosa oceánica
            Z = -4000 - 4000 * np.exp(-((X - 10)**2 + Y**2) / 200)
            Z += np.random.normal(0, 100, Z.shape)
            
        elif region_type == 'continental_shelf':
            # Plataforma continental
            distance_from_coast = np.abs(X + 40)
            Z = -10 * distance_from_coast - 0.1 * distance_from_coast**2
            Z = np.clip(Z, -3000, 0)
            Z += np.random.normal(0, 20, Z.shape)
            
        elif region_type == 'abyssal_plain':
            # Llanura abisal
            Z = -4500 + 200 * np.sin(X/10) * np.cos(Y/8)
            Z += np.random.normal(0, 30, Z.shape)
        
        return X, Y, Z
    
    def plot_3d_bathymetry(self, X, Y, Z, title="Batimetría 3D"):
        """Crear visualización 3D de batimetría usando Plotly"""
        
        fig = go.Figure(data=[go.Surface(
            x=X, y=Y, z=Z,
            colorscale='Blues_r',
            colorbar=dict(
                title="Profundidad (m)",
                titleside="right",
                tickmode="linear",
                tick0=np.min(Z),
                dtick=500
            ),
            hovertemplate="<b>Coordenadas</b><br>" +
                         "X: %{x:.1f}<br>" +
                         "Y: %{y:.1f}<br>" +
                         "Profundidad: %{z:.0f} m<extra></extra>"
        )])
        
        fig.update_layout(
            title=title,
            scene=dict(
                xaxis_title="Longitud relativa (km)",
                yaxis_title="Latitud relativa (km)",
                zaxis_title="Profundidad (m)",
                aspectmode='manual',
                aspectratio=dict(x=1, y=1, z=0.5),
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                )
            ),
            font=dict(size=12),
            width=800,
            height=600
        )
        
        return fig
    
    def plot_contour_bathymetry(self, X, Y, Z, title="Carta Batimétrica"):
        """Crear mapa de contornos batimétricos"""
        
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Contornos rellenos
        contourf = ax.contourf(X, Y, Z, levels=20, cmap='Blues_r', alpha=0.8)
        
        # Líneas de contorno
        contours = ax.contour(X, Y, Z, levels=15, colors='navy', alpha=0.6, linewidths=0.8)
        ax.clabel(contours, inline=True, fontsize=8, fmt='%0.0f')
        
        # Colorbar
        cbar = plt.colorbar(contourf, ax=ax, shrink=0.8)
        cbar.set_label('Profundidad (m)', rotation=270, labelpad=20)
        
        ax.set_xlabel('Longitud relativa (km)')
        ax.set_ylabel('Latitud relativa (km)')
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal')
        
        return fig, ax

class CurrentFlowVisualizer(OceanVisualizationBase):
    """Visualizador de corrientes oceánicas"""
    
    def generate_current_field(self, nx=50, ny=50, pattern='gyre'):
        """
        Generar campo de corrientes sintético
        
        Args:
            nx, ny: Resolución de la grilla
            pattern: Patrón de corriente ('gyre', 'jet', 'eddy', 'upwelling')
        """
        x = np.linspace(-100, 100, nx)
        y = np.linspace(-100, 100, ny)
        X, Y = np.meshgrid(x, y)
        
        if pattern == 'gyre':
            # Giro subtropical
            r = np.sqrt(X**2 + Y**2)
            theta = np.arctan2(Y, X)
            
            # Velocidad tangencial decreciente con radio
            v_theta = 0.5 * np.exp(-r/50) * (r/25)
            
            U = -v_theta * np.sin(theta)
            V = v_theta * np.cos(theta)
            
        elif pattern == 'jet':
            # Corriente de chorro (como Gulf Stream)
            U = 1.0 * np.exp(-(Y**2)/200) * np.ones_like(X)
            V = 0.1 * np.sin(X/20) * np.exp(-(Y**2)/200)
            
        elif pattern == 'eddy':
            # Remolino mesoscalar
            center_x, center_y = 0, 0
            r = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
            theta = np.arctan2(Y - center_y, X - center_x)
            
            # Vórtice con núcleo sólido
            v_circ = np.where(r < 20, 0.3 * r/20, 0.3 * 20/r)
            U = -v_circ * np.sin(theta)
            V = v_circ * np.cos(theta)
            
        elif pattern == 'upwelling':
            # Surgencia costera
            # Viento hacia el ecuador genera surgencia
            U = 0.2 * np.ones_like(X)  # Viento zonal
            V = -0.1 * np.exp(-np.abs(X)/30) * np.sign(Y)  # Surgencia/hundimiento
        
        # Añadir variabilidad temporal y ruido
        speed = np.sqrt(U**2 + V**2)
        
        return X, Y, U, V, speed
    
    def plot_vector_field(self, X, Y, U, V, speed, title="Campo de Corrientes"):
        """Visualizar campo vectorial de corrientes"""
        
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Campo de velocidades como contornos
        contourf = ax.contourf(X, Y, speed, levels=20, cmap='plasma', alpha=0.7)
        
        # Vectores de corriente (submuestrear para claridad)
        skip = 3
        ax.quiver(X[::skip, ::skip], Y[::skip, ::skip], 
                 U[::skip, ::skip], V[::skip, ::skip],
                 angles='xy', scale_units='xy', scale=1, 
                 color='white', alpha=0.8, width=0.003)
        
        # Líneas de corriente
        ax.streamplot(X, Y, U, V, color='white', density=1.5, linewidth=1, alpha=0.6)
        
        # Colorbar
        cbar = plt.colorbar(contourf, ax=ax, shrink=0.8)
        cbar.set_label('Velocidad (m/s)', rotation=270, labelpad=20)
        
        ax.set_xlabel('X (km)')
        ax.set_ylabel('Y (km)')
        ax.set_title(title)
        ax.set_aspect('equal')
        
        return fig, ax
    
    def plot_interactive_currents(self, X, Y, U, V, speed, title="Corrientes Interactivas"):
        """Crear visualización interactiva con Plotly"""
        
        # Crear subplots
        fig = make_subplots(rows=1, cols=2,
                           subplot_titles=["Campo de Velocidades", "Vectores de Corriente"],
                           specs=[[{"secondary_y": False}, {"secondary_y": False}]])
        
        # Mapa de velocidades
        fig.add_trace(
            go.Contour(x=X[0,:], y=Y[:,0], z=speed,
                      colorscale='Viridis',
                      name='Velocidad',
                      hovertemplate="X: %{x:.1f}<br>Y: %{y:.1f}<br>Velocidad: %{z:.2f} m/s<extra></extra>"),
            row=1, col=1
        )
        
        # Vectores (submuestrear)
        skip = 4
        X_sub = X[::skip, ::skip]
        Y_sub = Y[::skip, ::skip]
        U_sub = U[::skip, ::skip]
        V_sub = V[::skip, ::skip]
        
        # Calcular puntas de las flechas
        X_end = X_sub + U_sub * 2
        Y_end = Y_sub + V_sub * 2
        
        for i in range(X_sub.shape[0]):
            for j in range(X_sub.shape[1]):
                fig.add_trace(
                    go.Scatter(x=[X_sub[i,j], X_end[i,j]], 
                             y=[Y_sub[i,j], Y_end[i,j]],
                             mode='lines+markers',
                             line=dict(color='red', width=2),
                             marker=dict(size=[0, 8], symbol=['circle', 'triangle-up']),
                             showlegend=False,
                             hoverinfo='skip'),
                    row=1, col=2
                )
        
        fig.update_layout(height=500, title_text=title)
        
        return fig

class MarineLifeVisualizer(OceanVisualizationBase):
    """Visualizador de distribuciones de vida marina"""
    
    def generate_species_distribution(self, nx=100, ny=100, species_type='phytoplankton'):
        """
        Generar distribución espacial de especies marinas
        
        Args:
            species_type: Tipo de especie ('phytoplankton', 'zooplankton', 'fish', 'whales')
        """
        x = np.linspace(-100, 100, nx)
        y = np.linspace(-100, 100, ny)
        X, Y = np.meshgrid(x, y)
        
        if species_type == 'phytoplankton':
            # Máximo en upwelling, gradiente latitudinal
            upwelling_x = -50
            distance_upwelling = np.abs(X - upwelling_x)
            latitudinal_gradient = np.cos(Y * np.pi / 200)
            
            concentration = (10 * np.exp(-distance_upwelling/20) * 
                           (1 + latitudinal_gradient) + 
                           np.random.exponential(2, X.shape))
            
        elif species_type == 'zooplankton':
            # Siguiendo fitoplancton pero con retraso espacial
            upwelling_x = -40  # Ligeramente desplazado
            distance_upwelling = np.abs(X - upwelling_x)
            
            concentration = (5 * np.exp(-distance_upwelling/25) * 
                           np.exp(-Y**2/3000) + 
                           np.random.exponential(1, X.shape))
            
        elif species_type == 'fish':
            # Agregaciones en zonas productivas y estructuras
            # Cerca de montes submarinos y frentes
            center1 = np.sqrt((X - 20)**2 + (Y - 30)**2)
            center2 = np.sqrt((X + 30)**2 + (Y + 10)**2)
            
            concentration = (2 * np.exp(-center1/15) + 
                           1.5 * np.exp(-center2/20) +
                           0.5 * np.random.exponential(0.5, X.shape))
            
        elif species_type == 'whales':
            # Rutas migratorias y áreas de alimentación
            migration_route = np.exp(-((Y - 0.5*X)**2)/500)
            feeding_area = np.exp(-((X + 20)**2 + (Y - 40)**2)/300)
            
            concentration = (0.1 * migration_route + 
                           0.2 * feeding_area +
                           0.01 * np.random.exponential(1, X.shape))
        
        return X, Y, concentration
    
    def plot_species_hotspots(self, X, Y, concentration, species_name, threshold_percentile=75):
        """Visualizar hotspots de especies marinas"""
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Mapa de concentración continua
        im1 = ax1.contourf(X, Y, concentration, levels=20, 
                          cmap=self.color_palettes['chlorophyll'], alpha=0.8)
        ax1.contour(X, Y, concentration, levels=10, colors='darkgreen', alpha=0.6, linewidths=0.8)
        
        cbar1 = plt.colorbar(im1, ax=ax1, shrink=0.8)
        cbar1.set_label(f'Concentración {species_name}', rotation=270, labelpad=20)
        
        ax1.set_title(f'Distribución de {species_name}')
        ax1.set_xlabel('X (km)')
        ax1.set_ylabel('Y (km)')
        ax1.grid(True, alpha=0.3)
        
        # Hotspots (áreas de alta concentración)
        threshold = np.percentile(concentration, threshold_percentile)
        hotspots = concentration > threshold
        
        ax2.contourf(X, Y, concentration, levels=20, cmap='Blues', alpha=0.3)
        ax2.contourf(X, Y, hotspots.astype(int), levels=[0.5, 1.5], 
                    colors=['red'], alpha=0.7)
        
        ax2.set_title(f'Hotspots de {species_name} (>{threshold_percentile}° percentil)')
        ax2.set_xlabel('X (km)')
        ax2.set_ylabel('Y (km)')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig, (ax1, ax2)
    
    def create_biodiversity_dashboard(self, species_data_dict):
        """Crear dashboard de biodiversidad marina con múltiples especies"""
        
        n_species = len(species_data_dict)
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=list(species_data_dict.keys()),
            specs=[[{"type": "xy"}, {"type": "xy"}],
                   [{"type": "xy"}, {"type": "xy"}]]
        )
        
        positions = [(1,1), (1,2), (2,1), (2,2)]
        
        for idx, (species, (X, Y, data)) in enumerate(species_data_dict.items()):
            if idx >= 4:  # Máximo 4 especies
                break
                
            row, col = positions[idx]
            
            fig.add_trace(
                go.Contour(
                    x=X[0,:], y=Y[:,0], z=data,
                    colorscale='Viridis',
                    name=species,
                    showscale=True if idx == 0 else False,
                    hovertemplate=f"<b>{species}</b><br>" +
                                 "X: %{x:.1f}<br>Y: %{y:.1f}<br>" +
                                 "Concentración: %{z:.2f}<extra></extra>"
                ),
                row=row, col=col
            )
        
        fig.update_layout(
            height=800,
            title_text="Dashboard de Biodiversidad Marina",
            showlegend=False
        )
        
        return fig

class HydrographicProfiler(OceanVisualizationBase):
    """Visualizador de perfiles hidrográficos"""
    
    def generate_ctd_profile(self, max_depth=2000, station_type='open_ocean'):
        """
        Generar perfil CTD sintético
        
        Args:
            max_depth: Profundidad máxima del perfil
            station_type: Tipo de estación ('open_ocean', 'coastal', 'polar', 'tropical')
        """
        depths = np.linspace(0, max_depth, 200)
        
        if station_type == 'open_ocean':
            # Perfil típico océano abierto subtropical
            temp = 25 * np.exp(-depths/300) + 5 + 2*np.sin(depths/100)
            salinity = 35 + 1.5 * np.exp(-depths/500) - 0.5 * np.exp(-depths/50)
            oxygen = 250 - 150 * np.exp(-depths/200) + 50 * np.exp(-(depths-1000)**2/200000)
            
        elif station_type == 'coastal':
            # Influencia terrestre y surgencia
            temp = 20 * np.exp(-depths/200) + 8 + np.random.normal(0, 0.5, len(depths))
            salinity = 33 + 2 * np.exp(-depths/300) + np.random.normal(0, 0.1, len(depths))
            oxygen = 280 - 100 * np.exp(-depths/150)
            
        elif station_type == 'polar':
            # Aguas frías y bien oxigenadas
            temp = 2 + 3 * np.exp(-depths/500) + np.random.normal(0, 0.2, len(depths))
            salinity = 34.5 + 0.3 * np.exp(-depths/800)
            oxygen = 350 - 50 * np.exp(-depths/400)
            
        elif station_type == 'tropical':
            # Termoclina pronunciada
            temp = 28 * np.exp(-depths/100) + 4
            salinity = 36 - 1 * np.exp(-depths/200)
            oxygen = 200 - 100 * np.exp(-depths/300) + 80 * np.exp(-(depths-800)**2/100000)
        
        # Añadir ruido realista
        temp += np.random.normal(0, 0.1, len(depths))
        salinity += np.random.normal(0, 0.05, len(depths))
        oxygen += np.random.normal(0, 5, len(depths))
        
        return depths, temp, salinity, oxygen
    
    def plot_ts_diagram(self, temp, salinity, depths, title="Diagrama T-S"):
        """Crear diagrama Temperatura-Salinidad"""
        
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Colorear por profundidad
        scatter = ax.scatter(salinity, temp, c=depths, cmap='viridis_r', 
                           s=20, alpha=0.7, edgecolors='black', linewidth=0.5)
        
        # Isopicnas (densidad constante)
        sal_range = np.linspace(np.min(salinity)-0.5, np.max(salinity)+0.5, 100)
        temp_range = np.linspace(np.min(temp)-1, np.max(temp)+1, 100)
        S_grid, T_grid = np.meshgrid(sal_range, temp_range)
        
        # Aproximación simple de densidad (sigma-t)
        sigma_t = -T_grid + 0.8 * S_grid - 28
        
        contours = ax.contour(S_grid, T_grid, sigma_t, levels=10, 
                            colors='gray', alpha=0.5, linewidths=0.8)
        ax.clabel(contours, inline=True, fontsize=8, fmt='σₜ=%.1f')
        
        cbar = plt.colorbar(scatter, ax=ax, shrink=0.8)
        cbar.set_label('Profundidad (m)', rotation=270, labelpad=20)
        
        ax.set_xlabel('Salinidad (PSU)')
        ax.set_ylabel('Temperatura (°C)')
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        
        return fig, ax
    
    def plot_vertical_profiles(self, depths, temp, salinity, oxygen, station_name="Estación CTD"):
        """Visualizar perfiles verticales hidrográficos"""
        
        fig, axes = plt.subplots(1, 3, figsize=(15, 8), sharey=True)
        
        # Perfil de temperatura
        axes[0].plot(temp, -depths, 'r-', linewidth=2, label='Temperatura')
        axes[0].set_xlabel('Temperatura (°C)')
        axes[0].set_ylabel('Profundidad (m)')
        axes[0].set_title('Temperatura')
        axes[0].grid(True, alpha=0.3)
        axes[0].invert_yaxis()
        
        # Perfil de salinidad
        axes[1].plot(salinity, -depths, 'b-', linewidth=2, label='Salinidad')
        axes[1].set_xlabel('Salinidad (PSU)')
        axes[1].set_title('Salinidad')
        axes[1].grid(True, alpha=0.3)
        
        # Perfil de oxígeno
        axes[2].plot(oxygen, -depths, 'g-', linewidth=2, label='Oxígeno')
        axes[2].set_xlabel('Oxígeno (μmol/L)')
        axes[2].set_title('Oxígeno Disuelto')
        axes[2].grid(True, alpha=0.3)
        
        # Agregar referencias batimétricas
        for ax in axes:
            self.add_bathymetry_reference(ax, region='global')
        
        plt.suptitle(f'Perfiles Hidrográficos - {station_name}', fontsize=16)
        plt.tight_layout()
        
        return fig, axes

class TimeSeriesOceanVisualizer(OceanVisualizationBase):
    """Visualizador de series temporales oceanográficas"""
    
    def generate_ocean_timeseries(self, days=365, variables=['sst', 'chlorophyll', 'wave_height']):
        """Generar series temporales sintéticas de variables oceanográficas"""
        
        # Generar fechas
        start_date = datetime(2023, 1, 1)
        dates = [start_date + timedelta(days=i) for i in range(days)]
        
        # Crear DataFrame
        data = {'date': dates}
        
        for var in variables:
            if var == 'sst':  # Sea Surface Temperature
                # Ciclo estacional + variabilidad de alta frecuencia
                annual_cycle = 20 + 5 * np.cos(2 * np.pi * np.arange(days) / 365)
                high_freq = np.random.normal(0, 1, days)
                # Filtro pasa-bajas para simular inercia térmica
                sst = annual_cycle + np.convolve(high_freq, np.ones(7)/7, mode='same')
                data['sst'] = sst
                
            elif var == 'chlorophyll':
                # Bloom primaveral y otoñal
                spring_bloom = 2 * np.exp(-((np.arange(days) - 80)**2) / 300)
                fall_bloom = 1.5 * np.exp(-((np.arange(days) - 260)**2) / 200)
                baseline = 0.5 + np.random.exponential(0.3, days)
                data['chlorophyll'] = spring_bloom + fall_bloom + baseline
                
            elif var == 'wave_height':
                # Mayor altura en invierno (hemisferio norte)
                seasonal = 2 + 1.5 * np.cos(2 * np.pi * (np.arange(days) - 300) / 365)
                storms = np.random.exponential(0.5, days)
                data['wave_height'] = seasonal + storms
                
            elif var == 'wind_speed':
                # Vientos más fuertes en invierno
                seasonal = 8 + 4 * np.cos(2 * np.pi * (np.arange(days) - 300) / 365)
                variability = np.random.gamma(2, 2, days)
                data['wind_speed'] = seasonal + variability
        
        return pd.DataFrame(data)
    
    def plot_interactive_timeseries(self, df, title="Series Temporales Oceanográficas"):
        """Crear visualización interactiva de series temporales"""
        
        # Determinar número de subplots
        variables = [col for col in df.columns if col != 'date']
        n_vars = len(variables)
        
        fig = make_subplots(
            rows=n_vars, cols=1,
            shared_xaxes=True,
            subplot_titles=variables,
            vertical_spacing=0.08
        )
        
        colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
        
        for i, var in enumerate(variables):
            fig.add_trace(
                go.Scatter(
                    x=df['date'],
                    y=df[var],
                    mode='lines',
                    name=var,
                    line=dict(color=colors[i % len(colors)], width=2),
                    hovertemplate=f"<b>{var}</b><br>" +
                                 "Fecha: %{x}<br>" +
                                 "Valor: %{y:.2f}<extra></extra>"
                ),
                row=i+1, col=1
            )
            
            # Añadir línea de tendencia
            z = np.polyfit(range(len(df)), df[var], 1)
            trend = np.poly1d(z)(range(len(df)))
            
            fig.add_trace(
                go.Scatter(
                    x=df['date'],
                    y=trend,
                    mode='lines',
                    name=f'{var} tendencia',
                    line=dict(color=colors[i % len(colors)], width=1, dash='dash'),
                    showlegend=False,
                    hoverinfo='skip'
                ),
                row=i+1, col=1
            )
        
        fig.update_layout(
            height=150 * n_vars + 100,
            title_text=title,
            showlegend=True
        )
        
        fig.update_xaxes(title_text="Fecha", row=n_vars, col=1)
        
        return fig
    
    def plot_correlation_matrix(self, df, title="Matriz de Correlación"):
        """Crear matriz de correlación entre variables oceanográficas"""
        
        # Calcular correlaciones
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        corr_matrix = df[numeric_cols].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.round(2).values,
            texttemplate="%{text}",
            textfont={"size": 12},
            hovertemplate="<b>%{x} vs %{y}</b><br>" +
                         "Correlación: %{z:.3f}<extra></extra>"
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Variables",
            yaxis_title="Variables",
            width=600,
            height=600
        )
        
        return fig

# Función principal para demostración
def demo_ocean_visualizations():
    """Función de demostración de todos los módulos"""
    
    print("🌊 Iniciando demostración de visualizaciones oceanográficas...")
    
    # 1. Batimetría
    print("\n1. Creando visualización batimétrica...")
    bathy_viz = BathymetryVisualizer(figsize=(12, 8))
    X, Y, Z = bathy_viz.create_synthetic_bathymetry(region_type='seamount')
    
    # Plotear batimetría 3D
    fig_3d = bathy_viz.plot_3d_bathymetry(X, Y, Z, "Monte Submarino 3D")
    fig_3d.show()
    
    # 2. Corrientes
    print("\n2. Generando campo de corrientes...")
    current_viz = CurrentFlowVisualizer()
    X_c, Y_c, U, V, speed = current_viz.generate_current_field(pattern='gyre')
    
    fig_currents = current_viz.plot_interactive_currents(X_c, Y_c, U, V, speed)
    fig_currents.show()
    
    # 3. Vida marina
    print("\n3. Simulando distribución de especies...")
    life_viz = MarineLifeVisualizer()
    
    species_data = {}
    for species in ['phytoplankton', 'zooplankton', 'fish']:
        X_s, Y_s, conc = life_viz.generate_species_distribution(species_type=species)
        species_data[species] = (X_s, Y_s, conc)
    
    biodiversity_fig = life_viz.create_biodiversity_dashboard(species_data)
    biodiversity_fig.show()
    
    # 4. Perfiles hidrográficos
    print("\n4. Generando perfiles CTD...")
    hydro_viz = HydrographicProfiler()
    depths, temp, sal, oxy = hydro_viz.generate_ctd_profile(station_type='open_ocean')
    
    fig_profiles, _ = hydro_viz.plot_vertical_profiles(depths, temp, sal, oxy)
    plt.show()
    
    # 5. Series temporales
    print("\n5. Creando series temporales...")
    ts_viz = TimeSeriesOceanVisualizer()
    df_ts = ts_viz.generate_ocean_timeseries(days=365)
    
    fig_ts = ts_viz.plot_interactive_timeseries(df_ts)
    fig_ts.show()
    
    print("\n✅ Demostración completada!")
    print("💡 Todos los módulos son reutilizables y configurables")

if __name__ == "__main__":
    demo_ocean_visualizations()