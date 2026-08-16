import os
import tempfile
import pytest
from services.fuzzy_hash_service import FuzzyHashService, PureTLSH

def test_generate_ssdeep():
    data = b"Malware variant sample A - testing fuzzy piecewise hashing block triggers " * 50
    h1 = FuzzyHashService.generate_ssdeep(data)
    assert h1 is not None
    assert ":" in h1

def test_compare_ssdeep():
    data1 = b"The quick brown fox jumps over the lazy dog and explores the cyber network forest. " * 30
    data2 = data1 + b"Extra subroutines and debug strings appended here. " * 5
    data3 = b"Completely unrelated binary sequence numbers 1234567890 alpha beta gamma delta. " * 30

    h1 = FuzzyHashService.generate_ssdeep(data1)
    h2 = FuzzyHashService.generate_ssdeep(data2)
    h3 = FuzzyHashService.generate_ssdeep(data3)

    # Similar files should yield high score
    score_similar = FuzzyHashService.compare_ssdeep(h1, h2)
    assert score_similar > 60

    # Distinct files should yield 0 or low score
    score_diff = FuzzyHashService.compare_ssdeep(h1, h3)
    assert score_diff < 30

def test_generate_tlsh():
    data = b"TLSH requires minimum length byte distributions to construct 256 byte-pair buckets properly " * 10
    tlsh_hash = FuzzyHashService.generate_tlsh(data)
    assert tlsh_hash is not None
    assert tlsh_hash.startswith("T1")

def test_compare_tlsh():
    data1 = b"TLSH requires minimum length byte distributions to construct 256 byte-pair buckets properly " * 10
    data2 = b"TLSH requires minimum length byte distributions to construct 256 byte-pair buckets properly " * 10
    data3 = b"A completely different byte stream that has alternative character sets and entropy distribution " * 10

    h1 = FuzzyHashService.generate_tlsh(data1)
    h2 = FuzzyHashService.generate_tlsh(data2)
    h3 = FuzzyHashService.generate_tlsh(data3)

    dist_identical, pct_identical = FuzzyHashService.compare_tlsh(h1, h2)
    assert dist_identical == 0
    assert pct_identical == 100

    dist_diff, pct_diff = FuzzyHashService.compare_tlsh(h1, h3)
    assert dist_diff > 0
