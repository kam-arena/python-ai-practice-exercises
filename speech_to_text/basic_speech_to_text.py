import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

# Lee las credenciales desde variables de entorno
speech_key = os.getenv("SPEECH_KEY")
service_region = os.getenv("SPEECH_REGION")

# Configuración del servicio
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
speech_config.speech_recognition_language = "es-ES"  # Español

# Configuración del audio (micrófono por defecto)
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

# Crear el reconocedor
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

print("Habla algo en español...")
result = speech_recognizer.recognize_once()

# Mostrar el resultado
if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print(f"Texto reconocido: {result.text}")
elif result.reason == speechsdk.ResultReason.NoMatch:
    print("No se pudo reconocer la voz.")
elif result.reason == speechsdk.ResultReason.Canceled:
    print(f"Cancelado: {result.cancellation_details.reason}")
    if result.cancellation_details.error_details:
        print(f"Detalles del error: {result.cancellation_details.error_details}")
