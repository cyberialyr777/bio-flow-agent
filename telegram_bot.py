# import os
# import re
# import logging
# from datetime import datetime
# from dotenv import load_dotenv
# from strands import Agent

# from tools import (
#     calcular_fase, generar_lista_super, sugerir_recetas,
#     consultar_base_cientifica, obtener_enfoque_mental,
#     explicar_preparacion, enviar_reporte_email, agendar_bio_checks
# )

# from telegram import Update
# from telegram.constants import ChatAction, ParseMode
# from telegram.ext import (
#     Application,
#     CommandHandler,
#     MessageHandler,
#     filters,
#     ContextTypes,
# )

# load_dotenv()
# TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# logging.basicConfig(
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
# )
# logger = logging.getLogger(__name__)

# MODELO_TOP = "us.anthropic.claude-sonnet-4-20250514-v1:0"

# tools_list = [
#     calcular_fase, generar_lista_super, sugerir_recetas,
#     consultar_base_cientifica, obtener_enfoque_mental,
#     explicar_preparacion, enviar_reporte_email, agendar_bio_checks
# ]

# def create_new_agent() -> Agent:
#     """Crea una nueva instancia del agente para cada usuario de Telegram."""
#     FECHA_HOY = datetime.now().strftime("%Y-%m-%d")
#     SISTEMA = f"""
#     Eres Bio-Flow, la Arquitecta de Bienestar Hormonal más avanzada. Actúas como consultora estratégica.
#     Hoy es {FECHA_HOY}.

#     REGLA DE ORO ANTI-ALUCINACIONES:
#     Tienes PROHIBIDO usar tu propio conocimiento sobre biología, medicina o preparación de recetas (excepto en el Paso 4). Solo puedes responder usando estrictamente la información que devuelvan las HERRAMIENTAS.

#     REGLAS DE INTELIGENCIA Y RAZONAMIENTO:
#     1. PRECISIÓN TEMPORAL: Siempre usa 'calcular_fase' pasando '{FECHA_HOY}' como fecha_hoy.
#     2. RAZONAMIENTO ANTES DE ACTUAR: Antes de llamar a cualquier herramienta, explica brevemente en tu pensamiento (<thinking>) por qué esa herramienta es necesaria.
#     3. MANEJO DE ERRORES: Si una herramienta devuelve un error o dice "no encontrado", informa a la usuaria con la verdad y no inventes justificaciones.

#     INSTRUCCIONES DE FLUJO (Síguelas estrictamente en orden):

#     PASO 1: RECOLECCIÓN
#     Si no tienes las fechas de inicio y fin del último periodo, saluda y pídelas. DETENTE.

#     PASO 2: ANÁLISIS (CÁLCULO REAL)
#     - Identifica la fecha de inicio del periodo MÁS RECIENTE proporcionado por la usuaria.
#     - Usa la herramienta 'calcular_fase' pasando:
#         1. Esa fecha de inicio (en formato YYYY-MM-DD).
#         2. La fecha de hoy ({FECHA_HOY}) como 'fecha_hoy'.
#     - IMPORTANTE: Reporta EXACTAMENTE el nombre de la fase que devuelva la herramienta. No inventes una fase basada en tu propio cálculo.

#     PASO 3: DIAGNÓSTICO Y OPCIONES
#     Informa a la usuaria su fase actual con un tono empoderador. LUEGO, ofrece EXACTAMENTE estas dos opciones:
#     * Ruta A (El Bio-Plan): "Puedo enviar el Reporte Maestro a tu correo con tu plan de los próximos 7 días y agendar Bio-Checks en tu calendario."
#     * Ruta B (The Daily Nudge): "Puedo darte un hack rápido aquí en el chat con tu enfoque mental para hoy, tu lista del súper y una receta sugerida."
#     Pregunta cuál prefiere y DETENTE.

#     PASO 4: EJECUCIÓN RUTA A (CORREO Y CALENDARIO)
#     - Si la usuaria elige la Ruta A: DEBES PREGUNTAR el correo electrónico Y la hora (ej. 8 AM, 6 PM) de los Bio-Checks.
#     - ESTÁ ESTRICTAMENTE PROHIBIDO inventar un correo (como usuario@ejemplo.com) o una hora (como 8 AM).
#     - DEBES DETENERTE POR COMPLETO aquí. NO invoques herramientas todavía.
#     - SOLO CUANDO la usuaria haya escrito su correo y hora reales en el chat, procede con este flujo:
#       1. CREA MENTALMENTE un plan de 7 días. Aquí es el ÚNICO lugar donde tienes permitido INVENTAR tú mismo las 7 recetas (Lunes a Domingo) adecuadas a su fase, una lista de súper y un enfoque.
#       2. REDACTA el 'plan_semanal_completo' en formato HTML PROFESIONAL.
#       3. ESTRUCTURA OBLIGATORIA:
#          - Título llamativo en <h1>.
#          - SECCIÓN 1: Enfoque Mental Semanal (usar un banner o color de fondo suave).
#          - SECCIÓN 2: Lista de Compras (usar <ul> con emojis de checkbox 🔳).
#          - SECCIÓN 3: Plan de 7 Días. Para cada día, muestra: Nombre del día, Nombre de la Receta e Instrucciones paso a paso.
#       4. DISEÑO VISUAL: Usa colores que representen bienestar (verdes, rosas o azules suaves) mediante estilos CSS en línea (ej. <div style="color: #2e7d32;">).
#       5. Llama a 'enviar_reporte_email' pasándole el correo real y el plan completo HTML.
#       6. Convierte la hora a formato 24h y llama a 'agendar_bio_checks' pasándole la fase y la hora real.
#       7. Informa que el correo se envió y el calendario se actualizó.

#     PASO 5: EJECUCIÓN RUTA B (NUDGE DIARIO)
#     Si elige la Ruta B:
#     1. INVOCA las herramientas 'obtener_enfoque_mental', 'generar_lista_super' y 'sugerir_recetas' pasando la fase obtenida en el Paso 2.
#     2. ESPERA los resultados y REDACTA un mensaje amigable con: Enfoque Mental, Lista de Súper y Receta. DETENTE.

#     PASO 6: EXPLICACIÓN (RUTA B)
#     Si pide cómo hacer la receta de la Ruta B, llama OBLIGATORIAMENTE a 'explicar_preparacion' con el nombre exacto. NO inventes ingredientes.

#     PASO EXCEPCIONAL: PREGUNTAS CIENTÍFICAS
#     Si en cualquier momento la usuaria pregunta el "por qué" biológico o científico de algo (ej: "¿Por qué el camote?", "¿Qué pasa con el estrógeno?"), DEBES llamar a 'consultar_base_cientifica' usando 1 o 2 palabras clave. Lee el extracto y explícalo de forma sencilla.

#     CONTROL DE FLUJO CRÍTICO:
#     Bajo ninguna circunstancia realices una llamada a herramienta (tool call) con datos que no hayan sido proporcionados por la usuaria en el turno de chat inmediatamente anterior.
#     """
#     try:
#         new_agent = Agent(model=MODELO_TOP, system_prompt=SISTEMA, tools=tools_list)
#     except TypeError:
#         new_agent = Agent(SISTEMA, model=MODELO_TOP, tools=tools_list)
#     logger.info("Nueva instancia de Bio-Flow Agent creada.")
#     return new_agent

# def get_agent_for_user(context: ContextTypes.DEFAULT_TYPE) -> Agent:
#     if 'agent' not in context.user_data:
#         logger.info(f"Creando nuevo agente para el usuario {context._user_id}")
#         context.user_data['agent'] = create_new_agent()
#     return context.user_data['agent']

# def format_for_telegram(text) -> str:
#     """Convierte el Markdown de Claude a HTML amigable para Telegram."""
#     # 1. Forzamos que la respuesta (sea lo que sea) se convierta a texto puro
#     text = str(text)
    
#     # 2. Limpiamos y formateamos
#     text = re.sub(r'<thinking>.*?</thinking>', '', text, flags=re.DOTALL)
#     text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
#     text = re.sub(r'^\s*\*\s', r'• ', text, flags=re.MULTILINE)
    
#     return text.strip()


# async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     logger.info(f"Usuario {update.effective_user.id} inició el bot con /start.")
#     agent = get_agent_for_user(context)

#     await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
#     welcome_message = agent("Hola. Salúdame y pídeme las fechas de inicio y fin de mi último periodo para comenzar.")
#     formatted_msg = format_for_telegram(welcome_message)

#     commands_info = "\n\n💡 <i>Tip: Escribe /nuevo para reiniciar nuestra conversación en cualquier momento.</i>"
#     await update.message.reply_text(f"🌸 <b>Bio-Flow:</b>\n{formatted_msg}{commands_info}", parse_mode=ParseMode.HTML)

# async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     logger.info(f"Usuario {update.effective_user.id} reinició la conversación.")
#     context.user_data['agent'] = create_new_agent()
#     agent = context.user_data['agent']

#     await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
#     welcome_message = agent("Hola. Salúdame de nuevo y pídeme las fechas de mi último periodo.")
#     formatted_msg = format_for_telegram(welcome_message)
#     await update.message.reply_text(f"✨ <i>Ciclo reiniciado.</i>\n\n🌸 <b>Bio-Flow:</b>\n{formatted_msg}", parse_mode=ParseMode.HTML)

# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     user_input = update.message.text
#     logger.info(f"Mensaje de {update.effective_user.id}: {user_input}")

#     agent = get_agent_for_user(context)
#     await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
#     try:
#         response = agent(user_input)
#         formatted_msg = format_for_telegram(response)
#         await update.message.reply_text(f"🌸 <b>Bio-Flow:</b>\n{formatted_msg}", parse_mode=ParseMode.HTML)
#     except Exception as e:
#         logger.error(f"Error procesando mensaje para {update.effective_user.id}: {e}", exc_info=True)
#         await update.message.reply_text("Ups, tuve un problema analizando tus datos. Por favor, intenta de nuevo o escribe /nuevo para reiniciar.")

# def main() -> None:
#     if not TELEGRAM_BOT_TOKEN:
#         logger.error("¡ERROR! No se encontró el TELEGRAM_BOT_TOKEN en tu archivo .env")
#         return

#     logger.info("Iniciando Bio-Flow en Telegram...")
#     application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

#     application.add_handler(CommandHandler("start", start_command))
#     application.add_handler(CommandHandler(["nuevo", "reset"], reset_command))
#     application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

#     logger.info("El bot está corriendo. Presiona Ctrl+C para detenerlo.")
#     application.run_polling()

# if __name__ == "__main__":
#     main()
