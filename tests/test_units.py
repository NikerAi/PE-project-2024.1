import pytest
import pickle
from langdetect import detect
from transform import remove_extra_text, text_partition, translation

def read_pkl(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

# get the number of test samples to iterate through
ind = [i for i in range(len(read_pkl('tests/files_unit_testing/title.pkl')))]


@pytest.mark.parametrize('i', ind)
class TestUnit:
    """
    testing data transformation functions
    """

    @pytest.fixture(scope='session')
    def data(self):
        """
        fixture; loads all data required for testing
        """
        return {
            'en_text': read_pkl('tests/files_unit_testing/en_text.pkl'),
            'tables': read_pkl('tests/files_unit_testing/tables.pkl'),
            'title': read_pkl('tests/files_unit_testing/title.pkl'),
            'cleared_en_text': read_pkl('tests/files_unit_testing/cleared_en_text.pkl'),
            'split_en_text': read_pkl('tests/files_unit_testing/split_en_text.pkl'),
            'ru_text': read_pkl('tests/files_unit_testing/ru_text.pkl')
        }

    @pytest.fixture
    def data_ind(self, data, i):
        """
        fixture; slices loaded data according to parametrization parameter
        """
        return {'en_text': data['en_text'][i],
                'tables': data['tables'][i],
                'title': data['title'][i],
                'cleared_en_text': data['cleared_en_text'][i],
                'split_en_text': data['split_en_text'][i],
                'ru_text': data['ru_text'][i]}

    def test_remove_extra_text_u(self, data_ind):
        """
        test is passed if unnecessary text was removed
        """
        assert len(remove_extra_text(data_ind['en_text'], data_ind['tables'])) < len(data_ind['en_text'])

    def test_text_partition_u(self, data_ind):
        """
        test is passed if text was broken down into paragraphs;
        the whole text is not in one paragraph
        """
        assert len(text_partition(data_ind['cleared_en_text'])) > 1

    def test_translation_u(self, data_ind):
        """
        test is passed if the result of translation of each paragraph is not empty
        (no errors occurred during translation)
        """
        assert len(translation(data_ind['split_en_text'])) == len(data_ind['split_en_text'])

    def test_translation_lang(self, data_ind):
        """
        test is passed if the language of all paragraphs is ru
        """
        assert len(set([el==True for el in [detect(text)=='ru' for text in translation(data_ind['split_en_text'])]])) == 1

