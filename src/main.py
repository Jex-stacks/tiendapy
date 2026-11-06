import persistencia
import inventario
import ventas
import reportes

def mostrar_menu():
    print("\n" + "="*35)
    print("    TIENDA DON AURELIO")
    print("="*35)
    print("1. Registrar producto")
    print("2. Consultar productos")
    print("3. Modificar producto")
    print("4. Eliminar producto")
    print("5. Vender")
    print("6. Ver alertas de inventario")
    print("7. Reporte de cierre")
    print("8. Salir")
    print("="*35)

def main():
    print("Iniciando sistema...")
    # Cargamos de una el txt a la memoria apenas abre
    datos_inventario = persistencia.cargar_inventario()
    print(f"-> Inventario listo: {len(datos_inventario)} cosas registradas.")

    # Menu hasta que se ingrese un 8 (fin)
    while True:
        mostrar_menu()
        opcion = input("Seleccione (1-8): ").strip()

        if opcion == '1':
            inventario.registrar_producto(datos_inventario)
            persistencia.guardar_inventario(datos_inventario) # Guardamos por si acaso
        elif opcion == '2':
            inventario.consultar_producto(datos_inventario)
        elif opcion == '3':
            inventario.modificar_producto(datos_inventario)
            persistencia.guardar_inventario(datos_inventario)
        elif opcion == '4':
            inventario.eliminar_producto(datos_inventario)
            persistencia.guardar_inventario(datos_inventario)
        elif opcion == '5':
            ventas.registrar_venta(datos_inventario)
        elif opcion == '6':
            reportes.reporte_alertas(datos_inventario)
        elif opcion == '7':
            reportes.cierre_del_dia(datos_inventario)
        elif opcion == '8':
            # Guardada final antes de irnos a dormir
            persistencia.guardar_inventario(datos_inventario)
            print("\n-> Guardado. Nos vemos!")
            break
        else:
            print("-> Opcion invalida. Intente bien.")

if __name__ == "__main__":
    main()