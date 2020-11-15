import psycopg2
import csv
import datetime
from config import config

# Loads the specified csv into memory
def load_csv(filename):
    res = []
    try:
        with open(filename, 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:  
                res.append(row)
    except:
        print('Failed to read ' + filename)
        return []
    finally:
        return res 

# Facilitates connection to server - Base
def run(cases, deaths):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
        # get most recent date in the db
        get_last_date_sql = 'select max(r.date) from daily_record r;'
        cur.execute(get_last_date_sql)
        last_date_db = cur.fetchone()
        print('Most recent entry in db is ' + str(last_date_db[0]))

        # get most recent date in the csv
        datestring = cases[0][-1].split('/')
        last_date_csv = datetime.date(int('20' + datestring[2]), int(datestring[0]), int(datestring[1]))
        print('Most recent entry in csv is ' + str(last_date_csv))

        # find diff.
        diff = int((last_date_csv - last_date_db[0]) / datetime.timedelta(days = 1))
        print(str(diff) + ' days between csv and db')
        if diff <= 0:
            print('No new updates, terminating')
        else:
            insert_sql = 'INSERT INTO daily_record(COUNTY_FIPS, DATE, TOTAL_CASES, TOTAL_DEATHS) VALUES(%s, %s, %s, %s);'
            ct = 0
            for y in range(1, len(cases)):
                if not int(cases[y][0]) == 0:
                    for x in range(len(cases[y]) - diff, len(cases[y])):
                        cur.execute(insert_sql, (cases[y][0], cases[0][x], cases[y][x], deaths[y][x]))
                        ct += 1
                    print('Data for ' + cases[y][1] + ' ' + cases[y][2] + ' (row ' + str(y) + ') inserted for all new dates') 
            conn.commit()
            print('Inserted ' + str(ct) + ' items successfully.')

	    # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

if __name__ == '__main__':
    cases = load_csv('../raw/covid_confirmed_usafacts.csv')
    deaths = load_csv('../raw/covid_deaths_usafacts.csv')
    run(cases, deaths)