import os
import tempfile
import pytest
from services.hash_service import HashService

def test_calculate_md5_and_sha256():
    test_content = b"FUZZYHASH ANALYZER FORENSIC TEST STREAM 12345"
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        tf.write(test_content)
        temp_path = tf.name

    try:
        md5_hash = HashService.calculate_md5(temp_path)
        sha256_hash = HashService.calculate_sha256(temp_path)

        assert md5_hash is not None
        assert len(md5_hash) == 32
        assert sha256_hash is not None
        assert len(sha256_hash) == 64

        # Verify against calculate_all
        all_hashes = HashService.calculate_all(temp_path)
        assert all_hashes['md5'] == md5_hash
        assert all_hashes['sha256'] == sha256_hash
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

def test_hash_nonexistent_file():
    hashes = HashService.calculate_all("non_existent_file_path_xyz.bin")
    assert hashes['md5'] == 'ERROR'
    assert hashes['sha256'] == 'ERROR'
