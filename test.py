import geopy
from geopy.distance import geodesic
from unittest import result
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import time
import pandas as pd
from urllib.request import urlopen
import urllib

tiempo = datetime.today().strftime('%Y/%m/%Y%m%d')

e = urllib.request.urlopen(f"http://www.sismologia.cl/sismicidad/catalogo/{tiempo}.html").read()
# e = urllib.request.urlopen("http://www.sismologia.cl/sismicidad/catalogo/2022/05/20220505.html").read()
soup = BeautifulSoup(e, 'html.parser')


      # Obtenemos la tabla

tabla_sismos = soup.find('table', attrs={'class':'sismologia detalle'})

# Obtenemos todas las filass
rows = tabla_sismos.find_all('tr')

delimiter = ","                          # unambiguous string
for line_break in soup.findAll('br'):       # loop through line break tags
    line_break.replaceWith(delimiter)       # replace br tags with delimiter
strings = soup.get_text().split(delimiter)  # get list of strings

output_rows = []
for row in rows:
        # obtenemos todas las columns
    cells = row.find_all("td")
    output_row = []
    if len(cells) > 0:
        for cell in cells:
            output_row.append(cell.get_text())
            output_rows.append(output_row)

dataset = pd.DataFrame(output_rows).drop_duplicates()


dataset.columns = [
        "Fecha Local / Lugar",
        "Fecha UTC",
        "Latitud / Longitud",
        "Profundidad",
        "Magnitud (2)",
    ]


dataset[["Fecha Local", "Lugar"]] = dataset["Fecha Local / Lugar"].str.split(r",", expand=True)

dataset[["Latitud", "Longitud"]] = dataset["Latitud / Longitud"].str.split(r",", expand=True)



dataset = dataset.reindex(columns=['Fecha Local','Fecha UTC','Latitud','Longitud','Profundidad','Magnitud (2)','Lugar'])

tranque = (-24.39,-69.14)

latitud1 = dataset['Latitud'].values[0]
longitud1 = dataset['Longitud'].values[0]
profundidad = dataset['Profundidad'].values[0]
magnitud = dataset['Magnitud (2)'].values[0]
magnitud2 = magnitud.split(' ')
magnitud3 = float(magnitud2[0])
magnitud4 = magnitud2[1]
delhi = (latitud1, longitud1)
distancia = int(round((geodesic(tranque, delhi).km)))



def bot_send_text(bot_message):
    
    bot_token = '5231406261:AAE1lr7A9feeiv9Ejt3awEyigwzpxtyoqRo'  #'5242107370:AAGiBaDihZbdphDhybneHT0pU_4bJGDVWkk' <mel
    bot_chatID = '-796627951'     #-713984361' <mel
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


def sismo_scraping():  
    string="A ocurrido un sismo en las cercanías del Tranque Laguna Seca" "\n""\n" "*Datos del sismo:*" "\n" #titulo con salto de linea
    
    for column in dataset.head(1).columns:
        string += column +  " : " + str(dataset[column].values[0]) + "\n"
          
    return string

def distancias():       
    string2="El sismo se registro a una *DISTANCIA* de  "  f'{str(distancia)}' "Km del Tranque Laguna seca, y una *MAGNITUD* de " f'{str(magnitud3)}' "" f'{str(magnitud4)}'
    return string2

        
def main():
    Ultimo_simos= None
    while True:
        text = f'{sismo_scraping()}'
        text2 = f'{distancias()}'
        if text != Ultimo_simos:
            bot_send_text(text)
            Ultimo_simos = text
            bot_send_text(text2)
            # bot_send_text(text3)
        time.sleep(5) 

if __name__ == '__main__':

    main()
