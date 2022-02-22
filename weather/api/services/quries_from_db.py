import sqlite3

"select day, max(temperature) as maxx, min(temperature) as minn  from april2012 GROUP BY day"
# get max and min temperatue for per day

"select day, max(wind_speed) as maxx, min(wind_speed) as minn  from april2012 GROUP BY day"
# get max and min wind speed for per day

"""select * from january2012 where day = (select day
from january2012 GROUP by day ORDER by max(temperature) - min(temperature) DESC limit 1)"""
# get day  with biggest difference between max and min temperature

"""select * from january2012 where day = (select day
from january2012 GROUP by day ORDER by max(wind_speed) - min(wind_speed) DESC limit 1)"""
# get day  with biggest difference between max and min wind speed

"""select * from january2012 
where day = (select day from january2012 GROUP by day ORDER by avg(temperature) limit 1)"""
# get day with minimal temperature

"""select * from january2012 
where day = (select day from january2012 GROUP by day ORDER by avg(temperature) DESC limit 1)"""
# get day with maximal temperature


"""select * from january2012 
where day = (select day from january2012 GROUP by day ORDER by avg(wind_speed) limit 1)"""
# get day with minimal wind speed

"""select * from january2012 
where day = (select day from january2012 GROUP by day ORDER by avg(wind_speed) DESC limit 1)
"""
# get day with maximal wind speed

"""SELECT * from january2012 where 
day = (select day  from january2012 where wind_direction="Західний" 
GROUP by day ORDER by Count(wind_direction) DESC limit 1)"""
# get day where wind is mostly "Західний"


def query_to_json(query: tuple):
    return {
        "id": query[0],
        "day": query[1],
        "time": query[2],
        "temperature": query[3],
        "wind_direction": query[4],
        "wind_speed": query[5],
    }


def query_day_max_min_to_json(query: tuple):
    return {
        "id": query[0],
        "day": query[1],
        "max": query[2],
        "min": query[3]
    }


def connect_to_db():
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    return con, cur


def get_all_query_by_table(table_name: str):
    """get all data from specific table"""

    con, cur = connect_to_db()
    cur.execute(
        f"""select * from {table_name}""")

    con.commit()

    return [query_to_json(elem) for elem in cur.fetchall()]


def get_day_with_max_diff_temperature(table_name: str):
    """get day with biggest difference between max and min temperature"""

    con, cur = connect_to_db()
    cur.execute(
        f"""select * from {table_name} where day = (select day
            from {table_name} GROUP by day ORDER by max(temperature) - min(temperature) DESC limit 1)""")

    con.commit()

    return [query_to_json(elem) for elem in cur.fetchall()]


def get_day_with_max_diff_wind_speed(table_name: str):
    """get day with biggest difference between max and min wind speed"""

    con, cur = connect_to_db()
    cur.execute(
        f"""select * from {table_name} where day = (select day
            from {table_name} GROUP by day ORDER by max(wind_speed) - min(wind_speed) DESC limit 1)""")

    con.commit()

    return [query_to_json(elem) for elem in cur.fetchall()]


def get_day_with_some_temperature(table_name: str, slug):
    """get day with max or min average temperature"""

    con, cur = connect_to_db()
    if slug == "min":
        cur.execute(
            f"""select * from {table_name} 
                where day = (select day from {table_name} GROUP by day ORDER by avg(temperature) limit 1)""")
    else:
        cur.execute(
            f"""select * from {table_name} 
                where day = (select day from {table_name} GROUP by day ORDER by avg(temperature) DESC limit 1)""")
    con.commit()

    return [query_to_json(elem) for elem in cur.fetchall()]


def get_day_with_some_wind(table_name: str, slug):
    """get day with max or min average wind speed"""

    con, cur = connect_to_db()
    if slug == "min":
        cur.execute(
            f"""select * from {table_name} 
                where day = (select day from {table_name} GROUP by day ORDER by avg(wind_speed) limit 1)""")
    else:
        cur.execute(
            f"""select * from {table_name} 
                where day = (select day from {table_name} GROUP by day ORDER by avg(wind_speed) DESC limit 1)""")
    con.commit()

    return [query_to_json(elem) for elem in cur.fetchall()]


def get_day_with_some_wind_direction(table_name: str, wind_direction):
    """get day with most specific some wind direction"""

    con, cur = connect_to_db()

    cur.execute(
        f"""SELECT * from {table_name} where 
            day = (select day  from {table_name} where wind_direction='{wind_direction}' 
            GROUP by day ORDER by Count(wind_direction) DESC limit 1)""")
    con.commit()

    return [query_to_json(elem) for elem in cur.fetchall()]
