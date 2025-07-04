#!/usr/bin/env python3
"""
🌐 Dashboard Web CTD - Backend Flask
Sistema web interactivo para perfiles CTD por ambientes marinos
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
import numpy as np
from ctd_environments import CTDEnvironmentProfiler
import plotly.graph_objects as go
import plotly.utils

app = Flask(__name__)
CORS(app)  # Permitir requests desde frontend

# Instancia global del perfilador CTD
ctd_profiler = CTDEnvironmentProfiler()

@app.route('/')
def index():
    """Página principal del dashboard"""
    return render_template('ctd_dashboard.html')

@app.route('/api/environments')
def get_environments():
    """API: Obtener información de todos los ambientes"""
    return jsonify(ctd_profiler.environments)

@app.route('/api/profile/<environment>')
def get_profile(environment):
    """API: Obtener perfil CTD específico por ambiente"""
    
    try:
        if environment == 'fjord':
            depths, temp, sal, oxy = ctd_profiler.generate_fjord_profile()
        elif environment == 'delta':
            depths, temp, sal, oxy = ctd_profiler.generate_delta_profile()
        elif environment == 'coastal':
            depths, temp, sal, oxy = ctd_profiler.generate_coastal_profile()
        elif environment == 'oceanic':
            depths, temp, sal, oxy = ctd_profiler.generate_oceanic_profile()
        else:
            return jsonify({'error': 'Ambiente no válido'}), 400
        
        profile_data = {
            'environment': environment,
            'depths': depths.tolist(),
            'temperature': temp.tolist(),
            'salinity': sal.tolist(),
            'oxygen': oxy.tolist(),
            'color': ctd_profiler.colors[environment],
            'info': ctd_profiler.environments[environment]
        }
        
        return jsonify(profile_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mixed_profile', methods=['POST'])
def get_mixed_profile():
    """API: Obtener perfil CTD mixto con pesos personalizados"""
    
    try:
        data = request.get_json()
        
        # Obtener pesos (por defecto todos iguales)
        fjord_weight = data.get('fjord_weight', 0.25)
        delta_weight = data.get('delta_weight', 0.25)
        coastal_weight = data.get('coastal_weight', 0.25)
        oceanic_weight = data.get('oceanic_weight', 0.25)
        max_depth = data.get('max_depth', 500)
        
        # Generar perfil mixto
        depths, temp, sal, oxy = ctd_profiler.generate_mixed_profile(
            fjord_weight=fjord_weight,
            delta_weight=delta_weight,
            coastal_weight=coastal_weight,
            oceanic_weight=oceanic_weight,
            max_depth=max_depth
        )
        
        # Calcular nombre del ambiente dominante
        weights = {
            'Fiordo': fjord_weight,
            'Delta': delta_weight,
            'Costero': coastal_weight,
            'Oceánico': oceanic_weight
        }
        dominant_env = max(weights, key=weights.get)
        
        profile_data = {
            'environment': 'mixed',
            'dominant_environment': dominant_env,
            'weights': weights,
            'depths': depths.tolist(),
            'temperature': temp.tolist(),
            'salinity': sal.tolist(),
            'oxygen': oxy.tolist(),
            'max_depth': max_depth
        }
        
        return jsonify(profile_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/comparison_plot')
def get_comparison_plot():
    """API: Generar gráfico de comparación Plotly en JSON"""
    
    try:
        fig, data = ctd_profiler.create_interactive_dashboard()
        
        # Convertir figura Plotly a JSON
        graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        return jsonify({
            'plot': graph_json,
            'data': data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ts_diagram')
def get_ts_diagram():
    """API: Generar diagrama T-S para todos los ambientes"""
    
    try:
        fig = go.Figure()
        
        environments = ['fjord', 'delta', 'coastal', 'oceanic']
        colors = ['#2E8B57', '#8B4513', '#4682B4', '#191970']
        
        for i, env in enumerate(environments):
            if env == 'fjord':
                depths, temp, sal, oxy = ctd_profiler.generate_fjord_profile()
            elif env == 'delta':
                depths, temp, sal, oxy = ctd_profiler.generate_delta_profile()
            elif env == 'coastal':
                depths, temp, sal, oxy = ctd_profiler.generate_coastal_profile()
            elif env == 'oceanic':
                depths, temp, sal, oxy = ctd_profiler.generate_oceanic_profile()
            
            fig.add_trace(go.Scatter(
                x=sal,
                y=temp,
                mode='markers+lines',
                name=ctd_profiler.environments[env]['name'],
                marker=dict(
                    color=depths,
                    colorscale='Viridis_r',
                    size=6,
                    colorbar=dict(title="Profundidad (m)") if i == 0 else None,
                    showscale=True if i == 0 else False
                ),
                line=dict(color=colors[i], width=2),
                hovertemplate="<b>%{fullData.name}</b><br>" +
                             "Salinidad: %{x:.1f} PSU<br>" +
                             "Temperatura: %{y:.1f}°C<extra></extra>"
            ))
        
        fig.update_layout(
            title="Diagrama Temperatura-Salinidad por Ambiente",
            xaxis_title="Salinidad (PSU)",
            yaxis_title="Temperatura (°C)",
            width=800,
            height=600
        )
        
        graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        return jsonify({'plot': graph_json})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics/<environment>')
def get_environment_statistics(environment):
    """API: Obtener estadísticas de un ambiente específico"""
    
    try:
        if environment == 'fjord':
            depths, temp, sal, oxy = ctd_profiler.generate_fjord_profile()
        elif environment == 'delta':
            depths, temp, sal, oxy = ctd_profiler.generate_delta_profile()
        elif environment == 'coastal':
            depths, temp, sal, oxy = ctd_profiler.generate_coastal_profile()
        elif environment == 'oceanic':
            depths, temp, sal, oxy = ctd_profiler.generate_oceanic_profile()
        else:
            return jsonify({'error': 'Ambiente no válido'}), 400
        
        # Calcular estadísticas
        stats = {
            'environment': environment,
            'temperature': {
                'mean': float(np.mean(temp)),
                'min': float(np.min(temp)),
                'max': float(np.max(temp)),
                'std': float(np.std(temp)),
                'surface': float(temp[0]),
                'bottom': float(temp[-1])
            },
            'salinity': {
                'mean': float(np.mean(sal)),
                'min': float(np.min(sal)),
                'max': float(np.max(sal)),
                'std': float(np.std(sal)),
                'surface': float(sal[0]),
                'bottom': float(sal[-1])
            },
            'oxygen': {
                'mean': float(np.mean(oxy)),
                'min': float(np.min(oxy)),
                'max': float(np.max(oxy)),
                'std': float(np.std(oxy)),
                'surface': float(oxy[0]),
                'bottom': float(oxy[-1])
            },
            'depth_info': {
                'max_depth': float(depths[-1]),
                'n_points': len(depths)
            }
        }
        
        # Agregar índices oceanográficos
        # Índice de estratificación (diferencia superficie-fondo)
        stats['stratification'] = {
            'temperature': float(temp[0] - temp[-1]),
            'salinity': float(sal[-1] - sal[0]),  # Haloclina
            'oxygen': float(oxy[0] - oxy[-1])
        }
        
        # Profundidad de termoclina (máximo gradiente de temperatura)
        temp_gradient = np.abs(np.gradient(temp, depths))
        thermocline_depth = float(depths[np.argmax(temp_gradient)])
        stats['thermocline_depth'] = thermocline_depth
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🌐 Iniciando servidor web CTD Dashboard...")
    print("📍 Dirección: http://localhost:5000")
    print("🎮 Dashboard interactivo disponible")
    
    app.run(debug=True, host='0.0.0.0', port=5000)