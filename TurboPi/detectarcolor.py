#!/usr/bin/env python3
# encoding:utf-8
import cv2
import numpy as np
import time

def detect_color(frame):
    """
    Detecta colores azul, verde y negro en la imagen proporcionada.
    Retorna el nombre del color detectado más prominente o "Ninguno".
    """
    # Convertir a espacio de color HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Rango de color para azul
    lower_blue = np.array([100, 150, 0])
    upper_blue = np.array([140, 255, 255])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    # Rango de color para verde
    lower_green = np.array([35, 100, 100])
    upper_green = np.array([85, 255, 255])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Rango de color para negro
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 30])
    mask_black = cv2.inRange(hsv, lower_black, upper_black)

    # Calcular el área de cada máscara
    blue_area = cv2.countNonZero(mask_blue)
    green_area = cv2.countNonZero(mask_green)
    black_area = cv2.countNonZero(mask_black)

    # Umbral para determinar si hay un color significativo
    total_pixels = frame.shape[0] * frame.shape[1]
    min_area_threshold = total_pixels * 0.01  # Reduce a 1% del área total de la imagen

    # Verificar si las áreas detectadas son significativas
    if blue_area > min_area_threshold and blue_area > green_area and blue_area > black_area:
        return "Azul"
    elif green_area > min_area_threshold and green_area > blue_area and green_area > black_area:
        return "Verde"
    elif black_area > min_area_threshold:
        # Condición más permisiva para detectar negro
        black_ratio = black_area / total_pixels
        # Ajuste del rango de detección del negro
        if blue_area < min_area_threshold * 0.5 and green_area < min_area_threshold * 0.5:
            return "Negro"
        else:
            return "Ninguno"
    else:
        return "Ninguno"

def main():
    print("Iniciando detección de color...")
    cap = cv2.VideoCapture(-1)  # Asegúrate de que el índice de la cámara sea correcto
    if not cap.isOpened():
        print("No se pudo abrir la cámara.")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("No se pudo capturar el cuadro de la cámara.")
                break

            color_detected = detect_color(frame)
            print(f"Color detectado: {color_detected}")

            # Esperar brevemente antes de la siguiente captura
            time.sleep(0.5)  # Ajusta el tiempo según lo necesario

    except KeyboardInterrupt:
        print("Detección de color interrumpida por el usuario.")
    finally:
        cap.release()
        print("Cámara liberada.")

if __name__ == '__main__':
    main()
