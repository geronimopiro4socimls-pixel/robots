import streamlit as st
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================

st.set_page_config(
    page_title="🤖 Robot Optimizer",
    page_icon="🤖",
    layout="wide"
)

# ==========================================
# ESTILOS
# ==========================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #ff7b00,
        #ff9500,
        #ff5400
    );
}

h1, h2, h3, p, label {
    color: white !important;
}

[data-testid="stMetricValue"] {
    color: #00ff88 !important;
    font-size: 40px;
}

.stButton > button {
    background-color: #222222;
    color: white !important;
    font-weight: bold;
    border-radius: 12px;
    height: 60px;
    width: 100%;
    border: none;
    font-size: 18px;
}

.stButton > button:hover {
    background-color: #ffe5d0;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# TÍTULO
# ==========================================

st.title("🤖 Optimizador de Robots Industriales")

st.write(
    "Ingresá los costos y restricciones. "
    "El sistema calculará automáticamente "
    "la solución de menor costo."
)

# ==========================================
# COSTOS
# ==========================================

st.subheader("💰 Costos de Componentes (USD)")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    c1 = st.number_input(
        "LiDAR",
        min_value=1,
        value=450,
        step=1
    )

with col2:
    c2 = st.number_input(
        "Cámara",
        min_value=1,
        value=180,
        step=1
    )

with col3:
    c3 = st.number_input(
        "Procesador IA",
        min_value=1,
        value=350,
        step=1
    )

with col4:
    c4 = st.number_input(
        "Batería",
        min_value=1,
        value=220,
        step=1
    )

with col5:
    c5 = st.number_input(
        "Motor",
        min_value=1,
        value=160,
        step=1
    )

# ==========================================
# RESTRICCIONES
# ==========================================

st.subheader("📋 Restricciones")

r1 = st.number_input(
    "Mínimo Sensores + Cámaras",
    min_value=0,
    value=10,
    step=1
)

r2 = st.number_input(
    "Mínimo Procesadores + Baterías",
    min_value=1,
    value=8,
    step=1
)

r3 = st.number_input(
    "Mínimo Motores",
    min_value=0,
    value=6,
    step=1
)

presupuesto = st.number_input(
    "Presupuesto máximo LiDAR + Cámaras",
    min_value=0,
    value=2500,
    step=1
)

max_componentes = st.number_input(
    "Máximo total de componentes",
    min_value=1,
    value=25,
    step=1
)

min_lidar = st.number_input(
    "Mínimo de sensores LiDAR",
    min_value=0,
    value=2,
    step=1
)

# ==========================================
# BOTÓN
# ==========================================

resolver = st.button("🚀 Resolver")

# ==========================================
# OPTIMIZACIÓN
# ==========================================

if resolver:

    c = [c1, c2, c3, c4, c5]

    A = [
        [1, 1, 0, 0, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 0, 0, 1],
        [0, 0, -1, 1, 0],
        [c1, c2, 0, 0, 0],
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0]
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
            value=f"USD {int(round(res.fun))}"
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
            st.write(
                f"**{nombre}:** {int(round(valor))}"
            )

    else:

        st.error(
            "❌ No existe una solución factible para las restricciones ingresadas."
        )

        st.write(res.message)
