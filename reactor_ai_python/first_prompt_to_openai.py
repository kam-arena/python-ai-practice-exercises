import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai_client = openai.AzureOpenAI(azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"), 
                                   api_key=os.getenv("AZURE_OPENAI_APIKEY"),
                                   api_version=os.getenv("AZURE_OPENAI_VERSION"),
                                   max_retries=5)

system_prompt="Contestar de forma educada y en español"
user_prompt = "Cuentame una historia de un gato y un perro que son amigos, en 100 palabras"
prompt=[{"role": "system", "content": system_prompt}, 
        {"role": "user", "content": user_prompt}]

result = openai_client.chat.completions.create(messages=prompt, model=os.getenv("MODEL"))

print(result.choices[0].message.content)