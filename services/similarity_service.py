from services.fuzzy_hash_service import FuzzyHashService

class SimilarityService:
    """Service for evaluating, interpreting, and classifying file similarity."""

    @staticmethod
    def evaluate(ssdeep_hash_a: str | None, ssdeep_hash_b: str | None,
                 tlsh_hash_a: str | None, tlsh_hash_b: str | None) -> dict:
        """
        Evaluate file similarity using ssdeep and TLSH algorithm outputs.
        Calculates normalized score, assessment level, findings, and forensic warnings.
        """
        ssdeep_score = FuzzyHashService.compare_ssdeep(ssdeep_hash_a, ssdeep_hash_b)
        tlsh_dist, tlsh_sim_pct = FuzzyHashService.compare_tlsh(tlsh_hash_a, tlsh_hash_b)

        # Calculate weighted overall similarity score
        valid_scores = []
        if ssdeep_hash_a and ssdeep_hash_b and "UNAVAILABLE" not in ssdeep_hash_a and "UNAVAILABLE" not in ssdeep_hash_b:
            valid_scores.append(ssdeep_score)
        if tlsh_hash_a and tlsh_hash_b and "UNAVAILABLE" not in tlsh_hash_a and "UNAVAILABLE" not in tlsh_hash_b:
            valid_scores.append(tlsh_sim_pct)

        if valid_scores:
            overall_score = int(sum(valid_scores) / len(valid_scores))
        else:
            overall_score = ssdeep_score

        overall_score = max(0, min(100, overall_score))

        # Classify assessment range
        if overall_score <= 30:
            assessment = "Low Similarity"
            badge_color = "success"  # green/blue tone in UI
            description = "The analyzed files exhibit little to no structural or byte-sequence overlap."
            recommendation = "Files appear distinct. No immediate structural relation identified."
        elif overall_score <= 70:
            assessment = "Moderate Similarity"
            badge_color = "warning"  # amber tone in UI
            description = "The analyzed files share partial code sections, resources, or structural blocks."
            recommendation = "Further investigation recommended. Perform code diffing or static component inspection."
        else:
            assessment = "High Similarity"
            badge_color = "danger"  # red/cyan alert tone in UI
            description = "The analyzed files demonstrate a high degree of structural and sequence similarity according to fuzzy hashing algorithms."
            recommendation = "Strong indicator of file relationship, variant lineage, or code reuse. Full static/dynamic investigation advised."

        methodology = (
            "Fuzzy hashing algorithms (Context-Triggered Piecewise Hashing / ssdeep and "
            "Locality Sensitive Hashing / TLSH) generate digests by dividing data into pseudo-random "
            "blocks based on file content. Unlike cryptographic hashes (MD5, SHA-256) where a single byte edit "
            "completely alters the hash, fuzzy hashes produce similar values for structurally related files."
        )

        disclaimer = (
            "DISCLAIMER: Similarity assessment is an investigative file-relationship indicator "
            "and DOES NOT independently establish that a file is malicious. Malware determination "
            "requires comprehensive analysis including static analysis, dynamic sandboxing, YARA matching, "
            "PE structural review, behavioral monitoring, and threat intelligence context."
        )

        return {
            'overall_score': overall_score,
            'assessment': assessment,
            'badge_color': badge_color,
            'ssdeep_score': ssdeep_score,
            'tlsh_distance': tlsh_dist,
            'tlsh_similarity_pct': tlsh_sim_pct,
            'description': description,
            'recommendation': recommendation,
            'methodology': methodology,
            'disclaimer': disclaimer
        }
