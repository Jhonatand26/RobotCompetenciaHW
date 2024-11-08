#!/usr/bin/python3
# coding=utf8
import time
import HiwonderSDK.mecanum as mecanum

# Inicialización del chasis de las ruedas mecanum
chassis = mecanum.MecanumChassis()

def avanzar():
    """
    Controla el avance del robot.
    """
    print("El robot está avanzando.")
    chassis.set_velocity(80, 90, 0)  # Ajusta los valores según sea necesario (velocidad, ángulo de dirección, velocidad de guiñada)
    time.sleep(1)  # Ajusta la duración del movimiento si es necesario

def detener():
    """
    Detiene el movimiento del robot.
    """
    print("El robot se ha detenido.")
    chassis.set_velocity(0, 0, 0)
        
