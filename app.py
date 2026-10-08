"""Banco Nacional de Bob Esponja | experiencia de evaluación guiada."""
from pathlib import Path
import time

import joblib
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Banco Nacional de Bob Esponja | Solicitud",
    page_icon="⚓",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
html, body, [class*="css"], [data-testid="stAppViewContainer"] {font-family:'DM Sans',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;}
[data-testid="stAppViewContainer"] {background: #f8f8f5; color:#18212a;}
[data-testid="stHeader"] {background:transparent;}
[data-testid="stMainBlockContainer"] {max-width:610px; padding-top:2.8rem; padding-bottom:4rem;}
h1,h2,h3 {letter-spacing:-.035em;}
.brand {display:flex;align-items:center;gap:12px;margin-bottom:38px;}
.brand-logo {width:44px;height:44px;background:#143b47;color:#f3d17c;border-radius:14px;display:grid;place-items:center;font-size:25px;font-weight:700;}
.brand-title {font-weight:750;letter-spacing:-.03em;color:#183642;font-size:18px;line-height:1.12;}
.brand-sub {font-size:12px;color:#78828a;margin-top:3px;}
.eyebrow {color:#9e7a3a;font-size:12px;font-weight:750;letter-spacing:.14em;text-transform:uppercase; margin-bottom:11px;}
.headline {font-size:clamp(29px,6vw,40px);line-height:1.13;letter-spacing:-.048em;font-weight:750;color:#162e39;margin:0 0 12px;}
.lead {font-size:15px;color:#74808a;line-height:1.65;margin:0 0 25px;}
.step-label {display:flex;justify-content:space-between;color:#7c8990;font-size:12px;font-weight:600;margin-top:16px;margin-bottom:10px;}
[data-testid="stProgressBar"]>div>div {background-color:#c5a35d!important;}
div.stButton > button[kind="primary"] {background:#173f49;border:1px solid #173f49;color:white;min-height:53px;border-radius:16px;font-weight:700;}
div.stButton > button[kind="primary"]:hover {background:#205765;border-color:#205765;color:white;}
div.stButton > button[kind="secondary"] {background:white;border:1px solid #dedfdc;color:#25434d;min-height:53px;border-radius:16px;}
[data-testid="stNumberInput"] input, [data-testid="stSelectbox"]>div>div {border-radius:14px!important;background:white!important;min-height:48px!important;}
[data-testid="stAlert"] {border-radius:14px;}
.result-panel {border:1px solid #e8e8e2;background:white;border-radius:24px;padding:28px 24px;margin:12px 0 20px;box-shadow:0 8px 28px rgba(15,39,47,.035);}
.result-overline {font-size:12px;color:#858d93;text-transform:uppercase;letter-spacing:.11em;font-weight:750;}
.result-amount {font-size:clamp(36px,8vw,54px);font-weight:780;letter-spacing:-.065em;color:#173f49;line-height:1.2;margin:8px 0;}
.result-note {color:#7a858b;font-size:13px;line-height:1.6;}
.result-state {font-size:26px;font-weight:750;letter-spacing:-.04em;color:#173f49;margin:12px 0 6px;}
.rule {border-top:1px solid #eceeea;margin:20px 0;}
.footer {color:#9ba4a5;font-size:12px;text-align:center;margin-top:35px;}
@media(max-width:600px){[data-testid="stMainBlockContainer"] {padding-top:1.1rem;padding-left:1.15rem;padding-right:1.15rem;}.brand{margin-bottom:24px}.result-panel{padding:22px 19px}}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def cargar_modelo():
    return joblib.load(Path(__file__).parent / "mejor_modelo_credit_score.pkl")

try:
    modelo = cargar_modelo()
except Exception as exc:
    st.error("No se pudo cargar el modelo. Revisa el archivo .pkl y las dependencias.")
    with st.expander("Detalle técnico"):
        st.code(str(exc))
    st.stop()

CAMPOS = [
    ("edad", "¿Cuántos años tienes?", "Primero, necesitamos conocer tu edad."),
    ("genero", "¿Cuál es tu género?", "Selecciona la opción que corresponda."),
    ("ingreso", "¿Cuál es tu ingreso anual?", "Ingresa el monto anual que podrás comprobar."),
    ("educacion", "¿Cuál es tu nivel de estudios?", "Selecciona tu último nivel académico."),
    ("estado", "¿Cuál es tu estado civil?", "Esta información forma parte del perfil evaluado."),
    ("hijos", "¿Cuántos hijos tienes?", "Indica el número de hijos."),
    ("vivienda", "¿Tu vivienda es propia o rentada?", "Ya casi terminamos."),
]
VALORES = {
    "edad": 35,
    "genero": "Female",
    "ingreso": 75000,
    "educacion": "Bachelor's Degree",
    "estado": "Single",
    "hijos": 0,
    "vivienda": "Rented",
}
if "paso" not in st.session_state:
    st.session_state.paso = 0
if "resultado" not in st.session_state:
    st.session_state.resultado = None
for k,v in VALORES.items():
    if k not in st.session_state:
        st.session_state[k] = v


def reiniciar():
    for k,v in VALORES.items():
        st.session_state[k] = v
    st.session_state.paso = 0
    st.session_state.resultado = None


def predecir():
    cliente = pd.DataFrame([{
        "Age": st.session_state.edad,
        "Gender": st.session_state.genero,
        "Income": st.session_state.ingreso,
        "Education": st.session_state.educacion,
        "Marital Status": st.session_state.estado,
        "Number of Children": st.session_state.hijos,
        "Home Ownership": st.session_state.vivienda,
    }])
    return str(modelo.predict(cliente)[0])

st.markdown("""
<div class="brand"><div class="brand-logo">⚓</div>
<div><div class="brand-title">Banco Nacional de Bob Esponja</div>
<div class="brand-sub">Fondo de Bikini · Banca personal</div></div></div>
""", unsafe_allow_html=True)

if st.session_state.resultado is None:
    paso = st.session_state.paso
    key, pregunta, ayuda = CAMPOS[paso]
    st.markdown('<div class="eyebrow">Tu solicitud, a tu ritmo</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="headline">{pregunta}</div>', unsafe_allow_html=True)
    st.markdown(f'<p class="lead">{ayuda}</p>', unsafe_allow_html=True)
    st.markdown(f'<div class="step-label"><span>Datos personales</span><span>{paso + 1} de {len(CAMPOS)}</span></div>', unsafe_allow_html=True)
    st.progress((paso + 1) / len(CAMPOS))
    st.write("")

    if key == "edad":
        st.number_input("Edad (años)", min_value=18, max_value=100, step=1, key="edad")
    elif key == "genero":
        st.selectbox("Género", ["Female", "Male"], format_func=lambda x: {"Female":"Femenino", "Male":"Masculino"}[x], key="genero")
    elif key == "ingreso":
        st.number_input("Ingreso anual declarado ($)", min_value=0, max_value=100000000, step=1000, key="ingreso", help="El monto de crédito estimado se expresará en la misma unidad monetaria que declares.")
    elif key == "educacion":
        opciones = ["High School Diploma", "Associate's Degree", "Bachelor's Degree", "Master's Degree", "Doctorate"]
        nombres = ["Bachillerato", "Carrera técnica / grado asociado", "Licenciatura", "Maestría", "Doctorado"]
        st.selectbox("Escolaridad", opciones, format_func=lambda x: dict(zip(opciones,nombres))[x], key="educacion")
    elif key == "estado":
        st.selectbox("Estado civil", ["Single", "Married"], format_func=lambda x: {"Single":"Soltero/a", "Married":"Casado/a"}[x], key="estado")
    elif key == "hijos":
        st.number_input("Número de hijos", min_value=0, max_value=20, step=1, key="hijos")
    elif key == "vivienda":
        st.selectbox("Situación de vivienda", ["Rented", "Owned"], format_func=lambda x: {"Rented":"Rentada", "Owned":"Propia"}[x], key="vivienda")

    st.write("")
    anterior, siguiente = st.columns([1, 2], gap="small")
    with anterior:
        if paso > 0:
            if st.button("← Anterior", use_container_width=True):
                st.session_state.paso -= 1
                st.rerun()
    with siguiente:
        etiqueta = "Ver mi resultado →" if paso == len(CAMPOS)-1 else "Siguiente →"
        if st.button(etiqueta, type="primary", use_container_width=True):
            if paso < len(CAMPOS)-1:
                st.session_state.paso += 1
                st.rerun()
            else:
                try:
                    with st.spinner("Estamos evaluando tu perfil..."):
                        time.sleep(1.6)  # Breve transición visual; no representa tiempo de cálculo del modelo
                        st.session_state.resultado = predecir()
                    st.rerun()
                except Exception as exc:
                    st.error("No fue posible completar la evaluación.")
                    with st.expander("Detalle técnico"):
                        st.code(str(exc))
else:
    resultado = st.session_state.resultado
    ingresos = st.session_state.ingreso
    st.markdown('<div class="eyebrow">Evaluación completada</div>', unsafe_allow_html=True)
    if resultado == "Low":
        st.markdown('<div class="headline">Resultado de tu solicitud</div>', unsafe_allow_html=True)
        st.markdown('<p class="lead">Hemos revisado la información de tu perfil.</p>', unsafe_allow_html=True)
        st.markdown('''<div class="result-panel"><div class="result-overline">Estado de solicitud</div>
        <div class="result-state">No aprobado</div><div class="rule"></div>
        <div class="result-overline">Límite disponible</div><div class="result-amount">$0</div>
        <div class="result-note">Tu evaluación indica un nivel crediticio bajo. Por ahora no podemos habilitar una línea de crédito.</div></div>''', unsafe_allow_html=True)
    elif resultado in ("Average", "High"):
        porcentaje = 0.20 if resultado == "Average" else 0.50
        limite = ingresos * porcentaje
        nivel = "Medio" if resultado == "Average" else "Alto"
        st.markdown('<div class="headline">¡Tu perfil es elegible!</div>', unsafe_allow_html=True)
        st.markdown('<p class="lead">Tu evaluación preliminar está lista.</p>', unsafe_allow_html=True)
        st.markdown(f'''<div class="result-panel"><div class="result-overline">Línea de crédito preaprobada · Estimada</div>
        <div class="result-amount">${limite:,.0f}</div>
        <div class="result-note">Monto calculado como el {porcentaje:.0%} del ingreso anual declarado.</div>
        <div class="rule"></div><div class="result-overline">Nivel de puntaje crediticio</div>
        <div class="result-state">{nivel}</div>
        <div class="result-note">Para continuar con el trámite, deberás comprobar tus ingresos. El monto definitivo depende de su validación.</div></div>''', unsafe_allow_html=True)
    else:
        st.warning(f"El modelo devolvió una clasificación no reconocida: {resultado}")
    if st.button("Iniciar una nueva evaluación", use_container_width=True, type="primary"):
        reiniciar()
        st.rerun()

st.markdown('<div class="footer">Banco Nacional de Bob Esponja · Fondo de Bikini</div>', unsafe_allow_html=True)
