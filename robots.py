import streamlit as st
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

st.set_page_config(
page_title="Robot Optimizer",
page_icon="🤖",
layout="wide"
)

st.markdown("""

<style>
.main {
    background-color: #0f172a;
}

h1 {
    color: #38bdf8;
}

.stButton > button {
    background-color: #06b6d4;
    color: white;
    font-weight: bold;
    border-radius: 12px;
    height: 55px;
    width: 100%;
}

.result-box {
    padding:20px;
    border-radius:15px;
    background:#1e293b;
    color:white;
}
</style>

""", unsafe_allow_html=True)

st.title("🤖 Optimizador de Robots Industriales")

st.subheader("Costos de Componentes (USD)")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
c1 = st.number_input("LiDAR", value=450)

with col2:
c2 = st.number_input("Cámara", value=180)

with col3:
c3 = st.number_input("Procesador IA", value=350)

with col4:
c4 = st.number_input("Batería", value=220)

with col5:
c5 = st.number_input("Motor", value=160)

st.subheader("Restricciones")

r1 = st.number_input(
"Mínimo Sensores + Cámaras",
value=10
)

r2 = st.number_input(
"Mínimo Procesadores + Baterías",
value=8
)

r3 = st.number_input(
"Mínimo Motores",
value=6
)

presupuesto = st.number_input(
"Presupuesto máximo LiDAR + Cámaras",
value=2500
)

max_componentes = st.number_input(
"Máximo total de componentes",
value=25
)

min_lidar = st.number_input(
"Mínimo LiDAR",
value=2
)

resolver = st.button("🚀 Resolver")

if resolver:

```
c = [c1, c2, c3, c4, c5]

A = [
    [1,1,0,0,0],
    [0,0,1,1,0],
    [0,0,0,0,1],
    [0,0,-1,1,0],
    [c1,c2,0,0,0],
    [1,1,1,1,1],
    [1,0,0,0,0]
]

bl = [
    r1,
    r2,
    r3,
    0,
    -np.inf,
    -np.inf,
    min_lidar
]

bu = [
    np.inf,
    np.inf,
    np.inf,
    np.inf,
    presupuesto,
    max_componentes,
    np.inf
]

constraints = LinearConstraint(A, bl, bu)

bounds = Bounds(
    [0]*5,
    [np.inf]*5
)

res = milp(
    c=c,
    constraints=constraints,
    bounds=bounds,
    integrality=[1]*5
)

st.divider()

if res.success:

    st.success("Modelo resuelto correctamente")

    st.markdown(
        f"""
        <div class="result-box">
        <h2>💰 Costo mínimo: USD {res.fun:,.2f}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    nombres = [
        "LiDAR",
        "Cámaras",
        "Procesadores IA",
        "Baterías",
        "Motores"
    ]

    for nombre, valor in zip(nombres, res.x):
        st.write(f"**{nombre}:** {int(valor)}")

else:
    st.error(
        "No existe solución factible para las restricciones ingresadas."
    )
```
