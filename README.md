# Сервис перевода статей  
Проект реализовали студенты группы РИМ-140902 Быцюк Н.Н., Завьялов И.А.  
Данный проект разработан для оказания помощи в освоении дисциплины «Иностранный язык в сфере делового и профессионального общения».  
В функционал разработанного сервиса входит:
1) считывание текста статьи из файла в формате .pdf;
2) перевод текста статьи с английского языка на русский;
3) составление саммари статьи на английском языке (по желанию пользователя);
4) запись итоговых результатов в .docx файл с форматированием, соответствующим требованиям дисциплины.

Обратите внимание, что сервис предназначается для работы со статьями с сайта [IEEE Xplore](https://ieeexplore.ieee.org/Xplore/home.jsp), распространяющимися в закрытом доступе. Работа со статьями из открытого доступа в данный момент не поддерживается ввиду различий в оформлении статей.  
Обратите внимание, что при добавлении саммари текста статьи, время обработки запроса может занять некоторое время, ввиду низкой скорости работы модели HuggingFace «facebook/bart-large-cnn».  


## Обработка файлов .pdf
Для обработки файлов pdf используются слуедующие библиотеки:
- pymupdf для извлечения текста статей, а также поиска таблиц;
- regex позволяет находить типичные шаблоны в оформлении статей (некоторые элементы могут различаться в разных статьях, поэтому были подобраны наиболее универсальные варианты нахождения шаблонов);
- googletrans использует google translator api для перевода английского текста на русский язык;
- transformers пердоставляют возможность использования предобученной модели HuggingFace «facebook/bart-large-cnn», которая позволяет получать краткое содержание текста;
- python-docx библиотека позволяющая создавать, редактировать, форматировать docx-файлы при помощи python
Порядок обработки pdf файлов:
1) считывание текста из файла пользователя;
2) удаление таблиц, распознанных при помощи библиотеки pymupdf;
3) удаление лишнего тектса, не имеющего значения для конечного результата (н-р: таблицы, список литературы, рег. номер статьи и т.д);
4) разделение текста по разделам (при длине раздела более 3000 символов осуществляется разделение на меньшие части, до тех пор, пока все разделы не будут иметь длину менее 3000 симвлов, эта длина обусловлена особенностью работы модели саммаризации);
5) далее разделы подвергаются процессу перевода на русский язык;
6) на данном этапе осуществялется саммаризация текста по разделам при помощи предобученной модели HuggingFace «facebook/bart-large-cnn»;
7) на конечном этапе, полученные на предыдущих шагах обработанные текстовые данные, поступают на запись в документ формата docx в соответствии с требованиями дисциплины «Иностранный язык в сфере делового и профессионального общения».
  

## Разработка API
Серверная часть реализована с помощью библиотеки ```fastapi```. Включает в себя два адреса для отправки запросов:
1) ```/availability check``` для проверки доступоности сервиса;
2) ```/pdf_process/{summ}``` для реализации функционала сервиса, где ```/{summ}``` - параметр запроса, принимающий значение ```1```, когда пользователь желает добавить саммари статьи в .docx документ, и ```0``` когда саммари не требуется.

Для локального запуска API необходимо в терминале выполнить команду запуска uvicorn командой ```uvicorn fastapi_app:app```. Документация будет доступна по адресу: [English articles processing - Swagger UI](http://127.0.0.1:8000/docs#/default/get_user_pdf_pdf_process_post).   

## Пользовательский интерфейс
Интерфейс для взаимодействия пользователя с сервисом был разработан с использованием библиотеки ```streamlit```. 
В пользовательском интерфейсеприсутствует:
- поле для загрузки файла в формате .pdf;
- чекбокс для отметки, необходимо ли включить в итоговый документ саммари статьи;
- кнопка для отправки статьи;
- кнопка для скачивания итогового файла (появляется после выполнения перевода и саммаризации).

Для локального запуска UI необходимо в параллельном терминале выполнить команду запуска streamlit командой  ```streamlit run streamlit_app.py```. После этого будет доступен UI, 
с помощью которого можно осуществить преобразование pdf в docx (доступен по адресу http://localhost:8501/).  

## Тестирование  
Все необходимое для тестирования находится в директории ```tests```.  
#### Исходные данные:
- ```files_pdf``` - директория, содержащая примеры статей в формате .pdf для тестов;  
- ```files_unit_testing``` - директория, содержащая файлы с сгенерерованными данными для проведения модульных (unit) тестов. Генерация осуществлялась с помощью функции ```create_files_unit_testing``` из ```main.py```.  
#### Программы для тестирования:
- ```test_units.py``` - модульное тестирование отдельных функций обработки данных;
- ```test_integration.py``` - интеграционные тесты для всего пайплайна обработки данных;
- ```test_model_sum.py``` - тесты для модели саммаризации текста. Содержат модульные и приемочные тесты. Тесты для модели саммаризации были вынесены в отдельный блок из-за длительного времени работы модели HuggingFace «facebook/bart-large-cnn»;
- ```test_load.py``` - нагрузочные тесты для сервиса. Осуществляет одновременные запросы к API сервиса.

