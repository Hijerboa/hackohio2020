import psycopg2
import csv
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
def connect():
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
        
        # do things here

       
	    # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def temp_pop(pop_data):
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
        
        # do things here
        sql = 'INSERT INTO temp_pop VALUES(%s, %s, %s, %s);'
        first_row = True
        t_count = 0
        for row in pop_data:
            if not first_row:
                cur.execute(sql, (row[0], row[1], row[2], row[3],))
                t_count += 1
                print('row ' + str(t_count) + ' inserted.')
            first_row = False
        conn.commit()
        print('Inserted ' + str(t_count) + ' items successfully.')

	    # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def temp_pres(pres_data):
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
        
        # do things here
        sql = 'INSERT INTO temp_votes VALUES(%s, %s, %s, %s);'
        first_row = True
        for row in pres_data:
            if not first_row:
                cur.execute(sql, (row[0], row[1], row[2], row[4],))
                #t_count += 1
                #print('row ' + str(t_count) + ' inserted.')
            first_row = False
        conn.commit()
        print('Inserted ' + str(len(pres_data)) + ' items successfully.')

	    # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def temp_cov(covid_data):
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
        
        # do things here
        sql = 'INSERT INTO temp_corona VALUES(%s, %s, %s, %s);'
        first_row = True
        for row in covid_data:
            if not first_row:
                cur.execute(sql, (row[0], row[1], row[2], row[3],))
                #t_count += 1
                #print('row ' + str(t_count) + ' inserted.')
            first_row = False
        conn.commit()
        print('Inserted ' + str(len(pres_data)) + ' items successfully.')

	    # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def temp_state(abv_data):
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
        
        # do things here
        sql = 'INSERT INTO state_abv VALUES(%s, %s);'
        first_row = True
        for row in abv_data:
            if not first_row:
                cur.execute(sql, (row[0], row[1],))
                #t_count += 1
                #print('row ' + str(t_count) + ' inserted.')
            first_row = False
        conn.commit()
        print('Inserted ' + str(len(pres_data)) + ' items successfully.')

	    # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def temp_vpop(vpop_data):
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
        
        # do things here
        sql = 'INSERT INTO temp_vpop VALUES(%s, %s, %s);'
        first_row = True
        for row in vpop_data:
            if not first_row:
                cur.execute(sql, (row[0], row[1], row[2],))
                #t_count += 1
                #print('row ' + str(t_count) + ' inserted.')
            first_row = False
        conn.commit()
        print('Inserted ' + str(len(pres_data)) + ' items successfully.')

	    # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def insert_all_new_rows(covid_data, death_data):
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
        
        # do things here
        select_date_statement = 'select max(r.date) from daily_record r;'
        cur.execute(select_date_statement)
        most_recent_date = cur.fetchone()

        sql = 'INSERT INTO temp_vpop VALUES(%s, %s, %s);'
        first_row = True
        for row in vpop_data:
            if not first_row:
                cur.execute(sql, (row[0], row[1], row[2],))
                #t_count += 1
                #print('row ' + str(t_count) + ' inserted.')
            first_row = False
        conn.commit()
        print('Inserted ' + str(len(pres_data)) + ' items successfully.')

	    # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def insert_all_rows(covid_data, death_data):
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
        
        # Make a list of records we want to submit
        records = []


        # do things here
        sql = 'INSERT INTO daily_record(COUNTY_FIPS, DATE, TOTAL_CASES, TOTAL_DEATHS) VALUES(%s, %s, %s, %s);'
        ct = 0
        for y in range(1740, 1882):
            if not int(covid_data[y][0]) == 0:
                for x in range(4, len(covid_data[y])):
                    cur.execute(sql, (covid_data[y][0], covid_data[0][x], covid_data[y][x], death_data[y][x]))
                    ct += 1
                print('Data for ' + covid_data[y][1] + ' ' + covid_data[y][2] + ' (row ' + str(y) + ') inserted for all available dates') 
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
    pop_data = load_csv('../raw/covid_county_population_usafacts.csv')
    pres_data = load_csv('../raw/president_county_candidate.csv')
    covid_data = load_csv('../raw/covid_confirmed_usafacts.csv')
    death_data = load_csv('../raw/covid_deaths_usafacts.csv')
    state_data = load_csv('../raw/state_abv.csv')
    vpop_data = load_csv('../raw/president_county.csv')
    #temp_pres(pres_data)
    #temp_cov(covid_data)
    #temp_state(state_data)
    #temp_vpop(vpop_data)

    insert_all_rows(covid_data, death_data)
    #print(death_data)