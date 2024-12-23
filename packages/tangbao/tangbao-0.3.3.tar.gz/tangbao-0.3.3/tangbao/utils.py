from typing import Dict, Any

def extract_source(rag_output: Dict[str, Any]) -> str:
    text = ""
    titles = []
    for i, context in enumerate(rag_output["docs"], start=1):
        titles.append(context['metadata']['Source'])
        text += (
            f"<b>Chunk {i}:</b>"
            f"<br>"
            f"<u>Document name</u>: {context['metadata']['Source']}"
            f"<br>"
            f"<u>Page</u>: {context['metadata']['Page']}"
            f"<br>"
            f"<u>Content</u>: <em>{context['text']}</em>"
            f"<br><br>"
        )
    return text, titles