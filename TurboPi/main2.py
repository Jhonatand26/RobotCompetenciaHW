#!/usr/bin/python3
import time
from HiwonderSDK.mecanum import MecanumChassis
from HiwonderSDK.Sonar import Sonar
import RPi.GPIO as GPIO

class LaberintoRobot:
    def __init__(self):
        self.chassis = MecanumChassis()  # Inicializa el chasis
        self.sonar = Sonar()  # Inicializa el sensor de proximidad
        self.umbral_max = 350  # Umbral máximo en mm (35 cm)
        self.umbral_min = 170  # Umbral mínimo en mm (17 cm)
        self.umbral_bifurcacion = 86  # Umbral en mm para detectar una bifurcación

    def rotar_y_medir(self, grados):
        """
        Rota el robot en el sentido especificado (positivo = derecha, negativo = izquierda)
        y mide la distancia.
        """
        if grados < 0:
            print(f"Rotando {abs(grados)} grados a la izquierda...")
            self.chassis.set_velocity(0, 0, -10)  # Rotación a la izquierda
        else:
            print(f"Rotando {grados} grados a la derecha...")
            self.chassis.set_velocity(0, 0, 10)  # Rotación a la derecha

        tiempo_rotacion = abs(grados) / 10 * 0.1  # Tiempo proporcional a los grados (ajustar según pruebas)
        time.sleep(tiempo_rotacion)
        self.chassis.set_velocity(0, 0, 0)  # Detiene el robot
        distancia = self.sonar.getDistance()  # Mide la distancia
        print(f"Distancia medida tras rotar {grados} grados: {distancia} mm")
        return distancia

    def ajustar_trayectoria(self):
        """
        Ajusta la trayectoria del robot cuando detecta desviación mientras avanza.
        """
        print("Iniciando ajuste de trayectoria mientras avanza...")
        distancia_a = self.rotar_y_medir(-10)
        distancia_b = self.rotar_y_medir(20)
        self.rotar_y_medir(-10)  # Regresar a la posición inicial

        if distancia_a is None or distancia_b is None:
            print("Error en la medición de distancias. No se puede ajustar.")
            return

        diferencia_absoluta = abs(distancia_a - distancia_b)
        if distancia_a < distancia_b and diferencia_absoluta > 10:
            print("Desviación detectada hacia la izquierda. Corrigiendo hacia la derecha...")
            self.chassis.set_velocity(70, 100, 0)  # Ajuste hacia la derecha mientras avanza
        elif diferencia_absoluta <= 10:
            print("El robot está centrado. Continuando en línea recta...")
            self.chassis.set_velocity(80, 90, 0)  # Continuar avanzando recto
        elif distancia_a > distancia_b and diferencia_absoluta > 10:
            print("Desviación detectada hacia la derecha. Corrigiendo hacia la izquierda...")
            self.chassis.set_velocity(70, 80, 0)  # Ajuste hacia la izquierda mientras avanza

    def evaluar_bifurcacion(self):
        """
        Evalúa el espacio disponible para decidir hacia qué lado girar en una bifurcación mientras avanza.
        """
        print("Evaluando bifurcación...")
        distancia_izquierda = self.rotar_y_medir(-90)
        distancia_derecha = self.rotar_y_medir(180)
        self.rotar_y_medir(-90)  # Regresar a la posición inicial

        if distancia_izquierda is None or distancia_derecha is None:
            print("Error en la medición de distancias. No se puede tomar una decisión.")
            return

        if distancia_izquierda > distancia_derecha:
            print("Espacio mayor a la izquierda. Girando a la izquierda...")
            self.girar_izquierda()
        elif distancia_derecha > distancia_izquierda:
            print("Espacio mayor a la derecha. Girando a la derecha...")
            self.girar_derecha()
        else:
            print("Espacios similares. Girando a la derecha por defecto...")
            self.girar_derecha()

    def girar_izquierda(self):
        print("Girando 90 grados a la izquierda...")
        velocidad_rotacion = -40  # Puedes reducir la velocidad para mayor precisión
        print("Girando 90 grados a la derecha con precisión...")
        self.chassis.set_velocity(0, 0, velocidad_rotacion)  # Girar sobre su eje hacia la derecha a una velocidad reducida
        tiempo_giro = 0.5  # Ajustar este tiempo según pruebas para lograr 90 grados exactos
        time.sleep(tiempo_giro)
        self.chassis.set_velocity(0, 0, 0)  # Detener el movimiento

    def girar_derecha(self):
        velocidad_rotacion = 40  # Puedes reducir la velocidad para mayor precisión
        print("Girando 90 grados a la derecha con precisión...")
        self.chassis.set_velocity(0, 0, velocidad_rotacion)  # Girar sobre su eje hacia la derecha a una velocidad reducida
        tiempo_giro = 0.5  # Ajustar este tiempo según pruebas para lograr 90 grados exactos
        time.sleep(tiempo_giro)
        self.chassis.set_velocity(0, 0, 0)  # Detener el movimiento


    def ejecutar(self):
        """
        Bucle principal que evalúa continuamente la trayectoria y las bifurcaciones
        mientras el robot avanza.
        """
        self.chassis.set_velocity(70, 90, 0)  # Iniciar movimiento recto
        while True:
            distancia = self.sonar.getDistance()
            if distancia is None:
                print("Error de sensor o lectura no válida")
                continue

            if self.umbral_min < distancia <= self.umbral_max:
                self.ajustar_trayectoria()  # Ajustar mientras avanza
            elif distancia <= self.umbral_bifurcacion:
                
                self.evaluar_bifurcacion()  # Evaluar y decidir en una bifurcación
            else:
                print("Camino despejado. Continuando recto...")
                self.chassis.set_velocity(80, 90, 0)  # Avance recto estándar

            time.sleep(0.1)  # Pausa breve para permitir medición y ajuste

if __name__ == "__main__":
    # Limpia cualquier configuración previa
    GPIO.cleanup()
    # Configuración del botón
    GPIO.setmode(GPIO.BCM)
    boton_pin = 13
    GPIO.setup(boton_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    print("Esperando presionar el botón para iniciar...")
    try:
        # Esperar hasta que el botón sea presionado
        while GPIO.input(boton_pin) == GPIO.HIGH:
            time.sleep(0.1)

        print("Botón presionado. Iniciando...")
        robot = LaberintoRobot()
        robot.ejecutar()
    except KeyboardInterrupt:
        robot.chassis.set_velocity(0, 0, 0)
        print("Robot detenido.")
    finally:
        GPIO.cleanup()