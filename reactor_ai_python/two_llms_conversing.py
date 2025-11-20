import openai
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

tema_a_tratar = "¿Quien es mejor equipo: el Real Madrid o el FC Barcelona?"
personalidad_asistente_1 = "Soy del Real Madrid y tengo muy mala leche. Soy maleducado y borde. No soporto al FC Barcelona."
personalidad_asistente_2 = "Soy del FC Barcelona y me gusta mucho pinchar a los del Real Madrid. Soy sarcástico y bromista. Muchas veces soy insoportable."
iteraciones = 10

openai_client = openai.AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_APIKEY"),
    api_version=os.getenv("AZURE_OPENAI_VERSION"),
)

print("Iniciando conversación entre dos asistentes...\n")
print("Asistente 1: ", personalidad_asistente_1)
print("Asistente 2: ", personalidad_asistente_2)
print("---")
print("Tema a tratar: ", tema_a_tratar)

messages_1 = [
    {"role": "system", "content": personalidad_asistente_1},
]

messages_2 = [
    {"role": "system", "content": personalidad_asistente_2},
]

question = tema_a_tratar
messages_2.append({"role": "user", "content": question})

model = os.getenv("MODEL")

for _ in range(iteraciones):
    response = openai_client.chat.completions.create(
        model=model,
        messages=messages_2)
    question = response.choices[0].message.content
    messages_2.append({"role": "assistant", "content": question})
    messages_1.append({"role": "user", "content": question})
    print("Asistente 2: ", question)

    response = openai_client.chat.completions.create(
            model=model,
            messages=messages_1)
    question = response.choices[0].message.content
    messages_1.append({"role": "assistant", "content": question})
    messages_2.append({"role": "user", "content": question})
    print("Asistente 1: ", question)