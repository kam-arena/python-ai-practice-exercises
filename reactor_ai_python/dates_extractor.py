import os
from dotenv import load_dotenv
import openai

# Cargar variables de entorno desde .env
load_dotenv()

text_list = [
    "La conferencia de tecnología se llevará a cabo el 2023-04-15 en el centro de convenciones de la ciudad.",
    "La temporada cultural de otoño arranca con una serie de eventos imperdibles. El primero será la exposición de arte moderno que abre sus puertas el 10/15/2023 en el Museo de la Ciudad. A continuación, el 23 de octubre de 2023, se presentará la aclamada obra de teatro 'Luces de Bohemia' en el Teatro Principal. Finalmente, no te pierdas la feria del libro que se realizará del 11-01-2023 al 11-05-2023, donde podrás encontrar las últimas publicaciones y conocer a tus autores favoritos.",
    "El proyecto de desarrollo de software se desglosa en varias fases clave con fechas de entrega específicas. La fase de investigación debe completarse antes del 2023-05-20. La etapa de diseño y prototipado está programada para el período comprendido entre el 01/06/2023 y el 31/07/2023. La implementación del código comenzará el 1 de agosto de 2023 y se extenderá hasta el 30 de septiembre de 2023. Por último, la fase de pruebas y ajustes se llevará a cabo del 10-10-2023 al 10-12-2023, asegurando que el producto final esté listo para su lanzamiento el 15 de diciembre de 2023.",
    "El vuelo está programado para despegar a las 14:30 del 05-06-2023 desde el aeropuerto internacional.",
    "La videoconferencia internacional se iniciará a las 09:00 AM GMT del 22 de noviembre de 2023."
]

def extract_dates_from_text(text):
    openai_client = openai.AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_APIKEY"),
        api_version=os.getenv("AZURE_OPENAI_VERSION")
    )

    system_prompt = "Eres un asistente que extrae fechas de textos. Responde únicamente con las fechas en formato dd/mm/aaaa"
    user_prompt = f''' Extrae todas las fechas del siguiente texto: {text}

    Response:
    [
    '''

    response = openai_client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Extrae todas las fechas del siguiente texto: La reunión es el 3 de enero de 2024 y la entrega es el 12 de abril de 2024."},
            {"role": "assistant", "content": "03/01/2024, 12/04/2024"},
            {"role": "user", "content": user_prompt}
        ]
    )

    return response.choices[0].message.content

# Muestra el modelo utilizado
print(f"Usando el modelo: {os.getenv('MODEL')}")

# Itera text_list y extrae fechas
for i, text_with_dates in enumerate(text_list, start=1):
    dates = extract_dates_from_text(text_with_dates)
    print(dates)