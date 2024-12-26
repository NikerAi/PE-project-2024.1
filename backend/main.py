'''
to start streamlit use:
streamlit run streamlit_app.py

to start fastapi use:
uvicorn fastapi_app:app --reload

streamlit will be availiable at
http://localhost:8501/
'''

from transform import extract_data, remove_extra_text, text_partition, translation
from os import listdir
import pickle


def write_in_pkl(filename, content):
    with open(filename, 'wb') as f:
        pickle.dump(content, f)

def read_pkl(filename):
    with open(filename, 'rb') as f:
        tmp = pickle.load(f)
    return tmp


def create_files_unit_testing():
    """
    creates files for unit testing in 'tests/files_unit_testing' directory
    based on processed pdf files in 'tests/files_pdf' directory
    """
    if len(listdir('tests/files_pdf')) == 0:
        # raise exception if no pdf files were found
        raise Exception("No pdf files found")

    files_pdf = ['tests/files_pdf/' + file for file in listdir('tests/files_pdf')]
    d = {}

    d['en_text'], d['tables'], d['title'] = map(list, zip(*[extract_data(file) for file in files_pdf]))
    d['cleared_en_text'] = [remove_extra_text(text, table) for text, table in zip(d['en_text'], d['tables'])]
    d['split_en_text'] = [text_partition(cleared_en_t) for cleared_en_t in d['cleared_en_text']]
    d['ru_text'] = [translation(split_en_t) for split_en_t in d['split_en_text']]

    for key in list(d.keys()):
        write_in_pkl(f'tests/files_unit_testing/{key}.pkl', d[key])
    print('Unit testing files created successfully')


