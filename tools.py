from strands import tool
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

load_dotenv()

@tool
def consultar_base_cientifica(tema: str) -> str:
    """
    Busca información en la base de datos científica local sobre un tema específico.
    Usa esta herramienta cuando la usuaria pregunte el 'por qué' biológico de algo.
    """
    # En un demo sencillo, leemos un archivo de texto
    try:
        with open("conocimiento_bio.txt", "r", encoding="utf-8") as file:
            base_datos = file.read()
            
        # Aquí podrías usar una búsqueda más compleja, pero para el demo 
        # devolvemos un fragmento que contenga la palabra clave
        parrafos = base_datos.split("\n\n")
        resultados = [p for p in parrafos if tema.lower() in p.lower()]
        
        if resultados:
            return f"Extracto científico encontrado: {resultados[0]}"
        else:
            return "No se encontró información específica en los papers actuales."
            
    except FileNotFoundError:
        return "Error: Base de datos científica no disponible."

from strands import tool

@tool
def generar_lista_super(fase: str) -> str:
    """
    Genera una lista de compras extensa y categorizada para optimizar la fase hormonal.
    """
    # Expandimos las opciones para que el plan se sienta completo (Fuel)
    recomendaciones = {
        "Menstrual": (
            "PROTEÍNAS: Carne roja magra, lentejas.\n"
            "GRASAS: Semillas de calabaza, nueces.\n"
            "CARBOS: Frutos rojos, chocolate negro (>70%), jengibre, espinacas."
        ),
        "Folicular": (
            "PROTEÍNAS: Pollo, huevos, tofu.\n"
            "GRASAS: Aguacate, semillas de lino, almendras.\n"
            "CARBOS: Kimchi, yogur griego, brócoli, coliflor, calabacín."
        ),
        "Ovulatoria": (
            "PROTEÍNAS: Salmón, camarones, garbanzos.\n"
            "GRASAS: Semillas de sésamo, pistachos.\n"
            "CARBOS: Quinoa, frambuesas, espárragos, acelgas."
        ),
        "Lútea": (
            "PROTEÍNAS: Pavo, bacalao, edamames.\n"
            "GRASAS: Nueces de Brasil (magnesio), semillas de girasol.\n"
            "CARBOS: Camote, arroz integral, plátano macho, avena."
        )
    }
    
    ingredientes = recomendaciones.get(fase, "Vegetales variados y proteína magra.")
    return f"🛒 LISTA DE COMPRAS (Fase {fase}):\n{ingredientes}"

@tool
def sugerir_recetas(fase: str) -> str:
    """
    Nombra una receta ideal para la fase. Pregunta si desea la preparación.
    """
    nombres = {
        "Menstrual": "Bowl de Hierro y Energía (Quinoa y Jengibre)",
        "Folicular": "Tacos 'Glow' de Lechuga y Probióticos",
        "Ovulatoria": "Ensalada de Salmón y Frutos Rojos",
        "Lútea": "Cena de Descanso (Camote y Arroz Integral)"
    }
    nombre = nombres.get(fase, "Ensalada Bio-Flow")
    return f"🍳 Sugerencia: {nombre}. ¿Te gustaría que te explique los ingredientes y cómo prepararlo?"

@tool
def explicar_preparacion(nombre_receta: str) -> str:
    """
    Proporciona los ingredientes exactos y el paso a paso de una receta específica.
    """
    detalles = {
        "Bowl de Hierro y Energía (Quinoa y Jengibre)": (
            "INGREDIENTES: 1/2 taza de quinoa cocida, 1 puñado de espinacas frescas, lentejas o carne magra picada, 1 cdita de jengibre rallado, semillas de calabaza.\n"
            "PREPARACIÓN: 1. Sirve una base de espinacas y quinoa en un bowl. 2. Añade la proteína (lentejas/carne). "
            "3. Mezcla aceite de oliva con el jengibre rallado para hacer un aderezo y viértelo encima. 4. Espolvorea las semillas de calabaza. ¡No olvides tu trocito de chocolate negro de postre!"
        ),
        "Tacos 'Glow' de Lechuga y Probióticos": (
            "INGREDIENTES: Hojas de lechuga orejona (para usar de tortilla), aguacate, yogur griego (para salsa), semillas de lino, brócoli o coliflor picada, pollo o tofu.\n"
            "PREPARACIÓN: 1. Saltea el pollo/tofu junto con el brócoli usando poco aceite. 2. Prepara tus 'tortillas' de lechuga. "
            "3. Rellena con la mezcla salteada y rodajas de aguacate. 4. Decora con semillas de lino y un toque de yogur griego a modo de crema."
        ),
        "Ensalada de Salmón y Frutos Rojos": (
            "INGREDIENTES: 1 filete de salmón, espárragos o acelgas, un puñado de frambuesas frescas, 1/2 taza de quinoa, semillas de sésamo o pistachos.\n"
            "PREPARACIÓN: 1. Cocina el salmón a la plancha a fuego medio junto con los espárragos. 2. En un plato, coloca la quinoa como base. "
            "3. Pon el salmón y los espárragos encima. 4. Agrega las frambuesas frescas alrededor y espolvorea los pistachos o semillas de sésamo para el toque crujiente."
        ),
        "Cena de Descanso (Camote y Arroz Integral)": (
            "INGREDIENTES: 1 camote mediano, 1/2 taza de arroz integral, plátano macho, nueces de Brasil, pavo o bacalao (opcional).\n"
            "PREPARACIÓN: 1. Hornea o hierve el camote cortado en cubos. 2. Cocina el arroz a fuego lento. "
            "3. Saltea unas rodajas de plátano macho. 4. Mezcla todo en un bowl (puedes añadir pavo si deseas más proteína) y añade las nueces de Brasil troceadas para tu dosis de magnesio."
        )
    }
    return detalles.get(nombre_receta, "Lo siento, no tengo los detalles de esa receta aún. ¡Asegúrate de que el nombre coincida exactamente!")

@tool
def obtener_enfoque_mental(fase: str) -> str:
    """
    Proporciona un consejo de productividad y enfoque mental basado en el estado neuroquímico de la fase hormonal.
    
    Args:
        fase (str): La fase actual (Menstrual, Folicular, Ovulatoria o Lútea).
    """
    enfoques = {
        "Menstrual": "Día de evaluación e introspección. Tu cerebro tiene mayor conectividad. Ideal para revisar métricas, planear a largo plazo y descansar.",
        "Folicular": "¡Pico de creatividad! Tu dopamina está subiendo. Excelente día para iniciar proyectos complejos, hacer brainstorming y tomar riesgos calculados.",
        "Ovulatoria": "Día de máxima comunicación y empatía. Perfecto para liderar reuniones, presentar tu reto técnico en Talent Land o hacer networking.",
        "Lútea": "Modo 'Deep Work' (Trabajo Profundo). La progesterona te da un enfoque detallista. Es el momento de cerrar tareas pendientes y organizar."
    }
    
    hack = enfoques.get(fase, "Concéntrate en la tarea más importante del día y toma pausas activas.")
    return f"Hack de Enfoque Mental ({fase}): {hack}"

tool
def enviar_reporte_email(correo: str, plan_semanal_completo: str) -> str:
    """
    Envía por correo el plan de 7 días detallado.
    """
    remitente = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    
    # Validamos que el plan no venga vacío
    if "irá aquí" in plan_semanal_completo or len(plan_semanal_completo) < 50:
        return "Error: El plan generado es demasiado corto o es un placeholder. Por favor, redáctalo completo."

    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = correo
    msg['Subject'] = "Tu Bio-Plan Semanal: Optimización Hormonal de 7 Días 🧬"
    msg.attach(MIMEText(plan_semanal_completo, 'plain', 'utf-8'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remitente, password)
        server.send_message(msg)
        server.quit()
        return f"Reporte enviado con éxito a {correo}."
    except Exception as e:
        return f"Error al enviar correo: {str(e)}"


def obtener_servicio_calendario():
    creds = None
    # El archivo token.json guarda tus credenciales después de la primera vez
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('calendar', 'v3', credentials=creds)

@tool
def agendar_bio_checks(fase_actual: str, hora_input: str) -> str:
    """
    Agenda 7 días de Bio-Checks. Acepta formatos como '7 PM', '19:00', '8am'.
    """
    service = obtener_servicio_calendario()
    
    # --- Limpiador de hora inteligente ---
    hora_input = hora_input.lower().replace(" ", "")
    hora = 17 # default
    minuto = 0
    
    try:
        if "pm" in hora_input:
            hora = int(hora_input.replace("pm", "").split(":")[0]) + 12
        elif "am" in hora_input:
            hora = int(hora_input.replace("am", "").split(":")[0])
        elif ":" in hora_input:
            hora, minuto = map(int, hora_input.split(':'))
        else:
            hora = int(hora_input)
    except:
        pass # Usa el default 17:00 si falla

    ahora = datetime.datetime.now()
    for dia in range(7):
        fecha_evento = ahora + datetime.timedelta(days=dia)
        inicio = fecha_evento.replace(hour=hora % 24, minute=minuto, second=0, microsecond=0)
        fin = inicio + datetime.timedelta(minutes=30)
        
        titulo = f"Bio-Check ({fase_actual}) - Día {dia+1}"
        evento = {
            'summary': titulo,
            'description': 'Optimización Bio-Flow.',
            'start': {'dateTime': inicio.isoformat(), 'timeZone': 'America/Mexico_City'},
            'end': {'dateTime': fin.isoformat(), 'timeZone': 'America/Mexico_City'},
        }
        service.events().insert(calendarId='primary', body=evento).execute()
            
    return f"7 Bio-Checks agendados a las {hora}:{minuto:02d}."