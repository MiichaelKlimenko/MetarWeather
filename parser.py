#!/usr/bin/env python3
# coding: utf8
import mysql.connector
from bs4 import BeautifulSoup
import requests
import datetime
from metar import Metar

BeautifulSoup.features = "html.parser"
basicH = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}

mydb = mysql.connector.connect(     #here is your hostname, username, password and database name
  host="",
  user="",
  passwd="",
  database=""
)

params = {'temp':'1', }

def isfloat(element):
    import re
    if re.match(r'^-?\d+(?:\.\d+)?$', element) is None: return False
    else: return True


def Parse(id_airport,airport):
    UrlA = 'https://tgftp.nws.noaa.gov/data/observations/metar/stations/' + airport + '.TXT'
    session1 = requests.Session()
    requestA = session1.get(UrlA, headers=basicH)
    getmetar = str(requestA.text)[int(str(requestA.text).find(':')+4):]
    #print(getmetar)
    obs = Metar.Metar(getmetar)
    temp = str(obs.temp).replace(' C','')
    wind_speed = str(obs.wind_speed).replace(' mps','')
    wind_dir = str(obs.wind_dir).replace(' degrees','')
    vis = str(obs.vis).replace('less than ','').replace('greater than ','').replace(' meters','')
    press = str(obs.press).replace(' mb','')
    date = str(obs.time)


    if check(id_airport, date):

        if (isfloat(temp)): mycursor.execute("INSERT INTO measur (param_id, id_airport, date, value) VALUES ('" + GetParamId('Температура')
                         + "','" + id_airport + "', '" + date + "', '" + temp + "');")
        if (isfloat(wind_speed)): mycursor.execute("INSERT INTO measur (param_id, id_airport, date, value) VALUES ('" + GetParamId('Скорость ветра')
                         + "','" + id_airport + "', '" + date + "', '" + wind_speed + "');")
        if (isfloat(wind_dir)): mycursor.execute("INSERT INTO measur (param_id, id_airport, date, value) VALUES ('" + GetParamId('Направление ветра')
                         + "','" + id_airport + "', '" + date + "', '" + wind_dir + "');")
        if (isfloat(vis)): mycursor.execute("INSERT INTO measur (param_id, id_airport, date, value) VALUES ('" + GetParamId('Горизонтальная видимость')
                         + "','" + id_airport + "', '" + date + "', '" + vis + "');")
        if (isfloat(press)): mycursor.execute("INSERT INTO measur (param_id, id_airport, date, value) VALUES ('" + GetParamId('Давление')
                         + "','" + id_airport + "', '" + date + "', '" + press + "');")
        mydb.commit()


def GetParamId(param_name):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id FROM params WHERE name = '" + str(param_name) + "';")
    rows = mycursor.fetchall()
    #print(mycursor.rowcount)
    if mycursor.rowcount > 0:
        return str(rows[0][0])
    else: return False


def check(id_airport,date):
    mycursor = mydb.cursor(buffered=True)
    sql = "SELECT * FROM measur WHERE id_airport ='" + id_airport + "' AND date ='" + date + "';"
    #print(sql)
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    if mycursor.rowcount > 0: return False
    else: return True



mycursor = mydb.cursor()
mycursor.execute("SELECT id, icao FROM airports;")
rows = mycursor.fetchall()
for row in rows:
    #print(str(row[1]) + '\n')
    Parse(str(row[0]), str(row[1]))
