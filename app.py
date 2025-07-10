import streamlit as st
import pandas as pd
import os
from PIL import Image

# Configuración básica de la página
st.set_page_config(
    page_title="Quizz de Películas",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar datos desde CSV
@st.cache_data

def load_data():
    try:
        actores_directores = pd.read_csv('data/actores_directores.csv')
        return actores_directores
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return None

actores_directores = load_data()

# Título de la aplicación
st.title("🎬 Quizz de Recomendación de Películas")

st.write("""
Responde estas 6 preguntas y descubre 5 películas que se adapten a tus gustos.
""")

if actores_directores is not None:
    col1, col2 = st.columns(2)
    with col1:
        actor_sel = st.selectbox("1. ¿Actor que prefieres?", sorted(actores_directores['actor'].dropna().unique()))
        genero_sel = st.selectbox("2. ¿Género favorito?", sorted(actores_directores['genero'].dropna().unique()))
        duracion_max = st.slider("3. ¿Duración máxima que prefieres? (minutos)", 60, 240, 120)
    with col2:
        director_sel = st.selectbox("4. ¿Director favorito?", sorted(actores_directores['director'].dropna().unique()))
        pais_sel = st.selectbox("5. ¿País de origen de la película?", sorted(actores_directores['pais'].dropna().unique()))
        anio_max = st.slider("6. ¿Año máximo de estreno?", 1950, 2025, 2020)

    if st.button("🎬 Mostrar mis 5 películas ideales"):
        resultados = actores_directores[
            (actores_directores['actor'] == actor_sel) &
            (actores_directores['genero'] == genero_sel) &
            (actores_directores['director'] == director_sel) &
            (actores_directores['pais'] == pais_sel) &
            (actores_directores['duracion'] <= duracion_max) &
            (actores_directores['anio'] <= anio_max)
        ]

        if not resultados.empty:
            st.success("🎉 Aquí tienes tus recomendaciones:")
            for i, row in resultados.head(5).iterrows():
                st.subheader(row['pelicula'])
                st.write(f"🎬 Director: {row['director']}")
                st.write(f"🧑 Actor principal: {row['actor']}")
                st.write(f"🌍 País: {row['pais']}")
                st.write(f"🎭 Género: {row['genero']}")
                st.write(f"🕐 Duración: {row['duracion']} minutos")
                st.write(f"📅 Año: {row['anio']}")
                st.write("---")
        else:
            st.warning("😕 No se encontraron coincidencias exactas. Prueba con otras combinaciones.")
else:
    st.error("No se pudo cargar la base de datos. Asegúrate de que los archivos CSV estén en la carpeta 'data'.")
