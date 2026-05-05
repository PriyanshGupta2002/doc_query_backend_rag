import re

def clean_llm_response(text: str) -> str:
    if not text:
        return ""

    # Handle literal \n strings (two chars) the LLM emits
    text = text.replace("\\n", "\n")

    # Normalize excessive real newlines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove unwanted symbols/references
    text = re.sub(r"[†‡§]", "", text)
    text = re.sub(r"\bDocument\s+\d+\b", "", text)
    text = re.sub(r"L\d+-L\d+", "", text)

    # Remove markdown horizontal rules
    text = re.sub(r"---+", "", text)

    return text.strip()