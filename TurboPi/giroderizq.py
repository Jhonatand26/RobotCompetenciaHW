import time
from HiwonderSDK.mecanum import MecanumChassis  # Asegúrate de que este módulo esté disponible

class RobotMovement:
    def __init__(self):
        self.chassis = MecanumChassis()

    def rotate_right_90_degrees(self):
        """Gira el robot hacia la derecha 90 grados y se detiene."""
        print("Girando a la derecha 90 grados...")
        # Velocidad angular positiva para rotar a la derecha
        # Ajusta la velocidad y el tiempo según sea necesario
        angular_velocity = 30  # Ajusta este valor según la respuesta de tu robot
        rotation_duration = 1.5  # Ajusta este valor para lograr una rotación de 90 grados
        
        self.chassis.set_velocity(0, 0, angular_velocity)  # Iniciar rotación
        time.sleep(rotation_duration)  # Esperar el tiempo necesario para completar la rotación
        self.stop()  # Detener el robot
        print("Rotación completa. Robot detenido.")

    def stop(self):
        """Detiene el movimiento del robot."""
        self.chassis.set_velocity(0, 0, 0)
        print("Robot detenido.")

if __name__ == '__main__':
    robot = RobotMovement()
    try:
        robot.rotate_right_90_degrees()  # Gira a la derecha 90 grados
    except KeyboardInterrupt:
        robot.stop()
