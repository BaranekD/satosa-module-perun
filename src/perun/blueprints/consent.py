import os

from flask import Blueprint, render_template

consent = Blueprint('consent', __name__, template_folder=os.path.dirname(__file__) + '/templates')


@consent.route('/abc')
def show_consent():
    return render_template('consent/consent.html')
