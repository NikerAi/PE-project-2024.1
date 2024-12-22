import pytest
import requests
from os import listdir
from concurrent.futures import ThreadPoolExecutor

def get_content(filename):
    with open(filename, "rb") as f:
        return f.read()

def send_request(content):
    response = requests.post(url="http://127.0.0.1:8000/pdf_process/0",
                             files={"file": content})
    return response.status_code


@pytest.fixture(scope='session')
def parallel_status():
    files_pdf = ['files_pdf/' + file for file in listdir('files_pdf')]
    MAX_THREADS = 4

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        stat = list(executor.map(send_request, [get_content(file) for file in files_pdf]))

    return stat

ind = [i for i in range(len(['files_pdf/' + file for file in listdir('files_pdf')]))]



@pytest.mark.parametrize('i', ind)
def test_status(parallel_status, i):
    assert parallel_status[i] == 200
