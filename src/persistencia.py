import os

RUTA_INVENTARIO = "data/inventario.txt"
RUTA_VENTAS = "data/ventas.txt"

def cargar_inventario():
    inventario = {}
    # Si el archivo no esta, arrancamos de ceros para que no se explote el programa
    if not os.path.exists(RUTA_INVENTARIO):
        print("Aviso: No hay txt de inventario. Arrancamos en blanco.")
        return inventario
        
    with open(RUTA_INVENTARIO, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            try:
                # Partimos la linea por la barra | como pide el documento
                partes = linea.split("|")
                if len(partes) != 7:
                    print(f"Ojo: Linea rara ignorada -> {linea}")
                    continue
                    
                codigo = partes[0]
                inventario[codigo] = {
                    "nombre": partes[1],
                    "categoria": partes[2],
                    "precio": float(partes[3]),
                    "stock": int(partes[4]),
                    "stock_minimo": int(partes[5]),
                    "proveedor": partes[6]
                }
            except ValueError:
                print(f"Ojo: Error de numeros en esta linea -> {linea}")
                continue
                
    return inventario

def guardar_inventario(inventario):
    # Escribimos todo el diccionario otra vez en el txt
    with open(RUTA_INVENTARIO, "w", encoding="utf-8") as f:
        for codigo, datos in inventario.items():
            linea = f"{codigo}|{datos['nombre']}|{datos['categoria']}|{datos['precio']}|{datos['stock']}|{datos['stock_minimo']}|{datos['proveedor']}\n"
            f.write(linea)

def registrar_venta(linea_venta):
    # Aca pegamos la nueva venta al final del txt sin borrar lo que ya habia
    with open(RUTA_VENTAS, "a", encoding="utf-8") as f:
        f.write(linea_venta + "\n")