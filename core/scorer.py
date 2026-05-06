import re

def extract_score(analysis_text: str) -> int:
    """Extract compliance score from analysis text."""
    match = re.search(r'COMPLIANCE SCORE:\s*(\d+)', analysis_text)
    if match:
        score = int(match.group(1))
        return max(0, min(100, score))
    return 0

def get_score_label(score: int) -> str:
    """Return risk label based on score."""
    if score >= 80:
        return "LOW RISK"
    elif score >= 60:
        return "MEDIUM RISK"
    elif score >= 40:
        return "HIGH RISK"
    else:
        return "CRITICAL RISK"

def get_score_color(score: int) -> str:
    """Return color for UI display."""
    if score >= 80:
        return "green"
    elif score >= 60:
        return "orange"
    elif score >= 40:
        return "red"
    else:
        return "darkred"

def score_all(results: dict) -> dict:
    """
    Add scores to all framework results.
    Returns updated results dict with scores added.
    """
    scored = {}
    for framework, result in results.items():
        scored[framework] = result.copy()
        if "error" in result:
            scored[framework]["score"] = 0
            scored[framework]["label"] = "ERROR"
            scored[framework]["color"] = "grey"
        else:
            score = extract_score(result["analysis"])
            scored[framework]["score"] = score
            scored[framework]["label"] = get_score_label(score)
            scored[framework]["color"] = get_score_color(score)
    return scored

def overall_score(scored_results: dict) -> dict:
    """Calculate overall score across all frameworks."""
    scores = [v["score"] for v in scored_results.values() if "score" in v]
    if not scores:
        return {"score": 0, "label": "ERROR", "color": "grey"}
    avg = int(sum(scores) / len(scores))
    return {
        "score": avg,
        "label": get_score_label(avg),
        "color": get_score_color(avg)
    }

if __name__ == "__main__":
    # Test scorer
    dummy_results = {
        "dpdp": {"framework_name": "DPDP", "analysis": "COMPLIANCE SCORE: 70\nPASSED CHECKS:\n- something"},
        "gdpr": {"framework_name": "GDPR", "analysis": "COMPLIANCE SCORE: 55\nPASSED CHECKS:\n- something"},
    }
    scored = score_all(dummy_results)
    for fw, result in scored.items():
        print(f"{result['framework_name']}: {result['score']}/100 — {result['label']}")
    overall = overall_score(scored)
    print(f"\nOverall: {overall['score']}/100 — {overall['label']}")
