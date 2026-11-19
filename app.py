import unicodedata

import pandas as pd
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="xShots Quantitative Scanner • Pro",
    page_icon="⚽",
    layout="wide",
)

# Estilos visuales modernos (Dark Mode tipo Trading)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0d1117;
        color: #f8fafc;
    }
    div[data-testid="metric-container"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 15px;
        border-radius: 10px;
    }
    .main-title {
        font-size: 2rem;
        font-weight: bold;
        color: #ffffff;
    }
    .sub-title {
        color: #8b949e;
        margin-bottom: 20px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-title">⚽ xShots Quantitative Scanner</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-title">Análisis de Valor por Equipo & Edge de Mercado</div>',
    unsafe_allow_html=True,
)

EXCEL_BUNDESLIGA = "tiros_bundr.xlsx"
EXCEL_BRASIL = "Tiros Brasil .xlsx"

# Columnas estándar que usa el motor
COLS = [
    "PJ (Local)",
    "Tiros Hechos (local)",
    "Tiros recibidos (local)",
    "PJ (Visita)",
    "Tiros Hechos (visita)",
    "Tiros recibidos (visita)",
]

# Nombres distintos entre hojas/temporadas -> un solo nombre
ALIAS = {
    "BORUSSIA DORTMUND": "DORTMUND",
    "EINTRACHT FRANKFURT": "FRANKFURT",
    "MONCHENGLADBACH": "GLADBACH",
    "BAYER LEVERKUSEN": "LEVERKUSEN",
}


def normalizar_equipo(nombre):
    s = unicodedata.normalize("NFKD", str(nombre)).encode("ascii", "ignore").decode()
    s = s.strip().upper()
    return ALIAS.get(s, s)


def renombrar_columnas(df):
    df.columns = df.columns.astype(str).str.strip()
    mapping = {}
    for col in df.columns:
        c = col.lower()
        es_local = "local" in c or "(l)" in c
        es_visita = "visita" in c or "(v)" in c
        if "equipo" in c:
            mapping[col] = "Equipo"
        elif "pj" in c and es_local:
            mapping[col] = "PJ (Local)"
        elif "pj" in c and es_visita:
            mapping[col] = "PJ (Visita)"
        elif "total" in c:
            continue  # ignorar columnas de totales
        elif "hech" in c and es_local:
            mapping[col] = "Tiros Hechos (local)"
        elif "recib" in c and es_local:
            mapping[col] = "Tiros recibidos (local)"
        elif "hech" in c and es_visita:
            mapping[col] = "Tiros Hechos (visita)"
        elif "recib" in c and es_visita:
            mapping[col] = "Tiros recibidos (visita)"
    return df.rename(columns=mapping)


@st.cache_data
def cargar_y_normalizar_datos(path_excel):
    """Lee TODAS las hojas (temporadas), normaliza nombres y suma por equipo."""
    try:
        hojas = pd.read_excel(path_excel, sheet_name=None)
        frames = []
        for _, d in hojas.items():
            d = renombrar_columnas(d)
            if "Equipo" not in d.columns or not all(c in d.columns for c in COLS):
                continue
            d = d.dropna(subset=["Equipo"]).copy()
            d["Equipo"] = d["Equipo"].map(normalizar_equipo)
            frames.append(d[["Equipo"] + COLS])
        if not frames:
            return None
        df = pd.concat(frames).groupby("Equipo", as_index=False)[COLS].sum()
        # Evitar divisiones entre cero
        df = df[(df["PJ (Local)"] > 0) & (df["PJ (Visita)"] > 0)].reset_index(
            drop=True
        )
        return df
    except Exception:
        return None


def proyectar(df, local, visitante, prom_local, prom_visita):
    """Devuelve (xShots local, xShots visitante)."""
    dl = df[df["Equipo"] == local].iloc[0]
    dv = df[df["Equipo"] == visitante].iloc[0]

    tfl = dl["Tiros Hechos (local)"] / dl["PJ (Local)"]
    tpl = dl["Tiros recibidos (local)"] / dl["PJ (Local)"]
    tfv = dv["Tiros Hechos (visita)"] / dv["PJ (Visita)"]
    tpv = dv["Tiros recibidos (visita)"] / dv["PJ (Visita)"]

    xs_l = (tfl * tpv) / prom_local
    xs_v = (tfv * tpl) / prom_visita  # cada lado con su propio promedio
    return xs_l, xs_v


def diagnostico(dif):
    if dif >= 1.5:
        return "🔥 OVER MUY CLARO"
    if dif >= 0.5:
        return "✅ OVER LIGERO"
    if dif <= -1.5:
        return "❄️ UNDER CLARO"
    if dif <= -0.5:
        return "🔽 UNDER LIGERO"
    return "⚖️ SIN VALOR"


def mostrar_veredicto(equipo, xs, linea):
    """Muestra si la línea de la casa es buena opción comparada con la proyección."""
    dif = xs - linea
    texto = (
        f"**{equipo}** — Proyección: **{xs:.2f}** vs Línea: **{linea}** "
        f"(Edge {dif:+.2f}) → {diagnostico(dif)}"
    )
    if dif >= 1.5:
        st.success(texto + "\n\nBuena opción: la proyección está muy por encima de la línea (**OVER**).")
    elif dif >= 0.5:
        st.success(texto + "\n\nOpción moderada: ligera ventaja al **OVER**.")
    elif dif <= -1.5:
        st.error(texto + "\n\nBuena opción al lado contrario: la proyección está muy por debajo de la línea (**UNDER**).")
    elif dif <= -0.5:
        st.warning(texto + "\n\nOpción moderada: ligera ventaja al **UNDER**.")
    else:
        st.info(texto + "\n\nNo recomendable: la línea está muy ajustada a la proyección, sin valor claro.")


# --- SIDEBAR: SELECCIÓN DE LIGA Y MODO ---
st.sidebar.header("⚙️ Configuración General")
liga_seleccionada = st.sidebar.selectbox(
    "🌍 Selecciona la Liga:", ["Bundesliga 🇩🇪", "Brasileirão 🇧🇷"]
)

if "Bundesliga" in liga_seleccionada:
    df = cargar_y_normalizar_datos(EXCEL_BUNDESLIGA)
    nombre_liga = "Bundesliga"
else:
    df = cargar_y_normalizar_datos(EXCEL_BRASIL)
    nombre_liga = "Brasileirão"

modo = st.sidebar.radio(
    "Modo de análisis:", ["📋 Escáner de Jornada Completa", "🔍 Partido Individual"]
)

if df is None or "Equipo" not in df.columns or df.empty:
    st.error(
        f"No se pudo cargar o interpretar correctamente el archivo para"
        f" **{nombre_liga}**. Revisa que el archivo exista en la carpeta."
    )
else:
    equipos = sorted(df["Equipo"].unique())

    # Promedios generales de la liga por partido (cada lado con el suyo)
    prom_liga_local = df["Tiros Hechos (local)"].sum() / df["PJ (Local)"].sum()
    prom_liga_visita = df["Tiros Hechos (visita)"].sum() / df["PJ (Visita)"].sum()

    if modo == "📋 Escáner de Jornada Completa":
        st.subheader(f"📋 Diagnóstico de la Fecha — {nombre_liga}")

        num_partidos = st.sidebar.slider(
            "Número de partidos:", 1, max(1, len(equipos) // 2), min(5, len(equipos) // 2)
        )
        jornada_evaluada = []

        for i in range(num_partidos):
            st.markdown(f"**Partido {i+1}**")
            c1, c2 = st.columns(2)

            with c1:
                loc = st.selectbox(
                    f"Local P{i+1}", equipos, index=(i * 2) % len(equipos), key=f"loc_{i}"
                )
                linea_loc = st.number_input(
                    f"Línea {loc}", value=13.5, step=0.5, key=f"lin_l_{i}"
                )
                cuota_loc = st.number_input(
                    f"Cuota {loc}", value=1.85, step=0.05, key=f"cuo_l_{i}"
                )

            with c2:
                vis = st.selectbox(
                    f"Visitante P{i+1}",
                    equipos,
                    index=(i * 2 + 1) % len(equipos),
                    key=f"vis_{i}",
                )
                linea_vis = st.number_input(
                    f"Línea {vis}", value=10.5, step=0.5, key=f"lin_v_{i}"
                )
                cuota_vis = st.number_input(
                    f"Cuota {vis}", value=1.85, step=0.05, key=f"cuo_v_{i}"
                )

            if loc != vis:
                xs_l, xs_v = proyectar(
                    df, loc, vis, prom_liga_local, prom_liga_visita
                )
                dif_l = xs_l - linea_loc
                dif_v = xs_v - linea_vis

                jornada_evaluada.append(
                    {
                        "Equipo": f"{loc} (L)",
                        "Condición": "Local",
                        "Rival": vis,
                        "Tiros Proyectados": round(xs_l, 2),
                        "Línea Casa": linea_loc,
                        "Diferencia (Edge)": round(dif_l, 2),
                        "Cuota Over": cuota_loc,
                        "Diagnóstico": diagnostico(dif_l),
                    }
                )
                jornada_evaluada.append(
                    {
                        "Equipo": f"{vis} (V)",
                        "Condición": "Visitante",
                        "Rival": loc,
                        "Tiros Proyectados": round(xs_v, 2),
                        "Línea Casa": linea_vis,
                        "Diferencia (Edge)": round(dif_v, 2),
                        "Cuota Over": cuota_vis,
                        "Diagnóstico": diagnostico(dif_v),
                    }
                )

            st.markdown("---")

        if jornada_evaluada:
            st.subheader("🎯 Ranking General de Apuestas")
            df_resumen = pd.DataFrame(jornada_evaluada).sort_values(
                by="Diferencia (Edge)", ascending=False
            )
            st.dataframe(df_resumen, use_container_width=True)

    else:
        st.subheader(f"🔍 Partido Individual — {nombre_liga}")
        c_l, c_v = st.sidebar.columns(2)
        with c_l:
            local = st.selectbox("Local", equipos, index=0)
        with c_v:
            visitante = st.selectbox("Visitante", equipos, index=1)

        linea_loc_ind = st.sidebar.number_input(
            f"Línea {local}", value=13.5, step=0.5
        )
        linea_vis_ind = st.sidebar.number_input(
            f"Línea {visitante}", value=10.5, step=0.5
        )

        if local != visitante:
            xs_l, xs_v = proyectar(
                df, local, visitante, prom_liga_local, prom_liga_visita
            )

            col1, col2 = st.columns(2)
            with col1:
                st.metric(f"Tiros Esperados {local}", f"{xs_l:.2f}")
                st.write(
                    f"**Línea:** {linea_loc_ind} | **Edge:** {xs_l - linea_loc_ind:+.2f}"
                )
            with col2:
                st.metric(f"Tiros Esperados {visitante}", f"{xs_v:.2f}")
                st.write(
                    f"**Línea:** {linea_vis_ind} | **Edge:** {xs_v - linea_vis_ind:+.2f}"
                )

            st.markdown("### 🎯 ¿Es buena opción la línea de la casa?")
            mostrar_veredicto(local, xs_l, linea_loc_ind)
            mostrar_veredicto(visitante, xs_v, linea_vis_ind)
       #python -m streamlit run app.py