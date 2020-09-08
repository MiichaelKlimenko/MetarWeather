#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# coding: utf8
import cgi
import mysql.connector

Sharacter = {}
Sairport = {}
mydb = mysql.connector.connect(
    host="",       #here is your host
    user="",       #here is your name
    passwd="",     #here is your password
    database="")   #here is your DB name
mycursor = mydb.cursor()
mycursor.execute('SET NAMES UTF8;')
sql = "select id,name from params order by id;"
mycursor.execute(sql)
rows = mycursor.fetchall()
for row in rows:
    Sharacter[row[0]] = row[1]
sql = "select id,airport,city from airports order by airport;"     #sql request to get all airports and cities
mycursor.execute(sql)
rows = mycursor.fetchall()
for row in rows:
    Sairport[row[0]] = row[1] + " (" + row[2] + ")"

Sdata = {1: "day", 2: "week", 3: "month", 4: "year"}
Sdatarus = {1: "Сутки", 2: "Неделя", 3: "Месяц", 4: "Год"}
form = cgi.FieldStorage()
text1 = form.getfirst("spisok", "1")
text2 = form.getfirst("spisok_airport", "1")
text3 = form.getfirst("spisok_data", "1")
time = "1 " + str(Sdata[int(text3)])
sql = "select date_format(CONVERT_TZ(date,'+00:00','+03:00'),'%b %d %H:%i'), value from measur where date between now()- interval " + time + " AND now() AND " \
                                                                                                                                             "param_id = '" + str(
    text1) + "' AND id_airport = '" + str(text2) + "' order by date;"
znachenie = "['Дата и время', 'Значение']"
mycursor.execute(sql)
rows = mycursor.fetchall()
for row in rows:
    znachenie += ",['" + str(row[0]) + "'," + str(row[1]) + "]"
golova = """
<html>
<head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    <title>Погода!</title>

    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable([""" + str(znachenie) + """ ]);

        var options = {
          title: 'График',
          curveType: 'function',
          legend: { position: 'bottom' }

        };

        var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

        chart.draw(data, options);
      }
    </script>

</head>"""

telo = """
<body background="image.jpg">

    <style type="text/css">
   h1 {.
    font-size: 200%;.
    font-family: Helvetica;.
   }
  </style>

<center><h1>""" + Sharacter[int(text1)] + " в " + Sairport[int(text2)] + "</h1></center>" + """

<form>

    <select name="spisok" >"""

for val in Sharacter:
    sel = ""
    if (int(text1) == val): sel = "selected"
    telo += "<option value='" + str(val) + "' " + sel + ">" + str(Sharacter[val]) + "</option>"
telo += """
    </select>
    <select name="spisok_airport" >"""
for val in Sairport:
    sel = ""
    if (int(text2) == val): sel = "selected"
    telo += "<option value='" + str(val) + "' " + sel + ">" + Sairport[val] + "</option>"
telo += """
    </select>
    <select name="spisok_data" > """
for val in Sdatarus:
    sel = ""
    if (int(text3) == val): sel = "selected"
    telo += "<option value='" + str(val) + "' " + sel + ">" + Sdatarus[val] + "</option>"

telo += """
    </select>

    <input name="button" type="submit" value="Вывести график" />

</form>

<hr />
<p>&nbsp;</p>"""

print("Content-type: text/html")
print()
print(golova + telo)
print("<div id=\"curve_chart\" style=\"  padding: 10px; width: 70%; height: 70%\"></div>")
print("</body></html>")

