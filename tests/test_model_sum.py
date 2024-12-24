import pytest
import pickle
from transformers import pipeline
from transform import summarization


def read_pkl(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

# get the number of test samples to iterate through
ind = [i for i in range(len(read_pkl('tests/files_unit_testing/split_en_text.pkl')))]


@pytest.mark.parametrize('i', ind)
class TestModelSum:
    """
    testing summarization model
    """

    @pytest.fixture(scope='session')
    def data(self):
        """
        fixture; loads all data required for testing
        """
        return read_pkl('tests/files_unit_testing/split_en_text.pkl')

    @pytest.fixture
    def data_ind(self, data, i):
        """
        fixture; slices loaded data according to parametrization parameter
        """
        return data[i]

    def test_summarization(self, data_ind):
        """
        test is passed if summarization was made (not empty);
        unit test
        """
        assert len(summarization(data_ind)) > 0

    def test_summarization_load(self, data_ind):
        """
        test is passed if summarization model was successfully imported;
        acceptance/unit test
        """
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        assert str(type(summarizer)) == "<class 'transformers.pipelines.text2text_generation.SummarizationPipeline'>"