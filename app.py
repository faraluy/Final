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
    st.header("Sistema de recomendación de películas")
    st.write("""
    Encuentra películas según tus preferencias: actor, género, director o país.
    """)

    filtro_actor = st.selectbox("Selecciona un actor", sorted(actores_directores['actor'].dropna().unique()))
    filtro_genero = st.selectbox("Selecciona un género", sorted(actores_directores['genero'].dropna().unique()))
    filtro_director = st.selectbox("Selecciona un director", sorted(actores_directores['director'].dropna().unique()))
    filtro_pais = st.selectbox("Selecciona un país de origen", sorted(actores_directores['pais'].dropna().unique()))

    if st.button("Recomendar películas"):
        recomendaciones = actores_directores[
            (actores_directores['actor'] == filtro_actor) &
            (actores_directores['genero'] == filtro_genero) &
            (actores_directores['director'] == filtro_director) &
            (actores_directores['pais'] == filtro_pais)
        ]

        if not recomendaciones.empty:
            st.success("Películas recomendadas:")
            for i, row in recomendaciones.head(3).iterrows():
                st.subheader(row['pelicula'])
                st.write(f"🎬 Director: {row['director']}")
                st.write(f"🧑 Actor principal: {row['actor']}")
                st.write(f"🌍 País: {row['pais']}")
                st.write(f"🎭 Género: {row['genero']}")
                st.write("---")
        else:
            st.warning("No se encontraron películas que coincidan con todos los filtros.")

elif seleccion == "Acerca de":
    st.header("Acerca de este proyecto")
    st.write("""
    Este proyecto fue creado para analizar datos de películas y proporcionar 
    recomendaciones basadas en preferencias de usuarios.

    **Tecnologías utilizadas:**
    - Python
    - Streamlit
    - Pandas
    - Matplotlib/Seaborn
    """)
