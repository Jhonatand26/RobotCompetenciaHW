from HiwonderSDK.Sonar import Sonar
import time

def main():
    sonar = Sonar()  # Inicializa el sensor ultrasónico
    try:
        print("Iniciando prueba del sensor de proximidad...")
        while True:
            # Obtener la distancia medida por el sensor
            distance = sonar.getDistance()
            print(f"Distancia medida: {distance} mm")
            
            # Espera un momento antes de la siguiente lectura
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Prueba interrumpida por el usuario")
    finally:
        print("Finalizando prueba del sensor de proximidad.")

if __name__ == '__main__':
    main()
