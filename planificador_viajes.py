import requests
import time

API_KEY = "AIzaSyC-PWLVIDzX5jFU32WipfLMN3sJu5R9yIg"

def obtener_coordenadas(ciudad, pais):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": f"{ciudad}, {pais}",
        "key": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data["results"]:
        return data["results"][0]["geometry"]["location"]
    return None

def calcular_viaje():
    print("\n--- Planificador de Viaje Chile-Argentina ---")

    origen = input("Ciudad de Origen (Chile): ") + ", Chile"
    destino = input("Ciudad de Destino (Argentina): ") + ", Argentina"

    print("\nMedios de transporte disponibles:")
    print("1. Automóvil")
    print("2. Bicicleta")
    print("3. A pie")
    opcion = input("Seleccione (1-3): ").strip()

    modos = {
        "1": "driving",
        "2": "bicycling",
        "3": "walking"
    }
    modo = modos.get(opcion, "driving")

    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origen,
        "destination": destino,
        "mode": modo,
        "language": "es",
        "key": API_KEY
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data["routes"]:
            ruta = data["routes"][0]["legs"][0]

            distancia_km = ruta["distance"]["value"] / 1000
            distancia_millas = distancia_km * 0.621371
            duracion = ruta["duration"]["text"]

            print("\n--- Resultados del Viaje ---")
            print(f"Distancia: {distancia_km:.2f} km | {distancia_millas:.2f} millas")
            print(f"Duración estimada: {duracion}")
            print(f"Medio de transporte: {'Automóvil' if modo == 'driving' else 'Bicicleta' if modo == 'bicycling' else 'A pie'}")

            print("\n--- Itinerario ---")
            for paso in ruta["steps"]:
                instruccion = paso["html_instructions"]
                instruccion = instruccion.replace("<b>", "").replace("</b>", "")
                print(f"{instruccion} ({paso['distance']['text']})")
        else:
            print("Error: No se encontró ruta entre las ciudades especificadas.")

    except Exception as e:
        print(f"Error al calcular la ruta: {str(e)}")

def main():
    while True:
        print("\n" + "="*50)
        print("PLANIFICADOR DE VIAJES CHILE - ARGENTINA")
        print("="*50)
        print("1. Calcular nuevo viaje")
        print("s. Salir")

        opcion = input("\nSeleccione opción: ").strip().lower()

        if opcion == "s":
            print("¡Hasta luego!")
            break
        elif opcion == "1":
            calcular_viaje()
        else:
            print("Opción inválida. Intente nuevamente.")

        time.sleep(1)

if __name__ == "__main__":
    main()
