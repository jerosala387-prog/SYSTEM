import math
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
  --bg: #f4f7fb;
  --surface: #ffffff;
  --line: #e2e8f0;
  --text: #000000;
  --muted: #64748b;
  --accent: #2563eb;
}

html, body, .stApp, [class*="css"] {
  font-family: 'Manrope', system-ui, -apple-system, 'Segoe UI', sans-serif;
}

.stApp {
  background: var(--bg) !important;
  color: #0f172a !important;
}

.block-container {
  padding-top: 2rem;
  padding-bottom: 3rem;
  max-width: 1250px;
}

#MainMenu, footer {
  visibility: hidden;
}

header[data-testid="stHeader"] {
  background: transparent;
}

.app-title {
  font-size: 2.4rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: #0f172a;
  margin: 0;
  line-height: 1.1;
}

.app-sub {
  color: #64748b;
  margin: 6px 0 18px 0;
  font-size: 1rem;
}

.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 26px;
}

.chip {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 999px;
  padding: 6px 14px;
  font-size: .85rem;
  color: #64748b;
  box-shadow: 0 2px 5px rgba(15, 23, 42, .03);
}

.chip b {
  color: #0f172a;
  font-weight: 700;
  margin-left: 4px;
}

h2, h3, .stMarkdown h2, .stMarkdown h3 {
  font-weight: 700 !important;
  letter-spacing: -0.01em;
  color: #0f172a !important;
}

.sec-title {
  font-size: 1.35rem;
  font-weight: 800;
  margin: 30px 0 18px 0;
  color: #0f172a;
}

/* Barra lateral */
section[data-testid="stSidebar"] {
  background: #ffffff !important;
  border-right: 1px solid #e2e8f0;
}

/* Etiquetas de todos los controles en negro */
label,
label *,
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] * {
  color: #000000 !important;
  -webkit-text-fill-color: #000000 !important;
  font-weight: 600 !important;
  opacity: 1 !important;
}

/* ============================================================
   REDISEÑO COMPLETO DE TODOS LOS SELECTORES
   SIDEBAR + JORNADA COMPLETA + PARTIDO INDIVIDUAL
   ============================================================ */

/* Forzar tema claro */
:root,
.stApp,
section[data-testid="stSidebar"],
[data-testid="stSelectbox"] {
  color-scheme: light !important;
}

/* Contenedor de todos los selectores */
[data-testid="stSelectbox"] {
  background: transparent !important;
}

/* Caja principal del selector */
[data-testid="stSelectbox"] div[data-baseweb="select"] {
  background: #ffffff !important;
  background-color: #ffffff !important;
  border-radius: 12px !important;
}

/* Caja exterior */
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
  background: #ffffff !important;
  background-color: #ffffff !important;
  border: 1px solid #cbd5e1 !important;
  border-radius: 12px !important;
  box-shadow: none !important;
  transition: border 0.2s ease, box-shadow 0.2s ease !important;
}

/* Capas internas */
[data-testid="stSelectbox"] div[data-baseweb="select"] > div > div,
[data-testid="stSelectbox"] div[data-baseweb="select"] > div > div > div {
  background: #ffffff !important;
  background-color: #ffffff !important;
}

/* Texto seleccionado */
[data-testid="stSelectbox"] div[data-baseweb="select"] span,
[data-testid="stSelectbox"] div[data-baseweb="select"] div,
[data-testid="stSelectbox"] div[data-baseweb="select"] input {
  color: #000000 !important;
  -webkit-text-fill-color: #000000 !important;
  opacity: 1 !important;
}

/* Fondo blanco en hover */
[data-testid="stSelectbox"] div[data-baseweb="select"]:hover,
[data-testid="stSelectbox"] div[data-baseweb="select"]:hover > div,
[data-testid="stSelectbox"] div[data-baseweb="select"]:hover > div > div {
  background: #ffffff !important;
  background-color: #ffffff !important;
}

/* Borde al pasar el mouse */
[data-testid="stSelectbox"] div[data-baseweb="select"]:hover > div {
  border-color: #94a3b8 !important;
}

/* Focus */
[data-testid="stSelectbox"] div[data-baseweb="select"]:focus-within > div {
  background: #ffffff !important;
  background-color: #ffffff !important;
  border: 1px solid #2563eb !important;
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.12) !important;
}

/* Flecha */
[data-testid="stSelectbox"] div[data-baseweb="select"] svg,
[data-testid="stSelectbox"] div[data-baseweb="select"] svg * {
  fill: #000000 !important;
  color: #000000 !important;
  opacity: 1 !important;
}

/* Placeholders */
[data-testid="stSelectbox"] div[data-baseweb="select"] input::placeholder {
  color: #000000 !important;
  -webkit-text-fill-color: #000000 !important;
  opacity: 1 !important;
}

/* ============================================================
   MENÚ DESPLEGADO DE TODOS LOS SELECTORES
   ============================================================ */

/* Fondo del menú */
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
div[data-baseweb="popover"] ul,
ul[role="listbox"] {
  background: #ffffff !important;
  background-color: #ffffff !important;
  border-color: #e2e8f0 !important;
}

/* Todas las opciones */
li[role="option"],
li[role="option"] > div,
li[role="option"] span,
li[role="option"] div {
  background: #ffffff !important;
  background-color: #ffffff !important;
  color: #000000 !important;
  -webkit-text-fill-color: #000000 !important;
  opacity: 1 !important;
}

/* Hover de las opciones */
li[role="option"]:hover,
li[role="option"]:hover > div {
  background: #f1f5f9 !important;
  background-color: #f1f5f9 !important;
}

/* Opción seleccionada */
li[role="option"][aria-selected="true"],
li[role="option"][aria-selected="true"] > div {
  background: #f1f5f9 !important;
  background-color: #f1f5f9 !important;
  color: #000000 !important;
  -webkit-text-fill-color: #000000 !important;
}

/* Texto de las opciones */
[role="listbox"] *,
[role="option"] * {
  color: #000000 !important;
  -webkit-text-fill-color: #000000 !important;
}

/* Eliminar opacidades heredadas */
[data-testid="stSelectbox"] *,
[role="listbox"] *,
[role="option"] * {
  opacity: 1 !important;
}

/* ============================================================
   INPUTS NUMÉRICOS: FONDO BLANCO Y TEXTO NEGRO
   ============================================================ */

[data-testid="stNumberInput"],
[data-testid="stNumberInput"] *,
[data-testid="stNumberInput"] input,
[data-testid="stNumberInput"] [data-baseweb="input"],
[data-testid="stNumberInput"] [data-baseweb="input"] * {
  color: #000000 !important;
  -webkit-text-fill-color: #000000 !important;
  opacity: 1 !important;
}

[data-testid="stNumberInput"] [data-baseweb="input"],
[data-testid="stNumberInput"] [data-baseweb="input"] > div,
[data-testid="stNumberInput"] input,
[data-testid="stNumberInput"] button {
  background-color: #ffffff !important;
  background: #ffffff !important;
  border-color: #cbd5e1 !important;
}

[data-testid="stNumberInput"] [data-baseweb="input"] {
  border: 1px solid #cbd5e1 !important;
  border-radius: 10px !important;
}

[data-testid="stNumberInput"] button svg,
[data-testid="stNumberInput"] button svg * {
  fill: #000000 !important;
  color: #000000 !important;
  opacity: 1 !important;
}

/* ============================================================
   CONTENEDORES Y TARJETAS
   ============================================================ */

div[data-testid="stVerticalBlockBorderWrapper"] {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  border-radius: 16px !important;
  box-shadow: 0 4px 15px rgba(15, 23, 42, .04);
}

.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 16px;
}

.tc {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  border-left: 5px solid #94a3b8 !important;
  border-radius: 16px;
  padding: 22px;
  box-shadow: 0 5px 18px rgba(15, 23, 42, .05);
  transition: transform .2s ease, box-shadow .2s ease;
}

.tc:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 22px rgba(15, 23, 42, .08);
}

.tc.over-fuerte { border-left-color: #16a34a !important; }
.tc.over-leve { border-left-color: #86efac !important; }
.tc.under-fuerte { border-left-color: #dc2626 !important; }
.tc.under-leve { border-left-color: #fca5a5 !important; }
.tc.neutro { border-left-color: #94a3b8 !important; }

.tc-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
}

.tc-role {
  color: #64748b;
  font-size: .85rem;
}

.pill {
  font-size: .78rem;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 999px;
  background: #f1f5f9;
  color: #64748b;
  white-space: nowrap;
}

.over-fuerte .pill { background: #dcfce7; color: #15803d; }
.over-leve .pill { background: #f0fdf4; color: #16a34a; }
.under-fuerte .pill { background: #fee2e2; color: #dc2626; }
.under-leve .pill { background: #fff1f2; color: #e11d48; }
.neutro .pill { background: #f1f5f9; color: #64748b; }

.tc-name {
  font-size: 1.2rem;
  font-weight: 800;
  margin: 8px 0 14px 0;
  color: #0f172a;
}

.tc-nums {
  display: flex;
  align-items: flex-end;
  gap: 22px;
  flex-wrap: wrap;
}

.num-big {
  font-size: 2.7rem;
  font-weight: 800;
  line-height: 1;
  letter-spacing: -0.03em;
  font-variant-numeric: tabular-nums;
}

.num-mid {
  font-size: 1.35rem;
  font-weight: 700;
  line-height: 1.2;
  font-variant-numeric: tabular-nums;
  color: #0f172a;
}

.cap {
  color: #64748b;
  font-size: .8rem;
  margin-top: 4px;
}

.over-fuerte .num-big, .over-leve .num-big { color: #16a34a; }
.under-fuerte .num-big, .under-leve .num-big { color: #dc2626; }

.bar {
  position: relative;
  height: 8px;
  background: #e2e8f0;
  border-radius: 99px;
  margin: 18px 0 10px 0;
}

.bar .tick {
  position: absolute;
  left: 50%;
  top: -3px;
  width: 2px;
  height: 14px;
  background: #64748b;
  opacity: .6;
}

.bar .fill {
  position: absolute;
  top: 0;
  height: 8px;
  border-radius: 99px;
  background: #64748b;
}

.over-fuerte .fill, .over-leve .fill { background: #16a34a; }
.under-fuerte .fill, .under-leve .fill { background: #dc2626; }

.bar-scale {
  display: flex;
  justify-content: space-between;
  color: #64748b;
  font-size: .72rem;
}

.verdict {
  color: #475569;
  font-size: .92rem;
  margin-top: 12px;
  opacity: .95;
}

.meta-line {
  color: #64748b;
  font-size: .82rem;
  margin-top: 8px;
  font-variant-numeric: tabular-nums;
}

div[data-testid="stAlert"] { border-radius: 12px; }
hr { border-color: #e2e8f0 !important; }

@media (max-width: 640px) {
  .app-title { font-size: 1.8rem; }
  .num-big { font-size: 2.2rem; }
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

st.markdown(
    '<p class="app-title">xShots Scanner</p>'
    '<p class="app-sub">Tiros proyectados por equipo frente a la línea de la casa.</p>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Datos y cálculos
# ---------------------------------------------------------------------------
EXCEL_BUNDESLIGA = "tiros_bundr.xlsx"
EXCEL_BRASIL = "Tiros Brasil .xlsx"

COLS = [
    "PJ (Local)",
    "Tiros Hechos (local)",
    "Tiros recibidos (local)",
    "PJ (Visita)",
    "Tiros Hechos (visita)",
    "Tiros recibidos (visita)",
]

ALIAS = {
    "BORUSSIA DORTMUND": "DORTMUND",
    "EINTRACHT FRANKFURT": "FRANKFURT",
    "MONCHENGLADBACH": "GLADBACH",
    "BAYER LEVERKUSEN": "LEVERKUSEN",
    "BAYERN MUNICH": "BAYERN",
    "FC BAYERN MUNCHEN": "BAYERN",
    "RB LEIPZIG": "LEIPZIG",
    "VFB STUTTGART": "STUTTGART",
}


def normalizar_equipo(nombre):
    s = unicodedata.normalize("NFKD", str(nombre)).encode("ascii", "ignore").decode()
    s = " ".join(s.replace(".", " ").replace("-", " ").upper().split())
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
        elif "total" in c and "tiros" not in c:
            continue
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
    """Lee todas las hojas (temporadas), normaliza nombres y suma por equipo."""
    try:
        hojas = pd.read_excel(path_excel, sheet_name=None)
        frames = []
        for _, d in hojas.items():
            d = renombrar_columnas(d)
            if "Equipo" not in d.columns or not all(c in d.columns for c in COLS):
                continue
            d = d.dropna(subset=["Equipo"]).copy()
            d["Equipo"] = d["Equipo"].map(normalizar_equipo)
            for c in COLS:
                d[c] = pd.to_numeric(d[c], errors="coerce").fillna(0)
            frames.append(d[["Equipo"] + COLS])
        if not frames:
            return None
        df = pd.concat(frames, ignore_index=True).groupby("Equipo", as_index=False)[COLS].sum()
        df = df[(df["PJ (Local)"] > 0) & (df["PJ (Visita)"] > 0)].reset_index(drop=True)
        return df
    except Exception as e:
        st.session_state["error_carga"] = f"{type(e).__name__}: {e}"
        return None


def prob_over_poisson(lam, linea):
    """Calcula P(X > linea) con distribución de Poisson de forma numéricamente estable."""
    lam = max(0.0, float(lam))
    if lam == 0.0:
        return 0.0
    k_max = math.floor(linea)
    if k_max < 0:
        return 1.0

    p_k = math.exp(-lam)
    cdf = p_k
    for k in range(1, k_max + 1):
        p_k *= lam / k
        cdf += p_k

    return max(0.0, min(1.0, 1.0 - cdf))


def proyectar(df, local, visitante, prom_local, prom_visita):
    """Devuelve (xShots local, xShots visitante)."""
    dl = df[df["Equipo"] == local].iloc[0]
    dv = df[df["Equipo"] == visitante].iloc[0]

    tfl = dl["Tiros Hechos (local)"] / dl["PJ (Local)"]
    tpl = dl["Tiros recibidos (local)"] / dl["PJ (Local)"]
    tfv = dv["Tiros Hechos (visita)"] / dv["PJ (Visita)"]
    tpv = dv["Tiros recibidos (visita)"] / dv["PJ (Visita)"]

    xs_l = (tfl * tpv) / prom_local
    xs_v = (tfv * tpl) / prom_visita
    return xs_l, xs_v


def clasificar(dif):
    if dif >= 1.5:
        return "over-fuerte", "Over muy claro", "Buena opción: la proyección supera la línea por bastante."
    if dif >= 0.5:
        return "over-leve", "Over ligero", "Ventaja moderada al over."
    if dif <= -1.5:
        return "under-fuerte", "Under claro", "No recomendada: proyección muy por debajo de la línea (Under)."
    if dif <= -0.5:
        return "under-leve", "Under ligero", "No recomendada: inclinación al Under."
    return "neutro", "Sin valor", "La línea coincide con la proyección: no hay ventaja clara."


def tarjeta(equipo, rol, xs, linea, cuota=None):
    dif = xs - linea
    clase, etiqueta, texto = clasificar(dif)
    tope = 4.0
    pos = 50 + max(-tope, min(tope, dif)) / tope * 50
    izq = min(50, pos)
    ancho = abs(pos - 50)

    p_ov = prob_over_poisson(xs, linea)
    extra_html = ""
    if cuota is not None:
        ev_ov = (p_ov * cuota) - 1.0
        extra_html = (
            f'<div class="meta-line">'
            f'Prob. Over: <b>{p_ov * 100:.1f}%</b> · '
            f'Cuota Over: <b>{cuota:.2f}</b> · '
            f'EV Over: <b>{ev_ov * 100:+.1f}%</b>'
            f'</div>'
        )

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
        f'{extra_html}'
        f'<div class="verdict">{texto}</div>'
        f'</div>'
    )


def render_grid_tarjetas(filas):
    html = '<div class="cards">'
    for r in filas:
        html += tarjeta(
            r["Equipo"],
            f'{r["Condición"]}, frente a {r["Rival"]}',
            r["Tiros Proyectados"],
            r["Línea Casa"],
            cuota=r["Cuota Over"],
        )
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Sidebar y flujo principal
# ---------------------------------------------------------------------------
st.sidebar.markdown("### Configuración")
liga_seleccionada = st.sidebar.selectbox("Liga", ["Bundesliga 🇩🇪", "Brasileirão 🇧🇷"])

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
        "Revisa que el Excel esté en la misma carpeta que la app y que sus hojas "
        "tengan las columnas de equipo, partidos y tiros."
    )
    if "error_carga" in st.session_state:
        st.caption(f"Detalle técnico: {st.session_state['error_carga']}")
else:
    equipos = sorted(df["Equipo"].unique())
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

    if modo == "📋 Escáner de Jornada Completa":
        st.markdown(
            f'<div class="sec-title">Jornada de {nombre_liga}</div>',
            unsafe_allow_html=True,
        )

        max_partidos = max(1, len(equipos) // 2)
        num_partidos = st.sidebar.slider(
            "Número de partidos", 1, max_partidos, min(5, max_partidos)
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
                        f"Cuota Over {loc}", min_value=1.01, value=1.85, step=0.05, key=f"cuo_l_{i}"
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
                        f"Cuota Over {vis}", min_value=1.01, value=1.85, step=0.05, key=f"cuo_v_{i}"
                    )

                if loc == vis:
                    st.caption("⚠️ Selecciona dos equipos distintos para proyectar este partido.")

            if loc != vis:
                xs_l, xs_v = proyectar(df, loc, vis, prom_liga_local, prom_liga_visita)
                dif_l = xs_l - linea_loc
                dif_v = xs_v - linea_vis

                for eq, rol, rival, xs, lin, dif, cuo in [
                    (f"{loc} (L)", "Local", vis, xs_l, linea_loc, dif_l, cuota_loc),
                    (f"{vis} (V)", "Visitante", loc, xs_v, linea_vis, dif_v, cuota_vis),
                ]:
                    jornada_evaluada.append(
                        {
                            "Equipo": eq,
                            "Condición": rol,
                            "Rival": rival,
                            "Tiros Proyectados": xs,
                            "Línea Casa": lin,
                            "Diferencia (Edge)": dif,
                            "Cuota Over": cuo,
                        }
                    )

        if jornada_evaluada:
            recomendadas = sorted(
                [r for r in jornada_evaluada if r["Diferencia (Edge)"] >= 0.5],
                key=lambda x: x["Diferencia (Edge)"],
                reverse=True,
            )
            sin_valor = sorted(
                [r for r in jornada_evaluada if -0.5 < r["Diferencia (Edge)"] < 0.5],
                key=lambda x: abs(x["Diferencia (Edge)"]),
                reverse=True,
            )
            under_no_recom = sorted(
                [r for r in jornada_evaluada if r["Diferencia (Edge)"] <= -0.5],
                key=lambda x: x["Diferencia (Edge)"],
            )

            st.markdown(
                '<div class="sec-title">Recomendadas (Over)</div>',
                unsafe_allow_html=True,
            )
            if not recomendadas:
                st.info("No hay líneas Over con ventaja clara (>= +0.5 tiros) en esta jornada.")
            else:
                render_grid_tarjetas(recomendadas)

            if sin_valor:
                st.markdown(
                    '<div class="sec-title">Sin valor claro</div>',
                    unsafe_allow_html=True,
                )
                render_grid_tarjetas(sin_valor)

            if under_no_recom:
                st.markdown(
                    '<div class="sec-title">Under — No recomendadas</div>',
                    unsafe_allow_html=True,
                )
                render_grid_tarjetas(under_no_recom)

    else:
        st.markdown(
            f'<div class="sec-title">Partido individual en {nombre_liga}</div>',
            unsafe_allow_html=True,
        )
        c_l, c_v = st.sidebar.columns(2)
        with c_l:
            local = st.selectbox("Local", equipos, index=0)
        with c_v:
            visitante = st.selectbox("Visitante", equipos, index=min(1, len(equipos) - 1))

        linea_loc_ind = st.sidebar.number_input(
            f"Línea {local}", value=13.5, step=0.5, key="ind_lin_l"
        )
        linea_vis_ind = st.sidebar.number_input(
            f"Línea {visitante}", value=10.5, step=0.5, key="ind_lin_v"
        )
        cuota_loc_ind = st.sidebar.number_input(
            f"Cuota Over {local}", min_value=1.01, value=1.85, step=0.05, key="ind_cuo_l"
        )
        cuota_vis_ind = st.sidebar.number_input(
            f"Cuota Over {visitante}", min_value=1.01, value=1.85, step=0.05, key="ind_cuo_v"
        )

        if local != visitante:
            xs_l, xs_v = proyectar(df, local, visitante, prom_liga_local, prom_liga_visita)

            st.markdown(
                '<div class="cards">'
                + tarjeta(local, "Local", xs_l, linea_loc_ind, cuota=cuota_loc_ind)
                + tarjeta(visitante, "Visitante", xs_v, linea_vis_ind, cuota=cuota_vis_ind)
                + "</div>",
                unsafe_allow_html=True,
            )
            st.caption(
                f"Total proyectado del partido: {xs_l + xs_v:.2f} tiros. "
                "Diferencia = tiros proyectados menos la línea."
            )
        else:
            st.warning("Elige dos equipos distintos.")
       #python -m streamlit run app.py