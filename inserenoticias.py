import mysql.connector
from bs4 import BeautifulSoup
import requests
from datetime import date, datetime


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="robor2"
)


headers = requests.utils.default_headers()
headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'})

data = requests.get('http://br.investing.com/economic-calendar/', headers=headers)

resultados = []
mycursor = mydb.cursor()

sql = "DELETE FROM noticias;"
       
mycursor.execute(sql)

mydb.commit()

if data.status_code == requests.codes.ok:
	info = BeautifulSoup(data.text, 'html.parser')
	
	blocos = ((info.find('table', {'id': 'economicCalendarData'})).find('tbody')).findAll('tr', {'class': 'js-event-item'})
	
	for blocos2 in blocos:

                
            
		impacto = str((blocos2.find('td', {'class': 'sentiment'})).get('data-img_key')).replace('bull', '')
		horario = str(blocos2.get('data-event-datetime')).replace('/', '-')
		moeda = (blocos2.find('td', {'class': 'left flagCur noWrap'})).text.strip()
		nome = (blocos2.find('td', {'class': 'left event'})).text.strip()
		horario = horario [11:16]
		nome = nome [0:19] 


		resultados.append({'par': moeda, 'horario': horario, 'impacto': impacto,'nome': nome})

for info in resultados:
        mycursor = mydb.cursor()

        sql = "INSERT INTO noticias (hora, nome, par, touros) VALUES (%s, %s, %s, %s)"
        val = (info['horario'], info['nome'],  info['par'], info['impacto'])
        mycursor.execute(sql, val)

        mydb.commit()

        print(mycursor.rowcount, "record inserted.")
#print(resultados)






