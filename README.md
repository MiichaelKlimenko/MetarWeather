# MetarWeather
This program was made in 2019. It is weather service that gets forecast from METeorological Aerodrome Report
I do use Mysql database and two scripts: parser.py and weather.py

First of all about parser.py
This script gets data from METAR forecast and puts it to the MySQL database.
Also I put this script to cron so it commits every 15 minutes.

Talking about weather.py, it takes data from MySQL and puts it in html webpage
using google's opensource graph.

That's all, just simple forecast, but very first experience with databases :)
