import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

@st.cache  # 👈 Added this
def upload_data():
    df = pd.read_csv('monitor.csv', dtype=object)
    class_degree_dict = {'ЕГЭ. Базовая математика':'ЕГЭ', 'ЕГЭ для 10 класса':'10 класс'}
    df['class_degree'] = df['class_degree'].apply(lambda x: class_degree_dict.get(x,x))
    return df

df = upload_data()

def query_string(subject, degree, speaker, tariff, packet, student_list = ''):
    var_names = ['subject','class_degree','speaker','tariff', 'is_pack']
    vars = [subject, degree, speaker, tariff, packet]
    query = ' and '.join([f'{var_names[i]} == "{vars[i]}"' for i in range(len(var_names)) if vars[i] != 'Все'])
    filename = '-'.join([f'{var_names[i]}_{vars[i]}'.replace('Все','all') for i in range(len(var_names))])
    if query == '' and (student_list == '' or student_list == []):
        return filename,'subject != "marvan"'
    elif student_list != '':
        query = query+ 'student_id in @student_list'
        filename = filename+'_studlimited'
        return filename,query
    else:
        return filename,query

subject_names = df.subject.unique().tolist()
degree_names = df.class_degree.unique().tolist()
speaker_names = df.speaker.unique().tolist()
tariff_names = df.tariff.unique().tolist()



st.markdown('### Это вторая версия монитора метрик. Здесь используется файл актуальный на октябрь 2022 года. Ждите обновлений 🐱')
st.markdown('Если таблица не открылась, это не значит, что ничего не работает. Просто загрузка требует времени. Следите за надписью "Running" в правом верхнем углу.')
st.markdown('Отдельная просьба выставлять настройки фильтров реалистичными. Например не пытайтесь найти ОГЭ по Истории у Шарафиева.')
st.markdown('И сначала дождитесь первой закгрузки таблицы, а затем меняйте настройки.')

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    subject = st.selectbox('Выберите предмет',['Все']+subject_names)
with col2:
    degree = st.selectbox('Выберите класс',['Все']+degree_names)
with col3:
    speaker = st.selectbox('Выберите спикера',['Все']+speaker_names)
with col4:
    tariff = st.selectbox('Выберите тариф',['Все']+tariff_names)
with col5:
    packet = st.selectbox('Только пакеты?',['Все']+['0','1'], help = '1 - ученики с пакетами, 0 - без')

students = df.student_id.unique().tolist()
student_list = st.multiselect('Вы можете выбрать отдельных студентов по их ID', students, help = 'Выбирайте последовательно один за другим. Внутри вшит умный поиск')

with st.spinner('Выгружаем таблицу по текущим настройкам...'):
    filename, query = query_string(subject, degree, speaker, tariff, packet, student_list= student_list)
    dft = df.query(query)
st.dataframe(dft)

n_stud_unique = dft.student_id.nunique()
n_stud = len(dft.student_id)
mean_hw_result = round(dft.avg_result.astype(float).mean(),2)
mean_hw_count = round(dft.count_done_hw.astype(float).mean(),2)
mean_web_count = round(dft.count_vieved_web.astype(float).mean(),2)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric('Число учеников', n_stud, help = 'Если ученик купил два предмета - это два ученика')
with col2:
    st.metric('Число уникальных учеников', n_stud_unique, help = 'Если ученик купил 2 предмета - это один ученик')
with col3:
    st.metric('Средний результат ДЗ', mean_hw_result)
with col4:
    st.metric('Среднее число выполненных ДЗ', mean_hw_count)
with col5:
    st.metric('Среднее число просмотренных вебов', mean_web_count)

with st.expander('Посмотреть графики'):
    st.markdown('Раздел находится в разработке')




@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')
with st.expander('Сделать выгрузку'):
    st.markdown('Чтобы получить выгрузку, введите код')
    code = st.text_input('Введите код сюда')
    if code !='':

        st.markdown(filename+'.csv')
        csv = convert_df(dft)
        st.download_button(
            label="Сделать выгрузку по текущим фильтрам",
            data=csv,
            file_name=filename+'.csv',
            mime='text/csv',
        )

