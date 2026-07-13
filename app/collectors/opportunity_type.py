FREELANCE_INDICATORS = {
    "freelance", "freelancer", "project-based", "per project", "short-term contract",
}

def detect_opportunity_type(title: str, description: str = "") -> str:
    text = f"{title} {description}".lower()
    if any(word in text for word in FREELANCE_INDICATORS):
        return "freelance"
    return "remote_job"
