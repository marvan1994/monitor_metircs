import pandas as pd
import streamlit as st
st.set_page_config(layout="wide")
df = pd.read_csv('monitor.csv', dtype=object)

def query_string(subject, degree, speaker, tariff, packet):
    var_names = ['subject','class_degree','speaker','tariff', 'is_pack']
    vars = [subject, degree, speaker, tariff, packet]
    query = ' and '.join([f'{var_names[i]} == "{vars[i]}"' for i in range(len(var_names)) if vars[i] != 'Все'])
    if query == '':
        return 'subject != "marvan"'
    else:
        return query

subject_names = df.subject.unique().tolist()
degree_names = df.class_degree.unique().tolist()
speaker_names = df.speaker.unique().tolist()
tariff_names = df.tariff.unique().tolist()

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    subject = st.selectbox('Выберите предмет',['Все']+subject_names)
with col2:
    degree = st.selectbox('Выберите класс',['Все']+degree_names)
with col3:
    speaker = st.selectbox('Выберите спикера',['Все']+speaker_names)
with col4:
    tariff = st.selectbox('Выберите тарифф',['Все']+tariff_names)
with col5:
    packet = st.selectbox('Только пакеты?',['Все']+['0','1'])

dft = df.query(query_string(subject,degree,speaker,tariff, packet))
st.dataframe(dft)

n_stud_unique = dft.student_id.nunique()
n_stud = len(dft.student_id)
mean_hw_result = round(dft.avg_result.astype(float).mean(),2)
mean_hw_count = round(dft.count_done_hw.astype(float).mean(),2)
mean_web_count = round(dft.count_vieved_web.astype(float).mean(),2)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric('Число учеников', n_stud)
with col2:
    st.metric('Число уникальных учеников', n_stud_unique)
with col3:
    st.metric('Средний результат ДЗ', mean_hw_result)
with col4:
    st.metric('Среднее число выполненных ДЗ', mean_hw_count)
with col5:
    st.metric('Среднее число просмотренных вебов', mean_web_count)
