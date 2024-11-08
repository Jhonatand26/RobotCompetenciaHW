from HiwonderSDK.mecanum import MecanumChassis
import time

def main():
    chassis = MecanumChassis()

    try:
        # Mover hacia adelante
        chassis.set_velocity(50, 90, 0)  # Velocidad 50, dirección 90° (adelante)
        time.sleep(2)

        # Girar a la izquierda
        chassis.set_velocity(50, 135, 0)  # Velocidad 50, dirección 135° (izquierda)
        time.sleep(2)

        # Parar
        chassis.set_velocity(0, 0, 0)  # Detener
    except KeyboardInterrupt:
        print("Interrumpido por el usuario")
    finally:
        chassis.set_velocity(0, 0, 0)  # Asegúrate de detener los motores

if __name__ == '__main__':
    main()
