# Направления ветра
NORD = dict(zip(range(0, 6), ['Cевер'] * 100))
NORD_EST = dict(zip(range(6, 86), ['Cеверо-Bосток'] * 100))
EST = dict(zip(range(86, 96), ['Bосток'] * 100))
EST_SUD = dict(zip(range(96, 176), ['Юго-Bосток'] * 100))
SUD = dict(zip(range(176, 186), ['Юг'] * 100))
SUD_OVEST = dict(zip(range(186, 266), ['Юго-Запад'] * 100))
OVEST = dict(zip(range(266, 276), ['Запад'] * 100))
NORD_OVEST = dict(zip(range(276, 360), ['Cеверо-Запад'] * 100))

DIRECTION_WIND = NORD|NORD_EST|EST|EST_SUD|SUD|SUD_OVEST|OVEST|NORD_OVEST

# Месяца 
MONTHS = [0, 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 
          'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']