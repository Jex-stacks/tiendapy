from datetime import datetime
from validaciones import pedir_entero, pedir_decimal
import persistencia

def registrar_venta(inventario):
    print("\n--- NUEVA VENTA ---")
    carrito = {}
    
    # Bucle infinito para meter cosas al carrito hasta que escriban fin
    while True:
        codigo = input("Codigo del producto (o 'fin' para cobrar): ").strip().upper()
        if codigo == 'FIN':
            break
            
        if codigo not in inventario:
            print("-> Error: No tenemos eso.")
            continue
            
        producto = inventario[codigo]
        if producto['stock'] == 0:
            print(f"-> Error: '{producto['nombre']}' esta agotado, toca pedir mas.")
            continue
            
        cantidad = pedir_entero(f"Cuantos va a llevar de '{producto['nombre']}': ")
        
        # Se revisa si se pide mas de lo que hay sumando lo que ya metio al carrito
        cantidad_en_carrito = carrito.get(codigo, 0)
        if cantidad_en_carrito + cantidad > producto['stock']:
            print(f"-> Error: No alcanza. Solo hay {producto['stock']} unidades.")
            continue
            
        carrito[codigo] = cantidad_en_carrito + cantidad
        print(f"-> Agregado: {cantidad} x {producto['nombre']}")

    if not carrito:
        print("-> Cancelado (no compro nada).")
        return

    # Sumamos todo
    subtotal = sum(inventario[cod]['precio'] * cant for cod, cant in carrito.items())
    descuento = 0.0
    
    if subtotal >= 100000:
        descuento = subtotal * 0.10
        print("-> Coronaste descuento del 10% por compra grande!")
    elif subtotal >= 50000:
        descuento = subtotal * 0.05
        print("-> Descuentico del 5% aplicado!")
        
    total = subtotal - descuento
    
    print("\n--- RESUMEN ---")
    for cod, cant in carrito.items():
        print(f"{inventario[cod]['nombre']} x{cant} : ${inventario[cod]['precio'] * cant}")
    print(f"Subtotal: ${subtotal}")
    if descuento > 0:
        print(f"Descuento: -${descuento}")
    print(f"TOTAL: ${total}")

    # Cobramos y revisamos que no paguen de menos
    while True:
        pago = pedir_decimal("\nCon cuanto paga el cliente?: $")
        if pago < total:
            print(f"-> Error: Falta plata. Faltan ${total - pago}")
        else:
            cambio = pago - total
            print(f"-> Listo. Vueltas a dar: ${cambio}")
            break

    # Guardamos todo y bajamos el stock del inventario
    detalles_venta = []
    for cod, cant in carrito.items():
        inventario[cod]['stock'] -= cant 
        detalles_venta.append(f"{cod}:{cant}")
        
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    linea_venta = f"{fecha_actual}|{total}|{'; '.join(detalles_venta)}"
    
    persistencia.registrar_venta(linea_venta)
    persistencia.guardar_inventario(inventario)
    print("-> Venta guardada y stock actualizado.")