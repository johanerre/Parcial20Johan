from flask import Flask, request, jsonify
import time

app = Flask(__name__)

vehiculos = {}
parqueadero = [None] * 10
registro_tiempos = {}
historial_pagos = {}

def calcular_tarifa(placa, tiempo_total):
    tarifa_por_hora = 5000 if vehiculos[placa]["tipo"].lower() == "carro" else 3000
    horas = max(1, round(tiempo_total / 3600))
    total_pagar = horas * tarifa_por_hora
    historial_pagos[placa] = {"tiempo": horas, "total": total_pagar}
    return total_pagar

@app.route("/registrar", methods=["POST"])
def registrar_vehiculo():
    data = request.json
    placa = data.get("placa")
    tipo = data.get("tipo")
    propietario = data.get("propietario")
    
    if not placa or not tipo or not propietario:
        return jsonify({"error": "Faltan datos para registrar el vehículo."}), 400
    
    if placa in vehiculos:
        return jsonify({"error": "El vehículo ya está registrado."}), 400
    
    vehiculos[placa] = {"tipo": tipo, "propietario": propietario}
    return jsonify({"mensaje": f"Vehículo {placa} registrado correctamente."})

@app.route("/parqueadero", methods=["GET"])
def estado_parqueadero():
    return jsonify({str(i + 1): parqueadero[i] for i in range(10)})

@app.route("/ingresar", methods=["POST"])
def ingresar_vehiculo():
    data = request.json
    placa = data.get("placa")
    
    if placa not in vehiculos:
        return jsonify({"error": "Vehículo no registrado."}), 400
    
    if placa in parqueadero:
        return jsonify({"error": "El vehículo ya tiene un espacio asignado."}), 400
    
    for i in range(10):
        if parqueadero[i] is None:
            parqueadero[i] = placa
            registro_tiempos[placa] = time.time()
            return jsonify({"mensaje": f"Vehículo {placa} ingresado en espacio {i + 1}."})
    
    return jsonify({"error": "Parqueadero lleno."}), 400

@app.route("/salir", methods=["POST"])
def salir_vehiculo():
    data = request.json
    placa = data.get("placa")
    
    if placa not in parqueadero:
        return jsonify({"error": "El vehículo no está en el parqueadero."}), 400
    
    tiempo_ingreso = registro_tiempos.pop(placa, None)
    if tiempo_ingreso is None:
        return jsonify({"error": "No se encontró el tiempo de ingreso."}), 400
    
    tiempo_total = time.time() - tiempo_ingreso
    tarifa = calcular_tarifa(placa, tiempo_total)
    
    for i in range(10):
        if parqueadero[i] == placa:
            parqueadero[i] = None
            break
    
    return jsonify({"mensaje": f"Vehículo {placa} salió. Tarifa: {tarifa} COP."})

@app.route("/vehiculo/<placa>", methods=["GET"])
def obtener_vehiculo(placa):
    if placa in vehiculos:
        return jsonify(vehiculos[placa])
    return jsonify({"error": "Vehículo no encontrado."}), 404

@app.route("/tarifa/<placa>", methods=["GET"])
def obtener_tarifa(placa):
    if placa in historial_pagos:
        return jsonify(historial_pagos[placa])
    return jsonify({"error": "No hay historial de pagos para este vehículo."}), 404

if __name__ == "__main__":
    app.run(debug=True)