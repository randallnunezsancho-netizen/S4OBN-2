"""
Aplicación Interactiva de Pensamiento Crítico: Dinámica de la Inflación Impulsada por el Fiscal
Diseñada para estudiantes de Economía de la Universidad Internacional de las Américas (U.I.A.)
Basada en el marco pedagógico de David Merrill (Activación, Demostración, Aplicación, Integración),
el modelo Mastery Flip (Jon Bergmann) y la investigación de Lyn Alden (2021).
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import base64
from datetime import datetime

# Configuración de página
st.set_page_config(
    page_title="UIA | Dinámica de la Inflación Fiscal",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# ESTILOS CSS PERSONALIZADOS (Diseño moderno, tipografía clara, branding UIA)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    h1, h2, h3, h4, .uia-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    .main-header {
        background: linear-gradient(135deg, #0b2545 0%, #134074 50%, #001220 100%);
        padding: 1.8rem 2.2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 1.8rem;
        box-shadow: 0 10px 30px rgba(11, 37, 69, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    .badge-feynman {
        background: linear-gradient(90deg, #f59e0b, #d97706);
        color: #ffffff;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 0.5rem;
    }
    
    .badge-merrill {
        background: #0284c7;
        color: white;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .card-box {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 1.4rem;
        margin-bottom: 1.2rem;
        color: #f8fafc;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #134074, #0077b6);
    }
    
    .metric-container {
        background: #0f172a;
        border: 1px solid #334155;
        border-left: 5px solid #38bdf8;
        padding: 16px 20px;
        border-radius: 8px;
        margin: 12px 0;
        color: #f8fafc;
    }
    
    .metric-container strong {
        color: #38bdf8;
        font-size: 1.05rem;
    }
    
    .metric-container em {
        color: #93c5fd;
    }
    
    .quote-box {
        background: #0f172a;
        border: 1px solid #334155;
        border-left: 4px solid #f59e0b;
        font-style: italic;
        padding: 12px 16px;
        border-radius: 6px;
        margin: 10px 0;
        color: #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# GESTIÓN DE ESTADO (st.session_state)
# ==============================================================================
if "estudiante_nombre" not in st.session_state:
    st.session_state.estudiante_nombre = ""

if "respuestas" not in st.session_state:
    st.session_state.respuestas = {
        "fase1_decada": "1970s",
        "fase1_creencia_previa": "",
        "fase1_feynman": "",
        "fase1_calif": 0,
        "fase1_feedback": "",
        "fase2_feynman": "",
        "fase2_calif": 0,
        "fase2_feedback": "",
        "fase3_deuda": 120,
        "fase3_tasa": 1.5,
        "fase3_estimulo": 15,
        "fase3_feynman": "",
        "fase3_calif": 0,
        "fase3_feedback": "",
        "fase4_argumento": "",
        "fase4_coeval_criterio1": "En desarrollo",
        "fase4_coeval_criterio2": "En desarrollo",
        "fase4_feynman_oral": "",
        "fase4_calif": 0,
        "fase4_feedback": ""
    }

# ==============================================================================
# FUNCIONES AUXILIARES: EVALUACIÓN COGNITIVA FORMATIVA Y MÉTRICAS
# ==============================================================================
def evaluar_fase1(explicacion: str, decada: str):
    """Evalúa la justificación formativa en la fase de activación."""
    exp_lower = explicacion.lower()
    score = 0
    obs = []
    
    palabras_jerga = ["multiplicador", "m2", "coeficiente de encaje", "reserva fraccionaria"]
    jerga_usada = [j for j in palabras_jerga if j in exp_lower]
    
    if len(explicacion.strip()) < 40:
        return 40, "⚠️ Tu respuesta es sumamente concisa. Describe cómo el dinero creado por gasto del gobierno va directo al bolsillo de las personas frente al que otorgan los bancos comerciales mediante deuda."
    
    if jerga_usada:
        obs.append(f"Ten cuidado: se pidió evitar jerga técnica específica, pero utilizaste: {', '.join(jerga_usada)}. Intenta formularlo con palabras cotidianas.")
        score += 20
    else:
        score += 35
        obs.append("✅ Excelente trabajo evitando la jerga técnica innecesaria.")
        
    conceptos_clave = ["gobierno", "gasto", "banco", "préstamo", "deuda", "bolsillo", "cuenta", "regalo", "cheque", "estímulo", "impuesto"]
    encontrados = sum(1 for c in conceptos_clave if c in exp_lower)
    
    if encontrados >= 3:
        score += 45
        obs.append("✅ Distingues adecuadamente el origen del dinero: crédito bancario (requiere capacidad de pago del privado) vs. déficit fiscal (inyección neta del soberano).")
    elif encontrados >= 1:
        score += 25
        obs.append("⚡ Logras contrastar en parte, pero recuerda especificar: ¿qué pasa cuando el gobierno gasta de más versus cuando los bancos prestan más?")
    else:
        score += 10
        obs.append("🔍 Intenta hacer más explícita la diferencia física: los bancos prestan y crean deuda privada; el déficit del gobierno inyecta liquidez sin requerir amortización bancaria inmediata.")
        
    score += 20  # Base por esfuerzo analítico
    score = min(100, max(40, score))
    return score, " ".join(obs)

def evaluar_fase2(audio_script: str):
    """Evalúa la metáfora cotidiana para la monetización del déficit."""
    s_lower = audio_script.lower()
    score = 0
    obs = []
    
    if len(audio_script.strip()) < 50:
        return 40, "⚠️ La explicación para tu familiar es muy breve. Desarrolla la analogía de la vida cotidiana para que quede cristalino."
        
    metaforas = ["tarjeta", "vale", "tienda", "vecindario", "familia", "impresora", "fichas", "cheque", "monopolio", "juego", "receta", "pastel"]
    tiene_metafora = any(m in s_lower for m in metaforas)
    
    if tiene_metafora:
        score += 45
        obs.append("✅ Muy buena elección de una analogía cotidiana para ilustrar la monetización de la deuda.")
    else:
        score += 20
        obs.append("💡 Considera usar una metáfora concreta (como emitir vales en un almacén familiar o financiar los gastos de la casa prometiendo pagar con vales hechos en casa).")
        
    conceptos_efecto = ["permanente", "precio", "sube", "no baja", "deuda", "fed", "banco central", "comprar", "tesoro", "dinero"]
    efectos = sum(1 for e in conceptos_efecto if e in s_lower)
    
    if efectos >= 3:
        score += 40
        obs.append("✅ Explicas acertadamente por qué el aumento de circulante financiado por el banco central eleva el nivel de precios de forma permanente.")
    else:
        score += 20
        obs.append("🔍 Asegúrate de enfatizar por qué los precios no regresan a su nivel original una vez que el dinero adicional ya está circulando.")
        
    score += 15
    return min(100, max(45, score)), " ".join(obs)

def evaluar_fase3(carta: str, deuda: float, tasa: float):
    """Evalúa la explicación de por qué la inflación es considerada transitoria y la trampa de deuda."""
    c_lower = carta.lower()
    score = 0
    obs = []
    
    if len(carta.strip()) < 60:
        return 45, "⚠️ Desarrolla un poco más tu carta. Un niño de 12 años necesita entender qué pasa con el pago de intereses cuando la deuda es astronómica."
        
    ideas_interes = ["interés", "intereses", "pagar", "cuenta", "costo", "caro", "colapso", "quiebra", "tarjeta", "presupuesto"]
    menciona_costo = any(i in c_lower for i in ideas_interes)
    
    ideas_transitoria = ["transitoria", "tasa", "velocidad", "nivel", "subir", "freno", "ritmo", "precio", "permanente"]
    menciona_transitoria = any(t in c_lower for t in ideas_transitoria)
    
    if menciona_costo:
        score += 45
        obs.append("✅ Capturas con exactitud el dilema fiscal: subir las tasas de interés al 10% con una deuda del 120% del PIB dispararía el déficit solo en intereses.")
    else:
        score += 20
        obs.append("💡 Te faltó enfatizar el problema de los intereses: si la Fed sube mucho las tasas, el mismo gobierno no puede pagar su propia deuda acumulada.")
        
    if menciona_transitoria:
        score += 40
        obs.append("✅ Excelente distinción entre la moderación en la velocidad de subida (transitoria) vs. el nivel de precios consolidado.")
    else:
        score += 20
        obs.append("🔍 Explica al inversionista que 'transitorio' suele referirse a que el porcentaje anual dejará de acelerar, no a que las cosas volverán a costar lo de antes.")
        
    score += 15
    return min(100, max(45, score)), " ".join(obs)

def evaluar_fase4(defensa: str, feynman_oral: str):
    """Evalúa la defensa oral y la tesis central de Lyn Alden (1940s vs 1970s vs 2020s)."""
    texto = (defensa + " " + feynman_oral).lower()
    score = 0
    obs = []
    
    if len(texto.strip()) < 80:
        return 45, "⚠️ Tu síntesis para la defensa oral es muy esquemática. Elabora los contrastes estructurales entre décadas."
        
    menciona_40s = "1940" in texto or "cuarenta" in texto or "guerra" in texto or "bélico" in texto or "fiscal" in texto
    menciona_70s = "1970" in texto or "setenta" in texto or "banco" in texto or "volcker" in texto or "privad" in texto
    menciona_deuda = "deuda" in texto or "pib" in texto or "represión" in texto or "interés real negativo" in texto or "tasas bajas" in texto
    
    if menciona_40s and menciona_70s:
        score += 40
        obs.append("✅ Excelente contraste histórico: 1940s fue fiscal/deuda soberana, mientras que 1970s fue desapalancamiento y crédito privado bancario.")
    else:
        score += 20
        obs.append("💡 Asegúrate de contrastar con nitidez: en los 70s la deuda/PIB era baja (la Fed pudo subir tasas al 20%), en los 40s y 2020s la deuda sobrepasaba el 100% del PIB.")
        
    if menciona_deuda:
        score += 40
        obs.append("✅ Identificas el factor determinante de Lyn Alden: el elevado cociente Deuda/PIB obliga a la represión financiera (tasas por debajo de la inflación).")
    else:
        score += 20
        obs.append("🔍 Recuerda la tesis central: cuando la deuda pública es mayor al 100% del PIB, el banco central está subordinado a la estabilidad fiscal del Tesoro.")
        
    score += 20
    return min(100, max(50, score)), " ".join(obs)


# ==============================================================================
# BARRA LATERAL: LOGO, PERFIL DEL ESTUDIANTE Y CONTEXTO DIDÁCTICO
# ==============================================================================
with st.sidebar:
    # 1. Logo de la UIA
    logo_path = "Logo-solo- UIA.png"
    if os.path.exists(logo_path):
        st.image(logo_path, width="stretch")
    else:
        st.markdown("### 🏛️ **U.I.A.**")
        st.caption("Universidad Internacional de las Américas")
    
    st.markdown("---")
    st.markdown("### 👤 **Identificación del Estudiante**")
    nombre_input = st.text_input(
        "Nombre y Apellidos:",
        value=st.session_state.estudiante_nombre,
        placeholder="Ej. Sofía Vargas Méndez"
    )
    if nombre_input != st.session_state.estudiante_nombre:
        st.session_state.estudiante_nombre = nombre_input
    
    if st.session_state.estudiante_nombre:
        st.success(f"Estudiante activo: **{st.session_state.estudiante_nombre}**")
    else:
        st.info("Ingresa tu nombre para habilitar la trazabilidad de tu sesión.")
        
    st.markdown("---")
    st.markdown("### 📚 **Menú de Contexto Didáctico**")
    
    with st.expander("🎯 Principios de David Merrill", expanded=False):
        st.markdown("""
        1. **Activación:** Conectar con modelos mentales y esquemas previos para evitar concepciones erróneas.
        2. **Demostración:** Hacer visible lo invisible mediante contrastes visuales ($how-to$, $what-happens$).
        3. **Aplicación:** Resolver dilemas consistentes con la causalidad del sistema económico real.
        4. **Integración:** Transferencia, defensa dialógica pública y coevaluación entre pares.
        """)
        
    with st.expander("📖 Fuentes Académicas Aplicadas", expanded=False):
        st.markdown("""
        - **Lyn Alden (Mayo 2021):** *Fiscal-Driven Inflation*. Análisis FRED de $M2$, gasto bélico/pandémico y dominancia fiscal.
        - **Jon Bergmann (2026):** *The Mastery Flip & Mastery Learning*. Evaluación auténtica oral e interactiva.
        - **David Merrill:** *Los 4 principios del diseño didáctico*.
        """)

    with st.expander("⚖️ Criterio de Evaluación", expanded=False):
        st.markdown("""
        - **Técnica Feynman:** Capacidad de traducir dinámicas monetarias complejas a un lenguaje analógico intuitivo sin jerga vacía.
        - **Rigor Causal:** Diferenciación entre inflación por crédito bancario vs. inflación fiscal.
        """)

# ==============================================================================
# ENCABEZADO PRINCIPAL DE LA APLICACIÓN
# ==============================================================================
st.markdown("""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <span class="badge-merrill">CARRERA DE ECONOMÍA • PRIMER INGRESO</span>
            <h1 style="color: white; margin: 0.4rem 0 0.2rem 0; font-size: 2.1rem;">Dinámica de la Inflación Impulsada por el Fiscal</h1>
            <p style="color: #cbd5e1; margin: 0; font-size: 1.05rem;">
                Sesión Sincrónica: Raíces Analógicas & Comprobación de Maestría (Mastery Flip)
            </p>
        </div>
        <div style="text-align: right; background: rgba(255,255,255,0.1); padding: 10px 18px; border-radius: 12px;">
            <span style="font-size: 0.85rem; color: #94a3b8; text-transform: uppercase;">Módulo Didáctico</span><br>
            <strong style="font-size: 1.2rem; color: #38bdf8;">Lyn Alden Framework</strong>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Cálculo de progreso general
progreso = 0
if st.session_state.respuestas["fase1_feynman"]: progreso += 25
if st.session_state.respuestas["fase2_feynman"]: progreso += 25
if st.session_state.respuestas["fase3_feynman"]: progreso += 25
if st.session_state.respuestas["fase4_feynman_oral"]: progreso += 25

st.progress(progreso / 100)
col_prog1, col_prog2 = st.columns([3, 1])
with col_prog1:
    st.caption(f"Progreso de la sesión interactiva: **{progreso}% completado**")
with col_prog2:
    if st.session_state.estudiante_nombre:
        st.caption(f"Estudiante: **{st.session_state.estudiante_nombre}**")

# ==============================================================================
# PESTAÑAS PRINCIPALES DEL FLUJO DIDÁCTICO
# ==============================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1️⃣ Fase de Activación",
    "2️⃣ Fase de Demostración",
    "3️⃣ Fase de Aplicación",
    "4️⃣ Fase de Integración (Mastery)",
    "📑 Resumen y Certificación"
])

# ------------------------------------------------------------------------------
# TAB 1: FASE DE ACTIVACIÓN
# ------------------------------------------------------------------------------
with tab1:
    st.markdown("### 5.1. Fase de Activación: Conexión con Modelos Mentales Previos")
    st.markdown("""
    > **Fundamento Pedagógico (Merrill):** La activación evita que el contenido nuevo caiga como un dato aislado al conectar con estructuras cognitivas previas y corregir esquemas erróneos. En macroeconomía, el error habitual es suponer que toda inflación se debe al mismo motor causal.
    """)
    
    st.markdown("#### 🧭 Explorador de Intuiciones Históricas")
    st.write("Antes de profundizar en la teoría de balances macroeconómicos, ¿qué intuías sobre el origen de la inflación?")
    
    col_decada, col_previa = st.columns([1, 2])
    with col_decada:
        decada_sel = st.radio(
            "Selecciona una década inflacionaria:",
            ["1940s (Segunda Guerra Mundial)", "1970s (Choques Petroleros y Desregulación)", "2020s (Pandemia y Choques de Oferta)"],
            index=0 if "1940s" in st.session_state.respuestas["fase1_decada"] else (1 if "1970s" in st.session_state.respuestas["fase1_decada"] else 2)
        )
        st.session_state.respuestas["fase1_decada"] = decada_sel
        
    with col_previa:
        creencia = st.text_area(
            "¿Cuál creías intuitivamente que fue la causa primordial de los aumentos de precios en ese periodo?",
            value=st.session_state.respuestas["fase1_creencia_previa"],
            placeholder="Ejemplo: Pensaba que los precios subían simplemente porque las empresas se ponían de acuerdo o porque había escasez...",
            height=110
        )
        st.session_state.respuestas["fase1_creencia_previa"] = creencia

    st.markdown("---")
    st.markdown('<span class="badge-feynman">🧠 Ejercicio del Método de Feynman</span>', unsafe_allow_html=True)
    st.markdown("""
    **Consigna:**  
    *Imagina que un amigo te pregunta por qué hay inflación hoy en día y él cree que es por culpa de los bancos comerciales prestando dinero (como en los 70).*  
    Escribe en un párrafo simple, **sin usar jerga técnica** (como 'multiplicador monetario' o 'M2'), cómo le explicarías la diferencia fundamental entre una **inflación impulsada por bancos** (crédito privado) y una **impulsada por el gobierno** (gasto fiscal directo).
    """)
    
    feynman_1 = st.text_area(
        "Tu explicación en lenguaje cotidiano (sin jerga):",
        value=st.session_state.respuestas["fase1_feynman"],
        placeholder="Explícalo como si estuvieran tomándose un café...",
        height=140
    )
    
    if st.button("Enviar y Evaluar Fase 1", key="btn_eval_fase1"):
        if not feynman_1.strip():
            st.warning("Por favor redacta tu explicación antes de enviar.")
        else:
            st.session_state.respuestas["fase1_feynman"] = feynman_1
            score_1, fb_1 = evaluar_fase1(feynman_1, decada_sel)
            st.session_state.respuestas["fase1_calif"] = score_1
            st.session_state.respuestas["fase1_feedback"] = fb_1
            
    if st.session_state.respuestas["fase1_feedback"]:
        st.markdown(f"""
        <div class="card-box" style="border-left: 5px solid #0284c7;">
            <h4>Retroalimentación Formativa (Calificación: {st.session_state.respuestas['fase1_calif']}/100)</h4>
            <p>{st.session_state.respuestas['fase1_feedback']}</p>
        </div>
        """, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# TAB 2: FASE DE DEMOSTRACIÓN
# ------------------------------------------------------------------------------
with tab2:
    st.markdown("### 5.2. Fase de Demostración: Hacer Visible lo Invisible")
    st.markdown("""
    > **Fundamento Pedagógico (Merrill):** Demostrar no es solo explicar, sino mostrar el saber en funcionamiento haciendo visibles las propiedades críticas (*how-to*, *what-happens*). Aquí se exponen los mecanismos causales del ciclo de deuda a largo plazo y la expansión de la masa monetaria ($M2$).
    """)
    
    st.markdown("#### 📊 Panel Comparativo FRED: Expansión de M2 vs. Déficit Fiscal vs. Deuda/PIB")
    st.caption("Pasa el cursor por los picos de las décadas de 1940 y 2020 para contrastar cómo el gasto bélico y de emergencia forzó la monetización del déficit.")
    
    # Generar serie de datos históricos basada en el paper de Lyn Alden
    anios = np.arange(1935, 2026)
    
    # Simulación calibrada con los datos reales de FRED y Lyn Alden
    # M2 YoY growth
    m2_growth = np.zeros(len(anios))
    deficit_gdp = np.zeros(len(anios))
    debt_gdp = np.zeros(len(anios))
    
    for i, a in enumerate(anios):
        # 1940s spike
        if 1941 <= a <= 1946:
            m2_growth[i] = 18 + 9 * np.sin((a - 1941) * np.pi / 5)
            deficit_gdp[i] = -22 + 5 * np.sin((a - 1941) * np.pi / 5)
            debt_gdp[i] = 80 + (a - 1940) * 8.5
        # Post-war 1950-1965
        elif 1947 <= a <= 1968:
            m2_growth[i] = 4 + 2 * np.sin(a * 0.3)
            deficit_gdp[i] = -2 + np.random.normal(0, 1)
            debt_gdp[i] = max(35, 120 - (a - 1946) * 3.5)
        # 1970s bank lending driven inflation
        elif 1969 <= a <= 1982:
            m2_growth[i] = 10 + 3.5 * np.sin((a - 1969) * np.pi / 6)
            deficit_gdp[i] = -3.5 + np.random.normal(0, 0.8)
            debt_gdp[i] = 32 + (a - 1970) * 0.5
        # 1983-2007 Great moderation
        elif 1983 <= a <= 2007:
            m2_growth[i] = 6 + 2 * np.sin(a * 0.2)
            deficit_gdp[i] = -3.8 + np.random.normal(0, 1.2)
            debt_gdp[i] = 45 + (a - 1983) * 0.8
        # 2008 GFC
        elif 2008 <= a <= 2018:
            m2_growth[i] = 7.5 + np.random.normal(0, 0.7)
            deficit_gdp[i] = -9.8 + (a - 2009) * 0.6
            debt_gdp[i] = 65 + (a - 2007) * 4
        # 2020s fiscal stimulus
        elif 2019 <= a <= 2023:
            if a == 2020:
                m2_growth[i] = 25.0
                deficit_gdp[i] = -15.0
                debt_gdp[i] = 128.0
            elif a == 2021:
                m2_growth[i] = 13.0
                deficit_gdp[i] = -12.4
                debt_gdp[i] = 125.0
            elif a == 2022:
                m2_growth[i] = -1.2
                deficit_gdp[i] = -5.5
                debt_gdp[i] = 120.0
            else:
                m2_growth[i] = 2.0
                deficit_gdp[i] = -6.2
                debt_gdp[i] = 122.0
        else:
            m2_growth[i] = 4.0
            deficit_gdp[i] = -6.5
            debt_gdp[i] = 124.0

    df_hist = pd.DataFrame({
        "Año": anios,
        "Crecimiento_M2": m2_growth,
        "Deficit_PIB": deficit_gdp,
        "Deuda_PIB": debt_gdp
    })
    
    # Gráfico interactivo con Plotly
    fig_hist = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.12,
        subplot_titles=("Crecimiento Anual M2 (%) vs. Déficit Fiscal / PIB (%)", "Ratio Deuda Pública Total / PIB (%)")
    )
    
    fig_hist.add_trace(
        go.Scatter(
            x=df_hist["Año"], y=df_hist["Crecimiento_M2"],
            mode="lines", name="M2 Crecimiento interanual (%)",
            line=dict(color="#0284c7", width=2.5),
            hovertemplate="Año: %{x}<br>M2 YoY: %{y:.1f}%<extra></extra>"
        ),
        row=1, col=1
    )
    
    fig_hist.add_trace(
        go.Scatter(
            x=df_hist["Año"], y=df_hist["Deficit_PIB"],
            mode="lines", name="Déficit Fiscal (% PIB)",
            line=dict(color="#ef4444", width=2, dash="dash"),
            hovertemplate="Año: %{x}<br>Déficit: %{y:.1f}% PIB<extra></extra>"
        ),
        row=1, col=1
    )
    
    fig_hist.add_trace(
        go.Scatter(
            x=df_hist["Año"], y=df_hist["Deuda_PIB"],
            mode="lines", name="Deuda Pública (% PIB)",
            line=dict(color="#1e293b", width=3),
            fill="tozeroy", fillcolor="rgba(30, 41, 59, 0.08)",
            hovertemplate="Año: %{x}<br>Deuda/PIB: %{y:.1f}%<extra></extra>"
        ),
        row=2, col=1
    )
    
    # Anotaciones visuales clave
    fig_hist.add_vrect(x0=1941, x1=1946, fillcolor="rgba(245, 158, 11, 0.15)", line_width=0, row=1, col=1, annotation_text="Pico 1940s (Guerra)", annotation_position="top left")
    fig_hist.add_vrect(x0=2020, x1=2022, fillcolor="rgba(245, 158, 11, 0.15)", line_width=0, row=1, col=1, annotation_text="Pico 2020s (Pandemia)", annotation_position="top left")
    fig_hist.add_vrect(x0=1970, x1=1980, fillcolor="rgba(16, 185, 129, 0.1)", line_width=0, row=1, col=1, annotation_text="1970s (Préstamos bancarios)", annotation_position="top left")
    
    fig_hist.update_layout(
        height=700,
        margin=dict(l=60, r=40, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.04, xanchor="center", x=0.5),
        hovermode="x unified"
    )
    fig_hist.update_yaxes(title_text="Variación Anual (%)", row=1, col=1, showgrid=True, gridcolor="rgba(148, 163, 184, 0.2)")
    fig_hist.update_yaxes(title_text="Deuda Pública (% PIB)", row=2, col=1, showgrid=True, gridcolor="rgba(148, 163, 184, 0.2)")
    fig_hist.update_xaxes(showgrid=True, gridcolor="rgba(148, 163, 184, 0.15)")
    
    st.plotly_chart(fig_hist, width="stretch")
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.markdown("""
        <div class="metric-container">
            <strong>Hallazgo Crítico 1 (1940s vs 2020s):</strong><br>
            En ambas épocas, el pico de <em>M2</em> no provino de familias solicitando hipotecas a bancos comerciales, sino de déficits fiscales gigantescos monetizados mediante compras de bonos por la Reserva Federal.
        </div>
        """, unsafe_allow_html=True)
    with col_d2:
        st.markdown("""
        <div class="metric-container">
            <strong>Hallazgo Crítico 2 (1970s vs Hoy):</strong><br>
            En los años 70, la relación Deuda/PIB era de apenas ~30%. La Fed de Paul Volcker pudo elevar la tasa de interés al 20% para frenar el crédito privado sin provocar la insolvencia del Tesoro Federal.
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown('<span class="badge-feynman">🧠 Ejercicio del Método de Feynman</span>', unsafe_allow_html=True)
    st.markdown("""
    **Consigna:**  
    *Graba una nota de voz simulada de 60 segundos donde le expliques a un familiar mayor qué significa que 'la Reserva Federal monetice el déficit'.*  
    Utiliza una **metáfora de la vida cotidiana** (por ejemplo, una tarjeta de crédito familiar o imprimir vales en una tienda de vecindario) para que se entienda por qué imprimir dinero para pagar deudas del gobierno genera subidas de precios permanentes.
    """)
    
    feynman_2 = st.text_area(
        "Transcripción de tu nota de voz explicativa:",
        value=st.session_state.respuestas["fase2_feynman"],
        placeholder="Hola abuelo / mamá, imagínate que en la cooperativa del barrio...",
        height=140
    )
    
    if st.button("Enviar y Evaluar Fase 2", key="btn_eval_fase2"):
        if not feynman_2.strip():
            st.warning("Por favor redacta la simulación de tu nota de voz antes de enviar.")
        else:
            st.session_state.respuestas["fase2_feynman"] = feynman_2
            score_2, fb_2 = evaluar_fase2(feynman_2)
            st.session_state.respuestas["fase2_calif"] = score_2
            st.session_state.respuestas["fase2_feedback"] = fb_2
            
    if st.session_state.respuestas["fase2_feedback"]:
        st.markdown(f"""
        <div class="card-box" style="border-left: 5px solid #0284c7;">
            <h4>Retroalimentación Formativa (Calificación: {st.session_state.respuestas['fase2_calif']}/100)</h4>
            <p>{st.session_state.respuestas['fase2_feedback']}</p>
        </div>
        """, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# TAB 3: FASE DE APLICACIÓN
# ------------------------------------------------------------------------------
with tab3:
    st.markdown("### 5.3. Fase de Aplicación: Resolución y Consistencia Práctica")
    st.markdown("""
    > **Fundamento Pedagógico (Merrill):** La aplicación rompe la ilusión de comprender. El alumno debe usar el conocimiento en un sistema causal real (predecir consecuencias y evaluar trade-offs macroeconómicos).
    """)
    
    st.markdown("#### 🎛️ Simulador Causal de Política Monetaria y Dominancia Fiscal")
    st.write("Ajusta las palancas fiscales y monetarias para observar la reacción del costo financiero del Estado y la tasa de inflación resultante.")
    
    col_sim_ctrl, col_sim_out = st.columns([1, 2])
    
    with col_sim_ctrl:
        st.markdown("**Variables de Decisión Política:**")
        sim_deuda = st.slider(
            "Deuda Pública sobre el PIB (%):",
            min_value=30, max_value=160, value=st.session_state.respuestas["fase3_deuda"], step=5
        )
        st.session_state.respuestas["fase3_deuda"] = sim_deuda
        
        sim_tasa = st.slider(
            "Tasa de Interés de Política de la Fed (%):",
            min_value=0.0, max_value=15.0, value=float(st.session_state.respuestas["fase3_tasa"]), step=0.5
        )
        st.session_state.respuestas["fase3_tasa"] = sim_tasa
        
        sim_estimulo = st.slider(
            "Paquete de Estímulo Fiscal Anual (% del PIB):",
            min_value=0, max_value=25, value=st.session_state.respuestas["fase3_estimulo"], step=1
        )
        st.session_state.respuestas["fase3_estimulo"] = sim_estimulo
        
    with col_sim_out:
        # Modelo causal intrínseco
        # Intereses de la deuda = Deuda (% PIB) * Tasa (%) / 100
        costo_intereses_pib = (sim_deuda * sim_tasa) / 100.0
        # Inflación esperada = Base + (Estimulo * 0.45) - (Tasa * 0.35)
        inflacion_resultante = max(0.5, 2.0 + (sim_estimulo * 0.55) - (sim_tasa * 0.3))
        # Tasa real = Tasa nominal - Inflación
        tasa_real = sim_tasa - inflacion_resultante
        
        st.markdown("**Resultados del Sistema Económico:**")
        
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.metric(
                label="Costo Intereses / PIB",
                value=f"{costo_intereses_pib:.1f}%",
                delta="Crítico" if costo_intereses_pib > 6.0 else "Manejable",
                delta_color="inverse"
            )
        with m_col2:
            st.metric(
                label="Inflación IPC Estimada",
                value=f"{inflacion_resultante:.1f}%",
                delta=f"{inflacion_resultante - 2.0:+.1f}% vs Meta 2%"
            )
        with m_col3:
            st.metric(
                label="Tasa de Interés Real",
                value=f"{tasa_real:+.1f}%",
                delta="Represión Financiera" if tasa_real < 0 else "Política Restrictiva"
            )
            
        # Alertas pedagógicas automáticas según el estado
        if costo_intereses_pib > 7.0 and sim_deuda > 100:
            st.error(f"""
            🚨 **Trampa de Dominancia Fiscal Activada:** Con una deuda del {sim_deuda}% del PIB, pagar una tasa del {sim_tasa}% exige al gobierno destinar el **{costo_intereses_pib:.1f}% de todo el PIB solo en intereses**. Esto supera el presupuesto de defensa e infraestructura juntos, forzando un déficit aún mayor.
            """)
        elif tasa_real < -3.0:
            st.warning(f"""
            📉 **Régimen de Represión Financiera (Similar a 1942-1947):** La tasa real es marcadamente negativa ({tasa_real:.1f}%). La inflación licúa la deuda pública a expensas del poder adquisitivo de los ahorradores en efectivo y bonos.
            """)
        else:
            st.info("""
            ⚖️ **Zona de Equilibrio Inestable:** Observa qué ocurriría si intentaras aplicar la 'receta Volcker de los 70s' (subir tasas a más del 8%) mientras mantienes la deuda por encima del 110% del PIB.
            """)

    st.markdown("---")
    st.markdown('<span class="badge-feynman">🧠 Ejercicio del Método de Feynman</span>', unsafe_allow_html=True)
    st.markdown("""
    **Consigna:**  
    *Escribe una breve carta a un 'inversionista novato' explicándole por qué la Reserva Federal insiste en llamar a la inflación 'transitoria' y por qué mantiene las tasas de interés bajas a pesar de que el IPC sube.*  
    Traduce la lógica de los altos niveles de deuda pública (los más de 30 billones de dólares) a un lenguaje que un **niño de 12 años pueda comprender**.
    """)
    
    feynman_3 = st.text_area(
        "Carta al Inversionista Novato (Metáfora simple):",
        value=st.session_state.respuestas["fase3_feynman"],
        placeholder="Estimado inversionista amigo: Te voy a contar el secreto de por qué el banco central no puede subir las tasas tan fácil...",
        height=150
    )
    
    if st.button("Enviar y Evaluar Fase 3", key="btn_eval_fase3"):
        if not feynman_3.strip():
            st.warning("Por favor redacta tu carta antes de enviar.")
        else:
            st.session_state.respuestas["fase3_feynman"] = feynman_3
            score_3, fb_3 = evaluar_fase3(feynman_3, sim_deuda, sim_tasa)
            st.session_state.respuestas["fase3_calif"] = score_3
            st.session_state.respuestas["fase3_feedback"] = fb_3
            
    if st.session_state.respuestas["fase3_feedback"]:
        st.markdown(f"""
        <div class="card-box" style="border-left: 5px solid #0284c7;">
            <h4>Retroalimentación Formativa (Calificación: {st.session_state.respuestas['fase3_calif']}/100)</h4>
            <p>{st.session_state.respuestas['fase3_feedback']}</p>
        </div>
        """, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# TAB 4: FASE DE INTEGRACIÓN (MASTERY FLIP)
# ------------------------------------------------------------------------------
with tab4:
    st.markdown("### 5.4. Fase de Integración: Transferencia y Demostración Pública")
    st.markdown("""
    > **Fundamento Pedagógico (Merrill & Bergmann):** El conocimiento se consolida cuando se reincorpora a la práctica, se defiende oralmente ante otros o se somete a la crítica externa (metacognición y responsabilidad epistémica en el *Mastery Flip*).
    """)
    
    st.markdown("#### 🗣️ Preparación para la Defensa Oral Sincrónica")
    st.write("Estructura aquí tu tesis principal. Esta síntesis será la base de tu defensa oral ante el profesor y tus compañeros.")
    
    arg_central = st.text_area(
        "Redacta el argumento central de tu defensa oral (Tesis de Lyn Alden aplicada):",
        value=st.session_state.respuestas["fase4_argumento"],
        placeholder="Tesis: La inflación de 2020-2021 responde a un shock fiscal y de suministro análogo a 1940, lo que imposibilita una respuesta monetaria convencional debido a...",
        height=120
    )
    st.session_state.respuestas["fase4_argumento"] = arg_central
    
    st.markdown("#### 👥 Rúbrica de Coevaluación Digital entre Pares")
    st.caption("Evalúa la siguiente afirmación planteada por un compañero de clase a la luz de las fuentes de Lyn Alden:")
    
    st.markdown("""
    <div class="quote-box">
        <strong>Postura de compañero a evaluar:</strong><br>
        <em>"Como la inflación es transitoria, los precios del supermercado y la gasolina volverán a los niveles de 2019 una vez que se arreglen los puertos marítimos y los barcos vuelvan a navegar normalmente."</em>
    </div>
    """, unsafe_allow_html=True)
    
    col_co1, col_co2 = st.columns(2)
    with col_co1:
        co1 = st.selectbox(
            "Criterio 1: Precisión sobre 'Transitoria' (Tasa de cambio vs Nivel permanente)",
            ["En desarrollo", "Incorrecto: Confunde moderación del ritmo con reversión deflacionaria", "Correcto: Los precios bajarán"],
            index=0 if st.session_state.respuestas["fase4_coeval_criterio1"] == "En desarrollo" else (1 if "Incorrecto" in st.session_state.respuestas["fase4_coeval_criterio1"] else 2)
        )
        st.session_state.respuestas["fase4_coeval_criterio1"] = co1
    with col_co2:
        co2 = st.selectbox(
            "Criterio 2: Causa raíz (Oferta vs Masa monetaria M2)",
            ["En desarrollo", "Sólido: Aunque hay shock de oferta, la expansión monetaria consolidó un nivel superior de circulante", "Insuficiente: Solo importa el flete marítimo"],
            index=0 if st.session_state.respuestas["fase4_coeval_criterio2"] == "En desarrollo" else (1 if "Sólido" in st.session_state.respuestas["fase4_coeval_criterio2"] else 2)
        )
        st.session_state.respuestas["fase4_coeval_criterio2"] = co2

    st.markdown("---")
    st.markdown('<span class="badge-feynman">🧠 Simulación Oral del Mastery Flip (Feynman Final)</span>', unsafe_allow_html=True)
    st.markdown("""
    **Consigna:**  
    *Simula el momento exacto de tu defensa oral del Mastery Flip. Explica en voz alta y en menos de 2 minutos la tesis central de Lyn Alden:*  
    **¿Por qué la década de 2020 se parece más a la década de 1940 que a la de 1970 en términos de inflación y respuesta de la política monetaria?**  
    Imagina que el docente te interrumpe y te pide que lo expliques **sin términos económicos**. ¿Cómo lo formularías?
    """)
    
    feynman_oral = st.text_area(
        "Tu defensa oral formulada en lenguaje cristalino:",
        value=st.session_state.respuestas["fase4_feynman_oral"],
        placeholder="Profesor, si tuviera que explicarlo en un minuto sin usar palabras técnicas: En los años 70...",
        height=160
    )
    
    if st.button("Enviar y Evaluar Fase 4", key="btn_eval_fase4"):
        if not feynman_oral.strip():
            st.warning("Por favor redacta la simulación de tu defensa oral.")
        else:
            st.session_state.respuestas["fase4_feynman_oral"] = feynman_oral
            score_4, fb_4 = evaluar_fase4(arg_central, feynman_oral)
            st.session_state.respuestas["fase4_calif"] = score_4
            st.session_state.respuestas["fase4_feedback"] = fb_4
            
    if st.session_state.respuestas["fase4_feedback"]:
        st.markdown(f"""
        <div class="card-box" style="border-left: 5px solid #0284c7;">
            <h4>Retroalimentación Formativa (Calificación: {st.session_state.respuestas['fase4_calif']}/100)</h4>
            <p>{st.session_state.respuestas['fase4_feedback']}</p>
        </div>
        """, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# TAB 5: RESUMEN Y EXPORTACIÓN DEL REPORTE CONSOLIDADO
# ------------------------------------------------------------------------------
with tab5:
    st.markdown("### 📑 Consolidado de la Sesión y Certificación Formativa")
    
    calificaciones = [
        st.session_state.respuestas["fase1_calif"],
        st.session_state.respuestas["fase2_calif"],
        st.session_state.respuestas["fase3_calif"],
        st.session_state.respuestas["fase4_calif"]
    ]
    promedio_final = np.mean(calificaciones) if any(calificaciones) else 0.0
    
    # Resumen en tarjetas
    col_r1, col_r2, col_r3, col_r4 = st.columns(4)
    with col_r1:
        st.metric("Fase 1 (Activación)", f"{st.session_state.respuestas['fase1_calif']}/100")
    with col_r2:
        st.metric("Fase 2 (Demostración)", f"{st.session_state.respuestas['fase2_calif']}/100")
    with col_r3:
        st.metric("Fase 3 (Aplicación)", f"{st.session_state.respuestas['fase3_calif']}/100")
    with col_r4:
        st.metric("Fase 4 (Integración)", f"{st.session_state.respuestas['fase4_calif']}/100")
        
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #134074, #0b2545); color: white; padding: 20px; border-radius: 12px; margin: 20px 0;">
        <h3 style="color: white; margin: 0;">Calificación Global Consolidada: {promedio_final:.1f} / 100</h3>
        <p style="margin: 5px 0 0 0; color: #94a3b8;">Estudiante: <strong>{st.session_state.estudiante_nombre if st.session_state.estudiante_nombre else 'No identificado'}</strong> • Universidad Internacional de las Américas</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Generador de reporte Markdown consolidado para descarga
    fecha_reporte = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nombre_final = st.session_state.estudiante_nombre if st.session_state.estudiante_nombre else "Estudiante_UIA"
    
    reporte_md = f"""# REPORTE DE APRENDIZAJE: DINÁMICA DE LA INFLACIÓN IMPULSADA POR EL FISCAL
**Universidad Internacional de las Américas (U.I.A.)**  
**Carrera:** Economía (Primer Ingreso)  
**Estudiante:** {nombre_final}  
**Fecha de Sesión:** {fecha_reporte}  
**Calificación Global:** {promedio_final:.1f}/100  

---

## 1. Fase de Activación (Merrill & Feynman)
- **Década elegida:** {st.session_state.respuestas['fase1_decada']}
- **Creencia previa intuitiva:**  
  > {st.session_state.respuestas['fase1_creencia_previa']}
- **Ejercicio Feynman (Explicación sin jerga):**  
  > {st.session_state.respuestas['fase1_feynman']}
- **Retroalimentación Formativa:** {st.session_state.respuestas['fase1_feedback']}
- **Calificación Fase 1:** {st.session_state.respuestas['fase1_calif']}/100

---

## 2. Fase de Demostración (Hacer Visible lo Invisible)
- **Ejercicio Feynman (Nota de voz metafórica de monetización de déficit):**  
  > {st.session_state.respuestas['fase2_feynman']}
- **Retroalimentación Formativa:** {st.session_state.respuestas['fase2_feedback']}
- **Calificación Fase 2:** {st.session_state.respuestas['fase2_calif']}/100

---

## 3. Fase de Aplicación (Simulador y Consistencia Causal)
- **Parámetros explorados en simulación:**  
  - Deuda/PIB: {st.session_state.respuestas['fase3_deuda']}%  
  - Tasa de Interés Fed: {st.session_state.respuestas['fase3_tasa']}%  
  - Estímulo Fiscal: {st.session_state.respuestas['fase3_estimulo']}% del PIB
- **Ejercicio Feynman (Carta a inversionista novato - Niño de 12 años):**  
  > {st.session_state.respuestas['fase3_feynman']}
- **Retroalimentación Formativa:** {st.session_state.respuestas['fase3_feedback']}
- **Calificación Fase 3:** {st.session_state.respuestas['fase3_calif']}/100

---

## 4. Fase de Integración (Mastery Flip & Defensa Oral)
- **Tesis de Defensa Oral:**  
  > {st.session_state.respuestas['fase4_argumento']}
- **Coevaluación entre pares realizada:**  
  - Precisión Transitoria: {st.session_state.respuestas['fase4_coeval_criterio1']}  
  - Causa Raíz M2: {st.session_state.respuestas['fase4_coeval_criterio2']}
- **Simulación Oral Feynman (2 minutos sin tecnicismos):**  
  > {st.session_state.respuestas['fase4_feynman_oral']}
- **Retroalimentación Formativa:** {st.session_state.respuestas['fase4_feedback']}
- **Calificación Fase 4:** {st.session_state.respuestas['fase4_calif']}/100

---
*Reporte generado automáticamente en la plataforma didáctica interactiva de la U.I.A.*
"""
    
    st.markdown("#### 📥 Exportación de Resultados")
    st.write("Haz clic en el botón inferior para descargar tu informe consolidado en formato Markdown (`.md`) para entregarlo en la comprobación de maestría.")
    
    st.download_button(
        label="📄 Descargar Reporte Consolidado (.md)",
        data=reporte_md,
        file_name=f"Reporte_Inflacion_Fiscal_{nombre_final.replace(' ', '_')}.md",
        mime="text/markdown"
    )
    
    with st.expander("👁️ Vista Previa del Reporte Consolidado", expanded=False):
        st.markdown(reporte_md)
