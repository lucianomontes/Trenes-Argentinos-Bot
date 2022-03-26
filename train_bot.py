from importlib.resources import contents
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from datetime import date

# Tiempo
import schedule
import time

from telegram_bot import TelegramBot

BOT_ID = "TU BOT ID" # Bot chat
BOT_ID_GRUPO = "BOT ID GRUPO" # Grupo Trenes Argentinos
BOT_TOKEN = "TU BOT TOKEN"

DIA_SEMANA = ["LUN", "MAR", "MIE", "JUE", "VIE", "SAB", "DOM"]
MES_BUSQUEDA = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"]

ESTACIONES = ['Alberdi', 'Alem', 'Alta Córdoba', 'Argüello', 'Arroyo Seco', 'Azul', 'Bahía Blanca', 'Baradero', 'Batalla de Salta', 'Bell Ville', 'Betania', 'Bialet Massé', 'Bragado', 'Buenos Aires', 'Cacharí', 'Campana', 'Campo Quijano', 'Cañada de Gómez', 'Casa Bamba', 'Casa Grande', 'Cassaffousth', 'Castelli', 'Castilla', 'Ceres', 'Cevil Pozo (Tuc)', 'Chacabuco', 'Chascomús', 'Chivilcoy', 'Cnel. Brandsen', 'Cnel. Suárez', 'Cnel. Vidal', 'Colonia Dora', 'Combate de Rosario de Lerma', 'Córdoba', 'Córdoba (TDS)', 'Correa', 'Cosquín', 'Div. Pinamar', 'Dolores', 'Dumesnill', 'El Bordo', 'Empalme Villa Constitución', 'Franklin', 'Gálvez', 'Gral. Guido', 'Gral. Lamadrid', 'Gral. Madariaga', 'Gral. Pirán', 'GÜEMES', 'Hospital Neonatal', 'Iriarte', 'James Craik', 'Jose C Paz', 'Junín', 'La Banda', 'La Calera', 'Laguna Larga', 'Las Armas', 'Las Flores', 'La Tablada', 'Leones', 'Lezama', 'Lima', 'Luján', 'Maipú', 'Manfredi', 'Marcos Juarez', 'Mar del Plata', 'Mechita', 'Mercedes', 'Mercedes P', 'Monte', 'Narvaja', "O'Higgins", 'Olavarría', 'Oliva', 'Oncativo', 'Pacto de los Cerrillos', 'Pigüé', 'Pilar', 'Pilar (Córdoba)', 'Pinto', 'Rafaela', 'Ramallo', 'Rawson', 'Río Segundo', 'Rivas', 'Rod. del Busto', 'Rosario Norte', 'Rosario Sur', 'Rufino', 'Saavedra', 'Saenz Peña', 'Salta', 'San Nicolás', 'San Pedro', 'San Roque', 
'Santa María', 'Serodino', 'Sevigne', 'Sto. Domingo', 'Suipacha', 'Sunchales', 'Tio Pujio', 'Toledo', 'Tornquist', 'Vaccarezza', 'Valle Hermoso', 'Vedia', 'Villa Maria', 'Vivoratá', 'Zarate']


from webdriver_manager.chrome import ChromeDriverManager

import time

def mostrar_destinos():

      print("Estaciones disponibles = \n")

      indice = 1
      for origen in ESTACIONES:
            print( str(indice) + ". " + origen, end="  /  ")
            if indice%4 == 0:
                  print("\n")
            indice+=1


def parsear_fecha(fecha):

      diaString = str(fecha.day)
      diaSemanaBusqueda = DIA_SEMANA[fecha.weekday()]
      mesBusqueda = MES_BUSQUEDA[fecha.month - 1]

      fechaBusqueda = diaSemanaBusqueda + " " + diaString + " " + mesBusqueda    # parseamos a formato buscado (ej: VIE 11 MAR)
      celdaDia = "cell" + diaString +  "-fecha_ida" # parseamos a id buscado (ej: cell11-fecha_ida)

      return fechaBusqueda, celdaDia

def procesar_mensaje(mensajeBotTelegram):

      # SI SE ENCONTRO PASAJES PARA EL DIA BUSCADO, EL BOT DE TELEGRAM ENVIARÁ UN MENSAJE DE ALERTA AL CHAT INDICADO POR BOT_ID_GRUPO

      print("MENSAJE TELEGRAM:")
      print(mensajeBotTelegram)
      if mensajeBotTelegram != "DIAS DISPONIBLES: \n" :
            return True
      else:
            print("No se encontraron pasajes para el dia buscado, mensaje no será enviado al bot telegram.")
            return False

def find_trickets(fecha, origen, destino, botTelegram, chat_id = None):

      #options = ChromeOptions()

      # PARSEO DE DATOS
      diaBuscadoParseado, diaCelda  = parsear_fecha(fecha)
      
      # INICIAMOS WEBDRIVER Y ABRIMOS LA PAGINA DE VENTA DE PASAJES.
      driver = webdriver.Chrome("driver/chromedriver")

      driver.get(f"https://webventas.sofse.gob.ar")

      time.sleep(1)
      

      # COMPLETAMOS INFORMACION DE BUSQUEDA

      try:

            #Seleccionamos origen y destino del viaje.
            origenContenedor = driver.find_element_by_id("origen-selectized")
            origenContenedor.send_keys(origen)
            origenContenedor.send_keys(Keys.ENTER)

            time.sleep(1)

            destinoContenedor = driver.find_element_by_id("destino-selectized")
            destinoContenedor.send_keys(Keys.DOWN)
            destinoContenedor.click()
            destinoContenedor.send_keys(destino)
            destinoContenedor.send_keys(Keys.ENTER)

            time.sleep(1)


            # Seleccionamos cantidad de adultos igual a uno.
            adulto = driver.find_element_by_id("adulto")
            adulto.click()
            adulto.send_keys(Keys.DOWN)
            adulto.send_keys(Keys.ENTER)
            
            time.sleep(1)
            
            # Seleccionamos dia del viaje en el calendario.
            # Si queremos buscar para el mes siguiente, avanzamos clickeando en siguienteMes
            fecha_dia = driver.find_element_by_css_selector('.datepicker-button[aria-labelledby="datepicker-bn-open-label-fecha_ida"]')
            fecha_dia.click()
            time.sleep(1)
            if (fecha.month != date.today().month):
                  siguienteMes = driver.find_element_by_css_selector('#datepicker-calendar-fecha_ida > div.datepicker-month-wrap > div.datepicker-month-next.pull-right.enabled > span')
                  siguienteMes.click()
            time.sleep(1)
            dia_exacto = driver.find_element_by_id(diaCelda)
            dia_exacto.click()

            time.sleep(1)

            # Hacemos click en el boton buscar pasajes.
            
            driver.find_element_by_xpath('//*[@id="form_busqueda"]/div/div[7]/div/button').click()
            
            time.sleep(1)

      # CHEQUEO DE PASAJES 

            # Obtenemos la nueva pagina y verificamos los datos.
            # Mostramos en pantalla los dias disponibles y no disponibles con sus respectivos asientos.
            content = driver.page_source
            soup = BeautifulSoup(content, features="html.parser")
                  
            try:      
                  dias_no_disponibles = soup.findAll('span', {'class':'dia_numero_no_disponible'})
                  print("DIAS NO DISPONIBLES:")
                  for dia_no_disponible in dias_no_disponibles:
                        if dia_no_disponible.string != None:
                              print(dia_no_disponible.string + " = " + "0 disponibles")

                  dias_disponibles = soup.findAll('span', {'class':'dia_numero'})
                  asientos_disponibles = soup.findAll('p', {'class':'m-0 cantidad'})
                  i = 0
                  mensajeBotTelegram = "DIAS DISPONIBLES: \n"
                  print("DIAS DISPONIBLES:")
                  for dia_disponible in dias_disponibles:
                        if dia_disponible.string != None:
                              disponible = dia_disponible.string + " = " + asientos_disponibles[i].string + " disponibles"
                              print(disponible)
                              i+=1

                              # Si hay pasajes para el dia buscado, lo agregamos a mensajeBotTelegram
                              if dia_disponible.string == diaBuscadoParseado:
                                    mensajeBotTelegram = mensajeBotTelegram + disponible + "\n"
            except:
                  print("soup except")

      except:
            print("NO ENCONTRO")

      # CERRAMOS WEB DRIVER
      driver.quit()
      
      # Procesamos y enviamos el mensaje al chat indicado.
      if (procesar_mensaje(mensajeBotTelegram)):
            botTelegram.send_message(mensajeBotTelegram, chat_id)
            print("Mensaje será enviado al bot telegram")
      
      return mensajeBotTelegram


def train_bot():


      # INICIALIZACION DE BOT_TELEGRAM
      botTelegram = TelegramBot(BOT_TOKEN, BOT_ID)

      #Validamos inputs de fecha, minutosRefrezco, origen y destino.

      validacion_fecha = False
      validacion_minutos = False
      validacion_origen = False
      validacion_destino = False
      today = date.today()


      # Pedimos fecha del viaje y validamos
      while validacion_fecha == False:
            try:
                  fecha = datetime.fromisoformat(input("Ingresa una fecha en el formato YYYY-MM-DD: "))
                  if( (float(fecha.month) - float(today.month)) <= 1):
                        print("Fecha válida")
                        validacion_fecha = True
                  else: 
                        print("Fecha inválida")
            except ValueError:
                  print("Fecha inválida")

      # Pedimos tiempo de refrezco en minutos y validamos
      while validacion_minutos == False:
            try:
                  minutosRefrezco = (float)(input("Ingresa un tiempo de refrezco en minutos: "))
                  if(minutosRefrezco > 0.5 and minutosRefrezco < 60):
                        validacion_minutos = True
                        print("Refrezco válido")
                        print("Refrezco cada: " + str(minutosRefrezco) + " minutos")
                  else: 
                        print("Refrezco inválido")
            except ValueError:
                  print("Refrezco inválido")

      # Pedimos origen del viaje y validamos
      while validacion_origen == False:
            mostrar_destinos()
            opcionOrigen = (int)(input("Seleccione opción de origen y presione ENTER: ") )      
            if opcionOrigen>0 and opcionOrigen < 113:
                  print("Origen válido")
                  validacion_origen = True
                  origen = ESTACIONES[opcionOrigen-1]
                  print("Usted seleccionó: " + origen)
            else: 
                  print("Origen no válido")

      # Pedimos destino del viaje y validamos
      while validacion_destino == False:
            #mostrar_destinos()
            print("Antes de seleccionar el destino segurece de que el recorrido exista!!")
            opcionDestino = (int)(input("Seleccione opción de destino y presione ENTER: "))       
            if opcionDestino>0 and opcionDestino < 113:
                  print("Destino válido")
                  validacion_destino = True
                  destino = ESTACIONES[opcionDestino-1]
                  print("Usted seleccionó: " + destino)
            else: 
                  print("Destino no válido")
      


      # Llamamos a find_trickets con los datos solicitados con la frecuencia pedida en minutos. 
      schedule.every(minutosRefrezco).minutes.do(find_trickets, fecha, origen, destino, botTelegram, BOT_ID_GRUPO)
      

      while 1:
            schedule.run_pending()
      time.sleep(2)

train_bot()
