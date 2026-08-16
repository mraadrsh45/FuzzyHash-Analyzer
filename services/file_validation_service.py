import os
import uuid
import shutil
from werkzeug.utils import secure_filename
from config import Config

class FileValidationError(Exception):
    """Custom exception raised when file validation fails."""
    pass

class FileValidationService:
    """Service for securing, validating, and handling temporary files safely."""

    @staticmethod
    def validate_file(file_storage, max_size_bytes: int = None) -> dict:
        """
        Validate an uploaded file object.
        Checks for filename presence, extension safety, and size limits.
        """
        if not file_storage or not file_storage.filename:
            raise FileValidationError("No file uploaded or filename is empty.")

        filename = secure_filename(file_storage.filename)
        if not filename:
            # Fallback if secure_filename stripped everything
            filename = f"evidence_{uuid.uuid4().hex[:8]}.bin"

        # Check maximum allowed size
        max_limit = max_size_bytes or Config.MAX_CONTENT_LENGTH
        file_storage.seek(0, os.SEEK_END)
        size = file_storage.tell()
        file_storage.seek(0)  # Reset pointer to start

        if size == 0:
            raise FileValidationError(f"File '{filename}' is empty (0 bytes).")

        if size > max_limit:
            max_mb = max_limit / (1024 * 1024)
            raise FileValidationError(f"File '{filename}' exceeds maximum allowed size of {max_mb:.1f} MB.")

        # Check file extension
        _, ext = os.path.splitext(filename)
        ext = ext.lstrip('.').lower()
        if ext and Config.ALLOWED_EXTENSIONS and ext not in Config.ALLOWED_EXTENSIONS:
            raise FileValidationError(f"File extension '.{ext}' is not authorized for forensic ingestion.")

        return {
            'is_valid': True,
            'original_filename': file_storage.filename,
            'secure_filename': filename,
            'file_size': size,
            'extension': ext
        }

    @staticmethod
    def save_temp_file(file_storage, upload_dir: str = None) -> tuple[str, str]:
        """
        Save file to secure non-executable upload folder with unique internal filename.
        Returns tuple of (saved_file_path, unique_internal_filename).
        """
        target_dir = upload_dir or Config.UPLOAD_FOLDER
        os.makedirs(target_dir, exist_ok=True)

        orig_filename = secure_filename(file_storage.filename) or "upload.bin"
        unique_name = f"{uuid.uuid4().hex}_{orig_filename}"
        saved_path = os.path.join(target_dir, unique_name)

        file_storage.seek(0)
        file_storage.save(saved_path)

        # Set read-only permissions to prevent execution
        try:
            os.chmod(saved_path, 0o644)
        except Exception:
            pass

        return saved_path, unique_name

    @staticmethod
    def cleanup_file(file_path: str):
        """Remove a temporary file safely."""
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass

    @staticmethod
    def cleanup_directory(directory_path: str):
        """Clean all files in a directory."""
        if os.path.exists(directory_path):
            for fname in os.listdir(directory_path):
                fpath = os.path.join(directory_path, fname)
                try:
                    if os.path.isfile(fpath):
                        os.remove(fpath)
                    elif os.path.isdir(fpath):
                        shutil.rmtree(fpath)
                except Exception:
                    pass
