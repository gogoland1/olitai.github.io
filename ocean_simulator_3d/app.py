import dash
from dash import html, dcc, Input, Output, State, clientside_callback, ClientsideFunction
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from datetime import datetime
import json

# Inicializar app Dash
app = dash.Dash(__name__, external_stylesheets=[
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
])

# Configurar el layout principal
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("🌊 Simulador Oceánico 3D - Plotly + Three.js", 
                style={'color': '#60a5fa', 'textAlign': 'center', 'margin': '0'}),
        html.P("Exploración interactiva de ecosistemas marinos verticales",
               style={'textAlign': 'center', 'color': '#93c5fd', 'margin': '10px 0'})
    ], style={
        'background': 'linear-gradient(135deg, #0a1929 0%, #1e3a8a 100%)',
        'padding': '20px',
        'borderBottom': '2px solid rgba(59, 130, 246, 0.3)'
    }),
    
    # Panel de controles principales
    html.Div([
        html.Div([
            html.Label("⏰ Hora del Día", style={'color': '#60a5fa', 'fontWeight': 'bold'}),
            dcc.Slider(
                id='time-slider',
                min=0, max=23, step=1, value=12,
                marks={i: f'{i}:00' for i in range(0, 24, 6)},
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '0 20px'}),
        
        html.Div([
            html.Label("🌊 Tipo de Agua", style={'color': '#60a5fa', 'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='water-type-dropdown',
                options=[
                    {'label': '🌌 Oceánico (K=0.05)', 'value': 'oceanic'},
                    {'label': '🏖️ Costero (K=0.15)', 'value': 'coastal'},
                    {'label': '🏞️ Estuarino (K=0.5)', 'value': 'estuarine'}
                ],
                value='oceanic',
                style={'background': '#1e3a8a', 'color': 'white'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '0 20px'}),
        
        html.Div([
            html.Button("▶️ Iniciar Simulación", id='play-btn', n_clicks=0,
                       style={'background': '#22c55e', 'color': 'white', 'border': 'none', 
                             'padding': '10px 20px', 'borderRadius': '8px', 'margin': '5px'}),
            html.Button("⏸️ Pausar", id='pause-btn', n_clicks=0,
                       style={'background': '#f59e0b', 'color': 'white', 'border': 'none',
                             'padding': '10px 20px', 'borderRadius': '8px', 'margin': '5px'})
        ], style={'width': '30%', 'display': 'inline-block', 'textAlign': 'center', 'padding': '20px'})
    ], style={
        'background': 'rgba(0, 0, 0, 0.8)', 
        'padding': '20px',
        'borderBottom': '1px solid rgba(59, 130, 246, 0.3)'
    }),
    
    # Contenedor principal con paneles
    html.Div([
        # Panel Zona Fótica
        html.Div([
            html.H3("☀️ Zona Fótica (0-100m)", 
                   style={'color': '#22c55e', 'textAlign': 'center', 'marginBottom': '20px'}),
            
            # Gráfico 3D Plotly para zona fótica
            dcc.Graph(id='photic-zone-3d', style={'height': '400px'}),
            
            # Controles específicos zona fótica
            html.Div([
                html.Label("💡 Intensidad Lumínica (%)", style={'color': '#93c5fd'}),
                dcc.Slider(id='light-intensity', min=0, max=100, step=5, value=80,
                          marks={i: str(i) for i in range(0, 101, 25)}),
                
                html.Label("🧪 Nutrientes (μM)", style={'color': '#93c5fd'}),
                dcc.Slider(id='nutrients', min=0, max=30, step=1, value=15,
                          marks={i: str(i) for i in range(0, 31, 10)}),
                
                html.Label("🌡️ Temperatura (°C)", style={'color': '#93c5fd'}),
                dcc.Slider(id='temperature', min=5, max=25, step=1, value=18,
                          marks={i: str(i) for i in range(5, 26, 5)})
            ], style={'padding': '20px', 'background': 'rgba(34, 197, 94, 0.1)', 
                     'borderRadius': '10px', 'margin': '10px 0'})
            
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 
                 'padding': '20px', 'background': 'rgba(0, 0, 0, 0.6)', 
                 'borderRadius': '10px', 'margin': '1%'}),
        
        # Panel Zona Profunda
        html.Div([
            html.H3("🌊 Zona Profunda (100-2000m)", 
                   style={'color': '#8b5cf6', 'textAlign': 'center', 'marginBottom': '20px'}),
            
            # Gráfico 3D Plotly para zona profunda
            dcc.Graph(id='deep-zone-3d', style={'height': '400px'}),
            
            # Controles específicos zona profunda
            html.Div([
                html.Label("🦠 Actividad Microbiana (%)", style={'color': '#93c5fd'}),
                dcc.Slider(id='microbial-activity', min=0, max=100, step=5, value=60,
                          marks={i: str(i) for i in range(0, 101, 25)}),
                
                html.Label("🔄 Remineralización (%)", style={'color': '#93c5fd'}),
                dcc.Slider(id='remineralization', min=0, max=100, step=5, value=75,
                          marks={i: str(i) for i in range(0, 101, 25)}),
                
                html.Label("⬇️ Flux de Carbono (mg C/m²/día)", style={'color': '#93c5fd'}),
                dcc.Slider(id='carbon-flux', min=0, max=100, step=5, value=40,
                          marks={i: str(i) for i in range(0, 101, 25)})
            ], style={'padding': '20px', 'background': 'rgba(139, 92, 246, 0.1)', 
                     'borderRadius': '10px', 'margin': '10px 0'})
            
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 
                 'padding': '20px', 'background': 'rgba(0, 0, 0, 0.6)', 
                 'borderRadius': '10px', 'margin': '1%'})
    ], style={'padding': '20px'}),
    
    # Panel de Three.js (se incrustará dinámicamente)
    html.Div([
        html.H3("🎮 Vista 3D Interactiva - Three.js", 
               style={'color': '#60a5fa', 'textAlign': 'center'}),
        html.Div(id='threejs-container', style={
            'width': '100%', 
            'height': '500px', 
            'background': 'black',
            'borderRadius': '10px',
            'border': '2px solid rgba(59, 130, 246, 0.3)'
        })
    ], style={'padding': '20px', 'background': 'rgba(0, 0, 0, 0.8)', 'margin': '20px'}),
    
    # Panel de datos en tiempo real
    html.Div([
        html.H4("📊 Datos en Tiempo Real", style={'color': '#60a5fa'}),
        html.Div(id='realtime-data', style={'color': '#93c5fd'})
    ], style={
        'position': 'fixed', 'top': '100px', 'right': '20px', 'width': '300px',
        'background': 'rgba(0, 0, 0, 0.9)', 'padding': '15px', 'borderRadius': '10px',
        'border': '1px solid rgba(59, 130, 246, 0.3)', 'zIndex': '1000'
    }),
    
    # Stores para datos
    dcc.Store(id='simulation-data'),
    dcc.Store(id='organism-positions'),
    
    # Interval para animaciones
    dcc.Interval(
        id='animation-interval',
        interval=500,  # 500ms
        n_intervals=0,
        disabled=True
    )
    
], style={
    'background': 'linear-gradient(135deg, #0a1929 0%, #1e3a8a 100%)',
    'minHeight': '100vh',
    'color': 'white',
    'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
})

# Función para generar datos de organismos
def generate_organism_data(zone_type, time_hour, water_type, **params):
    """Genera posiciones y tipos de organismos según parámetros"""
    np.random.seed(42)  # Para reproducibilidad
    
    organisms = []
    
    if zone_type == 'photic':
        # Zona fótica: 0-100m
        depth_range = (0, 100)
        
        # Fitoplancton (más abundante en superficie)
        for i in range(50):
            depth = np.random.exponential(20)  # Concentrado en superficie
            if depth <= 100:
                organisms.append({
                    'type': 'phytoplankton',
                    'x': np.random.uniform(-50, 50),
                    'y': -depth,
                    'z': np.random.uniform(-50, 50),
                    'size': np.random.uniform(0.5, 2),
                    'color': '#22c55e'
                })
        
        # Diatomeas
        for i in range(30):
            depth = np.random.uniform(0, 80)
            organisms.append({
                'type': 'diatom',
                'x': np.random.uniform(-40, 40),
                'y': -depth,
                'z': np.random.uniform(-40, 40),
                'size': np.random.uniform(1, 3),
                'color': '#84cc16'
            })
        
        # Copépodos (migración vertical según hora)
        migration_factor = calculate_migration_factor(time_hour)
        for i in range(25):
            base_depth = np.random.uniform(20, 80)
            migrated_depth = base_depth - (migration_factor * 30)
            organisms.append({
                'type': 'copepod',
                'x': np.random.uniform(-45, 45),
                'y': -max(0, migrated_depth),
                'z': np.random.uniform(-45, 45),
                'size': np.random.uniform(2, 4),
                'color': '#f97316'
            })
            
    else:  # deep zone
        # Zona profunda: 100-2000m
        
        # Krill (migración nocturna)
        migration_factor = calculate_migration_factor(time_hour)
        for i in range(20):
            base_depth = np.random.uniform(100, 400)
            migrated_depth = base_depth - (migration_factor * 100)
            organisms.append({
                'type': 'krill',
                'x': np.random.uniform(-60, 60),
                'y': -max(100, migrated_depth),
                'z': np.random.uniform(-60, 60),
                'size': np.random.uniform(3, 6),
                'color': '#ef4444'
            })
        
        # Bacterias
        for i in range(80):
            depth = np.random.uniform(100, 1000)
            organisms.append({
                'type': 'bacteria',
                'x': np.random.uniform(-70, 70),
                'y': -depth,
                'z': np.random.uniform(-70, 70),
                'size': np.random.uniform(0.3, 1),
                'color': '#8b5cf6'
            })
        
        # Pellets fecales (hundimiento)
        for i in range(40):
            depth = np.random.uniform(100, 1500)
            organisms.append({
                'type': 'fecal_pellet',
                'x': np.random.uniform(-50, 50),
                'y': -depth,
                'z': np.random.uniform(-50, 50),
                'size': np.random.uniform(1, 3),
                'color': '#78716c'
            })
    
    return organisms

def calculate_migration_factor(time_hour):
    """Calcula factor de migración vertical según hora"""
    if time_hour >= 20 or time_hour <= 6:
        return 0.8  # Máxima migración nocturna
    elif 18 <= time_hour < 20:
        return (time_hour - 18) / 2 * 0.8  # Ascenso gradual
    elif 6 < time_hour <= 8:
        return (8 - time_hour) / 2 * 0.8  # Descenso gradual
    return 0  # Día - posición normal

def calculate_light_attenuation(depth, water_type, light_intensity):
    """Calcula atenuación de luz por profundidad y tipo de agua"""
    attenuation_coeffs = {
        'oceanic': 0.05,
        'coastal': 0.15,
        'estuarine': 0.5
    }
    
    k = attenuation_coeffs[water_type]
    surface_light = light_intensity / 100
    
    return surface_light * np.exp(-k * abs(depth))

# Callbacks para interactividad

@app.callback(
    Output('photic-zone-3d', 'figure'),
    [Input('time-slider', 'value'),
     Input('water-type-dropdown', 'value'),
     Input('light-intensity', 'value'),
     Input('nutrients', 'value'),
     Input('temperature', 'value'),
     Input('animation-interval', 'n_intervals')]
)
def update_photic_zone_3d(time_hour, water_type, light_intensity, nutrients, temperature, n_intervals):
    """Actualiza la visualización 3D de la zona fótica"""
    
    # Generar datos de organismos
    organisms = generate_organism_data('photic', time_hour, water_type, 
                                     light=light_intensity, nutrients=nutrients, temp=temperature)
    
    # Crear figura 3D
    fig = go.Figure()
    
    # Agrupar organismos por tipo
    organism_types = {}
    for org in organisms:
        if org['type'] not in organism_types:
            organism_types[org['type']] = {'x': [], 'y': [], 'z': [], 'sizes': [], 'colors': []}
        organism_types[org['type']]['x'].append(org['x'])
        organism_types[org['type']]['y'].append(org['y'])
        organism_types[org['type']]['z'].append(org['z'])
        organism_types[org['type']]['sizes'].append(org['size'])
        organism_types[org['type']]['colors'].append(org['color'])
    
    # Agregar cada tipo de organismo como scatter3d
    for org_type, data in organism_types.items():
        fig.add_trace(go.Scatter3d(
            x=data['x'],
            y=data['y'],
            z=data['z'],
            mode='markers',
            marker=dict(
                size=data['sizes'],
                color=data['colors'][0],  # Color uniforme por tipo
                opacity=0.8
            ),
            name=org_type.replace('_', ' ').title(),
            hovertemplate=f"<b>{org_type}</b><br>" +
                         "X: %{x}<br>Y: %{y}<br>Z: %{z}<extra></extra>"
        ))
    
    # Crear gradiente de fondo para simular atenuación de luz
    depths = np.linspace(0, -100, 20)
    light_grid = []
    for depth in depths:
        light_val = calculate_light_attenuation(depth, water_type, light_intensity)
        light_grid.append(light_val)
    
    # Configurar layout
    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[-60, 60], title="X (m)"),
            yaxis=dict(range=[-100, 0], title="Profundidad (m)"),
            zaxis=dict(range=[-60, 60], title="Z (m)"),
            bgcolor='rgba(0, 50, 100, 0.1)',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        title=f"Zona Fótica - {time_hour}:00h - {water_type.title()}",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    return fig

@app.callback(
    Output('deep-zone-3d', 'figure'),
    [Input('time-slider', 'value'),
     Input('water-type-dropdown', 'value'),
     Input('microbial-activity', 'value'),
     Input('remineralization', 'value'),
     Input('carbon-flux', 'value'),
     Input('animation-interval', 'n_intervals')]
)
def update_deep_zone_3d(time_hour, water_type, microbial, reminer, carbon_flux, n_intervals):
    """Actualiza la visualización 3D de la zona profunda"""
    
    # Generar datos de organismos
    organisms = generate_organism_data('deep', time_hour, water_type,
                                     microbial=microbial, reminer=reminer, flux=carbon_flux)
    
    # Crear figura 3D
    fig = go.Figure()
    
    # Agrupar organismos por tipo
    organism_types = {}
    for org in organisms:
        if org['type'] not in organism_types:
            organism_types[org['type']] = {'x': [], 'y': [], 'z': [], 'sizes': [], 'colors': []}
        organism_types[org['type']]['x'].append(org['x'])
        organism_types[org['type']]['y'].append(org['y'])
        organism_types[org['type']]['z'].append(org['z'])
        organism_types[org['type']]['sizes'].append(org['size'])
        organism_types[org['type']]['colors'].append(org['color'])
    
    # Agregar cada tipo de organismo
    for org_type, data in organism_types.items():
        fig.add_trace(go.Scatter3d(
            x=data['x'],
            y=data['y'],
            z=data['z'],
            mode='markers',
            marker=dict(
                size=data['sizes'],
                color=data['colors'][0],
                opacity=0.7
            ),
            name=org_type.replace('_', ' ').title(),
            hovertemplate=f"<b>{org_type}</b><br>" +
                         "X: %{x}<br>Y: %{y}<br>Z: %{z}<extra></extra>"
        ))
    
    # Configurar layout
    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[-80, 80], title="X (m)"),
            yaxis=dict(range=[-2000, -100], title="Profundidad (m)"),
            zaxis=dict(range=[-80, 80], title="Z (m)"),
            bgcolor='rgba(0, 0, 50, 0.3)',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        title=f"Zona Profunda - {time_hour}:00h - Loop Microbiano",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    return fig

@app.callback(
    Output('realtime-data', 'children'),
    [Input('time-slider', 'value'),
     Input('water-type-dropdown', 'value'),
     Input('light-intensity', 'value'),
     Input('nutrients', 'value'),
     Input('temperature', 'value'),
     Input('microbial-activity', 'value')]
)
def update_realtime_data(time_hour, water_type, light, nutrients, temp, microbial):
    """Actualiza datos en tiempo real"""
    
    # Cálculos en tiempo real
    day_factor = 1 if 6 <= time_hour <= 18 else 0.3
    productivity = (light/100) * (nutrients/30) * (temp/25) * day_factor * 100
    chlorophyll = productivity * 0.04
    
    attenuation_coeff = {'oceanic': 0.05, 'coastal': 0.15, 'estuarine': 0.5}[water_type]
    euphotic_depth = min(100, round(4.6 / attenuation_coeff))
    
    migration_factor = calculate_migration_factor(time_hour)
    
    return html.Div([
        html.P(f"⏰ Hora: {time_hour}:00"),
        html.P(f"🌊 Agua: {water_type.title()}"),
        html.P(f"💡 Productividad: {productivity:.0f}%"),
        html.P(f"🧬 Clorofila-a: {chlorophyll:.1f} mg/m³"),
        html.P(f"☀️ Zona Eufótica: {euphotic_depth}m"),
        html.P(f"🦐 Migración: {migration_factor*100:.0f}%"),
        html.P(f"🦠 Actividad Microbiana: {microbial}%"),
        html.Hr(style={'border': '1px solid rgba(59, 130, 246, 0.3)'}),
        html.P(f"🕒 Actualizado: {datetime.now().strftime('%H:%M:%S')}")
    ])

@app.callback(
    Output('animation-interval', 'disabled'),
    [Input('play-btn', 'n_clicks'),
     Input('pause-btn', 'n_clicks')],
    [State('animation-interval', 'disabled')]
)
def control_animation(play_clicks, pause_clicks, current_disabled):
    """Controla play/pause de la animación"""
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return current_disabled
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'play-btn':
        return False  # Habilitar animación
    elif button_id == 'pause-btn':
        return True   # Deshabilitar animación
    
    return current_disabled

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)