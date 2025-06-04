"""
Este archivo es largo a propósito y simula el funcionamiento del frontend
del sistema. Contiene un menú de inicio del que el usuario selecciona 
las opciones o escribe lo que se le indica para lo siguiente:

1. Agregar un viaje
2. Registrar un gasto en un viaje
3. Mostrar los gastos por día en el viaje (solo muestra los días
en los que hubo un gasto)
4. Mostrar los gastos por tipo (solo muestra los tipos en los que
hubo gastos)


"""

from datetime import datetime, date
from entidades.viaje import Viaje
from entidades.forma_pago import FormaPago
from entidades.tipo_gasto import TipoGasto
from controles.control_viaje import ControlViaje
from servicios.conversor_moneda import ConversorMoneda

def mostrar_menu():
    print("\n=== GESTOR DE VIAJES ===")
    print("1. Agregar un viaje")
    print("2. Registrar un gasto")
    print("3. Mostrar gastos por día")
    print("4. Mostrar gastos por tipo")
    print("5. Salir")

def main():
    control = ControlViaje()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            fecha_inicio = datetime.strptime(input("Fecha inicio (YYYY-MM-DD): "), "%Y-%m-%d").date()
            fecha_fin = datetime.strptime(input("Fecha fin (YYYY-MM-DD): "), "%Y-%m-%d").date()

            if control.obtener_viaje(fecha_inicio):
                print("Ya hay un viaje en esa fecha. Seleccione otra.")
                break
            pais = input("País de destino: ")
            moneda = input("Moneda local en código ISO (Si" \
            "no sabe el código ISO de la moneda, ingrese 0 para ver" \
            "todos los códigos ISO disponibles): ")

            if moneda not in ConversorMoneda.lista_monedas().keys():
                print("Moneda no válida, se va a poner COP por defecto.")
                moneda = "COP"

            if moneda == "0":
                print(ConversorMoneda.lista_monedas())
                moneda = input("Moneda en código ISO: ")

            presupuesto_diario = float(input("Presupuesto diario (en COP): "))

            viaje = Viaje(pais, fecha_inicio, fecha_fin, presupuesto_diario, moneda)
            control.agregar_viaje(viaje)
            print("Viaje agregado con éxito.")

        elif opcion == "2":
            fecha_gasto = datetime.strptime(input("Fecha del gasto (YYYY-MM-DD): "), "%Y-%m-%d").date()
            valor = float(input("Valor del gasto (en moneda local): "))

            print("Método de pago:")
            print("1. EFECTIVO")
            print("2. TARJETA")
            metodo_pago_opcion = input("Seleccione método (1/2): ")

            if metodo_pago_opcion == "1":
                metodo_pago = FormaPago.EFECTIVO
            elif metodo_pago_opcion == "2":
                metodo_pago = FormaPago.TARJETA
            else:
                print("Opción inválida. Se seleccionará EFECTIVO por defecto.")
                metodo_pago = FormaPago.EFECTIVO

            print("Tipo de gasto:")
            print("1. Alojamiento")
            print("2. Alimentación")
            print("3. Transporte")
            print("4. Entretenimiento")
            print("5. Compras")
            tipo_gasto_opcion = input("Seleccione tipo (1-5): ")

            if tipo_gasto_opcion == "1":
                tipo_gasto = TipoGasto.ALOJAMIENTO
            elif tipo_gasto_opcion == "2":
                tipo_gasto = TipoGasto.ALIMENTACION
            elif tipo_gasto_opcion == "3":
                tipo_gasto = TipoGasto.TRANSPORTE
            elif tipo_gasto_opcion == "4":
                tipo_gasto = TipoGasto.ENTRETENIMIENTO
            elif tipo_gasto_opcion == "5":
                tipo_gasto = TipoGasto.COMPRAS
            else:
                print("Opción inválida. Se seleccionará Compras por defecto.")
                tipo_gasto = TipoGasto.ENTRETENIMIENTO

            try:
                diferencia = control.registrar_gasto(fecha_gasto, valor, metodo_pago, tipo_gasto)
                print(f"Gasto registrado. Diferencia de presupuesto ese día: {diferencia:.2f} COP")
            except ValueError as e:
                print(e)

        elif opcion == "3":
            fecha_consulta = datetime.strptime(input("Fecha (YYYY-MM-DD) para buscar viaje activo: "), "%Y-%m-%d").date()
            viaje = control.obtener_viaje(fecha_consulta)
            if viaje:
                resumen = control.mostrar_gastos_por_dia(viaje)
                for fecha, valores in resumen.items():
                    total = valores["EFECTIVO"] + valores["TARJETA"]
                    print(f"Fecha: {fecha}")
                    print(f"  Efectivo: {valores['EFECTIVO']}")
                    print(f"  Tarjeta: {valores['TARJETA']}")
                    print(f"  Total: {total}")
            else:
                print("No hay viaje activo para esa fecha.")

        elif opcion == "4":
            fecha_consulta = datetime.strptime(input("Fecha (YYYY-MM-DD) para buscar viaje activo: "), "%Y-%m-%d").date()
            viaje = control.obtener_viaje(fecha_consulta)
            if viaje:
                resumen = control.mostrar_gastos_por_tipo(viaje)
                for tipo, valores in resumen.items():
                    total = valores["EFECTIVO"] + valores["TARJETA"]
                    print(f"Tipo de gasto: {tipo.name}")
                    print(f"  Efectivo: {valores['EFECTIVO']}")
                    print(f"  Tarjeta: {valores['TARJETA']}")
                    print(f"  Total: {total}")
            else:
                print("No hay viaje activo para esa fecha.")

        elif opcion == "5":
            print("Saliendo...")
            break

        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main()
