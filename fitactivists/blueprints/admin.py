# Third party libs
import flask
from flask import Blueprint
from flask import render_template
from flask.ext.login import login_required

blueprint = Blueprint('admin',
                      __name__,
                      url_prefix='/company',
                      static_folder='../../client/static',
                      template_folder='../../client/templates')

@blueprint.route('/dashboard')
@login_required
def index():
    return render_template('admin/index.html')
