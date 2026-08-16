import pytest
from services.similarity_service import SimilarityService
from services.fuzzy_hash_service import FuzzyHashService

def test_similarity_evaluation_high():
    data1 = b"The quick brown fox jumps over the lazy dog and explores the cyber network forest. " * 30
    data2 = data1 + b"Extra subroutines and debug strings appended here. " * 5

    ssdeep_a = FuzzyHashService.generate_ssdeep(data1)
    ssdeep_b = FuzzyHashService.generate_ssdeep(data2)
    tlsh_a = FuzzyHashService.generate_tlsh(data1)
    tlsh_b = FuzzyHashService.generate_tlsh(data2)

    res = SimilarityService.evaluate(ssdeep_a, ssdeep_b, tlsh_a, tlsh_b)
    
    assert res['overall_score'] >= 71
    assert res['assessment'] == "High Similarity"
    assert "DISCLAIMER" in res['disclaimer']

def test_similarity_evaluation_low():
    data1 = b"The quick brown fox jumps over the lazy dog and explores the cyber network forest. " * 30
    data2 = b"Completely unrelated binary sequence numbers 1234567890 alpha beta gamma delta. " * 30

    ssdeep_a = FuzzyHashService.generate_ssdeep(data1)
    ssdeep_b = FuzzyHashService.generate_ssdeep(data2)
    tlsh_a = FuzzyHashService.generate_tlsh(data1)
    tlsh_b = FuzzyHashService.generate_tlsh(data2)

    res = SimilarityService.evaluate(ssdeep_a, ssdeep_b, tlsh_a, tlsh_b)

    assert res['overall_score'] <= 30
    assert res['assessment'] == "Low Similarity"

def test_similarity_threshold_classification():
    # Test low threshold (0-30%)
    res_low = SimilarityService.evaluate("UNAVAILABLE", "UNAVAILABLE", None, None)
    assert res_low['assessment'] == "Low Similarity"
    assert res_low['overall_score'] == 0
