import streamlit as st
import requests

# page formatting
st.set_page_config(layout='wide')
st.title('Перевод статьи')
st.write('''Проект предназначается для работы со статьями в формате pdf с сайта IEEE Xplore
 распространяющимися в закрытом доступе, работа со статьями открытого доступа 
 не поддерживается ввиду различий в оформлении стаей.''')
st.write('''После загрузки pdf файла и его обработки вам станет доступен для загрузки отформатированный docx документ, 
который соответствует критериям оформления отчета по статьям по дисциплине 
«Иностранный язык в сфере делового и профессионального общения». 
Также в конце документа присутствует краткое содержание по разделам статьи''')
st.write('''Обработка pdf документа может занять более двух минут...''')

# load file box
uploaded_file = st.file_uploader("Загрузите статью...", type=["pdf"])
summ = st.checkbox("Составить краткое содержание статьи на английском (summarization)?",
                   value=True)

if st.button('Translate'):

    if uploaded_file is None:
        st.write(':red[**Сначала загрузите pdf документ!!!**]')
    else:

        # pretty loading spinner
        with st.spinner('Wait for it...'):

            # sending request to fastapi
            response = requests.post(url=f"http://127.0.0.1:8000/pdf_process/{int(summ)}",
                                     files={"file": uploaded_file.getvalue()})

        # show download button
        st.title('Перевод готов! Скачать перевод:')
        st.download_button('Скачать', response.content, file_name='translation.docx')
