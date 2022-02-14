import imp
from scipy.interpolate import interp1d
import numpy as np
from weather.models import UsedFiles
import sqlite3
from django.utils.text import slugify


def add_data_to_used_files_table(filename):
    UsedFiles.objects.update_or_create(name=filename, slug=slugify(filename))


def get_day(sheet):
    return [elem.value for elem in sheet["A"][1:]]


def get_time(sheet):
    return [elem.value.strftime("%H") + elem.value.strftime("%M") for elem in sheet["B"][1:]]


def get_cloud_interpolated_data(sheet):
    cloud_number = np.array(
        [elem.value if elem.value else np.nan for elem in sheet["N"][1: sheet.max_row]]
    )
    not_nan = np.logical_not(np.isnan(cloud_number))
    indices = np.arange(len(cloud_number))
    interp = interp1d(indices[not_nan],
                      cloud_number[not_nan], fill_value="extrapolate")
    return [float(elem) for elem in interp(indices)]


def get_wind_interpolated_data(sheet):

    storage = {
        "Западный": 1,
        "Ю-З": 2,
        "Южный": 3,
        "Переменный": 4,
        "С-З": 5,
        "Ю-В": 6,
        "Восточный": 7,
        "С-В": 8,
        "Северный": 9,
        "without": None
    }

    storage_2 = {val: key for key, val in storage.items()}

    wind = np.array(
        [
            storage[elem.value] if elem.value else np.nan
            for elem in sheet["D"][1: sheet.max_row]
        ]
    )
    not_nan = np.logical_not(np.isnan(wind))
    indices = np.arange(len(wind))
    interp = interp1d(indices[not_nan], wind[not_nan],
                      fill_value="extrapolate")
    return [storage_2.get(int(round(elem))) if storage_2.get(int(round(elem))) else storage_2[None] for elem in interp(indices)]


def get_wind_speed_interpolated_data(sheet):
    temp = np.array(
        [elem.value if elem else np.nan for elem in sheet["E"][1: sheet.max_row]]
    )

    not_nan = np.logical_not(np.isnan(temp))
    indices = np.arange(len(temp))
    interp = interp1d(indices[not_nan], temp[not_nan],
                      fill_value="extrapolate")

    # interp(indices)
    return [round(elem, 2) for elem in interp(indices)]


def get_weather_interpolated_data(sheet):
    storage = {
        "SN": 1,
        "SNRA": 2,
        "BR+SHRA": 3,
        "SHRA": 4,
        "BR+DZ": 5,
        "BR": 6,
        "RA": 7,
        "SHSN": 8,
        "BR+SNRA": 9,
        "FG+SNRA": 10,
        "BR+SHSN": 11,
        "BR+SN": 12,
        "FZ+SN": 13,
        "FG": 14,
        "BL+SHSN": 15,
        "FZ": 16,
        "BR+RA": 17,
        "FG+RA": 18,
        "DZ+FG": 19,
        "DZ": 20,
        "SHRA+TS": 21,
        "RA+TS": 22,
        "TS": 23,
        "BL+SN": 24,
        "BR+FZ": 26
    }

    storage_2 = {val: key for key, val in storage.items()}

    weather = np.array(
        [
            storage[elem.value] if elem.value else np.nan
            for elem in sheet["F"][1: sheet.max_row]
        ]
    )

    not_nan = np.logical_not(np.isnan(weather))
    indices = np.arange(len(weather))
    interp = interp1d(indices[not_nan],
                      weather[not_nan], fill_value="extrapolate")
    return [storage_2.get(int(round(elem))) if storage_2.get(int(round(elem))) else storage_2[23] for elem in interp(indices)]


def get_temperature_interpolated_data(sheet):
    temp = np.array(
        [elem.value if elem else np.nan for elem in sheet["C"][1: sheet.max_row]]
    )

    not_nan = np.array([bool(elem) for elem in temp])
    indices = np.arange(len(temp))
    interp = interp1d(indices[not_nan], temp[not_nan],
                      fill_value="extrapolate")

    # interp(indices)
    return [round(float(elem), 2) for elem in interp(indices)]


def create_database(filename):
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()

    try:
        cur.execute(f'''CREATE TABLE {filename}
			   (day NUMERIC, time varchar, temperature NUMERIC,
			   wind_direction varchar, wind_speed NUMERIC,
			   weather_kod varchar, cloud_number NUMERIC)''')

        # Save (commit) the changes
    except Exception as ex:
        pass

    con.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    con.close()


def check_if_table_exists(cursor, filename):

    # if the count is 1, then table exists
    try:
        cursor.execute(f''' SELECT * FROM {filename} ''')
        if cursor.fetchone()[0] == 1:
            return True
    except Exception:
        return False


def insert_data(filename, sheet, days, times, temperaturas, wind_directions, wind_speeds, weather_kods, cloudss):

    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    if not check_if_table_exists(cursor=cur, filename=filename):
        create_database(filename)
        add_data_to_used_files_table(filename=filename)
    else:
        cur.execute(f"""DELETE from {filename} """)

    try:
        for i in range(sheet.max_row-1):
            cur.execute(
                    f"""INSERT INTO {filename} VALUES ({days[i]},{times[i]},{temperaturas[i]},
				'{wind_directions[i]}', {wind_speeds[i]}, '{weather_kods[i]}', {cloudss[i]})""")
            con.commit()
    except Exception as ex:
        print(ex)

        return {"result": ex}

    return {"result": "done"}
