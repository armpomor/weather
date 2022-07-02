import requests
from datetime import timedelta, datetime
import sqlite3 as sq

from config import *


class Request_weather:
    def __init__(self, lat=40.18316726007202, lon=44.505733238299776, appid = None, lang = 'ru', units = 'metric'):
        self.lat = lat
        self.lon = lon
        self.appid = appid
        self.lang = lang 
        self.units = units
        self.params = {'lat': self.lat, 'lon': self.lon, 'appid': self.appid, 'lang': self.lang, 'units': self.units}
        self.request_weather()
        self.city = self.weather_now.json()['name']
        self.temp_cur = self.weather_now.json()['main']['temp']
        self.temp_sens = self.weather_now.json()['main']['feels_like']
        self.description = self.weather_now.json()['weather'][0]['description']
        self.cloudiness = self.weather_now.json()['clouds']['all']
        self.long_day = self.longitude_day(self.weather_now.json()['sys']['sunset'], 
                                           self.weather_now.json()['sys']['sunrise'])
        self.pressure = self.weather_now.json()['main']['pressure']
        self.humidity = self.weather_now.json()['main']['humidity']
        self.wind_speed = self.weather_now.json()['wind']['speed']
        self.wind_direct = self.weather_now.json()['wind']['deg']
        self.population = self.weather_forecast.json()['city']['population']
        
    def longitude_day(self, sunset: int, sunrise: int):
        """
        Долгота дня
        """
        daylight_hours = timedelta(seconds=(sunset - sunrise))
        t = datetime.strptime(str(daylight_hours), '%H:%M:%S')
        return t.hour, t.minute
    
    def request_weather (self):
        """
        Запрос прогноза погоды и погоды сейчас
        """
        self.weather_now = requests.get('https://api.openweathermap.org/data/2.5/weather', params=self.params)
        self.weather_forecast = requests.get('https://api.openweathermap.org/data/2.5/forecast', params=self.params)
        return self.weather_now.json(), self.weather_forecast.json()
    
    def basic_data_output(self):
        """
        Вывод стандартных данных о погоде
        """
        print(f'Температура - {self.temp_cur} градусов С')
        print(f'Ощущается как {self.temp_sens} градусов С')
        print(self.description)
        print(f'Облачность {self.cloudiness} %')
        print(f'Давление - {self.pressure} мм рт. ст.')
        print(f'Влажность - {self.humidity}%')
        print(f'Скорость ветра {self.wind_speed} м/c')
        print(f'Направление ветра {DIRECTION_WIND[self.wind_direct]} или {self.wind_direct} градусов')
        
    def write_db(self):
        """
        Записываем полученные данные в базу данных
        """
        with sq.connect(f'weather_{self.city}.db') as con:
            cur = con.cursor()

            # cur.execute('DROP TABLE IF EXISTS weather')
            cur.execute(f"""CREATE TABLE IF NOT EXISTS weather(
                           data_now TEXT,
                           temp_cur REAL,
                           temp_sens REAL,
                           description TEXT,
                           cloudiness TEXT,
                           pressure TEXT,
                           humidity TEXT,
                           wind_speed TEXT,
                           wind_direct TEXT,
                           long_day TEXT)""")
            cur.execute("INSERT INTO weather VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                        (f'{datetime.now().year} год {datetime.now().day} {MONTHS[datetime.now().month]} '+
                            f'{datetime.now().hour} часов', 
                         self.temp_cur, self.temp_sens, self.description, f'{self.cloudiness}%', 
                         f'{self.pressure} мм рт ст', f'{self.humidity}%', f'{self.wind_speed} м/c', 
                         DIRECTION_WIND[self.wind_direct], f'{self.long_day[0]} часов {self.long_day[1]} минут'))
    
    def output_weather_now(self):  
        print(f'Город - {self.city}')
        print(f'{datetime.now().year} год {datetime.now().day} {MONTHS[datetime.now().month]} '+
                f'{datetime.now().hour} час {datetime.now().minute} минут')
        self.basic_data_output()
        print(f'Долгота дня {self.long_day[0]} часов и {self.long_day[1]} минут')
        
    def output_weather_forecast(self):
        daily_forecasts = self.weather_forecast.json()['list']
        print()
        print(f'Город {self.city}')
        print(f'Население {self.population} человек')
        print()
        for i in daily_forecasts:
            print(i['dt_txt'])
            self.basic_data_output()
            print(f"Вероятность осадков {i['pop'] * 100} %")
            print()



if __name__ == '__main__':
    weather = Request_weather(appid=None)  # Здесь должен быть твой API
    weather.output_weather_now()
    weather.output_weather_forecast()
    weather.write_db()
   

