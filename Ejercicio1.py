import time
import json
from flask import Flask

app = Flask(__name__)

vehiculos = {}
parqueadero = [None] * 10
registro_tiempos = {}
historial_pagoss = {}

class VehiculoNoRegistrado(Exception):
    pass

def registrar_vehiculo(vehiculos, placa, tipo, propietario):
    if placa in vehiculos:
        print(f"Error: La placa {placa} ya está registrada.")
        return False
    else:
        vehiculos[placa] = {"tipo": tipo, "propietario": propietario}
        print(f"Vehículo con placa {placa} registrado exitosamente.")
        return True

def asignar_espacio(placa):
    if placa not in vehiculos:
        print(f"Error: La placa {placa} no está registrada. Registre el vehículo primero.")
        return
    
    if placa in parqueadero:
        print(f"Error: El vehículo con placa {placa} ya tiene un espacio asignado.")
        return

    for i in range(10):
        if parqueadero[i] is None:
            parqueadero[i] = placa
            print(f"Espacio {i + 1} asignado a vehículo con placa {placa}.")
            return
    
    print("Error: El parqueadero está lleno.")

import json

def mostrar_vehiculos(vehiculos):
    if not vehiculos:
        print("No hay vehículos registrados.")
    else:
        print(json.dumps(vehiculos, indent=4, ensure_ascii=False)) 

def calcular_tarifa(placa, tiempo_total):
    tarifa_por_hora = 5000 if vehiculos[placa]["tipo"].lower() == "carro" else 3000
    horas = max(1, round(tiempo_total / 3600))  
    total_pagar = horas * tarifa_por_hora
    historial_pagoss[placa] = {"tiempo": horas, "total": total_pagar}
    print(f"Tarifa calculada: {total_pagar} COP ({horas} horas).")

def registrar_ingreso_salida(placa):
    try:
        if placa not in vehiculos:
            raise VehiculoNoRegistrado(f"Error: La placa {placa} no está registrada.")

        if placa in registro_tiempos:
            tiempo_ingreso = registro_tiempos.pop(placa)
            tiempo_total = time.time() - tiempo_ingreso
            horas = int(tiempo_total // 3600)
            minutos = int((tiempo_total % 3600) // 60)
            print(f"Vehículo {placa} salió. Tiempo total: {horas} horas y {minutos} minutos.")
            calcular_tarifa(placa, tiempo_total)
        else:
            registro_tiempos[placa] = time.time()
            print(f"Vehículo {placa} ingresó a las {time.strftime('%H:%M')}.")

    except VehiculoNoRegistrado as e:
        print(e)

def generar_reporte():
    if not historial_pagoss:
        print("No hay historial de pagos.")
    else:
        print(json.dumps(historial_pagoss, indent=4))

def menu():
    while True:
        print("\nMenú:")
        print("1. Registrar vehículo")
        print("2. Asignar espacio de parqueo")
        print("3. Mostrar vehículos")
        print("4. Registrar ingreso/salida")
        print("5. Generar reporte de pagos")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            while True:
                placa = input("Ingrese la placa del vehículo: ").strip().upper()
                if placa in vehiculos:
                    print(f"Error: La placa {placa} ya está registrada. Intente con otra.")
                else:
                    break  
            
            tipo = input("Ingrese el tipo de vehículo (Carro/Moto): ").strip()
            propietario = input("Ingrese el nombre del propietario: ").strip()
            registrar_vehiculo(vehiculos, placa, tipo, propietario)
        
        elif opcion == "2":
            placa = input("Ingrese la placa del vehículo para asignar parqueo: ").strip().upper()
            asignar_espacio(placa)

        elif opcion == "3":
            mostrar_vehiculos(vehiculos)

        elif opcion == "4":
            placa = input("Ingrese la placa del vehículo para registrar ingreso/salida: ").strip().upper()
            registrar_ingreso_salida(placa)

        elif opcion == "5":
            generar_reporte()

        elif opcion == "6":
            break
        
        else:
            print("Opción no válida. Intente nuevamente.")
menu()