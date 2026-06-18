# En app.py, dentro de tu función manejar_mensaje
@socketio.on("message")
def manejar_mensaje(mensaje):
    # 1. Mostrar el mensaje del usuario en la web
    socketio.send(mensaje, broadcast=True)
    
    # 2. Si el mensaje es un comando, el servidor web procesa la respuesta
    # (Ya tienes la lógica en comandos.py, podemos replicarla aquí fácilmente)
    texto = mensaje.split(":")[-1].strip().lower()
    
    if texto.startswith("/"):
        # Lógica de respuestas (puedes copiar el diccionario de tu comandos.py)
        respuestas = {
            "/laptops": "💻 Laptops: Lenovo, HP, ASUS, Dell.",
            "/pcgamer": "🖥️ PC Gamer: Ryzen 5/7 + RTX 3060/4060.",
            "/ofertas": "🔥 Ofertas: Desde Bs. 3.999."
        }
        respuesta = respuestas.get(texto, "Comando no reconocido.")
        socketio.send(f"🤖 Bot TechStore: {respuesta}", broadcast=True)