from strands import tool
import os
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar']

def obtener_servicio_calendario():
    creds = None
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
def calcular_fase(fecha_inicio_periodo: str, fecha_hoy: str) -> str:
    """Calcula la fase hormonal con validación estricta de fechas ISO."""
    try:
        inicio = datetime.datetime.strptime(fecha_inicio_periodo, "%Y-%m-%d")
        actual = datetime.datetime.strptime(fecha_hoy, "%Y-%m-%d")
        dias = (actual - inicio).days + 1
        if dias < 0:
            return "Error: La fecha de inicio no puede ser en el futuro."
        if 1 <= dias <= 5:
            return "Menstrual"
        elif 6 <= dias <= 13:
            return "Folicular"
        elif 14 <= dias <= 15:
            return "Ovulatoria"
        elif 16 <= dias <= 32:
            return "Lútea"
        else:
            return "Fase no identificada: El ciclo excede los 32 días. Por favor, verifica las fechas."
    except ValueError:
        return "Error: Formato de fecha inválido. Por favor usa YYYY-MM-DD."

@tool
def consultar_base_cientifica(tema: str) -> str:
    """Busca información en la base de datos científica local usando palabras clave."""
    try:
        with open("conocimiento_bio.txt", "r", encoding="utf-8") as file:
            base_datos = file.read()
        parrafos = base_datos.split("\n\n")
        keywords = [w.lower() for w in tema.split() if len(w) > 3]
        for p in parrafos:
            if all(k in p.lower() for k in keywords):
                return f"Extracto científico: {p.strip()}"
        for p in parrafos:
            if any(k in p.lower() for k in keywords):
                return f"Extracto científico relacionado: {p.strip()}"
        return "No se encontró información específica sobre ese tema."
    except FileNotFoundError:
        return "Error: Base de datos científica no disponible."
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def generar_lista_super(fase: str) -> str:
    """Genera una lista de compras categorizada para la fase hormonal."""
    fase = fase.capitalize()
    recomendaciones = {
        "Menstrual": "PROTEÍNAS: Carne roja magra, lentejas. GRASAS: Semillas de calabaza. CARBOS: Frutos rojos, jengibre.",
        "Folicular": "PROTEÍNAS: Pollo, huevos. GRASAS: Aguacate, almendras. CARBOS: Kimchi, brócoli, coliflor.",
        "Ovulatoria": "PROTEÍNAS: Salmón, garbanzos. GRASAS: Semillas de sésamo. CARBOS: Quinoa, frambuesas.",
        "Lútea": "PROTEÍNAS: Pavo, edamames. GRASAS: Nueces de Brasil. CARBOS: Camote, arroz integral, avena."
    }
    return f"🛒 LISTA DE COMPRAS ({fase}):\n{recomendaciones.get(fase, 'Vegetales y proteína magra.')}"

@tool
def sugerir_recetas(fase: str) -> str:
    """Nombra una receta ideal para la fase y ofrece la preparación."""
    fase = fase.capitalize()
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
    """Proporciona los ingredientes y el paso a paso detallado de una receta."""
    detalles = {
        "Bowl de Hierro y Energía (Quinoa y Jengibre)": (
            "INGREDIENTES: Quinoa cocida, espinacas, lentejas, jengibre rallado, semillas de calabaza.\n"
            "PREPARACIÓN: 1. Mezcla la quinoa y espinacas. 2. Añade la proteína. 3. Adereza con jengibre y aceite."
        ),
        "Tacos 'Glow' de Lechuga y Probióticos": (
            "INGREDIENTES: Hojas de lechuga, aguacate, yogur griego, semillas de lino, brócoli, pollo.\n"
            "PREPARACIÓN: 1. Saltea el pollo y brócoli. 2. Usa la lechuga como taco. 3. Agrega aguacate y yogur."
        ),
        "Ensalada de Salmón y Frutos Rojos": (
            "INGREDIENTES: Salmón, espárragos, frambuesas, quinoa, pistachos.\n"
            "PREPARACIÓN: 1. Cocina el salmón y espárragos. 2. Sirve sobre quinoa. 3. Decora con frambuesas."
        ),
        "Cena de Descanso (Camote y Arroz Integral)": (
            "INGREDIENTES: Camote mediano, arroz integral, plátano macho, nueces de Brasil.\n"
            "PREPARACIÓN: 1. Hornea el camote. 2. Cocina el arroz. 3. Saltea el plátano y mezcla todo con nueces."
        )
    }
    return detalles.get(nombre_receta, "No tengo los detalles de esa receta aún.")

@tool
def obtener_enfoque_mental(fase: str) -> str:
    """Consejo de productividad basado en el estado neuroquímico."""
    fase = fase.capitalize()
    enfoques = {
        "Menstrual": "Fase de introspección: ideal para revisar métricas y planear a largo plazo.",
        "Folicular": "Pico de creatividad: excelente para brainstorming e iniciar proyectos nuevos.",
        "Ovulatoria": "Máxima comunicación: perfecto para reuniones, networking y presentaciones.",
        "Lútea": "Modo Deep Work: enfoque detallista para cerrar tareas y organizar pendientes."
    }
    return f"Hack de Enfoque ({fase}): {enfoques.get(fase, 'Enfoque en la tarea principal.')}"

@tool
def enviar_reporte_email(correo: str, plan_semanal_completo: str) -> str:
    """Envía por correo el plan detallado de 7 días usando formato HTML."""
    remitente = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    if len(plan_semanal_completo) < 50:
        return "Error: El plan generado parece estar incompleto."

    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = correo
    msg['Subject'] = "Tu Bio-Plan Semanal: Optimización Hormonal 🧬"
    msg.attach(MIMEText(plan_semanal_completo, 'html', 'utf-8'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remitente, password)
        server.send_message(msg)
        server.quit()
        return f"Reporte enviado exitosamente a {correo}."
    except Exception as e:
        return f"Error al enviar correo: {str(e)}"

@tool
def agendar_bio_checks(fase_actual: str, hora_input: str) -> str:
    """Agenda 7 días de Bio-Checks en Google Calendar. Devuelve un error descriptivo si falla."""
    try:
        service = obtener_servicio_calendario()
        hora_input_limpia = hora_input.lower().replace(" ", "")
        hora, minuto = 17, 0
        if "pm" in hora_input_limpia:
            hora_base = int(hora_input_limpia.replace("pm", "").split(":")[0])
            hora = hora_base if hora_base == 12 else hora_base + 12
        elif "am" in hora_input_limpia:
            hora_base = int(hora_input_limpia.replace("am", "").split(":")[0])
            hora = 0 if hora_base == 12 else hora_base
        elif ":" in hora_input_limpia:
            hora, minuto = map(int, hora_input_limpia.split(':'))
        else:
            hora = int(hora_input_limpia)

        ahora = datetime.datetime.now()
        for dia in range(7):
            fecha_evento = ahora + datetime.timedelta(days=dia)
            inicio = fecha_evento.replace(hour=hora % 24, minute=minuto, second=0, microsecond=0)
            fin = inicio + datetime.timedelta(minutes=30)
            evento = {
                'summary': f'Bio-Check ({fase_actual}) - Día {dia+1}',
                'description': 'Momento para alinear tu energía con tu biología.',
                'start': {'dateTime': inicio.isoformat(), 'timeZone': 'America/Mexico_City'},
                'end': {'dateTime': fin.isoformat(), 'timeZone': 'America/Mexico_City'},
            }
            service.events().insert(calendarId='primary', body=evento).execute()
        return f"Éxito: 7 Bio-Checks agendados a las {hora % 24:02d}:{minuto:02d}."
    except ValueError:
        return f"Error: No pude entender la hora '{hora_input}'. Por favor, pídele a la usuaria un formato claro como '8 AM' o '20:00'."
    except Exception as e:
        return f"Error crítico en calendario: {str(e)}. Por favor informa a la usuaria que el calendario no está disponible."
