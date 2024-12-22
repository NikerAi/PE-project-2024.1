import pytest
from os import listdir
from langdetect import detect
import transform

# make list of all files in tests/files_pdf directory to parametrize testing
files_pdf = ['files_pdf/' + file for file in listdir('files_pdf')]


@pytest.mark.parametrize('files', files_pdf)
class TestIntegration:
    """
    testing a pipeline of data transformation
    """

    @pytest.fixture
    def perform_transform(self, files):
        """
        fixture; performs all data transformation steps and records the results from each step
        into the dictionary; used for testing data transformation pipline
        """
        en_text, tables, title = transform.extract_data(files)
        cleared_en_text = transform.remove_extra_text(en_text, tables)
        split_en_text = transform.text_partition(cleared_en_text)
        ru_text = transform.translation(split_en_text)
        #summary = transform.summarization(split_en_text)
        return {'en_text': en_text,
                'tables': tables,
                'title': title,
                'cleared_en_text': cleared_en_text,
                'split_en_text': split_en_text,
                #'summary': summary,
                'ru_text': ru_text}


    def test_extract_data(self, perform_transform):
        """
        test is passed if the pdf document was parsed correctly
        """
        assert len(perform_transform['en_text']) > 0

    def test_remove_extra_text(self, perform_transform):
        """
        test is passed if unnecessary text was removed
        """
        assert len(perform_transform['cleared_en_text']) < len(perform_transform['en_text'])

    def test_text_partition(self, perform_transform):
        """
        test is passed if text was broken down into paragraphs;
        the whole text is not in one paragraph
        """
        assert len(perform_transform['split_en_text']) > 1

    def test_translation(self, perform_transform):
        """
        test is passed if the result of translation of each paragraph is not empty
        (no errors occurred during translation)
        """
        assert len(perform_transform['ru_text']) == len(perform_transform['split_en_text'])

    def test_translation_lang(self, perform_transform):
        """
        test is passed if the language of all paragraphs is ru
        """
        assert len(set([el==True for el in [detect(text)=='ru' for text in perform_transform['ru_text']]])) == 1
