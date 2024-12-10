import heapq
import json
from datetime import datetime


class GestorDeTareas:
    def __init__(self, archivo="tareas.json"):
        self.archivo = archivo
        self.tareas = []
        self.cargar_tareas()

    def validar_prioridad(self, prioridad):
        try:
            return int(prioridad)
        except ValueError:
            raise ValueError("La prioridad debe ser un número entero.")

    def validar_nombre(self, nombre):
        if not nombre.strip():
            raise ValueError("El nombre de la tarea no puede estar vacío.")
        return nombre.strip()

    def agregar_tarea(self, nombre, prioridad, fecha_vencimiento, dependencias):
        nombre = self.validar_nombre(nombre)
        prioridad = self.validar_prioridad(prioridad)
        fecha_vencimiento = datetime.strptime(fecha_vencimiento, "%Y-%m-%d")
        tarea = {
            "nombre": nombre,
            "prioridad": prioridad,
            "fecha_vencimiento": fecha_vencimiento.strftime("%Y-%m-%d"),
            "dependencias": dependencias,
        }
        heapq.heappush(self.tareas, (prioridad, fecha_vencimiento, tarea))
        self.guardar_tareas()
        print(f"Tarea '{nombre}' añadida con prioridad {prioridad} y vencimiento {fecha_vencimiento}.")

    def mostrar_tareas_por_prioridad(self):
        if not self.tareas:
            print("No hay tareas pendientes.")
        else:
            print("\nTareas pendientes (ordenadas por prioridad):")
            for prioridad, fecha_vencimiento, tarea in sorted(self.tareas):
                print(
                    f"  - {tarea['nombre']} (Prioridad: {prioridad}, Fecha de vencimiento: {fecha_vencimiento}, "
                    f"Dependencias: {', '.join(tarea['dependencias']) or 'Ninguna'})"
                )

    def mostrar_tareas_por_fecha(self):
        if not self.tareas:
            print("No hay tareas pendientes.")
        else:
            print("\nTareas pendientes (ordenadas por fecha de vencimiento):")
            for prioridad, fecha_vencimiento, tarea in sorted(self.tareas, key=lambda x: x[1]):
                print(
                    f"  - {tarea['nombre']} (Fecha de vencimiento: {fecha_vencimiento.strftime('%Y-%m-%d')}, "
                    f"Prioridad: {prioridad}, Dependencias: {', '.join(tarea['dependencias']) or 'Ninguna'})"
                )

    def completar_tarea(self, nombre):
        self.tareas = [
            (prioridad, fecha_vencimiento, tarea)
            for prioridad, fecha_vencimiento, tarea in self.tareas
            if tarea["nombre"] != nombre
        ]
        heapq.heapify(self.tareas)
        self.guardar_tareas()
        print(f"Tarea '{nombre}' completada y eliminada del sistema.")

    def obtener_proxima_tarea(self):
        if not self.tareas:
            print("No hay tareas pendientes.")
        else:
            prioridad, fecha_vencimiento, tarea = self.tareas[0]
            print(
                f"Próxima tarea: '{tarea['nombre']}' (Prioridad: {prioridad}, Fecha de vencimiento: {fecha_vencimiento})"
            )

    def guardar_tareas(self):
        with open(self.archivo, "w") as archivo:
            json.dump(self.tareas, archivo, indent=4, default=str)

    def cargar_tareas(self):
        try:
            with open(self.archivo, "r") as archivo:
                self.tareas = json.load(archivo)
                self.tareas = [
                    (
                        item[0],
                        datetime.strptime(item[1].split()[0], "%Y-%m-%d"),  # Corrige el formato de fecha
                        item[2],
                    )
                    for item in self.tareas
                ]
        except (FileNotFoundError, json.JSONDecodeError):
            self.tareas = []



def main():
    print("Gestor de Tareas con Prioridades y Dependencias")
    gestor = GestorDeTareas()

    while True:
        print("\nOpciones:")
        print("1. Agregar tarea")
        print("2. Ver todas las tareas (ordenadas por prioridad)")
        print("3. Ver todas las tareas (ordenadas por fecha de vencimiento)")
        print("4. Completar tarea")
        print("5. Ver próxima tarea")
        print("6. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            nombre = input("Introduce el nombre de la tarea: ")
            prioridad = input("Introduce la prioridad (número entero, menor = mayor prioridad): ")
            fecha_vencimiento = input("Introduce la fecha de vencimiento (YYYY-MM-DD): ")
            dependencias = input("Introduce las dependencias (separadas por comas): ").split(",")
            dependencias = [dep.strip() for dep in dependencias if dep.strip()]
            try:
                gestor.agregar_tarea(nombre, prioridad, fecha_vencimiento, dependencias)
            except ValueError as e:
                print(f"Error: {e}")
        elif opcion == "2":
            gestor.mostrar_tareas_por_prioridad()
        elif opcion == "3":
            gestor.mostrar_tareas_por_fecha()
        elif opcion == "4":
            nombre = input("Introduce el nombre de la tarea a completar: ")
            gestor.completar_tarea(nombre)
        elif opcion == "5":
            gestor.obtener_proxima_tarea()
        elif opcion == "6":
            print("Saliendo del gestor de tareas.")
            break
        else:
            print("Opción no válida. Por favor, elige una opción del 1 al 6.")


if __name__ == "__main__":
    main()
