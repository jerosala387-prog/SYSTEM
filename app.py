import unicodedata

import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Configuración de la página
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="xShots Scanner",
    page_icon="⚽",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Estilos
# ---------------------------------------------------------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
  --bg: #0c111b;
  --surface: #131a28;
  --surface-2: #19223a;
  --line: #243049;
  --text: #e9eef7;
  --muted: #8b98b0;
  --accent: #6c8cff;
  --over: #2fd4a4;
  --under: #ff7d6e;
  --neutral: #8b98b0;
}

html, body, .stApp, [class*="css"] {
  font-family: 'Manrope', system-ui, -apple-system, 'Segoe UI', sans-serif;
}
.stApp {
  background: radial-gradient(1200px 500px at 10% -10%, #17223d 0%, var(--bg) 55%);
  color: var(--text);
}
.block-container { padding-top: 2.2rem; padding-bottom: 4rem; max-width: 1200px; }
#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }

/* Encabezado */
.app-title {
  font-size: 2.1rem; font-weight: 800; letter-spacing: -0.02em;
  color: var(--text); margin: 0; line-height: 1.1;
}
.app-sub { color: var(--muted); margin: 6px 0 18px 0; font-size: 1rem; }
.chips { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 26px; }
.chip {
  background: var(--surface); border: 1px solid var(--line);
  border-radius: 999px; padding: 6px 14px; font-size: .85rem; color: var(--muted);
}
.chip b { color: var(--text); font-weight: 700; margin-left: 4px; }

/* Títulos de sección */
h2, h3, .stMarkdown h2, .stMarkdown h3 {
  font-weight: 700 !important; letter-spacing: -0.01em; color: var(--text) !important;
}
.sec-title { font-size: 1.25rem; font-weight: 700; margin: 28px 0 14px 0; color: var(--text); }

/* Sidebar */
section[data-testid="stSidebar"] {
  background: var(--surface); border-right: 1px solid var(--line);
}
section[data-testid="stSidebar"] * { color: var(--text); }

/* Inputs */
div[data-baseweb="input"], div[data-baseweb="select"] > div {
  background-color: var(--surface-2) !important;
  border-radius: 10px !important;
  border: 1px solid var(--line) !important;
}
div[data-baseweb="input"]:focus-within, div[data-baseweb="select"] > div:focus-within {
  border-color: var(--accent) !important;
}
label, .stNumberInput label, .stSelectbox label { color: var(--muted) !important; font-weight: 600 !important; }

/* Contenedores de partido */
div[data-testid="stVerticalBlockBorderWrapper"] {
  background: var(--surface);
  border: 1px solid var(--line) !important;
  border-radius: 16px !important;
}

/* Tarjetas de resultado */
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px; }
.tc {
  background: var(--surface); border: 1px solid var(--line);
  border-left: 4px solid var(--neutral);
  border-radius: 16px; padding: 18px 20px;
}
.tc.over-fuerte  { border-left-color: var(--over); }
.tc.over-leve    { border-left-color: rgba(47,212,164,.55); }
.tc.under-fuerte { border-left-color: var(--under); }
.tc.under-leve   { border-left-color: rgba(255,125,110,.55); }

.tc-top { display: flex; justify-content: space-between; align-items: center; gap: 10px; }
.tc-role { color: var(--muted); font-size: .85rem; }
.pill {
  font-size: .78rem; font-weight: 700; padding: 4px 10px; border-radius: 999px;
  background: rgba(139,152,176,.15); color: var(--neutral); white-space: nowrap;
}
.over-fuerte .pill  { background: rgba(47,212,164,.18);  color: var(--over); }
.over-leve .pill    { background: rgba(47,212,164,.10);  color: #7fe6c6; }
.under-fuerte .pill { background: rgba(255,125,110,.18); color: var(--under); }
.under-leve .pill   { background: rgba(255,125,110,.10); color: #ffaa9f; }

.tc-name { font-size: 1.15rem; font-weight: 700; margin: 8px 0 14px 0; color: var(--text); }
.tc-nums { display: flex; align-items: flex-end; gap: 26px; flex-wrap: wrap; }
.num-big { font-size: 2.6rem; font-weight: 800; line-height: 1; letter-spacing: -0.03em; font-variant-numeric: tabular-nums; }
.num-mid { font-size: 1.35rem; font-weight: 700; line-height: 1.2; font-variant-numeric: tabular-nums; }
.cap { color: var(--muted); font-size: .8rem; margin-top: 4px; }
.over-fuerte .num-big, .over-leve .num-big { color: var(--over); }
.under-fuerte .num-big, .under-leve .num-big { color: var(--under); }

/* Barra de diferencia */
.bar { position: relative; height: 8px; background: var(--surface-2); border-radius: 99px; margin: 18px 0 10px 0; }
.bar .tick { position: absolute; left: 50%; top: -3px; width: 2px; height: 14px; background: var(--muted); opacity: .6; }
.bar .fill { position: absolute; top: 0; height: 8px; border-radius: 99px; background: var(--neutral); }
.over-fuerte .fill, .over-leve .fill { background: var(--over); }
.under-fuerte .fill, .under-leve .fill { background: var(--under); }
.bar-scale { display: flex; justify-content: space-between; color: var(--muted); font-size: .72rem; }
.verdict { color: var(--text); font-size: .92rem; margin-top: 12px; opacity: .9; }

/* Tabla */
div[data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 14px; overflow: hidden; }

/* Mensajes */
div[data-testid="stAlert"] { border-radius: 12px; }

hr { border-color: var(--line) !important; }

@media (max-width: 640px) {
  .app-title { font-size: 1.6rem; }
  .num-big { font-size: 2.1rem; }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

st.markdown(
    '<p class="app-title">xShots Scanner</p>'
    '<p class="app-sub">Tiros proyectados por equipo frente a la línea de la casa.</p>',
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


def clasificar(dif):
    """Devuelve (clase css, etiqueta, texto del veredicto)."""
    if dif >= 1.5:
        return "over-fuerte", "Over muy claro", "Buena opción: la proyección supera la línea por bastante."
    if dif >= 0.5:
        return "over-leve", "Over ligero", "Ventaja moderada al over."
    if dif <= -1.5:
        return "under-fuerte", "Under claro", "Buena opción al under: la proyección queda muy por debajo de la línea."
    if dif <= -0.5:
        return "under-leve", "Under ligero", "Ventaja moderada al under."
    return "neutro", "Sin valor", "La línea coincide con la proyección: no hay ventaja clara."


def tarjeta(equipo, rol, xs, linea):
    """HTML de una tarjeta de resultado (sin sangrías para que Markdown no la rompa)."""
    dif = xs - linea
    clase, etiqueta, texto = clasificar(dif)
    tope = 4.0
    pos = 50 + max(-tope, min(tope, dif)) / tope * 50
    izq = min(50, pos)
    ancho = abs(pos - 50)
    return (
        f'<div class="tc {clase}">'
        f'<div class="tc-top"><span class="tc-role">{rol}</span><span class="pill">{etiqueta}</span></div>'
        f'<div class="tc-name">{equipo}</div>'
        f'<div class="tc-nums">'
        f'<div><div class="num-big">{xs:.2f}</div><div class="cap">Tiros proyectados</div></div>'
        f'<div><div class="num-mid">{linea}</div><div class="cap">Línea de la casa</div></div>'
        f'<div><div class="num-mid">{dif:+.2f}</div><div class="cap">Diferencia</div></div>'
        f'</div>'
        f'<div class="bar"><div class="tick"></div><div class="fill" style="left:{izq:.1f}%;width:{ancho:.1f}%"></div></div>'
        f'<div class="bar-scale"><span>Under</span><span>Over</span></div>'
        f'<div class="verdict">{texto}</div>'
        f'</div>'
    )


def color_edge(v):
    if v >= 0.5:
        return "color: #2fd4a4; font-weight: 700"
    if v <= -0.5:
        return "color: #ff7d6e; font-weight: 700"
    return "color: #8b98b0"


def estilizar(tabla):
    st_ = tabla.style
    aplicar = getattr(st_, "map", None) or st_.applymap
    return aplicar(color_edge, subset=["Diferencia (Edge)"])


# ---------------------------------------------------------------------------
# Sidebar: liga y modo
# ---------------------------------------------------------------------------
st.sidebar.markdown("### Configuración")
liga_seleccionada = st.sidebar.selectbox(
    "Liga", ["Bundesliga 🇩🇪", "Brasileirão 🇧🇷"]
)

if "Bundesliga" in liga_seleccionada:
    df = cargar_y_normalizar_datos(EXCEL_BUNDESLIGA)
    nombre_liga = "Bundesliga"
else:
    df = cargar_y_normalizar_datos(EXCEL_BRASIL)
    nombre_liga = "Brasileirão"

modo = st.sidebar.radio(
    "Modo de análisis", ["📋 Escáner de Jornada Completa", "🔍 Partido Individual"]
)

if df is None or "Equipo" not in df.columns or df.empty:
    st.error(
        f"No se pudo cargar el archivo de **{nombre_liga}**. "
        "Revisa que el Excel esté en la misma carpeta que app.py y que sus hojas "
        "tengan las columnas de equipo, partidos y tiros."
    )
else:
    equipos = sorted(df["Equipo"].unique())

    # Promedios generales de la liga por partido (cada lado con el suyo)
    prom_liga_local = df["Tiros Hechos (local)"].sum() / df["PJ (Local)"].sum()
    prom_liga_visita = df["Tiros Hechos (visita)"].sum() / df["PJ (Visita)"].sum()

    st.markdown(
        '<div class="chips">'
        f'<span class="chip">Liga<b>{nombre_liga}</b></span>'
        f'<span class="chip">Equipos<b>{len(equipos)}</b></span>'
        f'<span class="chip">Promedio de local<b>{prom_liga_local:.1f} tiros</b></span>'
        f'<span class="chip">Promedio de visitante<b>{prom_liga_visita:.1f} tiros</b></span>'
        "</div>",
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------------------------
    # MODO 1: escáner de jornada
    # -----------------------------------------------------------------------
    if modo == "📋 Escáner de Jornada Completa":
        st.markdown(
            f'<div class="sec-title">Jornada de {nombre_liga}</div>',
            unsafe_allow_html=True,
        )

        num_partidos = st.sidebar.slider(
            "Número de partidos", 1, max(1, len(equipos) // 2), min(5, len(equipos) // 2)
        )
        jornada_evaluada = []

        for i in range(num_partidos):
            with st.container(border=True):
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
                xs_l, xs_v = proyectar(df, loc, vis, prom_liga_local, prom_liga_visita)
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

        if jornada_evaluada:
            df_resumen = pd.DataFrame(jornada_evaluada).sort_values(
                by="Diferencia (Edge)", ascending=False
            )

            # Mejores oportunidades (las de mayor diferencia, en cualquier sentido)
            destacadas = df_resumen[df_resumen["Diferencia (Edge)"].abs() >= 0.5]
            destacadas = destacadas.reindex(
                destacadas["Diferencia (Edge)"].abs().sort_values(ascending=False).index
            ).head(4)

            st.markdown(
                '<div class="sec-title">Mejores oportunidades</div>',
                unsafe_allow_html=True,
            )
            if destacadas.empty:
                st.info("Ninguna línea se separa lo suficiente de la proyección en esta jornada.")
            else:
                html = '<div class="cards">'
                for _, r in destacadas.iterrows():
                    html += tarjeta(
                        r["Equipo"],
                        f'{r["Condición"]}, frente a {r["Rival"]}',
                        r["Tiros Proyectados"],
                        r["Línea Casa"],
                    )
                html += "</div>"
                st.markdown(html, unsafe_allow_html=True)

            st.markdown(
                '<div class="sec-title">Ranking completo</div>',
                unsafe_allow_html=True,
            )
            st.dataframe(
                estilizar(df_resumen),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Tiros Proyectados": st.column_config.NumberColumn(format="%.2f"),
                    "Línea Casa": st.column_config.NumberColumn(format="%.1f"),
                    "Diferencia (Edge)": st.column_config.NumberColumn(format="%+.2f"),
                    "Cuota Over": st.column_config.NumberColumn(format="%.2f"),
                },
            )

    # -----------------------------------------------------------------------
    # MODO 2: partido individual
    # -----------------------------------------------------------------------
    else:
        st.markdown(
            f'<div class="sec-title">Partido individual en {nombre_liga}</div>',
            unsafe_allow_html=True,
        )
        c_l, c_v = st.sidebar.columns(2)
        with c_l:
            local = st.selectbox("Local", equipos, index=0)
        with c_v:
            visitante = st.selectbox("Visitante", equipos, index=1)

        linea_loc_ind = st.sidebar.number_input(f"Línea {local}", value=13.5, step=0.5)
        linea_vis_ind = st.sidebar.number_input(f"Línea {visitante}", value=10.5, step=0.5)

        if local != visitante:
            xs_l, xs_v = proyectar(df, local, visitante, prom_liga_local, prom_liga_visita)

            st.markdown(
                '<div class="cards">'
                + tarjeta(local, "Local", xs_l, linea_loc_ind)
                + tarjeta(visitante, "Visitante", xs_v, linea_vis_ind)
                + "</div>",
                unsafe_allow_html=True,
            )
            st.caption(
                "Diferencia = tiros proyectados menos la línea. Positiva favorece al over, negativa al under."
            )
        else:
            st.warning("Elige dos equipos distintos.")

       #python -m streamlit run app.py