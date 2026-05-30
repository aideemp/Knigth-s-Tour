#no pongan nada

"""
AI & Student Life — Dashboard Interactivo
Dataset: AI Student Life Pakistan 2026
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="AI & Student Life · Pakistan 2026",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Paleta de colores ────────────────────────────────────────────────────────
TOOL_COLORS = {
    "ChatGPT":   "#10A37F",
    "Copilot":   "#6E40C9",
    "Grammarly": "#15CF74",
    "Gemini":    "#4285F4",
    "Notion AI": "#FF6584",
}

GRADE_COLORS = {
    "Improved":       "#43E8C2",
    "No Change":      "#FFB347",
    "Slight Decline": "#FF6584",
}

CITY_COLORS = {
    "Lahore":     "#6C63FF",
    "Karachi":    "#FF6584",
    "Islamabad":  "#43E8C2",
    "Multan":     "#FFB347",
    "Faisalabad": "#10A37F",
}

# ── CSS global ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=JetBrains+Mono&display=swap');

  html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

  .header-hero {
    background: linear-gradient(135deg, #0f1117 0%, #1a1040 50%, #0f1117 100%);
    border: 1px solid #2a2060;
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    text-align: center;
  }
  .header-hero h1 { font-size: 2.6rem; font-weight: 700; color: #e8e8f0; margin: 0; }
  .header-hero p  { color: #8889aa; font-size: 1.05rem; margin-top: .5rem; }

  .section-title {
    font-size: 1.25rem; font-weight: 700; color: #e8e8f0;
    border-left: 4px solid #6C63FF; padding-left: 12px;
    margin: 2rem 0 1rem;
  }

  .kpi-card {
    background: #1a1d27; border: 1px solid #2a2d3e;
    border-radius: 12px; padding: 1.2rem 1.5rem; text-align: center;
  }
  .kpi-value { font-size: 2.2rem; font-weight: 700; color: #6C63FF; }
  .kpi-label { font-size: .85rem; color: #8889aa; margin-top: .3rem; }

  div[data-testid="stExpander"] {
    background: #1a1d27; border: 1px solid #2a2d3e; border-radius: 12px;
  }
</style>
""", unsafe_allow_html=True)

# ── Carga de datos ───────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("AI_Student_Life_Pakistan_2026.csv")
    return df

df = load_data()

# ── HERO HEADER ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-hero">
  <h1>🎓 AI & Student Life · Pakistan 2026</h1>
  <p>Explora cómo las herramientas de Inteligencia Artificial están transformando el rendimiento académico estudiantil</p>
</div>
""", unsafe_allow_html=True)

# ── KPIs ─────────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
improved_pct = round(len(df[df["Impact_on_Grades"] == "Improved"]) / len(df) * 100, 1)
anomaly_count = len(df[(df["Satisfaction_Level"] == "High") & (df["Impact_on_Grades"] == "Slight Decline")])
avg_hours = round(df["Daily_Usage_Hours"].mean(), 1)

with k1:
    st.markdown(f'<div class="kpi-card"><div class="kpi-value">{len(df)}</div><div class="kpi-label">Estudiantes analizados</div></div>', unsafe_allow_html=True)
with k2:
    st.markdown(f'<div class="kpi-card"><div class="kpi-value">{improved_pct}%</div><div class="kpi-label">Con notas mejoradas</div></div>', unsafe_allow_html=True)
with k3:
    st.markdown(f'<div class="kpi-card"><div class="kpi-value">{avg_hours}h</div><div class="kpi-label">Uso diario promedio</div></div>', unsafe_allow_html=True)
with k4:
    st.markdown(f'<div class="kpi-card"><div class="kpi-value">{anomaly_count}</div><div class="kpi-label">Casos anómalos detectados</div></div>', unsafe_allow_html=True)

st.markdown("---")

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 1 — Impacto por Herramienta + Filtro Geográfico
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📊 1 · Impacto en Notas por Herramienta de IA</div>', unsafe_allow_html=True)

col_ctrl, col_chart = st.columns([1, 3])
with col_ctrl:
    cities = ["Todas las ciudades"] + sorted(df["City"].unique().tolist())
    city_sel = st.selectbox("🏙️ Filtrar por ciudad", cities)

df1 = df if city_sel == "Todas las ciudades" else df[df["City"] == city_sel]

# Tabla de proporciones
pivot1 = (
    df1.groupby(["AI_Tool_Used", "Impact_on_Grades"])
    .size()
    .reset_index(name="count")
)
total_per_tool = pivot1.groupby("AI_Tool_Used")["count"].transform("sum")
pivot1["pct"] = (pivot1["count"] / total_per_tool * 100).round(1)

fig1 = px.bar(
    pivot1,
    x="AI_Tool_Used",
    y="pct",
    color="Impact_on_Grades",
    color_discrete_map=GRADE_COLORS,
    barmode="stack",
    text="pct",
    labels={"pct": "% de estudiantes", "AI_Tool_Used": "Herramienta IA", "Impact_on_Grades": "Impacto"},
    title=f"Distribución del impacto en notas — {city_sel}",
    category_orders={"Impact_on_Grades": ["Improved", "No Change", "Slight Decline"]},
)
fig1.update_traces(texttemplate="%{text:.1f}%", textposition="inside", textfont_size=11)
fig1.update_layout(
    plot_bgcolor="#0f1117", paper_bgcolor="#0f1117",
    font_color="#e8e8f0", legend_title_text="Impacto en notas",
    height=420, margin=dict(t=50, b=20),
)
st.plotly_chart(fig1, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 2 — Propósitos: Coding vs Writing vs …
# ════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="section-title">🎯 2 · Comparativa de Propósitos de Uso</div>', unsafe_allow_html=True)

purposes = sorted(df["Purpose"].unique().tolist())
purpose_sel = st.radio("Selecciona el propósito de uso:", purposes, horizontal=True)

df2 = df[df["Purpose"] == purpose_sel]
grade_counts2 = df2["Impact_on_Grades"].value_counts().reset_index()
grade_counts2.columns = ["Impact_on_Grades", "count"]

fig2 = px.bar(
    grade_counts2,
    x="Impact_on_Grades",
    y="count",
    color="Impact_on_Grades",
    color_discrete_map=GRADE_COLORS,
    text="count",
    title=f"Impacto en notas cuando se usa IA para: {purpose_sel}",
    labels={"count": "N° de estudiantes", "Impact_on_Grades": "Impacto en notas"},
    category_orders={"Impact_on_Grades": ["Improved", "No Change", "Slight Decline"]},
)
fig2.update_traces(textposition="outside", showlegend=False)
fig2.update_layout(
    plot_bgcolor="#0f1117", paper_bgcolor="#0f1117",
    font_color="#e8e8f0", height=380, margin=dict(t=50, b=20),
)

c2a, c2b = st.columns([2, 1])
with c2a:
    st.plotly_chart(fig2, use_container_width=True)
with c2b:
    st.markdown("**Resumen del propósito seleccionado**")
    st.dataframe(
        df2.groupby("AI_Tool_Used")["Impact_on_Grades"]
        .value_counts()
        .unstack(fill_value=0)
        .reset_index()
        .rename(columns={"AI_Tool_Used": "Herramienta"}),
        use_container_width=True,
        hide_index=True,
    )

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 3 — Anomalías: Alta Satisfacción + Notas en Declive
# ════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="section-title">⚠️ 3 · Anomalías: Alta Satisfacción con Notas en Declive</div>', unsafe_allow_html=True)

st.info("🔍 Estos estudiantes reportan **alta satisfacción** con la IA, pero sus notas presentan una **ligera caída**. ¿Están sobre-dependiendo de las herramientas?")

hours_range = st.slider(
    "Filtrar por horas de uso diario (Daily_Usage_Hours):",
    min_value=float(df["Daily_Usage_Hours"].min()),
    max_value=float(df["Daily_Usage_Hours"].max()),
    value=(float(df["Daily_Usage_Hours"].min()), float(df["Daily_Usage_Hours"].max())),
    step=0.1,
    format="%.1f h",
)

df3 = df[
    (df["Satisfaction_Level"] == "High") &
    (df["Impact_on_Grades"] == "Slight Decline") &
    (df["Daily_Usage_Hours"] >= hours_range[0]) &
    (df["Daily_Usage_Hours"] <= hours_range[1])
]

c3a, c3b = st.columns([1, 2])
with c3a:
    st.metric("Casos en el rango seleccionado", len(df3))
    if len(df3) > 0:
        tool_anom = df3["AI_Tool_Used"].value_counts().reset_index()
        tool_anom.columns = ["Herramienta", "Frecuencia"]
        fig3b = px.pie(
            tool_anom, names="Herramienta", values="Frecuencia",
            color="Herramienta", color_discrete_map=TOOL_COLORS,
            title="Herramientas usadas por casos anómalos",
            hole=0.45,
        )
        fig3b.update_layout(
            plot_bgcolor="#0f1117", paper_bgcolor="#0f1117",
            font_color="#e8e8f0", height=300, margin=dict(t=40, b=0),
        )
        st.plotly_chart(fig3b, use_container_width=True)

with c3b:
    st.markdown("**Detalle de estudiantes anómalos**")
    cols_show = ["Student_ID", "Age", "Gender", "Education_Level", "City",
                 "AI_Tool_Used", "Daily_Usage_Hours", "Purpose"]
    st.dataframe(
        df3[cols_show].reset_index(drop=True),
        use_container_width=True,
        hide_index=True,
    )

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 4 — Demografía y Uso (Checkboxes)
# ════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="section-title">👥 4 · Demografía y Horas de Uso Diario</div>', unsafe_allow_html=True)

c4ctrl1, c4ctrl2, _ = st.columns([1, 1, 2])
with c4ctrl1:
    by_gender = st.checkbox("Desglosar por Género")
with c4ctrl2:
    by_edu = st.checkbox("Desglosar por Nivel Educativo")

if by_gender and by_edu:
    df4 = df.groupby(["Education_Level", "Gender"])["Daily_Usage_Hours"].mean().reset_index()
    df4.columns = ["Education_Level", "Gender", "avg_hours"]
    fig4 = px.bar(
        df4, x="Education_Level", y="avg_hours", color="Gender",
        barmode="group", text_auto=".2f",
        title="Promedio de horas diarias por Nivel Educativo y Género",
        labels={"avg_hours": "Horas promedio/día", "Education_Level": "Nivel Educativo"},
        color_discrete_sequence=["#6C63FF", "#FF6584"],
    )
elif by_gender:
    df4 = df.groupby("Gender")["Daily_Usage_Hours"].mean().reset_index()
    df4.columns = ["Gender", "avg_hours"]
    fig4 = px.bar(
        df4, x="Gender", y="avg_hours", color="Gender",
        text_auto=".2f", title="Promedio de horas diarias por Género",
        labels={"avg_hours": "Horas promedio/día"},
        color_discrete_sequence=["#6C63FF", "#FF6584"],
    )
elif by_edu:
    df4 = df.groupby("Education_Level")["Daily_Usage_Hours"].mean().reset_index()
    df4.columns = ["Education_Level", "avg_hours"]
    fig4 = px.bar(
        df4, x="Education_Level", y="avg_hours", color="Education_Level",
        text_auto=".2f", title="Promedio de horas diarias por Nivel Educativo",
        labels={"avg_hours": "Horas promedio/día", "Education_Level": "Nivel Educativo"},
        color_discrete_sequence=["#43E8C2", "#6C63FF", "#FFB347"],
    )
else:
    overall = df["Daily_Usage_Hours"].mean()
    fig4 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=overall,
        title={"text": "Promedio general de horas de uso diario", "font": {"color": "#e8e8f0"}},
        gauge={
            "axis": {"range": [0, df["Daily_Usage_Hours"].max() + 1], "tickcolor": "#8889aa"},
            "bar": {"color": "#6C63FF"},
            "bgcolor": "#1a1d27",
            "steps": [
                {"range": [0, 2], "color": "#1a1d27"},
                {"range": [2, 5], "color": "#2a2d3e"},
                {"range": [5, df["Daily_Usage_Hours"].max() + 1], "color": "#3a1040"},
            ],
        },
        number={"suffix": " h/día", "font": {"color": "#e8e8f0"}},
    ))

fig4.update_layout(
    plot_bgcolor="#0f1117", paper_bgcolor="#0f1117",
    font_color="#e8e8f0", height=380, margin=dict(t=50, b=20),
)
if not (by_gender or by_edu):
    fig4.update_layout(paper_bgcolor="#0f1117", font_color="#e8e8f0")
st.plotly_chart(fig4, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 5 — Rendimiento Regional (Multiselect)
# ════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="section-title">🗺️ 5 · Rendimiento Regional por Ciudad</div>', unsafe_allow_html=True)

all_cities = sorted(df["City"].unique().tolist())
cities_sel = st.multiselect(
    "Selecciona una o más ciudades para comparar:",
    options=all_cities,
    default=all_cities,
)

if cities_sel:
    df5 = df[df["City"].isin(cities_sel)]
    city_grade = (
        df5.groupby(["City", "Impact_on_Grades"])
        .size()
        .reset_index(name="count")
    )
    total_city = city_grade.groupby("City")["count"].transform("sum")
    city_grade["pct"] = (city_grade["count"] / total_city * 100).round(1)

    improved5 = (
        city_grade[city_grade["Impact_on_Grades"] == "Improved"]
        .sort_values("pct", ascending=False)
    )

    c5a, c5b = st.columns([2, 1])
    with c5a:
        fig5 = px.bar(
            city_grade,
            x="City", y="pct", color="Impact_on_Grades",
            color_discrete_map=GRADE_COLORS,
            barmode="stack", text="pct",
            title="Distribución de impacto por ciudad",
            labels={"pct": "%", "City": "Ciudad"},
            category_orders={"Impact_on_Grades": ["Improved", "No Change", "Slight Decline"]},
        )
        fig5.update_traces(texttemplate="%{text:.1f}%", textposition="inside")
        fig5.update_layout(
            plot_bgcolor="#0f1117", paper_bgcolor="#0f1117",
            font_color="#e8e8f0", height=400, margin=dict(t=50, b=20),
        )
        st.plotly_chart(fig5, use_container_width=True)

    with c5b:
        st.markdown("**Ranking: % de notas mejoradas**")
        for _, row in improved5.iterrows():
            medal = "🥇" if _ == improved5.index[0] else ("🥈" if _ == improved5.index[1] else "🏅")
            st.markdown(f"{medal} **{row['City']}** — `{row['pct']:.1f}%`")

        if len(improved5) >= 2:
            best  = improved5.iloc[0]
            worst = improved5.iloc[-1]
            st.success(f"**Mayor mejora:** {best['City']} ({best['pct']:.1f}%)")
            st.error(f"**Menor mejora:** {worst['City']} ({worst['pct']:.1f}%)")
else:
    st.warning("Selecciona al menos una ciudad.")

# ════════════════════════════════════════════════════════════════════════════
# FASE 2 — Insights
# ════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="section-title">💡 Descubrimientos Clave (Insights)</div>', unsafe_allow_html=True)

with st.expander("🔍 Insight 1 — ChatGPT domina, pero no siempre mejora las notas"):
    st.markdown("""
    **ChatGPT** es la herramienta más utilizada por los estudiantes pakistaníes, con una presencia
    significativa en todos los niveles educativos y ciudades. Sin embargo, al analizar el impacto
    en las notas, se observa que su uso no garantiza una mejora académica: una porción considerable
    de sus usuarios cae en la categoría **"No Change"** o incluso **"Slight Decline"**.

    Esto sugiere que el volumen de usuarios no equivale a calidad de resultado. Los estudiantes
    podrían estar usando ChatGPT de manera pasiva (copiando respuestas) en lugar de aprovecharla
    como herramienta de aprendizaje activo.
    """)

with st.expander("⚠️ Insight 2 — La paradoja de la satisfacción: ¿más cómodo, peor rendimiento?"):
    st.markdown("""
    Existen **estudiantes con alta satisfacción** hacia las herramientas de IA que, paradójicamente,
    presentan un **declive en sus notas**. Este fenómeno es especialmente notable en quienes usan
    la IA más de **3 horas diarias**.

    La hipótesis más plausible es la **sobre-dependencia**: el estudiante se siente productivo y
    satisfecho porque la IA resuelve sus tareas rápidamente, pero al no procesar el contenido
    activamente, su comprensión y desempeño real en evaluaciones disminuye.
    Más horas de uso no implica mayor aprendizaje.
    """)

with st.expander("🏙️ Insight 3 — Diferencias regionales: Islamabad lidera la mejora académica"):
    st.markdown("""
    Al comparar las ciudades, **Islamabad** muestra consistentemente el mayor porcentaje de
    estudiantes con notas mejoradas. Esto podría estar relacionado con el acceso a mejor
    infraestructura educativa, mayor familiaridad con herramientas digitales o un perfil
    estudiantil con más formación universitaria.

    Por el contrario, ciudades como **Multan** y **Faisalabad** muestran menor proporción de
    mejora, lo que sugiere que el acceso a la tecnología por sí solo no garantiza resultados
    sin el contexto educativo adecuado.
    """)

with st.expander("📚 Insight 4 — El propósito importa: 'Research' genera mejores resultados que 'Homework'"):
    st.markdown("""
    Los estudiantes que usan la IA con propósitos de **Research** (investigación) muestran
    una mayor proporción de mejora en notas comparado con quienes la usan principalmente
    para **Homework** (tareas).

    Esto tiene sentido pedagógico: usar IA para investigar activa habilidades de análisis y
    síntesis, mientras que usarla para completar tareas puede fomentar la delegación sin
    aprendizaje. La intención detrás del uso define su impacto real.
    """)

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#8889aa; font-size:.85rem;'>"
    "Dashboard desarrollado con Streamlit · Dataset: AI Student Life Pakistan 2026 (Kaggle) · "
    "Visualizaciones: Plotly"
    "</p>",
    unsafe_allow_html=True,
)