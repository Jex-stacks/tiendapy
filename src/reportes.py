import os
from tabulate import tabulate

RUTA_VENTAS = "data/ventas.txt"

def reporte_alertas(inventario):
    print("\n--- ALERTAS DE STOCK ---")
    alertas = {}
    
    # Revisamos que se esta acabando segun el stock minimo de cada cosa
    for cod, p in inventario.items():
        if p['stock'] <= p['stock_minimo']:
            prov = p['proveedor']
            if prov not in alertas:
                alertas[prov] = []
            
            estado = "AGOTADO" if p['stock'] == 0 else "Poco"
            alertas[prov].append([cod, p['nombre'], p['stock'], p['stock_minimo'], estado])
    
    if not alertas:
        print("-> Todo relax. Hay buen stock de todo.")
        return

    for prov, productos in alertas.items():
        print(f"\nProveedor: {prov}")
        print(tabulate(productos, headers=["Codigo", "Nombre", "Stock Actual", "Minimo", "Estado"], tablefmt="grid"))


def cierre_del_dia(inventario):
    print("\n--- CIERRE DEL DIA ---")
    if not os.path.exists(RUTA_VENTAS):
        print("-> No se ha vendido nada mijo.")
        return

    total_vendido = 0.0
    num_ventas = 0
    cantidades_vendidas = {cod: 0 for cod in inventario.keys()}

    with open(RUTA_VENTAS, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            
            # Sacamos los datos de cada linea de venta
            partes = linea.split("|")
            if len(partes) >= 3:
                num_ventas += 1
                total_vendido += float(partes[1])
                
                detalles = partes[2].split(";")
                for detalle in detalles:
                    if ":" in detalle:
                        cod_vendido, cant_vendida = detalle.split(":")
                        cod_vendido = cod_vendido.strip()
                        if cod_vendido in cantidades_vendidas:
                            cantidades_vendidas[cod_vendido] += int(cant_vendida)

    if num_ventas == 0:
        print("-> Hoy no hubo ventas.")
        return

    ticket_promedio = total_vendido / num_ventas
    
    producto_mas_vendido = None
    max_cantidad = -1
    productos_sin_ventas = []

    # Buscamos cual fue el que mas pego y cuales se quedaron frios
    for cod, cant in cantidades_vendidas.items():
        if cant > max_cantidad and cant > 0:
            max_cantidad = cant
            producto_mas_vendido = inventario[cod]['nombre']
        
        if cant == 0:
            productos_sin_ventas.append(inventario[cod]['nombre'])

    print(f"Total vendido: ${total_vendido:,.2f}")
    print(f"Transacciones: {num_ventas}")
    print(f"Ticket promedio: ${ticket_promedio:,.2f}")
    
    if producto_mas_vendido:
        print(f"El mas vendido: {producto_mas_vendido} ({max_cantidad} unidades)")
    
    print(f"Productos sin ventas hoy: {len(productos_sin_ventas)}")
    if productos_sin_ventas:
        print("-> Cero rotacion (ejemplos):", ", ".join(productos_sin_ventas[:5]) + ("..." if len(productos_sin_ventas) > 5 else ""))