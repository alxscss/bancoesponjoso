from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Banco de Fondo de Bikini | Puntaje crediticio", page_icon="🏦", layout="centered")

@st.cache_resource
def cargar_modelo():
    return joblib.load(Path(__file__).parent / "mejor_modelo_credit_score.pkl")

st.title("🏦 Banco Nacional de Bob Esponja")
st.subheader("Evaluación preliminar de puntaje crediticio")

try:
    modelo = cargar_modelo()
except Exception as error:
    st.error(f"No fue posible cargar el modelo: {error}")
    st.info("Instala las dependencias de requirements.txt en un entorno nuevo.")
    st.stop()

with st.form("percebe"):
    st.markdown("### Datos del cliente")
    col1, col2 = st.columns(2)
    with col1:
        edad = st.number_input("Edad", min_value=18, max_value=100, value=35, step=1)
        genero = st.selectbox("Género", ["Female", "Male"], format_func=lambda x: {"Female": "Femenino", "Male": "Masculino"}[x])
        ingreso = st.number_input("Ingreso (unidades del dataset)", min_value=0, value=75000, step=1000)
        hijos = st.number_input("Número de hijos", min_value=0, max_value=20, value=0, step=1)
    with col2:
        educacion = st.selectbox("Escolaridad", ["High School Diploma", "Associate's Degree", "Bachelor's Degree", "Master's Degree", "Doctorate"], format_func=lambda x: {"High School Diploma": "Bachillerato", "Associate's Degree": "Grado asociado", "Bachelor's Degree": "Licenciatura", "Master's Degree": "Maestría", "Doctorate": "Doctorado"}[x])
        estado_civil = st.selectbox("Estado civil", ["Single", "Married"], format_func=lambda x: {"Single": "Soltero/a", "Married": "Casado/a"}[x])
        vivienda = st.selectbox("Vivienda", ["Rented", "Owned"], format_func=lambda x: {"Rented": "Rentada", "Owned": "Propia"}[x])
    enviar = st.form_submit_button("Evaluar puntaje crediticio", type="primary", use_container_width=True)

if enviar:
    cliente = pd.DataFrame([{
        "Age": edad,
        "Gender": genero,
        "Income": ingreso,
        "Education": educacion,
        "Marital Status": estado_civil,
        "Number of Children": hijos,
        "Home Ownership": vivienda,
    }])
    try:
        resultado = str(modelo.predict(cliente)[0])
        mensajes = {
            "Low": ("Bajo", "Suerte para la proxima unu."),
            "Average": ("Medio", "A lo mejor y te damos algo pero no taaanto."),
            "High": ("Alto", "Felicidades, eres candidato para un producto con límite alto, bienvenido."),
        }
        titulo, descripcion = mensajes.get(resultado, (resultado, "Clasificación obtenida."))
        st.divider()
        st.markdown("### Resultado de la evaluación")
        st.metric("Puntaje crediticio estimado", titulo)
        st.info(descripcion)
        if edad < 25 or edad > 53 or ingreso < 25000 or ingreso > 162500 or hijos > 3:
            st.warning("Algunos valores están fuera de los rangos observados en el dataset utilizado: interpreta esta predicción con cautela.")
    except Exception as error:
        st.error(f"No fue posible generar la predicción: {error}")
