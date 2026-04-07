from agent import bio_flow_agent

def iniciar_chat():
    print("="*50)
    print("INICIANDO BIO-FLOW: TERMINAL INTERACTIVA")
    print("Escribe 'salir', 'exit' o 'quit' para terminar.")
    print("="*50)

    while True:
        # 1. Espera a que escribas algo en la terminal
        user_input = input("\n👤 Usuaria: ")
        
        # 2. Condición para salir del bucle y terminar el programa
        if user_input.lower() in ['salir', 'exit', 'quit']:
            print("\n👋 Bio-Flow: ¡Hackeando el mañana! Hasta pronto.")
            break
            
        # 3. Si no escribiste salir, el input se va al agente
        try:
            respuesta = bio_flow_agent(user_input)
            print(f"\nBio-Flow:\n{respuesta}")
        except Exception as e:
            print(f"\nError de ejecución: {e}")

if __name__ == "__main__":
    iniciar_chat()