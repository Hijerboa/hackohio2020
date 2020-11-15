import functools, json
import psycopg2.extras

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from . import db

bp = Blueprint('index', __name__, url_prefix='/')
cache = dict()


@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@bp.route('/geodata', methods=['GET'])
def geodata():
    method = request.args.get('method')
    global cache

    if method in cache:
        return cache[method]

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
    cursor.execute(query)
    records = cursor.fetchall()
    cache[method] = records
    return json.dumps(records)


@bp.route('/coviddata', methods=['GET'])
def coviddata():
    pass