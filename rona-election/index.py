import functools
import psycopg2.extras

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

from . import db


bp = Blueprint('index', __name__, url_prefix='/')
cache = dict()


@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@bp.route('/geodata', methods=['GET'])
def geodata():
    global cache
    method = request.args.get('method')
    print(f'+++ METHOD = {method} +++')

    if method in cache:
        return jsonify(cache[method])

    conn = db.get_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if method == 'countydata':
        query = (
            """
            SELECT ST_AsGeoJSON(t.*)
            FROM (SELECT * FROM tl_2019_us_county T WHERE T.statefp != '02' AND T.statefp != '09' AND T.statefp != '23' AND T.statefp != '33' AND T.statefp != '44' AND T.statefp != '50' AND T.statefp != '11')
            AS t(id, name, geom)
            """
        )
    elif method == 'statedata':
        query = (
            """
            SELECT ST_AsGeoJSON(t.*)
            FROM (SELECT * FROM tl_2019_us_state T WHERE T.statefp = '02' OR T.statefp = '09' OR T.statefp = '23' OR T.statefp = '33' OR T.statefp = '44' OR T.statefp = '50' OR T.statefp = '11')
            AS t(id, name, geom);
            """
        )
    elif method == 'countystatedata':
        query = (
            """
            SELECT ST_AsGeoJSON(t.*)
            FROM (SELECT * FROM tl_2019_us_state)
            AS t(id, name, geom);
            """
        )
    else:
        cursor.close()
        error = 'Error: Invalid method specified!, Try one of {countydata, statedata, countystatedata}!'
        return jsonify({'err': error})
    
    try:
        cursor.execute(query)
        records = cursor.fetchall()
        cache[method] = records
        cursor.close()
        return jsonify(records)
    except BaseException:
        error = 'Error: An unexpected error occurred, try again later!'
        return jsonify({'err': error})


@bp.route('/coviddata', methods=['GET'])
def coviddata():
    method = request.args.get('method')
    granularity = request.args.get('granularity')
    
    if method is None or granularity is None:
        error = ''
        return jsonify({'err': error})

    conn = db.get_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if method == 'casesatdate':
        if granularity == 'county':
            query = (
                '''
                (select county_fips, total_cases 
                    from daily_record 
                    where date in (
                        select max(r.date) 
                        from daily_record r
                    )
                )
                union
                (select state_fips, total_cases 
                    from state_record 
                    where date in (
                        select max(r.date) from daily_record r
                    )
                );
                '''
            )
        elif granularity == 'state':
            query = (
                '''
                (select d.state_fips, sum(r.total_cases) 
                    from daily_record r, county_data d 
                    where r.county_fips = d.FIPS and r.date in (
                        select max(r.date) 
                        from daily_record r
                    ) group by d.STATE_FIPS
                )
                union
                (select r.state_fips, r.total_cases 
                    from state_record r 
                    where r.date in (
                        select max(r.date) 
                        from daily_record r
                    )
                );
                '''
            )
        else:
            cursor.close()
            error = ''
            return jsonify({'err': error})
    elif method == 'deathsatdate':
        if granularity == 'county':
            query = (
                '''
                (select county_fips, total_deaths 
                    from daily_record 
                    where date in (
                        select max(r.date) from daily_record r
                    )
                )
                union
                (select state_fips, total_deaths 
                    from state_record 
                    where date in (
                        select max(r.date) from daily_record r
                    )
                );
                '''
            )
        elif granularity == 'state':
            query = (
                '''
                (select d.state_fips, sum(r.total_deaths) 
                    from daily_record r, county_data d 
                    where r.county_fips = d.FIPS and r.date in (
                        select max(r.date) from daily_record r
                    ) group by d.STATE_FIPS
                )
                union
                (select r.state_fips, r.total_deaths 
                    from state_record r 
                    where r.date in (
                        select max(r.date) from daily_record r
                    )
                );
                '''
            )
        else:
            cursor.close()
            error = ''
            return jsonify({'err': error})
    elif method == 'cases100katdate':
        if granularity == 'county':
            query = (
                '''
                (select r.county_fips, float4(r.total_cases)/float4(d.population) * 100000.0 as cases_per_100k 
                    from daily_record r, county_data d  
                    where d.FIPS = r.COUNTY_FIPS and r.date in (
                        select max(r.date) from daily_record r
                    )
                )
                union
                (select r.state_fips, float4(r.total_cases)/float4(d.population) * 100000.0 as cases_per_100k 
                    from state_record r, state_data d  
                    where d.FIPS = r.STATE_FIPS and r.date in (
                        select max(r.date) from daily_record r
                    )
                );
                '''
            )
        elif granularity == 'state':
            query = (
                '''
                (select d.state_fips, float4(sum(r.total_cases)) / float4(sum(d.population)) * 100000.0 
                    from daily_record r, county_data d 
                    where r.county_fips = d.FIPS and r.date in (
                        select max(r.date) from daily_record r
                    ) group by d.STATE_FIPS
                )
                union
                (select r.state_fips, float4(r.total_cases)/float4(d.population) * 100000.0 as cases_per_100k 
                    from state_record r, state_data d  
                    where d.FIPS = r.STATE_FIPS and r.date in (
                        select max(r.date) from daily_record r
                    )
                );
                '''
            )
        else:
            cursor.close()
            error = ''
            return jsonify({'err': error})
    elif method == 'deaths100katdate':
        if granularity == 'county':
            query = (
                '''
                (select r.county_fips, float4(r.TOTAL_DEATHS)/float4(d.population) * 100000.0 as deaths_per_100k from daily_record r, county_data d  where d.FIPS = r.COUNTY_FIPS and r.date in (select max(r.date) from daily_record r))/*placeholder*/
                union
                (select r.state_fips, float4(r.TOTAL_DEATHS)/float4(d.population) * 100000.0 as deaths_per_100k from state_record r, state_data d  where d.FIPS = r.STATE_FIPS and r.date in (select max(r.date) from daily_record r))/*placeholder*/;
                '''
            )
        elif granularity == 'state':
            query = (
                '''
                (select d.state_fips, float4(sum(r.total_deaths)) / float4(sum(d.population)) * 100000.0 from daily_record r, county_data d where r.county_fips = d.FIPS and r.date in (select max(r.date) from daily_record r) group by d.STATE_FIPS)
                union
                (select r.state_fips, float4(r.TOTAL_DEATHS)/float4(d.population) * 100000.0 as deaths_per_100k from state_record r, state_data d  where d.FIPS = r.STATE_FIPS and r.date in (select max(r.date) from daily_record r))/*placeholder*/;
                '''
            )
        else:
            cursor.close()
            error = ''
            return jsonify({'err': error})
    elif method == 'cases100katdatevmov':
        if granularity == 'county':
            query = (
                '''
                (select r.county_fips, (float4(r.total_cases)/float4(d.population) * 100000.0) * float4(d.MOV) as cases_per_100k_v_MoV from daily_record r, county_data d  where d.FIPS = r.COUNTY_FIPS and r.date in (select max(r.date) from daily_record r))/*placeholder*/
                union
                (select r.state_fips, (float4(r.total_cases)/float4(d.population) * 100000.0) * float4(d.MOV) as cases_per_100k_v_MoV from state_record r, state_data d  where d.FIPS = r.STATE_FIPS and r.date in (select max(r.date) from daily_record r))/*placeholder*/;
                '''
            )
        elif granularity == 'state':
            query = (
                '''
                (select d.state_fips, float4(sum(r.total_cases)) / float4(sum(d.population)) * 100000.0 * (sum(d.MoV) / float4(count(d.STATE_FIPS))) from daily_record r, county_data d where r.county_fips = d.FIPS and r.date in (select max(r.date) from daily_record r) group by d.STATE_FIPS)
                union
                (select r.state_fips, (float4(r.total_cases)/float4(d.population) * 100000.0) * float4(d.MOV) as cases_per_100k_v_MoV from state_record r, state_data d  where d.FIPS = r.STATE_FIPS and r.date in (select max(r.date) from daily_record r))/*placeholder*/;
                '''
            )
        else:
            cursor.close()
            error = ''
            return jsonify({'err': error})
    elif method == 'deaths100katdatemov':
        if granularity == 'county':
            query = (
                '''
                (select r.county_fips, (float4(r.total_deaths)/float4(d.population) * 100000.0) * float4(d.MOV) as cases_per_100k_v_MoV from daily_record r, county_data d  where d.FIPS = r.COUNTY_FIPS and r.date in (select max(r.date) from daily_record r))/*placeholder*/
                union
                (select r.state_fips, (float4(r.total_deaths)/float4(d.population) * 100000.0) * float4(d.MOV) as cases_per_100k_v_MoV from state_record r, state_data d  where d.FIPS = r.STATE_FIPS and r.date in (select max(r.date) from daily_record r))/*placeholder*/;
                '''
            )
        elif granularity == 'state':
            query = (
                '''
                (select d.state_fips, float4(sum(r.total_deaths)) / float4(sum(d.population)) * 100000.0 * (sum(d.MoV) / float4(count(d.STATE_FIPS))) from daily_record r, county_data d where r.county_fips = d.FIPS and r.date in (select max(r.date) from daily_record r) group by d.STATE_FIPS)
                union
                (select r.state_fips, (float4(r.total_deaths)/float4(d.population) * 100000.0) * float4(d.MOV) as cases_per_100k_v_MoV from state_record r, state_data d  where d.FIPS = r.STATE_FIPS and r.date in (select max(r.date) from daily_record r))/*placeholder*/;
                '''
            )
        else:
            cursor.close()
            error = ''
            return jsonify({'err': error})
    else:
        cursor.close()
        error = ''
        return jsonify({'err': error})
    
    try:
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        return jsonify(records)
    except BaseException:
        error = 'Error: An unexpected error occurred, try again later!'
        return jsonify({'err': error})