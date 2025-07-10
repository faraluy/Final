import streamlit as st
import pandas as pd
import os
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración básica de la página
st.set_page_config(
    page_title="Análisis de Películas",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar datos desde CSV
@st.cache_data

def load_data():
    try:
        actores_directores = pd.read_csv('data/actores_directores.csv')
        peliculas_premios = pd.read_csv('data/peliculas_premios.csv')
        recaudacion = pd.read_csv('data/recaudacion_peliculas.csv')
        top_vistas = pd.read_csv('data/top_10_mas_vistas.csv')
        top_puntuadas = pd.read_csv('data/top_10_mejor_puntuadas.csv')
        return actores_directores, peliculas_premios, recaudacion, top_vistas, top_puntuadas
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return None, None, None, None, None

actores_directores, peliculas_premios, recaudacion, top_vistas, top_puntuadas = load_data()

# Título de la aplicación
st.title("Análisis de Películas 🎥")

# Sidebar para navegación
st.sidebar.title("Navegación")
opciones = ["Inicio", "Visualizaciones", "Recomendador", "Acerca de"]
seleccion = st.sidebar.radio("Ir a", opciones)

if seleccion == "Inicio":
    st.header("Bienvenido al análisis de películas")
    st.write("""
    Esta aplicación te permite explorar datos interesantes sobre películas, 
    actores, directores y más. Usa el menú de la izquierda para navegar.
    """)

    st.subheader("Algunas estadísticas")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Películas en top vistas", "10")
    with col2:
        st.metric("Películas mejor puntuadas", "10")
    with col3:
        st.metric("Países con datos", "50+")

elif seleccion == "Visualizaciones":
    st.header("Visualizaciones de datos")
    st.subheader("Top 10 películas más vistas")
    try:
        fig, ax = plt.subplots()
        sns.barplot(x='vistas', y='pelicula', data=top_vistas, ax=ax)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"No se pudo cargar la visualización: {e}")

elif seleccion == "Recomendador":
    st.header("Quizz de recomendación de películas 🎯")
    st.write("Responde las siguientes 6 preguntas y obtendrás 5 recomendaciones según tu perfil cinéfilo.")

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

elif seleccion == "Acerca de":
    st.header("Acerca de este proyecto")
    st.write("""
    Este proyecto fue creado para analizar datos de películas y proporcionar 
    recomendaciones personalizadas según decisiones del usuario.

    **Tecnologías utilizadas:**
    - Python
    - Streamlit
    - Pandas
    - Matplotlib/Seaborn
    """)
