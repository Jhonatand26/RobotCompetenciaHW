import cv2
import numpy as np
import threading
import time
from Camera import Camera  # Asegúrate de que esta clase esté correctamente configurada

# Límite HSV para cada color (puede que necesites ajustar estos valores)
lower_blue = np.array([100, 150, 0])
upper_blue = np.array([140, 255, 255])

lower_green = np.array([40, 50, 50])
upper_green = np.array([80, 255, 255])

lower_black = np.array([0, 0, 0])
upper_black = np.array([180, 255, 50])

class ColorDetect:
    def __init__(self):
        self.camera = Camera()
        self.running = False

    def start_detection(self):
        self.camera.camera_open()
        self.running = True
        threading.Thread(target=self.run, daemon=True).start()

    def stop_detection(self):
        self.running = False
        self.camera.camera_close()

    def detect_color(self, frame, lower_bound, upper_bound):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        result = cv2.bitwise_and(frame, frame, mask=mask)
        return mask, result, cv2.countNonZero(mask)  # Devuelve también el área de color detectado

    def run(self):
        while self.running:
            frame = self.camera.frame
            if frame is None:
                continue

            # Detectar Azul
            _, _, area_blue = self.detect_color(frame, lower_blue, upper_blue)

            # Detectar Verde
            _, _, area_green = self.detect_color(frame, lower_green, upper_green)

            # Detectar Negro
            _, _, area_black = self.detect_color(frame, lower_black, upper_black)

            # Lógica de Comportamiento según el Color Detectado
            if area_blue > 1000:  # Ajusta este umbral según sea necesario
                self.handle_blue()
            elif area_green > 1000:
                self.handle_green()
            elif area_black > 1000:
                self.handle_black()

            # Mostrar resultados (puedes comentar esto para evitar abrir ventanas si no es necesario)
            cv2.imshow('Vista de la Cámara', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop_detection()
                break

    def handle_blue(self):
        print("Azul detectado: Girar a la izquierda")
        # Lógica para girar a la izquierda usando los motores
        # Puedes insertar aquí tu código para manejar los motores

    def handle_green(self):
        print("Verde detectado: Girar a la derecha")
        # Lógica para girar a la derecha usando los motores
        # Puedes insertar aquí tu código para manejar los motores

    def handle_black(self):
        print("Negro detectado: Detenerse (fin del laberinto)")
        # Lógica para detener el robot
        # Puedes insertar aquí tu código para manejar los motores
        self.stop_detection()

if __name__ == '__main__':
    detector = ColorDetect()
    try:
        detector.start_detection()
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        detector.stop_detection()
        cv2.destroyAllWindows()
