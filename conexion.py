import mysql.connector

def conectar():
    conexion = mysql.connector.connect(
        host='localhost',
        user='root',
        port='3307',
        password='rootroot',
        database='productos'
    )
    return conexion

def consulta_id():
    conexion = conectar()
    cursor = conexion.cursor()
    while True:
        id_producto = input("ID del producto: ")
        # Consultar la cantidad actual del producto
        consulta_actual = "SELECT ProductId FROM producto WHERE ProductId = %s"
        cursor.execute(consulta_actual, (id_producto,))

        # Verificar si se encontró el producto
        producto_encontrado = cursor.fetchone()
        if producto_encontrado is not None:
            return int(id_producto)
            # Continuar con la lógica para actualizar el producto
        else:
            print("El producto con el ID especificado no fue encontrado.")
            # Puedes decidir qué hacer en este caso, por ejemplo, salir de la función o manejar el error de alguna otra manera

def agregar_producto():
    conexion = conectar()
    cursor = conexion.cursor()
    nombre = input("Ingrese el nombre del producto: ")
    descripcion = input("Ingrese la descripción del producto: ")
    
    precioCorrecto = False
    while not precioCorrecto:
        precio_str = input("Ingrese el precio: ")
        try:
            precio = float(precio_str)
            if precio > 0:
                precioCorrecto = True
            else:
                print("El precio debe ser mayor que 0.")
        except ValueError:
            print("Debe ingresar un valor numérico para el precio.")

    cantidadCorrecta = False
    while not cantidadCorrecta:
        cantidad_str = input("Ingrese la cantidad en stock del producto: ")
        try:
            cantidad = int(cantidad_str)
            if cantidad > 0:
                cantidadCorrecta = True
            else:
                print("La cantidad debe ser mayor que 0.")
        except ValueError:
            print("Debe ingresar un valor numérico entero para la cantidad.")

    consulta = "INSERT INTO producto (Nombre, descripcion, price, cantidad) VALUES (%s, %s, %s, %s)"
    datos = (nombre, descripcion, precio, cantidad)
    cursor.execute(consulta, datos)

    # Obtener el ID del producto recién insertado
    producto_id = cursor.lastrowid

    # Insertar una nueva transacción en la tabla InventoryTransactions
    consulta_transaccion = """
    INSERT INTO InventoryTransactions (ProductID, PreviousQuantity, NewQuantity, TransactionType)
    VALUES (%s, %s, %s, %s)
    """
    datos_transaccion = (producto_id, 0, cantidad, 'Entrada')  # Se asume que la transacción es una entrada de producto
    cursor.execute(consulta_transaccion, datos_transaccion)

    conexion.commit()
    print("Producto agregado con éxito!!!! \n")

def consultar_productos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM producto")
    productos = cursor.fetchall()
    for p in productos:
        print("=================================")
        datos = """ 
        ID: {0} 
        Nombre: {1} 
        Descripción: {2} 
        Precio: {3} 
        Cantidad: {4} 
        """
        print(datos.format(p[0], p[1], p[2], p[3], p[4]))
    print("\n")

def actualizar_producto():
    conexion = conectar()
    cursor = conexion.cursor()
    print("Primero coloque el ID del producto a actualizar \n")
    id_producto =  consulta_id()
    
    # Consultar la cantidad actual del producto
    consulta_cantidad_actual = "SELECT cantidad FROM producto WHERE ProductId = %s"
    cursor.execute(consulta_cantidad_actual, (id_producto,))
    cantidad_actual_row = cursor.fetchone()
    #print(cantidad_actual_row)
    
    if cantidad_actual_row is None:
        print("El producto con el ID especificado no fue encontrado.")
        return

    cantidad_actual = cantidad_actual_row[0]

    nuevo_nombre = input("Ingrese el nuevo nombre del producto: ")
    nuevo_descripcion = input("Ingrese la nueva descripción del producto: ")

    precioCorrecto = False
    while not precioCorrecto:
        precio_str = input("Ingrese el nuevo precio: ")
        try:
            nuevo_precio = float(precio_str)
            if nuevo_precio > 0:
                precioCorrecto = True
            else:
                print("El precio debe ser mayor que 0.")
        except ValueError:
            print("Debe ingresar un valor numérico para el precio.")

    cantidadCorrecta = False
    while not cantidadCorrecta:
        cantidad_str = input("Ingrese la cantidad en stock del producto: ")
        try:
            nuevo_cantidad = int(cantidad_str)
            if nuevo_cantidad > 0:
                cantidadCorrecta = True
            else:
                print("La cantidad debe ser mayor que 0.")
        except ValueError:
            print("Debe ingresar un valor numérico entero para la cantidad.")

    consulta = "UPDATE producto SET Nombre = %s, descripcion = %s, price = %s, cantidad = %s WHERE ProductId = %s"
    datos = (nuevo_nombre, nuevo_descripcion, nuevo_precio, nuevo_cantidad, id_producto)
    cursor.execute(consulta, datos)



    # Calcular la diferencia entre la cantidad actual y la nueva cantidad
    diferencia_cantidad = nuevo_cantidad - cantidad_actual

    # Insertar una nueva transacción en la tabla InventoryTransactions
    consulta_transaccion = """
    INSERT INTO InventoryTransactions (ProductID, PreviousQuantity, NewQuantity, TransactionType)
    VALUES (%s, %s, %s, %s)
    """
    # Determinar el tipo de transacción
    tipo_transaccion = 'Entrada' if diferencia_cantidad > 0 else 'Salida'
    #print(cantidad_actual)
    datos_transaccion = (id_producto, cantidad_actual, nuevo_cantidad, tipo_transaccion)
    cursor.execute(consulta_transaccion, datos_transaccion)

    conexion.commit()
    print("Producto actualizado con éxito !!! \n")

def eliminar_producto():
    conexion = conectar()
    cursor = conexion.cursor()
    print("Coloque el ID del producto a borrar \n")
    id_producto = consulta_id()

    # Eliminar los registros relacionados en InventoryTransactions
    consulta_eliminar_transacciones = "DELETE FROM InventoryTransactions WHERE ProductID = %s"
    cursor.execute(consulta_eliminar_transacciones, (id_producto,))

    consulta = "DELETE FROM producto WHERE ProductId = %s"
    datos = (id_producto,)
    cursor.execute(consulta, datos)
    conexion.commit()
    print("Producto eliminado con éxito !!! \n")
