from openpyxl import load_workbook
from scipy.interpolate import interp1d
import numpy as np
import sys
import pandas as pd

import imp
from scipy.interpolate import interp1d
import numpy as np
from weather.models import UsedFiles
import sqlite3
from django.utils.text import slugify


def get_all_interpolated_data(sheet, **kwars):

    temperature = [round(float(elem), 2)
                   for elem in pd.Series([elem.value
                                          if elem else np.nan for elem in sheet["C"][1:]]).
                   interpolate(**kwars)]

    wind_speed = [round(float(elem), 2)
                  for elem in pd.Series([elem.value
                                         for elem in sheet["E"][1:]]).
                  interpolate(**kwars)]

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
        None: None
    }

    storage_2 = {9: "Північний", 5: 'Північно-Західний', 1: "Західний", 2:
                 'Південно-Західний', 3: "Південний", 6: 'Південно-Східний', 7: "Східний",
                 8: 'Північно-Східний', 4: "Змінний", "None": "None"}

    wind = [elem
            for elem in pd.Series([storage[elem.value]
                                   for elem in sheet["D"][1:]]).
            interpolate(**kwars)]

    a = []
    for i in wind:
        try:
            int(i)
        except:
            i = 0
        if i < 1:
            a.append(1)
        elif i >= 9:
            a.append(8)
        else:
            a.append(i)
    wind_list = [storage_2[round(x)] for x in a]

    return temperature, wind_list, wind_speed
