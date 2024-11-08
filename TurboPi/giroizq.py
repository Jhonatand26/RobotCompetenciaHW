#!/usr/bin/python3
import time
from HiwonderSDK.mecanum import MecanumChassis

def girar_90_izq_preciso():
    chassis = MecanumChassis()  # Inicializa el chasis
    velocidad_rotacion = -40  # Puedes reducir la velocidad para mayor precisión
    print("Girando 90 grados a la derecha con precisión...")
    chassis.set_velocity(0, 0, velocidad_rotacion)  # Girar sobre su eje hacia la derecha a una velocidad reducida
    tiempo_giro = 0.5  # Ajustar este tiempo según pruebas para lograr 90 grados exactos
    time.sleep(tiempo_giro)
    chassis.set_velocity(0, 0, 0)  # Detener el movimiento

if __name__ == "__main__":
    girar_90_izq_preciso()
