import streamlit as st
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

# --------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# --------------------------------------------------

st.set_page_config(
    page_title="Robot Optimizer",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------------------------
# ESTILOS
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}

h1 {
    color: #38bdf8;
}

h2, h3 {
    color: white;
}

[data-testid="stMetricValue"] {
    color: #22c55e;
}

.stButton > button {
    background-color: #06b6d4;
    color: white;
    border-radius: 12px;
    font-weight: bold;
    height: 55px;
    width: 100%;
    border: none;
}

.stButton > button:hover {
    background-color: #0891b2;
}

.result-box {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    color: white;
    border: 1px solid #38bdf8;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# TÍTULO
# --------------------------------------------------

st.title("🤖 Optimizador de Robots Industriales")

st.write(
    "Ingresá los costos y restricciones del problema para encontrar "
    "la combinación de componentes de menor costo."
)

# --------------------------------------------------
# COSTOS
# --------------------------------------------------

st.subheader("💰 Costos de los Componentes")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    c1 = st.number_input(
        "LiDAR",
        min_value=0.0,
        value=450.0
    )

with col2:
    c2 = st.number_input(
        "Cámara",
        min_value=0.0,
        value=180.0
    )

with col3:
    c3 = st.number_input(
        "Procesador IA",
        min_value=0.0,
        value=350.0
    )

with col4:
    c4 = st.number_input(
        "Batería",
        min_value=0.0,
        value=220.0
    )

with col5:
    c5 = st.number_input(
        "Motor",
        min_value=0.0,
        value=160.0
    )

# --------------------------------------------------
# RESTRICCIONES
# --------------------------------------------------

st.subheader("📋 Restricciones")

r1 = st.number_input(
    "Mínimo Sensores + Cámaras",
    min_value=0,
    value=10
)

r2 = st.number_input(
    "Mínimo Procesadores + Baterías",
    min_value=0,
    value=8
)

r3 = st.number_input(
    "Mínimo Motores",
    min_value=0,
    value=6
)

presupuesto = st.number_input(
    "Presupuesto máximo LiDAR + Cámaras (USD)",
    min_value=0.0,
    value=2500.0
)

max_componentes = st.number_input(
    "Máximo total de componentes",
    min_value=1,
    value=25
)

min_lidar = st.number_input(
    "Mínimo de sensores LiDAR",
    min_value=0,
    value=2
)

# --------------------------------------------------
# BOTÓN
# --------------------------------------------------

resolver = st.button("🚀 Resolver")

# --------------------------------------------------
# RESOLVER
# --------------------------------------------------

if resolver:

    c = [c1, c2, c3, c4, c5]

    A = [
        [1, 1, 0, 0, 0],        # x1 + x2 >= r1
        [0, 0, 1, 1, 0],        # x3 + x4 >= r2
        [0, 0, 0, 0, 1],        # x5 >= r3
        [0, 0, -1, 1, 0],       # x4 >= x3
        [c1, c2, 0, 0, 0],      # costo percepción
        [1, 1, 1, 1, 1],        # máximo componentes
        [1, 0, 0, 0, 0]         # mínimo lidar
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
        [0, 0, 0, 0, 0],
        [np.inf, np.inf, np.inf, np.inf, np.inf]
    )

    res = milp(
        c=c,
        constraints=constraints,
        bounds=bounds,
        integrality=[1, 1, 1, 1, 1]
    )

    st.divider()

    if res.success:

        st.success("✅ Solución encontrada")

        st.metric(
            label="Costo mínimo",
            value=f"USD {res.fun:,.2f}"
        )

        st.subheader("🔧 Componentes óptimos")

        nombres = [
            "LiDAR",
            "Cámaras",
            "Procesadores IA",
            "Baterías",
            "Motores"
        ]

        for nombre, valor in zip(nombres, res.x):
            st.write(f"**{nombre}:** {int(round(valor))}")

    else:

        st.error(
            "❌ No existe una solución factible para las restricciones ingresadas."
        )

        st.write(res.message)
