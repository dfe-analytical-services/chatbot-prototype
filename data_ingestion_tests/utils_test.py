from data_ingestion.utils import temp_method_for_proof_of_concept_tests


def test_that_tests_run():
    assert 1 == 1


def test_that_tests_can_import_the_module():
    result = temp_method_for_proof_of_concept_tests(2)
    expected = 4

    assert result == expected
