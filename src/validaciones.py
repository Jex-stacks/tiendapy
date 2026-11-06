# Aca creamos nuestros propios errores para controlar que no hagan cosas raras
class ReglaNegocioError(Exception):
    pass

class StockInsuficienteError(ReglaNegocioError):
    pass

class PagoInsuficienteError(ReglaNegocioError):
    pass

def pedir_entero(mensaje, permitir_cero=False):
    # Obligamos al usuario a meter un numero y si mete letras lo ponemos a repetir
    while True:
        entrada = input(mensaje)
        try:
            valor = int(entrada)
            if valor < 0 or (not permitir_cero and valor == 0):
                print("-> Error: El valor no puede ser negativo ni cero.")
                continue
            return valor
        except ValueError:
            print("-> Error: Tienes que meter un numero entero (ej. 15).")

def pedir_decimal(mensaje):
    # Lo mismo de arriba pero para la plata (decimales)
    while True:
        entrada = input(mensaje)
        try:
            valor = float(entrada)
            if valor <= 0:
                print("-> Error: El precio o pago debe ser mayor a cero.")
                continue
            return valor
        except ValueError:
            print("-> Error: Tienes que meter un numero valido (ej. 4500.50).")