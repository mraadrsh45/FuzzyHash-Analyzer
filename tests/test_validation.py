import io
import os
import pytest
from werkzeug.datastructures import FileStorage
from services.file_validation_service import FileValidationService, FileValidationError

def test_file_validation_success():
    data = io.BytesIO(b"Valid forensic test log file content data 12345")
    file = FileStorage(stream=data, filename="sample_artifact.log")
    
    val = FileValidationService.validate_file(file)
    assert val['original_filename'] == "sample_artifact.log"
    assert val['file_size'] > 0

def test_file_validation_empty():
    data = io.BytesIO(b"")
    file = FileStorage(stream=data, filename="empty.txt")
    
    with pytest.raises(FileValidationError, match="empty"):
        FileValidationService.validate_file(file)

def test_file_validation_invalid_extension():
    data = io.BytesIO(b"Unauthorized extension content")
    file = FileStorage(stream=data, filename="payload.unsupported_xyz_extension")
    
    with pytest.raises(FileValidationError, match="extension"):
        FileValidationService.validate_file(file)

def test_save_and_cleanup_temp_file():
    data = io.BytesIO(b"Temporary file storage and cleanup verification")
    file = FileStorage(stream=data, filename="test_cleanup.bin")
    
    saved_path, safe_name = FileValidationService.save_temp_file(file)
    assert os.path.exists(saved_path)
    
    FileValidationService.cleanup_file(saved_path)
    assert not os.path.exists(saved_path)
