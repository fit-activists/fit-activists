# Standard libs
import datetime
import urlparse

# Third party libs
import flask
from flask import Blueprint
from flask import flash
from flask import json
from flask import redirect
from flask import render_template
from flask import Response
from flask import request
from flask import url_for
from flask.ext.login import current_user
from flask.ext.login import login_required

# Our libs
from fitactivists.models import MongoRecord
from fitactivists.models import Report

blueprint = Blueprint('api',
                      __name__,
                      url_prefix='/api',
                      static_folder='../../client/static',
                      template_folder='../../client/templates')

@blueprint.route('/reports/add', methods=['post'])
@login_required
def reports_add():
    report_data = {
        'activity':  int(request.form.get('activity', '')),
        'nutrition': int(request.form.get('nutrition', '')),
        'stress':    int(request.form.get('stress', '')),
        'happiness': int(request.form.get('happiness', '')),
        'user_id':   current_user['_id']
    }

    report = Report(report_data)

    if not report.is_valid():
        return redirect(url_for('root.index'))

    current_date = datetime.datetime.now()
    current_date = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
    existing_report = current_user.get_report_by_date(current_date)
    if existing_report:
        report_data['_id'] = existing_report['_id']
        report.update(report_data)
    else:
        report.create()

    return redirect(url_for('root.index'))

@blueprint.route('/reports/list')
@login_required
def reports_list():
    data = {
        'reports': [report.data for report in current_user.get_reports()],
    }
    return Response(json.dumps(data, cls=ReportJSONEncoder), mimetype='application/json')

class ReportJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        return super(self.__class__, self).default(obj)

