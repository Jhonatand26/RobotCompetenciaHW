import time
from HiwonderSDK.mecanum import MecanumChassis  # Asegúrate de que este módulo esté disponible

class RobotMovement:
    def __init__(self):
        self.chassis = MecanumChassis()

    def rotate_right(self, duration=2):
        """Gira el robot hacia la derecha sobre su eje."""
        print("Girando a la derecha...")
        # Velocidad positiva para rotación hacia la derecha
        self.chassis.set_velocity(0, 0, 30)  # velocidad angular positiva (ajusta según sea necesario)
        time.sleep(duration)
        self.stop()

    def rotate_left(self, duration=2):
        """Gira el robot hacia la izquierda sobre su eje."""
        print("Girando a la izquierda...")
        # Velocidad negativa para rotación hacia la izquierda
        self.chassis.set_velocity(0, 0, -30)  # velocidad angular negativa (ajusta según sea necesario)
        time.sleep(duration)
        self.stop()

    def stop(self):
        """Detiene el movimiento del robot."""
        self.chassis.set_velocity(0, 0, 0)
        print("Robot detenido.")

if __name__ == '__main__':
    robot = RobotMovement()
    try:
        # Prueba de rotación: gira a la derecha por 2 segundos, luego a la izquierda por 2 segundos
        robot.rotate_right()
        time.sleep(1)  # Pausa entre movimientos
        robot.rotate_left()
    except KeyboardInterrupt:
        robot.stop()
