import os
import hashlib

class HashService:
    """Service for computing cryptographic hashes (MD5, SHA-256)."""
    
    @staticmethod
    def calculate_md5(file_path_or_bytes: str | bytes) -> str:
        """Compute MD5 hex digest of a file or bytes in chunks."""
        hasher = hashlib.md5()
        if isinstance(file_path_or_bytes, bytes):
            hasher.update(file_path_or_bytes)
        else:
            with open(file_path_or_bytes, 'rb') as f:
                for chunk in iter(lambda: f.read(65536), b''):
                    hasher.update(chunk)
        return hasher.hexdigest().lower()

    @staticmethod
    def calculate_sha256(file_path_or_bytes: str | bytes) -> str:
        """Compute SHA-256 hex digest of a file or bytes in chunks."""
        hasher = hashlib.sha256()
        if isinstance(file_path_or_bytes, bytes):
            hasher.update(file_path_or_bytes)
        else:
            with open(file_path_or_bytes, 'rb') as f:
                for chunk in iter(lambda: f.read(65536), b''):
                    hasher.update(chunk)
        return hasher.hexdigest().lower()

    @staticmethod
    def calculate_all(file_path: str) -> dict:
        """Calculate both MD5 and SHA-256 in a single file pass."""
        if not file_path or not os.path.exists(file_path):
            return {
                'md5': 'ERROR',
                'sha256': 'ERROR'
            }
            
        md5_hasher = hashlib.md5()
        sha256_hasher = hashlib.sha256()
        
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(65536), b''):
                    md5_hasher.update(chunk)
                    sha256_hasher.update(chunk)
                    
            return {
                'md5': md5_hasher.hexdigest().lower(),
                'sha256': sha256_hasher.hexdigest().lower()
            }
        except Exception:
            return {
                'md5': 'ERROR',
                'sha256': 'ERROR'
            }
