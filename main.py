import conexion 

def mostrar_menu():
    print("===== Menú Principal =====")
    print("1. Agregar Producto")
    print("2. Consultar Productos")
    print("3. Actualizar Producto")
    print("4. Eliminar Producto")
    print("5. Salir")
    print("\n")

def obtener_opcion():
    while True:
        opcion = input("Seleccione una opción: ")
        if opcion.isdigit():  # Verifica si la entrada son solo dígitos
            return int(opcion)  # Convierte la entrada a un entero y la devuelve
        else:
            print("Error: Por favor ingrese solo números.")

def main():
    while True:
        mostrar_menu()
        opcion = obtener_opcion()
        if opcion == 1:
            conexion.agregar_producto()
        elif opcion == 2:
            conexion.consultar_productos()
        elif opcion == 3:
            conexion.actualizar_producto()
        elif opcion == 4:
            conexion.eliminar_producto()
        elif opcion == 5:
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()