import re

def clean_text(text: str) -> str:
    """Função helper para limpar o texto (HTML, pontuação, etc.)."""
    if not isinstance(text, str):
        return ""
    text = re.sub(r'<[^>]+>', '', text)  # Remove HTML
    text = re.sub(r'[^\w\s]', '', text)   # Remove pontuação
    text = re.sub(r'\d+', '', text)       # Remove números
    text = text.lower().strip()
    return text