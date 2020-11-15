import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('index', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@bp.route('/mapdata', methods=['GET'])
def mapdata():
    # CALL THE DATABASE
    pass