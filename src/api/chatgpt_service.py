import openai
import os
import fitz
# Configura la clave de API desde el entorno
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text")
    return text


def summarize_text(text):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    max_tokens = 14000  # Límite de seguridad (menos de 16,385 tokens)
    
    # Divide el texto en palabras y limita la cantidad
    words = text.split()
    limited_text = " ".join(words[:max_tokens])  # Corta en palabras completas
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "Eres un asistente experto en resumir textos."},
            {"role": "user", "content": f"Resume el siguiente texto: {text}"}
        ]
    )
    
    return response.choices[0].message.content.strip()