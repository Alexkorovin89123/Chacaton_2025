import streamlit as st
import pandas as pd
import plotly.express as px
import json

# --- Оформление страницы ---
st.set_page_config(page_title='Отчет о нарушениях', page_icon='🚦', layout="wide")

st.markdown("""
    <style>
        .main {background-color: #f8f9fa;}
        .reportview-container {background: #f8f9fa;}
        h1 {color: #EF5350;}
        h3 {color: #1976D2;}
    </style>
""", unsafe_allow_html=True)

st.title("🚦 Отчет о нарушениях")
st.subheader("Анализ нарушений по камерам наблюдения")

# --- Загрузка данных ---
with open("C:/Users/alex_dextop/PycharmProjects/Yolo_2/violations_report.json", "r", encoding="utf-8") as file:
    data = json.load(file)
df = pd.DataFrame(data)

# --- Преобразование столбца времени ---
df['time'] = pd.to_datetime(df['time'])

# --- Фильтры ---
st.sidebar.header("Фильтры")
violation_type = st.sidebar.multiselect("Тип нарушения", df['violation_type'].unique(), default=list(df['violation_type'].unique()))
classes = st.sidebar.multiselect("Класс нарушения", df['violation_class'].unique(), default=list(df['violation_class'].unique()))

filtered_df = df[(df['violation_type'].isin(violation_type)) & (df['violation_class'].isin(classes))]

# --- График: Количество нарушений по классам ---
st.markdown("### Количество нарушений по классам")
fig1 = px.histogram(filtered_df, x="violation_class", color="violation_class", title="Нарушения по классам")
st.plotly_chart(fig1, use_container_width=True)

# --- График: Нарушения по времени ---
st.markdown("### Нарушения по времени")
filtered_df['time_hour'] = filtered_df['time'].dt.hour
fig2 = px.histogram(filtered_df, x="time_hour", nbins=24, title="Распределение нарушений по часам", labels={'time_hour': 'Час суток'})
st.plotly_chart(fig2, use_container_width=True)

# --- График: Количество обнаруженных объектов в нарушениях ---
st.markdown("### Обнаруженные объекты в нарушениях")
object_counts = pd.DataFrame(filtered_df['detected_objects'].explode().value_counts()).reset_index()
object_counts.columns = ['Объект', 'Количество']
fig3 = px.bar(object_counts, x='Объект', y='Количество', title="Обнаруженные объекты в нарушениях")
st.plotly_chart(fig3, use_container_width=True)

# --- График: Нарушения по номерам (топ 10) ---
st.markdown("### ТОП 10 номеров с наибольшим количеством нарушений")
top_numbers = filtered_df['number'].value_counts().head(10).reset_index()
top_numbers.columns = ['Номер', 'Количество']
fig4 = px.bar(top_numbers, x='Номер', y='Количество', title="ТОП 10 номеров нарушителей")
st.plotly_chart(fig4, use_container_width=True)

# --- Просмотр данных ---
st.markdown("### Данные о нарушениях")
st.dataframe(filtered_df)
