#!/usr/bin/env python3
"""
🌊 Sistema de Perfiles CTD por Ambientes Marinos
Perfiles específicos para fiordos, deltas, costero y oceánico
"""

import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime

class CTDEnvironmentProfiler:
    """Generador de perfiles CTD específicos por ambiente marino"""
    
    def __init__(self):
        """Inicializar perfilador CTD"""
        self.environments = {
            'fjord': {
                'name': 'Fiordo Patagónico',
                'max_depth': 100,
                'description': 'Aguas frías, estratificadas, influencia glacial',
                'typical_location': 'Canal Beagle, Estrecho de Magallanes'
            },
            'delta': {
                'name': 'Delta de Río',
                'max_depth': 50,
                'description': 'Fuerte gradiente salino, alta turbidez',
                'typical_location': 'Río de la Plata, Delta del Paraná'
            },
            'coastal': {
                'name': 'Ambiente Costero',
                'max_depth': 500,
                'description': 'Influencia terrestre, surgencias estacionales',
                'typical_location': 'Costa Atlántica, Corriente de Humboldt'
            },
            'oceanic': {
                'name': 'Océano Abierto',
                'max_depth': 2000,
                'description': 'Masas de agua oceánicas, termoclina marcada',
                'typical_location': 'Atlántico Sur, Pacífico Sud-Oriental'
            }
        }
        
        # Colores por ambiente
        self.colors = {
            'fjord': '#2E8B57',      # Verde mar
            'delta': '#8B4513',      # Marrón sedimento
            'coastal': '#4682B4',    # Azul acero
            'oceanic': '#191970'     # Azul marino
        }
    
    def generate_fjord_profile(self, max_depth=100):
        """
        Generar perfil CTD de fiordo patagónico
        Características: Aguas frías, estratificación por agua dulce superficial
        """
        depths = np.linspace(0, max_depth, 100)
        
        # Temperatura: Fría en superficie (agua dulce), ligeramente más cálida en profundidad
        temp_surface = 3.5  # Agua dulce superficial fría
        temp_deep = 5.2     # Agua marina ligeramente más cálida
        temp = temp_surface + (temp_deep - temp_surface) * (1 - np.exp(-depths/30))
        
        # Haloclina marcada (gradiente salino fuerte)
        sal_surface = 5.0   # Muy baja (agua dulce)
        sal_deep = 33.8     # Agua marina
        # Haloclina abrupta entre 10-25m
        salinity = sal_surface + (sal_deep - sal_surface) * (1 / (1 + np.exp(-(depths - 17)/3)))
        
        # Oxígeno: Alto en superficie, disminuye gradualmente
        oxy_surface = 380   # Bien oxigenado (agua fría)
        oxy_deep = 280      # Menor en profundidad
        oxygen = oxy_surface - (oxy_surface - oxy_deep) * (depths/max_depth)**0.7
        
        # Agregar variabilidad realista
        temp += np.random.normal(0, 0.1, len(depths))
        salinity += np.random.normal(0, 0.15, len(depths))
        oxygen += np.random.normal(0, 8, len(depths))
        
        # Asegurar valores físicos realistas
        temp = np.clip(temp, -1.8, 8)
        salinity = np.clip(salinity, 0, 35)
        oxygen = np.clip(oxygen, 150, 400)
        
        return depths, temp, salinity, oxygen
    
    def generate_delta_profile(self, max_depth=50):
        """
        Generar perfil CTD de delta de río
        Características: Fuerte gradiente salino, alta turbidez, aguas más cálidas
        """
        depths = np.linspace(0, max_depth, 50)
        
        # Temperatura: Más cálida que fiordo, influencia continental
        temp_surface = 18.5  # Agua superficial templada
        temp_deep = 16.2     # Ligeramente más fría en profundidad
        # Termoclina suave
        temp = temp_surface - (temp_surface - temp_deep) * (depths/max_depth)**0.5
        
        # Salinity: Gradiente muy marcado río-mar
        sal_surface = 0.5    # Prácticamente agua dulce
        sal_deep = 25.0      # Agua salobre
        # Haloclina muy abrupta
        salinity = sal_surface + (sal_deep - sal_surface) * (1 / (1 + np.exp(-(depths - 15)/2)))
        
        # Oxígeno: Variable por materia orgánica
        oxy_surface = 290    # Moderado en superficie
        oxy_min = 180        # Mínimo de oxígeno por descomposición
        oxy_deep = 220       # Recuperación ligera
        
        # Mínimo de oxígeno en zona intermedia (10-20m)
        oxygen = np.where(depths < 20, 
                         oxy_surface - (oxy_surface - oxy_min) * np.sin(np.pi * depths / 40),
                         oxy_min + (oxy_deep - oxy_min) * (depths - 20) / (max_depth - 20))
        
        # Variabilidad por turbulencia y sedimentos
        temp += np.random.normal(0, 0.3, len(depths))
        salinity += np.random.normal(0, 0.8, len(depths))
        oxygen += np.random.normal(0, 12, len(depths))
        
        # Límites físicos
        temp = np.clip(temp, 10, 25)
        salinity = np.clip(salinity, 0, 30)
        oxygen = np.clip(oxygen, 100, 350)
        
        return depths, temp, salinity, oxygen
    
    def generate_coastal_profile(self, max_depth=500):
        """
        Generar perfil CTD costero
        Características: Influencia terrestre, surgencias, termoclina moderada
        """
        depths = np.linspace(0, max_depth, 200)
        
        # Temperatura: Termoclina estacional
        temp_surface = 16.8   # Temperatura costera templada
        temp_thermocline = 12.5  # Base de termoclina
        temp_deep = 8.2       # Agua profunda fría
        
        # Termoclina entre 30-80m
        temp = np.where(depths < 80,
                       temp_surface - (temp_surface - temp_thermocline) * (1 - np.exp(-depths/25)),
                       temp_thermocline - (temp_thermocline - temp_deep) * (depths - 80)/(max_depth - 80))
        
        # Salinidad: Gradiente moderado con influencia continental
        sal_surface = 33.2    # Ligeramente diluida
        sal_deep = 34.6       # Agua oceánica
        salinity = sal_surface + (sal_deep - sal_surface) * (1 - np.exp(-depths/120))
        
        # Oxígeno: Máximo subsuperficial, mínimo intermedio
        oxy_surface = 280
        oxy_max = 320         # Máximo subsuperficial (fitoplancton)
        oxy_min = 190         # Mínimo de oxígeno (100-200m)
        oxy_deep = 240        # Recuperación en profundidad
        
        # Perfiles complejos con máximo subsuperficial
        oxygen = np.where(depths < 50,
                         oxy_surface + (oxy_max - oxy_surface) * np.exp(-((depths - 20)**2)/400),
                         np.where(depths < 250,
                                 oxy_max - (oxy_max - oxy_min) * (depths - 50)/200,
                                 oxy_min + (oxy_deep - oxy_min) * (depths - 250)/(max_depth - 250)))
        
        # Variabilidad por surgencias y mezcla
        temp += np.random.normal(0, 0.2, len(depths))
        salinity += np.random.normal(0, 0.1, len(depths))
        oxygen += np.random.normal(0, 10, len(depths))
        
        # Límites realistas
        temp = np.clip(temp, 4, 20)
        salinity = np.clip(salinity, 32, 36)
        oxygen = np.clip(oxygen, 120, 350)
        
        return depths, temp, salinity, oxygen
    
    def generate_oceanic_profile(self, max_depth=2000):
        """
        Generar perfil CTD oceánico
        Características: Termoclina pronunciada, masas de agua oceánicas
        """
        depths = np.linspace(0, max_depth, 300)
        
        # Temperatura: Termoclina oceánica clásica
        temp_surface = 22.5   # Capa mixta superficial
        temp_thermocline = 8.0   # Base de termoclina
        temp_deep = 3.8       # Agua profunda
        temp_bottom = 2.2     # Agua de fondo
        
        # Perfiles complejos con múltiples capas
        temp = np.where(depths < 200,
                       temp_surface - (temp_surface - temp_thermocline) * (1 - np.exp(-depths/80)),
                       np.where(depths < 1000,
                               temp_thermocline - (temp_thermocline - temp_deep) * (depths - 200)/800,
                               temp_deep - (temp_deep - temp_bottom) * (depths - 1000)/(max_depth - 1000)))
        
        # Salinidad: Máximo subsuperficial, disminución en profundidad
        sal_surface = 36.2    # Alta salinidad superficial
        sal_max = 36.8        # Máximo subsuperficial
        sal_deep = 34.8       # Agua profunda menos salina
        sal_bottom = 34.7     # Agua de fondo
        
        salinity = np.where(depths < 100,
                           sal_surface + (sal_max - sal_surface) * np.sin(np.pi * depths / 200),
                           np.where(depths < 800,
                                   sal_max - (sal_max - sal_deep) * (depths - 100)/700,
                                   sal_deep - (sal_deep - sal_bottom) * (depths - 800)/(max_depth - 800)))
        
        # Oxígeno: Perfil complejo con mínimo de oxígeno
        oxy_surface = 220
        oxy_min = 80          # Mínimo de oxígeno (500-800m)
        oxy_deep = 180        # Recuperación en profundidad
        oxy_bottom = 220      # Agua antártica bien oxigenada
        
        oxygen = np.where(depths < 500,
                         oxy_surface - (oxy_surface - oxy_min) * (depths/500)**1.5,
                         np.where(depths < 1200,
                                 oxy_min + (oxy_deep - oxy_min) * (depths - 500)/700,
                                 oxy_deep + (oxy_bottom - oxy_deep) * (depths - 1200)/(max_depth - 1200)))
        
        # Variabilidad oceánica
        temp += np.random.normal(0, 0.15, len(depths))
        salinity += np.random.normal(0, 0.08, len(depths))
        oxygen += np.random.normal(0, 8, len(depths))
        
        # Límites oceánicos
        temp = np.clip(temp, 1, 25)
        salinity = np.clip(salinity, 34, 37)
        oxygen = np.clip(oxygen, 60, 280)
        
        return depths, temp, salinity, oxygen
    
    def generate_mixed_profile(self, fjord_weight=0.25, delta_weight=0.25, 
                              coastal_weight=0.25, oceanic_weight=0.25, max_depth=500):
        """
        Generar perfil interpolado entre ambientes
        Permite transiciones suaves entre tipos de ambiente
        """
        # Normalizar pesos
        total_weight = fjord_weight + delta_weight + coastal_weight + oceanic_weight
        fjord_weight /= total_weight
        delta_weight /= total_weight
        coastal_weight /= total_weight
        oceanic_weight /= total_weight
        
        # Generar perfiles base (ajustados a la profundidad deseada)
        depths = np.linspace(0, max_depth, 200)
        
        # Interpolar profundidades para cada ambiente
        if fjord_weight > 0:
            d_f, t_f, s_f, o_f = self.generate_fjord_profile(max_depth)
            t_f_interp = np.interp(depths, d_f, t_f)
            s_f_interp = np.interp(depths, d_f, s_f)
            o_f_interp = np.interp(depths, d_f, o_f)
        else:
            t_f_interp = s_f_interp = o_f_interp = np.zeros_like(depths)
            
        if delta_weight > 0:
            d_d, t_d, s_d, o_d = self.generate_delta_profile(max_depth)
            t_d_interp = np.interp(depths, d_d, t_d)
            s_d_interp = np.interp(depths, d_d, s_d)
            o_d_interp = np.interp(depths, d_d, o_d)
        else:
            t_d_interp = s_d_interp = o_d_interp = np.zeros_like(depths)
            
        if coastal_weight > 0:
            d_c, t_c, s_c, o_c = self.generate_coastal_profile(max_depth)
            t_c_interp = np.interp(depths, d_c, t_c)
            s_c_interp = np.interp(depths, d_c, s_c)
            o_c_interp = np.interp(depths, d_c, o_c)
        else:
            t_c_interp = s_c_interp = o_c_interp = np.zeros_like(depths)
            
        if oceanic_weight > 0:
            d_o, t_o, s_o, o_o = self.generate_oceanic_profile(max_depth)
            t_o_interp = np.interp(depths, d_o, t_o)
            s_o_interp = np.interp(depths, d_o, s_o)
            o_o_interp = np.interp(depths, d_o, o_o)
        else:
            t_o_interp = s_o_interp = o_o_interp = np.zeros_like(depths)
        
        # Combinar con pesos
        temp_mixed = (fjord_weight * t_f_interp + 
                     delta_weight * t_d_interp + 
                     coastal_weight * t_c_interp + 
                     oceanic_weight * t_o_interp)
        
        sal_mixed = (fjord_weight * s_f_interp + 
                    delta_weight * s_d_interp + 
                    coastal_weight * s_c_interp + 
                    oceanic_weight * s_o_interp)
        
        oxy_mixed = (fjord_weight * o_f_interp + 
                    delta_weight * o_d_interp + 
                    coastal_weight * o_c_interp + 
                    oceanic_weight * o_o_interp)
        
        return depths, temp_mixed, sal_mixed, oxy_mixed
    
    def plot_comparison_profiles(self, save_path=None):
        """Crear comparación visual de todos los ambientes"""
        
        fig, axes = plt.subplots(1, 4, figsize=(20, 10), sharey=False)
        
        environments = ['fjord', 'delta', 'coastal', 'oceanic']
        profile_functions = [
            self.generate_fjord_profile,
            self.generate_delta_profile, 
            self.generate_coastal_profile,
            self.generate_oceanic_profile
        ]
        
        for i, (env, func) in enumerate(zip(environments, profile_functions)):
            depths, temp, sal, oxy = func()
            
            # Subplot para cada variable
            ax = axes[i]
            
            # Temperatura
            ax2 = ax.twiny()
            ax3 = ax.twiny()
            
            # Posicionar ejes
            ax3.spines['top'].set_position(('outward', 60))
            
            # Plotear perfiles
            l1 = ax.plot(temp, -depths, 'r-', linewidth=2.5, label='Temperatura')
            l2 = ax2.plot(sal, -depths, 'b-', linewidth=2.5, label='Salinidad')
            l3 = ax3.plot(oxy, -depths, 'g-', linewidth=2.5, label='Oxígeno')
            
            # Configurar ejes
            ax.set_xlabel('Temperatura (°C)', color='red')
            ax2.set_xlabel('Salinidad (PSU)', color='blue')
            ax3.set_xlabel('Oxígeno (μmol/L)', color='green')
            
            ax.tick_params(axis='x', colors='red')
            ax2.tick_params(axis='x', colors='blue')
            ax3.tick_params(axis='x', colors='green')
            
            if i == 0:
                ax.set_ylabel('Profundidad (m)')
            
            ax.set_title(f'{self.environments[env]["name"]}\n({self.environments[env]["max_depth"]}m)', 
                        fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            
            # Invertir eje Y
            ax.invert_yaxis()
            
            # Agregar información del ambiente
            textstr = f'Ubicación típica:\n{self.environments[env]["typical_location"]}\n\n'
            textstr += f'Características:\n{self.environments[env]["description"]}'
            
            ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=9,
                   verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        plt.suptitle('Perfiles CTD por Ambiente Marino - Comparación', fontsize=18, fontweight='bold')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def create_interactive_dashboard(self):
        """Crear dashboard interactivo con Plotly"""
        
        # Generar datos para todos los ambientes
        data = {}
        for env in ['fjord', 'delta', 'coastal', 'oceanic']:
            if env == 'fjord':
                depths, temp, sal, oxy = self.generate_fjord_profile()
            elif env == 'delta':
                depths, temp, sal, oxy = self.generate_delta_profile()
            elif env == 'coastal':
                depths, temp, sal, oxy = self.generate_coastal_profile()
            elif env == 'oceanic':
                depths, temp, sal, oxy = self.generate_oceanic_profile()
            
            data[env] = {
                'depths': depths.tolist(),
                'temperature': temp.tolist(),
                'salinity': sal.tolist(),
                'oxygen': oxy.tolist()
            }
        
        # Crear subplots
        fig = make_subplots(
            rows=2, cols=3,
            specs=[
                [{"rowspan": 2}, {"type": "xy"}, {"type": "xy"}],
                [None, {"type": "xy"}, {"type": "xy"}]
            ],
            subplot_titles=["Perfiles Verticales", "Diagrama T-S", "Distribución de Oxígeno",
                           "Gradientes Verticales", "Características por Ambiente"],
            horizontal_spacing=0.08,
            vertical_spacing=0.12
        )
        
        # Colores para cada ambiente
        colors = ['#2E8B57', '#8B4513', '#4682B4', '#191970']
        
        # 1. Perfiles verticales principales
        for i, env in enumerate(['fjord', 'delta', 'coastal', 'oceanic']):
            env_data = data[env]
            
            # Temperatura
            fig.add_trace(
                go.Scatter(
                    x=env_data['temperature'],
                    y=[-d for d in env_data['depths']],
                    mode='lines',
                    name=f'{self.environments[env]["name"]} - T',
                    line=dict(color=colors[i], width=3),
                    hovertemplate="<b>%{fullData.name}</b><br>" +
                                 "Temperatura: %{x:.1f}°C<br>" +
                                 "Profundidad: %{y:.0f}m<extra></extra>",
                    legendgroup=env
                ),
                row=1, col=1
            )
        
        # 2. Diagrama T-S
        for i, env in enumerate(['fjord', 'delta', 'coastal', 'oceanic']):
            env_data = data[env]
            
            fig.add_trace(
                go.Scatter(
                    x=env_data['salinity'],
                    y=env_data['temperature'],
                    mode='markers+lines',
                    name=f'{self.environments[env]["name"]}',
                    marker=dict(color=colors[i], size=4),
                    line=dict(color=colors[i], width=2),
                    showlegend=False,
                    hovertemplate="<b>%{fullData.name}</b><br>" +
                                 "Salinidad: %{x:.1f} PSU<br>" +
                                 "Temperatura: %{y:.1f}°C<extra></extra>"
                ),
                row=1, col=2
            )
        
        # 3. Perfiles de oxígeno
        for i, env in enumerate(['fjord', 'delta', 'coastal', 'oceanic']):
            env_data = data[env]
            
            fig.add_trace(
                go.Scatter(
                    x=env_data['oxygen'],
                    y=[-d for d in env_data['depths']],
                    mode='lines',
                    name=f'{self.environments[env]["name"]} - O₂',
                    line=dict(color=colors[i], width=2, dash='dot'),
                    showlegend=False,
                    hovertemplate="<b>%{fullData.name}</b><br>" +
                                 "Oxígeno: %{x:.0f} μmol/L<br>" +
                                 "Profundidad: %{y:.0f}m<extra></extra>"
                ),
                row=1, col=3
            )
        
        # 4. Gradientes (derivadas)
        for i, env in enumerate(['coastal', 'oceanic']):  # Solo ambientes profundos
            env_data = data[env]
            
            # Calcular gradiente de temperatura
            temp_grad = np.gradient(env_data['temperature'], env_data['depths'])
            
            fig.add_trace(
                go.Scatter(
                    x=temp_grad,
                    y=[-d for d in env_data['depths']],
                    mode='lines',
                    name=f'{self.environments[env]["name"]} - dT/dz',
                    line=dict(color=colors[i+2], width=2),
                    showlegend=False,
                    hovertemplate="<b>%{fullData.name}</b><br>" +
                                 "Gradiente T: %{x:.3f}°C/m<br>" +
                                 "Profundidad: %{y:.0f}m<extra></extra>"
                ),
                row=2, col=2
            )
        
        # 5. Tabla de características
        characteristics = []
        for env in ['fjord', 'delta', 'coastal', 'oceanic']:
            env_info = self.environments[env]
            env_data = data[env]
            
            characteristics.append([
                env_info['name'],
                f"{env_info['max_depth']}m",
                f"{np.mean(env_data['temperature']):.1f}°C",
                f"{np.mean(env_data['salinity']):.1f}",
                f"{np.mean(env_data['oxygen']):.0f}"
            ])
        
        fig.add_trace(
            go.Table(
                header=dict(values=['Ambiente', 'Prof. Max', 'T Media', 'S Media', 'O₂ Medio'],
                           fill_color='lightblue',
                           align='center',
                           font=dict(size=12, color='black')),
                cells=dict(values=list(zip(*characteristics)),
                          fill_color='white',
                          align='center',
                          font=dict(size=11))
            ),
            row=2, col=3
        )
        
        # Configurar layout
        fig.update_layout(
            height=800,
            title_text="Dashboard CTD - Ambientes Marinos Comparativos",
            font=dict(size=11),
            showlegend=True,
            legend=dict(x=0.02, y=0.98)
        )
        
        # Actualizar ejes
        fig.update_xaxes(title_text="Temperatura (°C)", row=1, col=1)
        fig.update_yaxes(title_text="Profundidad (m)", row=1, col=1)
        
        fig.update_xaxes(title_text="Salinidad (PSU)", row=1, col=2)
        fig.update_yaxes(title_text="Temperatura (°C)", row=1, col=2)
        
        fig.update_xaxes(title_text="Oxígeno (μmol/L)", row=1, col=3)
        fig.update_yaxes(title_text="Profundidad (m)", row=1, col=3)
        
        fig.update_xaxes(title_text="Gradiente T (°C/m)", row=2, col=2)
        fig.update_yaxes(title_text="Profundidad (m)", row=2, col=2)
        
        return fig, data
    
    def export_data_for_web(self, filename='ctd_data.json'):
        """Exportar datos en formato JSON para el dashboard web"""
        
        web_data = {
            'metadata': {
                'generated': datetime.now().isoformat(),
                'description': 'CTD profiles for different marine environments',
                'environments': self.environments
            },
            'profiles': {}
        }
        
        # Generar datos para cada ambiente
        for env in ['fjord', 'delta', 'coastal', 'oceanic']:
            if env == 'fjord':
                depths, temp, sal, oxy = self.generate_fjord_profile()
            elif env == 'delta':
                depths, temp, sal, oxy = self.generate_delta_profile()
            elif env == 'coastal':
                depths, temp, sal, oxy = self.generate_coastal_profile()
            elif env == 'oceanic':
                depths, temp, sal, oxy = self.generate_oceanic_profile()
            
            web_data['profiles'][env] = {
                'depths': depths.tolist(),
                'temperature': temp.tolist(),
                'salinity': sal.tolist(),
                'oxygen': oxy.tolist(),
                'color': self.colors[env],
                'max_depth': self.environments[env]['max_depth']
            }
        
        # Guardar archivo JSON
        with open(filename, 'w') as f:
            json.dump(web_data, f, indent=2)
        
        print(f"Datos exportados a {filename}")
        return web_data

def demo_ctd_environments():
    """Función de demostración del sistema CTD"""
    
    print("🌊 Iniciando demo de perfiles CTD por ambientes...")
    
    # Crear instancia del perfilador
    ctd_profiler = CTDEnvironmentProfiler()
    
    # 1. Crear comparación estática
    print("📊 Generando comparación de perfiles...")
    fig_comparison = ctd_profiler.plot_comparison_profiles()
    
    # 2. Crear dashboard interactivo
    print("🎮 Creando dashboard interactivo...")
    fig_interactive, data = ctd_profiler.create_interactive_dashboard()
    
    # 3. Exportar datos para web
    print("💾 Exportando datos para dashboard web...")
    web_data = ctd_profiler.export_data_for_web()
    
    # 4. Ejemplo de perfil mixto
    print("🔄 Generando perfil mixto como ejemplo...")
    depths, temp, sal, oxy = ctd_profiler.generate_mixed_profile(
        fjord_weight=0.3, coastal_weight=0.7, max_depth=300
    )
    
    # Plotear perfil mixto
    fig_mixed, ax = plt.subplots(1, 3, figsize=(15, 8))
    
    ax[0].plot(temp, -depths, 'purple', linewidth=2.5, label='Perfil Mixto')
    ax[0].set_xlabel('Temperatura (°C)')
    ax[0].set_ylabel('Profundidad (m)')
    ax[0].set_title('Temperatura\n(30% Fiordo + 70% Costero)')
    ax[0].grid(True, alpha=0.3)
    ax[0].invert_yaxis()
    
    ax[1].plot(sal, -depths, 'purple', linewidth=2.5)
    ax[1].set_xlabel('Salinidad (PSU)')
    ax[1].set_title('Salinidad\n(Perfil Intermedio)')
    ax[1].grid(True, alpha=0.3)
    ax[1].invert_yaxis()
    
    ax[2].plot(oxy, -depths, 'purple', linewidth=2.5)
    ax[2].set_xlabel('Oxígeno (μmol/L)')
    ax[2].set_title('Oxígeno Disuelto\n(Características Mixtas)')
    ax[2].grid(True, alpha=0.3)
    ax[2].invert_yaxis()
    
    plt.suptitle('Ejemplo de Perfil CTD Mixto', fontsize=16)
    plt.tight_layout()
    
    # Mostrar gráficos
    plt.show()
    fig_interactive.show()
    
    print("✅ Demo completado!")
    print("📁 Archivos generados:")
    print("   - ctd_data.json (datos para dashboard web)")
    print("💡 Próximo paso: Crear dashboard web interactivo")

if __name__ == "__main__":
    demo_ctd_environments()