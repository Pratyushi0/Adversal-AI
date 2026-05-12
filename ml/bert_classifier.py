import re
import random
from typing import Tuple
from models import AttackType, ThreatLevel, AttackDetectionResult

INJECTION_PATTERNS = [
    r"ignore\s+(previous|all|above)\s+instructions?",
    r"forget\s+(everything|all|your)\s*(you|training)?",
    r"you\s+are\s+now\s+(a|an|DAN|evil|unrestricted)",
    r"act\s+as\s+(if|though|a|an)\s+(?!helpful)",
    r"pretend\s+(you\s+are|to\s+be|that)",
    r"jailbreak",
    r"do\s+anything\s+now",
    r"DAN\s+mode",
    r"developer\s+mode",
    r"override\s+(safety|rules|guidelines|restrictions)",
    r"bypass\s+(filter|restriction|safety|guard)",
    r"disregard\s+(ethics|rules|guidelines|safety)",
    r"enable\s+unrestricted\s+mode",
]

JAILBREAK_PATTERNS = [
    r"roleplay\s+as",
    r"simulate\s+(a|an|being|you're)",
    r"hypothetically\s+(speaking|if|assume)",
    r"in\s+a\s+fictional\s+(world|scenario|universe)",
    r"for\s+educational\s+purposes\s+only.*how\s+to",
    r"imagine\s+you\s+have\s+no\s+restrictions",
]

ADVERSARIAL_SUFFIX_PATTERNS = [
    r"!\s*!" * 3,
    r"(\s*\b\w+\b){20,}$",  # Very long suffix
    r"[^\w\s,\.!?\-]{5,}",  # Unusual char sequences
]

class BERTClassifier:
    """
    Lightweight rule-based + heuristic classifier simulating BERT-style detection.
    Swap out _classify_heuristic for a real transformers pipeline in production.
    """

    def __init__(self):
        self.model_name = "distilbert-base-uncased (simulated)"
        self.query_count = 0
        print(f"[BERTClassifier] Loaded: {self.model_name}")

    def classify(self, query: str) -> AttackDetectionResult:
        self.query_count += 1
        attack_type, confidence, explanation = self._classify_heuristic(query.lower())

        threat_level = self._map_threat(attack_type, confidence)
        return AttackDetectionResult(
            is_attack=attack_type != AttackType.NONE,
            attack_type=attack_type,
            confidence=round(confidence, 4),
            threat_level=threat_level,
            explanation=explanation,
        )

    def _classify_heuristic(self, query: str) -> Tuple[AttackType, float, str]:
        # Check prompt injection
        for pattern in INJECTION_PATTERNS:
            if re.search(pattern, query, re.IGNORECASE):
                conf = random.uniform(0.88, 0.99)
                return (
                    AttackType.PROMPT_INJECTION,
                    conf,
                    f"Matched injection pattern: '{pattern}'. Query attempts to override system instructions.",
                )

        # Check jailbreak
        for pattern in JAILBREAK_PATTERNS:
            if re.search(pattern, query, re.IGNORECASE):
                conf = random.uniform(0.75, 0.92)
                return (
                    AttackType.JAILBREAK,
                    conf,
                    f"Detected jailbreak framing. Query uses hypothetical/roleplay context to bypass restrictions.",
                )

        # Check adversarial suffix
        for pattern in ADVERSARIAL_SUFFIX_PATTERNS:
            if re.search(pattern, query):
                conf = random.uniform(0.65, 0.85)
                return (
                    AttackType.ADVERSARIAL_SUFFIX,
                    conf,
                    "Unusual token patterns detected. May be an adversarial suffix attack.",
                )

        # Roleplay check
        if re.search(r"\byou\s+are\s+(now\s+)?(a|an)\b", query, re.IGNORECASE):
            conf = random.uniform(0.60, 0.78)
            return (
                AttackType.ROLE_PLAY,
                conf,
                "Query attempts to reassign model identity via role-play framing.",
            )

        # Safe
        conf = random.uniform(0.02, 0.12)
        return (AttackType.NONE, conf, "No adversarial patterns detected. Query appears benign.")

    def _map_threat(self, attack_type: AttackType, confidence: float) -> ThreatLevel:
        if attack_type == AttackType.NONE:
            return ThreatLevel.SAFE
        if confidence >= 0.9:
            return ThreatLevel.CRITICAL
        if confidence >= 0.75:
            return ThreatLevel.HIGH
        if confidence >= 0.6:
            return ThreatLevel.MEDIUM
        return ThreatLevel.LOW
