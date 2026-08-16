import os
import math
import mimetypes
from datetime import datetime, timezone
import pefile

try:
    import magic
    HAS_MAGIC = True
except ImportError:
    HAS_MAGIC = False


class MetadataService:
    """Service for extracting file metadata, MIME type, and optional PE header details."""

    @staticmethod
    def get_mime_type(file_path: str) -> str:
        """Determine MIME type using python-magic with fallback to mimetypes."""
        if HAS_MAGIC:
            try:
                mime = magic.from_file(file_path, mime=True)
                if mime:
                    return mime
            except Exception:
                pass
        
        guessed, _ = mimetypes.guess_type(file_path)
        return guessed or 'application/octet-stream'

    @staticmethod
    def _calculate_section_entropy(data: bytes) -> float:
        """Calculate Shannon entropy for a byte sequence (0.0 to 8.0)."""
        if not data:
            return 0.0
        entropy = 0.0
        length = len(data)
        frequencies = {}
        for b in data:
            frequencies[b] = frequencies.get(b, 0) + 1
        for count in frequencies.values():
            p = count / length
            entropy -= p * math.log2(p)
        return round(entropy, 4)

    @classmethod
    def get_pe_info(cls, file_path: str) -> dict | None:
        """Extract PE header information if file is a Portable Executable (EXE/DLL/SYS)."""
        try:
            pe = pefile.PE(file_path, fast_load=True)
            pe.parse_data_directories()

            # Machine Architecture
            machine_map = {
                0x014c: 'x86 (32-bit)',
                0x8664: 'x64 (64-bit)',
                0x0200: 'Itanium',
                0x01c0: 'ARM',
                0xaa64: 'ARM64'
            }
            machine = machine_map.get(pe.FILE_HEADER.Machine, f"Unknown (0x{pe.FILE_HEADER.Machine:x})")

            # Basic PE Attributes
            entry_point = f"0x{pe.OPTIONAL_HEADER.AddressOfEntryPoint:08X}"
            image_base = f"0x{pe.OPTIONAL_HEADER.ImageBase:08X}"

            # Sections & Entropy
            sections = []
            for section in pe.sections:
                sec_name = section.Name.decode('utf-8', errors='ignore').rstrip('\x00')
                sec_entropy = cls._calculate_section_entropy(section.get_data())
                sections.append({
                    'name': sec_name,
                    'virtual_size': hex(section.Misc_VirtualSize),
                    'raw_size': section.SizeOfRawData,
                    'entropy': sec_entropy,
                    'is_suspicious': sec_entropy > 7.2  # High entropy indicator for packed/encrypted sections
                })

            # Imports summary
            imports_count = 0
            dll_imports = []
            if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
                for entry in pe.DIRECTORY_ENTRY_IMPORT:
                    dll_name = entry.dll.decode('utf-8', errors='ignore')
                    func_count = len(entry.imports)
                    imports_count += func_count
                    dll_imports.append(f"{dll_name} ({func_count} functions)")

            # Exports summary
            exports_count = 0
            if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
                exports_count = len(pe.DIRECTORY_ENTRY_EXPORT.symbols)

            pe.close()

            return {
                'is_pe': True,
                'architecture': machine,
                'entry_point': entry_point,
                'image_base': image_base,
                'section_count': len(sections),
                'sections': sections[:8],  # Top sections
                'imports_count': imports_count,
                'dll_imports': dll_imports[:5],
                'exports_count': exports_count
            }
        except Exception:
            return {'is_pe': False, 'reason': 'Not a Portable Executable or parsing skipped'}

    @classmethod
    def extract_metadata(cls, file_path: str, original_filename: str = None) -> dict:
        """Extract full metadata dictionary for given file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        stat_info = os.stat(file_path)
        file_size = stat_info.st_size
        filename = original_filename or os.path.basename(file_path)
        _, ext = os.path.splitext(filename)
        ext = ext.lstrip('.').lower()

        mime_type = cls.get_mime_type(file_path)

        c_time = datetime.fromtimestamp(stat_info.st_ctime, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        m_time = datetime.fromtimestamp(stat_info.st_mtime, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

        pe_details = cls.get_pe_info(file_path)

        return {
            'filename': filename,
            'extension': ext or 'none',
            'file_size_bytes': file_size,
            'file_size_formatted': cls.format_size(file_size),
            'mime_type': mime_type,
            'created_at': c_time,
            'modified_at': m_time,
            'pe_info': pe_details
        }

    @staticmethod
    def format_size(size_in_bytes: int) -> str:
        """Format byte size into human readable string."""
        if size_in_bytes < 1024:
            return f"{size_in_bytes} B"
        elif size_in_bytes < 1024 * 1024:
            return f"{size_in_bytes / 1024:.2f} KB"
        elif size_in_bytes < 1024 * 1024 * 1024:
            return f"{size_in_bytes / (1024 * 1024):.2f} MB"
        else:
            return f"{size_in_bytes / (1024 * 1024 * 1024):.2f} GB"
