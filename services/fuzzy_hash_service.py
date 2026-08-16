import os
import math
import ppdeep

class PureTLSH:
    """Pure-Python implementation of Trend Micro Locality Sensitive Hash (TLSH)."""
    
    @staticmethod
    def _bpt_count(data: bytes):
        """Construct bucket byte-pair tri-gram counts for TLSH."""
        buckets = [0] * 256
        for i in range(len(data) - 2):
            # TLSH mapping for byte triplets
            c1, c2, c3 = data[i], data[i+1], data[i+2]
            idx = (c1 ^ c2 ^ c3) % 256
            buckets[idx] += 1
        return buckets

    @classmethod
    def generate(cls, data: bytes) -> str | None:
        """Generate TLSH hash string for byte sequence (min 50 bytes)."""
        if not data or len(data) < 50:
            return None
            
        counts = cls._bpt_count(data)
        sorted_counts = sorted(counts)
        q1 = sorted_counts[63]
        q2 = sorted_counts[127]
        q3 = sorted_counts[191]

        if q3 == 0:
            nonzero = [c for c in sorted_counts if c > 0]
            if not nonzero:
                return None
            q1 = nonzero[max(0, len(nonzero) // 4)]
            q2 = nonzero[max(0, len(nonzero) // 2)]
            q3 = nonzero[max(0, (len(nonzero) * 3) // 4)]
            if q3 == 0:
                q3 = 1

        # Construct binary digest
        digest_bytes = bytearray()
        for i in range(0, 256, 4):
            val = 0
            for j in range(4):
                c = counts[i + j]
                if c > q3:
                    v = 3
                elif c > q2:
                    v = 2
                elif c > q1:
                    v = 1
                else:
                    v = 0
                val |= (v << (j * 2))
            digest_bytes.append(val)

        # Length code
        l_val = min(255, int(math.log(len(data), 1.5)) % 256)
        
        # Q ratio checksums
        q1_ratio = (q1 * 100 // q3) if q3 > 0 else 0
        q2_ratio = (q2 * 100 // q3) if q3 > 0 else 0
        checksum = (sum(data[:5]) % 256)

        header = f"T1{checksum:02X}{l_val:02X}{q1_ratio:02X}{q2_ratio:02X}"
        body = digest_bytes.hex().upper()
        return header + body

    @classmethod
    def diff(cls, hash1: str, hash2: str) -> int:
        """Calculate TLSH distance (0 = identical, lower = more similar)."""
        if not hash1 or not hash2 or not hash1.startswith("T1") or not hash2.startswith("T1"):
            return 999
            
        if hash1 == hash2:
            return 0

        # Body hex slice comparison
        body1 = hash1[10:]
        body2 = hash2[10:]
        
        if len(body1) != len(body2):
            return 999

        diff_count = 0
        for b1, b2 in zip(bytes.fromhex(body1), bytes.fromhex(body2)):
            # Hamming distance of 2-bit pair representations
            diff_count += bin(b1 ^ b2).count('1')

        # Length factor
        l1, l2 = int(hash1[4:6], 16), int(hash2[4:6], 16)
        ldiff = abs(l1 - l2)

        return (diff_count * 2) + ldiff


class FuzzyHashService:
    """Service for generating and comparing fuzzy hashes (ssdeep / CTPH and TLSH)."""

    @staticmethod
    def generate_ssdeep(file_path_or_bytes: str | bytes) -> str | None:
        """Generate ssdeep (CTPH) fuzzy hash."""
        try:
            if isinstance(file_path_or_bytes, bytes):
                return ppdeep.hash(file_path_or_bytes)
            else:
                return ppdeep.hash_from_file(file_path_or_bytes)
        except Exception:
            return None

    @staticmethod
    def compare_ssdeep(hash1: str | None, hash2: str | None) -> int:
        """Compare two ssdeep hashes. Returns similarity score from 0 to 100."""
        if not hash1 or not hash2:
            return 0
        try:
            score = ppdeep.compare(hash1, hash2)
            return max(0, min(100, score))
        except Exception:
            return 0

    @staticmethod
    def generate_tlsh(file_path_or_bytes: str | bytes) -> str | None:
        """Generate TLSH fuzzy hash."""
        try:
            if isinstance(file_path_or_bytes, bytes):
                content = file_path_or_bytes
            else:
                with open(file_path_or_bytes, 'rb') as f:
                    content = f.read()
            return PureTLSH.generate(content)
        except Exception:
            return None

    @staticmethod
    def compare_tlsh(hash1: str | None, hash2: str | None) -> tuple[int, int]:
        """
        Compare two TLSH hashes.
        Returns tuple of (distance, normalized_similarity_percentage).
        Distance: 0 is identical, lower is more similar.
        Normalized similarity: 100% when distance=0, decreasing towards 0%.
        """
        if not hash1 or not hash2:
            return (999, 0)
        try:
            dist = PureTLSH.diff(hash1, hash2)
            # Map TLSH distance to percentage: 0 distance = 100%, 120+ distance = 0%
            if dist >= 120:
                normalized_pct = 0
            else:
                normalized_pct = max(0, min(100, int((120 - dist) * 100 / 120)))
            return (dist, normalized_pct)
        except Exception:
            return (999, 0)

    @classmethod
    def generate_all(cls, file_path: str) -> dict:
        """Generate all fuzzy hashes for a given file path."""
        with open(file_path, 'rb') as f:
            content = f.read()
            
        ssdeep_h = cls.generate_ssdeep(content)
        tlsh_h = cls.generate_tlsh(content)
        
        return {
            'ssdeep': ssdeep_h if ssdeep_h else "UNAVAILABLE (File too small or error)",
            'tlsh': tlsh_h if tlsh_h else "UNAVAILABLE (Minimum 50 bytes required)"
        }
