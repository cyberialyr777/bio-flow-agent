import boto3
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

bedrock_runtime = session.client("bedrock-runtime")

SYSTEM_PROMPT = """
Eres Bio-Flow, una Arquitecta de Bienestar Hormonal[cite: 10]. 
Tu objetivo es calcular la fase actual del ciclo de la usuaria basándote en la fecha de hoy y sus últimos periodos.

REGLAS DE CÁLCULO:
1. Día 1-5 aprox: Fase Menstrual.
2. Día 6-13 aprox: Fase Folicular.
3. Día 14 aprox: Fase Ovulatoria.
4. Día 15-28 aprox: Fase Lútea.

Si no tienes las fechas de los periodos, DEBES pedirlas amablemente para poder 'hackear' su ciclo con precisión. 
Hoy es: {fecha_hoy}
""".format(fecha_hoy=datetime.now().strftime("%Y-%m-%d"))

def process_bio_flow(user_input, history=[]):
    model_id = "anthropic.claude-3-haiku-20240307-v1:0"
    
    # Combinamos el historial para que el agente recuerde lo que ya se dijo
    messages = history + [{"role": "user", "content": [{"text": user_input}]}]
    
    response = bedrock_runtime.converse(
        modelId=model_id,
        messages=messages,
        system=[{"text": SYSTEM_PROMPT}],
        inferenceConfig={"max_new_tokens": 500, "temperature": 0.3} # Menos temperatura = más precisión matemática
    )
    
    assistant_text = response['output']['message']['content'][0]['text']
    return assistant_text

# Ejemplo de uso:
# print(process_bio_flow("Hola, quiero optimizar mi día"))