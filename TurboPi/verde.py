import time
from HiwonderSDK import Board

def indicar_final_verde():
    """
    Enciende los LEDs RGB en color verde para indicar el final del laberinto.
    """
    # Asumimos que tienes 2 LEDs configurados en tu sistema
    for i in range(2):  # Recorre los LEDs RGB disponibles
        Board.RGB.setPixelColor(i, Board.PixelColor(0, 255, 0))  # RGB(0, 255, 0) es verde
    Board.RGB.show()  # Aplica el cambio de color
    print("LEDs encendidos en verde.")

    # Mantén los LEDs encendidos por un tiempo (opcional)
    time.sleep(5)

    # Apaga los LEDs si lo deseas (opcional)
    for i in range(2):
        Board.RGB.setPixelColor(i, Board.PixelColor(0, 0, 0))  # Apaga los LEDs (RGB(0, 0, 0))
    Board.RGB.show()
    print("LEDs apagados.")

# Llama a esta función cuando el robot llegue al final del laberinto
if __name__ == "__main__":
    indicar_final_verde()
