#fuente para los diferentes widgets
fuente_wid = ('Tahoma',12, 'bold')
fuente_botones = ('Tahoma',8, 'bold')
fuente_promo = ('Tahoma',10, 'bold')
fuente_deudas = ('Helvetica Rounded LT Std', 14, 'bold')
fuente_deudas_title = ('Helvetica Rounded LT Std', 16, 'bold')

#errores en base de datos
MENSAJE_DB="ERROR AL CONECTAR A BASE DE DATOS"

#año que se muestran en la caja, combobox
lista_anio = [2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027,
              2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035, 2036,
              2037, 2038, 2039, 2040, 2041, 2042, 2042, 2043, 2044,
              2045, 2046, 2047, 2048, 2049, 2050
              ]
lista_mes = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
             "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

dias_fin_de_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

TEXTO_COMANDA = "Lote: %s\nManzana: %s\nCantidad de pedidos: %d"

PRECIO_TOTAL = "Precio total: $%d"

PRECIO_UNITARIO = "Precio unitario: $%d"
PRECIO_PROMOCION = u"Precio promoción:"


acompania = u"Acompaña al pedido\nNo se cobra"


AVISO_DATOS_PEDIDO = u"El pedido no se ha guardado.\nPara continuar debe guardar el pedido o pulsar el botón Cancelar."

TEXTO_FIADOS = "Pedidos Fiados - Cantidad: %d"
TEXTO_PAGADOS= "Pedidos Pagados - Cantidad: %d"
ESTADISTICA  = (u"Para mirar la estadistica de venta de un producto, "+
                "seleccione un producto\nLuego elija el rango en el que desea verlo y pulse Aceptar.\n"+
                "Nota: El rango siempre se elije sobre el mismo mes.")

INFO_SELECCION = (u"Para mirar los pedidos vendidos del día\n"+
                u"Seleccione un día pulsando la opción Selección Día.")

INFO_PROMO = (u"Cuando agregas una promoción, esta se mostrará según "+
              "el orden en el que se agrega. Ej:\n"+
              "Milanesa\nPapas fritas\n...\netc")

AVISO_CARGOENVIO = (u"El cliente ya realizo pedidos con cargo de envío\n"+
                    "Si quita el cargo de envío, esto se aplicara a todos los pedidos\n"+
                    "¿Desea continuar?")

AVISO_DESCUENTO = (u"El cliente ya realizo pedidos con descuento\n"+
                    "Si quita el descuento, esto se aplicara a todos los pedidos\n"+
                    "¿Desea continuar?")

ENVIO = u"Cargo de envío: $%d"
DESCUENTO= "Descuento: %d %%"
NOMBRE_CLIENTE = "CLiente:"

#colores de fondo para los pedidos
#y algunos frames 
BG_PEDIDOS = "#625F72"
BG_FRAMES = "#9C94B9"

#colores para mostrar las comandas en pedidos
BG_COMANDA_ENTREGA = "#86A5A2"
BG_COMANDA_DELIVERY="#8BCD8D"

#colores para la ventana mostrar pedido cliente
BG_PEDIDO_PED_PREPA = "#C5C2D1"

#colores para la funcion crear pedido
BG_BOTONES ="#606082"

#colores para deudas
BG_DEUDA_NOMBRES = '#000000'
FG_LABELS_DEUDA = 'black'
BG_BOTONES_DEUDA = '#7e6e86'
FG_BOTON_DEUDA = '#f1f1f1'

#mensajes cambiar de estado pedidos
MSJ_DESPACHADOS = "Todos los pedidos del cliente deben estar preparados para poder despacharlos"
MSJ_DELIVERY = "Todos los pedidos del cliente deben estar preparados para que el delivery los lleve"


