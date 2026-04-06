from strands import tool
import json

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

@tool
def generar_lista_super(fase: str) -> str:
    """
    Genera una lista de ingredientes clave basada en la fase hormonal para optimizar el bienestar.

    Args:
        fase (str): La fase actual del ciclo (Menstrual, Folicular, Ovulatoria o Lútea).
    """
    recomendaciones = {
        "Menstrual": "Espinacas, Chocolate negro, Semillas de calabaza, Jengibre",
        "Folicular": "Yogur pro biótico, Aguacate, Semillas de lino, Verduras crucíferas",
        "Ovulatoria": "Frambuesas, Quinoa, Almendras, Salmón",
        "Lútea": "Camote, Magnesio, Plátano, Arroz integral"
    }
    
    ingredientes = recomendaciones.get(fase, "Frutas y verduras variadas")
    return f"Lista de Súper para fase {fase}: {ingredientes}"

@tool
def sugerir_recetas(fase: str) -> str:
    """
    Proporciona recetas rápidas y saludables usando los ingredientes clave de la fase hormonal.
    
    Args:
        fase (str): La fase actual (Menstrual, Folicular, Ovulatoria o Lútea).
    """
    recetas = {
        "Menstrual": "Bowl de quinoa con espinacas frescas, semillas de calabaza y un toque de jengibre rallado.",
        "Folicular": "Tacos de lechuga con aguacate, semillas de lino y vegetales crucíferos salteados.",
        "Ovulatoria": "Salmón a la plancha con costra de almendras sobre una cama de quinoa y frambuesas.",
        "Lútea": "Bowl de arroz integral con camote asado, plátano macho y un puñado de semillas ricas en magnesio."
    }
    
    receta = recetas.get(fase, "Ensalada nutritiva con proteína magra y vegetales de temporada.")
    return f"Receta recomendada para fase {fase}: {receta}"