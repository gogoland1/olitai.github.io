# 🚀 INICIO RÁPIDO - Dashboard CTD

## ⚡ Opción 1: Terminal (Solo 2 comandos)

```bash
cd ~/proyectos/olitai
python3 run_dashboard.py
```

**¡Eso es todo!** El navegador se abre automáticamente en http://localhost:5000

---

## 🔧 Si no funciona (instalar dependencias):

```bash
cd ~/proyectos/olitai
pip3 install flask flask-cors plotly numpy matplotlib scipy pandas
python3 run_dashboard.py
```

---

## 🌐 Alternativa: Usar con virtual environment

```bash
cd ~/proyectos/olitai
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_web.txt
python3 run_dashboard.py
```

---

## 📱 ¿Qué verás?
- Dashboard interactivo con sliders
- 4 ambientes marinos (fiordo, delta, costero, oceánico)
- Gráficos en tiempo real
- Perfiles de temperatura, salinidad y oxígeno

## 🛑 Para detener
Presiona `Ctrl+C` en la terminal