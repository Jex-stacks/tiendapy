from tabulate import tabulate
from validaciones import pedir_entero, pedir_decimal

def registrar_producto(inventario):
    print("\n--- REGISTRAR NUEVO PRODUCTO ---")
    codigo = input("Ingrese el codigo del producto (ej. LAC001): ").strip().upper()
    
    # Pillamos que el codigo no lo hayan metido antes
    if codigo in inventario:
        print(f"-> Error: El codigo {codigo} ya existe mi pez.")
        return

    nombre = input("Nombre del producto: ").strip()
    categoria = input("Categoria (Lacteos, Bebidas, Aseo, Abarrotes, Snacks): ").strip().capitalize()
    
    # Usamos las funciones de validacion para que no metan letras por falta de conocimiento
    precio = pedir_decimal("Precio de venta unitario (COP): ")
    stock = pedir_entero("Unidades disponibles (Stock): ", permitir_cero=True)
    stock_minimo = pedir_entero("Stock minimo para generar alertas: ", permitir_cero=True)
    proveedor = input("Nombre del proveedor: ").strip()

    # Guardamos en la memoria
    inventario[codigo] = {
        "nombre": nombre,
        "categoria": categoria,
        "precio": precio,
        "stock": stock,
        "stock_minimo": stock_minimo,
        "proveedor": proveedor
    }
    print(f"-> Listo! Producto '{nombre}' guardado.")

def consultar_producto(inventario):
    print("\n--- CONSULTAR PRODUCTOS ---")
    opcion = input("Buscar por (1) Codigo o (2) Categoria: ").strip()
    
    resultados = []
    if opcion == "1":
        codigo = input("Ingrese el codigo a buscar: ").strip().upper()
        if codigo in inventario:
            p = inventario[codigo]
            resultados.append([codigo, p['nombre'], p['categoria'], p['precio'], p['stock'], p['stock_minimo'], p['proveedor']])
        else:
            print("-> Ese producto no existe.")
            return
    elif opcion == "2":
        categoria = input("Ingrese la categoria a buscar: ").strip().capitalize()
        for cod, p in inventario.items():
            if p['categoria'] == categoria:
                resultados.append([cod, p['nombre'], p['categoria'], p['precio'], p['stock'], p['stock_minimo'], p['proveedor']])
        if not resultados:
            print("-> No hay nada con esa categoria.")
            return
    else:
        print("-> Opcion paila.")
        return
        
    headers = ["Codigo", "Nombre", "Categoria", "Precio", "Stock", "Stock Min.", "Proveedor"]
    print("\n" + tabulate(resultados, headers=headers, tablefmt="grid"))

def modificar_producto(inventario):
    print("\n--- MODIFICAR PRECIO Y STOCK ---")
    codigo = input("Ingrese el codigo del producto a cambiar: ").strip().upper()
    
    if codigo not in inventario:
        print("-> Ese producto no existe.")
        return
        
    print(f"Cambiando cosas de: {inventario[codigo]['nombre']}")
    nuevo_precio = pedir_decimal("Nuevo precio (COP): ")
    nuevo_stock = pedir_entero("Nuevo stock disponible: ", permitir_cero=True)
    
    inventario[codigo]['precio'] = nuevo_precio
    inventario[codigo]['stock'] = nuevo_stock
    print("-> Actualizado!")

def eliminar_producto(inventario):
    print("\n--- ELIMINAR PRODUCTO ---")
    codigo = input("Ingrese el codigo a eliminar: ").strip().upper()
    
    if codigo in inventario:
        confirmacion = input(f"Seguro que quiere borrar '{inventario[codigo]['nombre']}'? (s/n): ").strip().lower()
        if confirmacion == 's':
            del inventario[codigo]
            print("-> Producto borrado.")
        else:
            print("-> Cancelado.")
    else:
        print("-> Ese producto no existe.")