# -*- coding: utf-8 -*-

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
import sendgrid

# Our libs
from fitactivists.models import MongoRecord
from fitactivists.models import Report

blueprint = Blueprint('api',
                      __name__,
                      url_prefix='/api',
                      static_folder='../../client/static',
                      template_folder='../../client/templates')

HTML = '''<div><div><div class="adM">
 </div><div align="center"><div class="adM">

 </div><table style="" bgcolor="#ffffff" border="0" width="100%" cellspacing="0" cellpadding="0">
 <tbody><tr>
 <td style="padding:14px 14px 14px 14px" valign="top" rowspan="1" colspan="1" align="center">

 <table style="background:transparent" border="0" width="100%" cellspacing="0" cellpadding="0">
 <tbody><tr>
 <td valign="top" width="100%" rowspan="1" colspan="1" align="center">
 <table style="width:640px" border="0" width="1" cellspacing="0" cellpadding="0">
 <tbody><tr>

 <td style="padding:0px 0px 0px 0px" valign="top" width="100%" rowspan="1" colspan="1" align="center">

 

 <table border="0" width="100%" cellspacing="0" cellpadding="0">
 <tbody><tr>
 <td style="padding-bottom:14px;height:1px;line-height:1px" height="1" rowspan="1" colspan="1" align="center"><img height="1" vspace="0" border="0" hspace="0" width="5" style="display:block" alt="" src="http://img.constantcontact.com/letters/images/1101116784221/S.gif"></td>
 </tr>
 </tbody></table>

 </td>

 </tr>
 </tbody></table>
 </td>
 </tr>
 </tbody></table>

 <table style="width:640px" border="0" width="1" cellspacing="0" cellpadding="0">
 <tbody><tr>
 <td style="background-color:#dfdfdf;padding:1px 1px 1px 1px" bgcolor="#dfdfdf" valign="top" rowspan="1" colspan="1" align="center">

 <table style="background-color:#ffffff" bgcolor="#ffffff" border="0" width="100%" cellspacing="0" cellpadding="0">
 <tbody><tr>
 <td valign="top" rowspan="1" colspan="1" align="center">

 <table border="0" width="100%" cellspacing="0" cellpadding="0">
 <tbody><tr>

 <td style="padding:0px 0px 0px 0px" valign="top" width="100%" rowspan="1" colspan="1" align="center">

 <table style="background-color:#ffffff" bgcolor="#FFFFFF" border="0" width="100%" cellspacing="0" cellpadding="0"><tbody><tr><td style="color:#76b5be;font-family:Arial,Helvetica,sans-serif;font-size:10pt;padding:32px 32px 32px 32px" valign="center" rowspan="1" colspan="1" align="left">
<div><a shape="rect" href="http://your.website.address.here?id=preview" target="_blank"><img style="display:block" vspace="0" border="0" name="144eff43b54a5d88_ACCOUNT.IMAGE.1" hspace="0" width="169" src="https://origin.ih.constantcontact.com/fs155/1116884498439/img/1.png" align="left"></a></div>
</td><td style="color:#76b5be;font-family:Arial,Helvetica,sans-serif;font-size:10pt;padding:32px 32px 32px 0px" valign="center" width="100%" rowspan="1" colspan="1" align="right">
<br></td></tr></tbody></table>

 <table style="margin:0px 0px 0px 0px" border="0" width="100%" cellspacing="0" cellpadding="0">
 <tbody><tr>
 <td style="padding:0px 0px 0px 0px;height:1px;line-height:1px" rowspan="1" colspan="1">
 <table border="0" width="100%" cellspacing="0" cellpadding="0">
 <tbody><tr>
 <td style="padding-bottom:9px;background-color:#4c4c4c;height:1px;line-height:1px" height="1" bgcolor="#4C4C4C" rowspan="1" colspan="1" align="center"><img height="1" vspace="0" border="0" hspace="0" width="5" style="display:block" alt="" src="http://img.constantcontact.com/letters/images/1101116784221/S.gif"></td>
 </tr>
 </tbody></table>
 </td>
 </tr>
 </tbody></table>

 </td>

 </tr>
 </tbody></table>

 <table border="0" width="100%" cellspacing="0" cellpadding="0">
 <tbody><tr>

 <td style="padding:0px 0px 0px 0px" valign="top" width="100%" rowspan="1" colspan="1" align="center">

 

 <a name="144eff43b54a5d88_LETTER.BLOCK6"></a><table style="background-color:#ebf5f6" bgcolor="#ebf5f6" border="0" width="100%" cellspacing="0" cellpadding="0"><tbody><tr><td style="font-size:10pt;font-family:Arial,Helvetica,sans-serif;padding:8px 32px 18px 32px" valign="top" rowspan="1" colspan="1" align="left">
<div><br> <img style="display:block" height="234" vspace="5" border="0" name="144eff43b54a5d88_ACCOUNT.IMAGE.4" hspace="10" width="220" src="https://origin.ih.constantcontact.com/fs155/1116884498439/img/4.jpg" align="right"><div style="color:#ee5624;font-family:Arial,Helvetica,sans-serif;font-size:18pt"><span style="color:#4288c6"><b>
<div>Relax.&nbsp;</div>
<div>Group Meditation at <span class="aBn" data-term="goog_739398388" tabindex="0"><span class="aQJ">4pm</span></span> on Mondays.</div>
</b></span></div><br> Meditation is a great way to unplug, reduce stress, and increase focus. Join our team at <span class="aBn" data-term="goog_739398389" tabindex="0"><span class="aQJ">4pm</span></span> on Mondays to decompress. Learn more about meditation&nbsp;<div><a style="font-weight:bold;color:rgb(66,136,198);text-decoration:none" shape="rect" href="http://r20.rs6.net/tn.jsp?e=001na4Jpnr6WvWjg7-jOlHVEz_rUb0XkCx16SragQjxrXWFQz12x4AinPjzmPupR1qAg6PNcOC1EPqqcvx2hnsOeXXoBzJtytz-ms3wIxe_pUuWca1QparMd0PEB9TnR78WoK6UzQXXoX6KIMhZSAwr0mpgYpH66z6D-TnRJxuH4pYv3QAo1OXzuH3SF1tDyNVy" target="_blank">here.</a><br><br></div></div>
</td></tr></tbody></table>

 <table style="margin:0px 0px 0px 0px" border="0" width="100%" cellspacing="0" cellpadding="0">
 <tbody><tr>
 <td style="padding:0px 0px 0px 0px;height:1px;line-height:1px" rowspan="1" colspan="1">
 <table border="0" width="100%" cellspacing="0" cellpadding="0">
 <tbody><tr>
 <td style="padding-bottom:0px;background-color:#d3ddde;height:1px;line-height:1px" height="1" bgcolor="#d3ddde" rowspan="1" colspan="1" align="center"><img height="1" vspace="0" border="0" hspace="0" width="5" style="display:block" alt="" src="http://img.constantcontact.com/letters/images/1101116784221/S.gif"></td>
 </tr>
 </tbody></table>
 </td>
 </tr>
 </tbody></table>

 

 

 

 </td>

 </tr>
 </tbody></table>

 <table border="0" width="100%" cellspacing="0" cellpadding="0">
 <tbody><tr>

 <td style="padding:0px 0px 0px 0px" valign="top" width="100%" rowspan="1" colspan="1" align="center">

 

 <a name="144eff43b54a5d88_LETTER.BLOCK12"></a><table border="0" width="100%" cellspacing="0" cellpadding="0"><tbody><tr><td style="color:#454545;font-family:Arial,Helvetica,sans-serif;font-size:10pt;padding:8px 32px 9px 32px" valign="top" rowspan="1" colspan="1" align="left">
<div><br> <img style="display:block" height="112" vspace="5" border="0" name="144eff43b54a5d88_ACCOUNT.IMAGE.3" hspace="10" width="150" src="https://origin.ih.constantcontact.com/fs155/1116884498439/img/3.jpg" align="right"><div style="color:#ee5624;font-family:Arial,Helvetica,sans-serif;font-size:14pt"><span style="color:#4288c6"><b>Napping helps the mind focus</b></span></div><br> That's right, we WANT you to sleep on the job. A 20 minute nap can work wonders on the mind and the body. Grab a comfy spot and snooze away...then get back after it. Want to learn more about the science behind happing?&nbsp;<div><a style="font-weight:bold;color:rgb(66,136,198);text-decoration:none" shape="rect" href="http://r20.rs6.net/tn.jsp?e=001na4Jpnr6WvWjg7-jOlHVEz_rUb0XkCx16SragQjxrXWFQz12x4AinPjzmPupR1qAg6PNcOC1EPrs4iw3PZK0l8qBZWaMWi2mGWcywzOsCL_sbuyfEsqV-0IukEbwMmj4fk04xfg5o2BZtxGGnw3j2ww5ALmd4rKpWTk9p64AE7LGo4nMzGRNo4IvhlvBZ7oV" target="_blank">Check it out.</a><br><br></div></div>
</td></tr></tbody></table>

 <table style="margin:0px 0px 0px 0px" border="0" width="100%" cellspacing="0" cellpadding="0">
 <tbody><tr>
 <td style="padding:0px 0px 0px 0px;height:1px;line-height:1px" valign="top" rowspan="1" colspan="1" align="left">
 <table border="0" width="100%" cellspacing="0" cellpadding="0">
 <tbody><tr>
 <td style="background-color:#d3ddde;padding-bottom:0px;height:1px;line-height:1px" height="1" bgcolor="#d3ddde" valign="top" rowspan="1" colspan="1" align="center"><img height="1" vspace="0" border="0" hspace="0" width="5" style="display:block" alt="" src="http://img.constantcontact.com/letters/images/1101116784221/S.gif"></td>
 </tr>
 </tbody></table>
 </td>
 </tr>
 </tbody></table>

 <a name="144eff43b54a5d88_LETTER.BLOCK14"></a><table border="0" width="100%" cellspacing="0" cellpadding="0"><tbody><tr><td style="color:#454545;font-family:Arial,Helvetica,sans-serif;font-size:10pt;padding:8px 32px 9px 32px" valign="top" rowspan="1" colspan="1" align="left">
<div><br> <img style="display:block" height="129" vspace="5" border="0" name="144eff43b54a5d88_ACCOUNT.IMAGE.5" hspace="10" width="150" src="https://origin.ih.constantcontact.com/fs155/1116884498439/img/5.jpg" align="right"><div style="color:#ee5624;font-family:Arial,Helvetica,sans-serif;font-size:14pt"><span style="color:#4288c6"><b>Take a Deep Breath</b></span></div><br> Deep breathing has shown to reduce cortisol levels. What's cortisol? It's the hormone that makes you feel stress and anxious. Don't believe us? Well maybe you'll believe&nbsp;&nbsp;<div><a style="font-weight:bold;color:rgb(66,136,198);text-decoration:none" shape="rect" href="http://r20.rs6.net/tn.jsp?e=001na4Jpnr6WvWjg7-jOlHVEz_rUb0XkCx16SragQjxrXWFQz12x4AinPjzmPupR1qAg6PNcOC1EPpnlHSwozcLHDuWLORRoEFBAq6JUdNzvlqTPptbQARFZ7HfDQdAVovHW6lysDIp0-I=" target="_blank">SCIENCE.</a><br></div></div>
</td></tr></tbody></table>

 

 

 

 

 

 

 

 </td>

 </tr>
 </tbody></table>

 <table border="0" width="100%" cellspacing="0" cellpadding="0">
 <tbody><tr>

 <td style="padding:0px 0px 0px 0px" valign="middle" width="100%" rowspan="1" colspan="1" align="center">

 

 <table style="background-color:#4288c6" bgcolor="#4288C6" border="0" width="100%" cellspacing="0" cellpadding="0"><tbody><tr><td style="color:#ffffff;font-family:Arial,Helvetica,sans-serif;font-size:10pt;padding:25px 25px 25px 50px" valign="top" width="100%" rowspan="1" colspan="1" align="left">
<div><br><b>Milli Vanilli</b><br> 555.555.5555<br> <br> Our work and our people are regularly covered in publications around the world.<br> <br></div>
</td><td style="color:#ffffff;font-family:Arial,Helvetica,sans-serif;font-size:10pt;padding:25px 50px 25px 25px" valign="center" rowspan="1" colspan="1" align="left">
<div>
<table border="0" width="1" cellpadding="0" cellspacing="0" align="right"><tbody><tr><td style="padding:0px 0px 0px 0px;color:#454545;font-family:Arial,Helvetica,sans-serif;font-size:10pt" valign="top" rowspan="1" colspan="1" align="left">
<table style="width:220px;margin:0px 0px 0px 0px" border="0" width="1" cellpadding="0" cellspacing="0"><tbody><tr><td style="padding:0px;height:1px;line-height:1px;color:#454545" height="1" valign="top" rowspan="1" colspan="1" align="left">
<div><img height="5" vspace="0" border="0" hspace="0" width="1" src="https://imgssl.constantcontact.com/letters/images/1101116784221/S.gif"></div>
</td></tr></tbody></table>
</td></tr><tr><td style="background-color:#4c4c4c;border:1px solid #ffffff;border-color:#ffffff;padding:10px 10px 10px 10px;color:#ffffff;font-family:Arial,Helvetica,sans-serif;font-size:12pt" bgcolor="#4C4C4C" valign="top" rowspan="1" colspan="1" align="center">
<div><b><i>Give us a call today!</i></b></div>
</td></tr></tbody></table>
</div>
</td></tr></tbody></table>

 <table style="background-color:#f3f2f4" bgcolor="#f3f2f4" border="0" width="100%" cellspacing="0" cellpadding="0">
 <tbody><tr>
 <td style="color:#625467;font-family:Arial,Helvetica,sans-serif;font-size:8pt;padding:18px 32px 14px 32px" valign="top" rowspan="1" colspan="1" align="center">
 <div>
 <b><i>STAY CONNECTED</i></b><br>
 <br>
 <a style="color:#ffffff;font-family:Arial,Helvetica,sans-serif;font-size:10pt" shape="rect" href="#144eff43b54a5d88_"><img height="22" vspace="0" border="0" hspace="0" width="22" alt="Facebook" src="https://imgssl.constantcontact.com/ui/images1/ic_fbk_22.png"></a>
 &nbsp;&nbsp;
 <a style="color:#ffffff;font-family:Arial,Helvetica,sans-serif;font-size:10pt" shape="rect" href="#144eff43b54a5d88_"><img height="22" vspace="0" border="0" hspace="0" width="22" alt="Twitter" src="https://imgssl.constantcontact.com/ui/images1/ic_twit_22.png"></a>
 &nbsp;&nbsp;
 <a style="color:#ffffff;font-family:Arial,Helvetica,sans-serif;font-size:10pt" shape="rect" href="#144eff43b54a5d88_"><img height="22" vspace="0" border="0" hspace="0" width="22" alt="LinkedIn" src="https://imgssl.constantcontact.com/ui/images1/ic_lkdin_22.png"></a>
 &nbsp;&nbsp;
 <a style="color:#ffffff;font-family:Arial,Helvetica,sans-serif;font-size:10pt" shape="rect" href="#144eff43b54a5d88_"><img height="22" vspace="0" border="0" hspace="0" width="22" alt="Pinterest" src="https://imgssl.constantcontact.com/ui/images1/pinterest-22.png"></a><br>
 </div>
 </td>
 </tr>
 </tbody></table>

 </td>

 </tr>
 </tbody></table>

 </td>
 </tr>
 </tbody></table>
 </td>
 </tr>
 </tbody></table>

 <table style="background:transparent" border="0" width="100%" cellspacing="0" cellpadding="0">
 <tbody><tr>
 <td valign="top" width="100%" rowspan="1" colspan="1" align="center">
 <table style="width:640px" border="0" width="1" cellspacing="0" cellpadding="0">
 <tbody><tr>

 <td style="padding:0px 0px 0px 0px" valign="top" width="100%" rowspan="1" colspan="1" align="center">

 <table border="0" width="100%" cellspacing="0" cellpadding="0">
 <tbody><tr>
 <td style="padding:0px 8px 0px 8px;color:#777777;font-family:Arial,Helvetica,sans-serif;font-size:8pt" valign="top" rowspan="1" colspan="1" align="center"><div><img height="21" vspace="0" border="0" hspace="0" width="556" style="display:block" alt="" src="http://img.constantcontact.com/letters/images/1101116784221/PM_B2BA_BottomShadow.png"></div>
 </td>
 </tr>
 </tbody></table>

 

 

 </td>

 </tr>
 </tbody></table>
 </td>
 </tr>
 </tbody></table>

 </td>
 </tr>
 </tbody></table>

 </div>
 <div align="center" style="">
<table style="text-align:left" border="0" cellpadding="0" cellspacing="0">
<tbody><tr>
<td rowspan="1" colspan="1" align="center">

<div><div style="text-align:center;font-size:8pt;font-family:tahoma,sans-serif;font-weight:bold;padding-bottom:10px"><font style="font-size:8pt;font-family:tahoma,sans-serif" color="#000000" size="1" face="tahoma,sans-serif"><a shape="rect" href="http://ui.constantcontact.com/sa/fwtf.jsp?llr=ha5byfqab&amp;m=1116884498439&amp;ea=fitactivists@gmail.com&amp;a=1116894486081&amp;id=preview" target="_blank">Forward this email</a></font></div>


<table style="color:#2f2f2f;font-size:11px;font-family:tahoma,sans-serif" border="0" width="619" cellspacing="0" cellpadding="0">
<tbody><tr>
<td rowspan="1" colspan="1"><font style="font-family:tahoma,sans-serif;font-size:11px;color:#2f2f2f" color="#000000" size="1" face="tahoma,sans-serif">
<table border="0" width="100%">
<tbody><tr>
<td valign="middle" width="100" rowspan="1" colspan="1"><a shape="rect" href="http://visitor.constantcontact.com/do?p=un&amp;mse=001Fshzv3LjoSHRNbU-3_6T20PdWc-KoIbTuOSzPp4OUzDRuHR6zx2gXg%3D%3D&amp;t=001GLH1wMEQxelP6-Qj7nuHBQ%3D%3D&amp;l=001FCSs65SMrsI%3D&amp;id=001b-xBWU3VMkfiyUAmPrKYhqWHxAYR5_ui&amp;llr=ha5byfqab" target="_blank"><img border="0" src="http://img.constantcontact.com/letters/images/SafeUnsubscribe_Footer_Logo_New.png"></a>
</td>
<td width="519" rowspan="1" colspan="1" align="right"><a shape="rect" href="http://www.constantcontact.com/index.jsp?cc=PM_B2BA&amp;id=preview" target="_blank"><img border="0" src="http://img.constantcontact.com/letters/images/CC_Footer_Logo_New.png"></a>
</td>
</tr>
</tbody></table><div>This email was sent to <a href="mailto:fitactivists@gmail.com" target="_blank">fitactivists@gmail.com</a> by <a style="color:#0000ff" shape="rect" href="mailto:fitactivists@gmail.com" target="_blank">fitactivists@gmail.com</a> <span style="color:#bababa"> | </span> &nbsp; </div>
<div><a style="color:#0000ff" shape="rect" href="http://visitor.constantcontact.com/do?p=oo&amp;mse=001Fshzv3LjoSHRNbU-3_6T20PdWc-KoIbTuOSzPp4OUzDRuHR6zx2gXg%3D%3D&amp;t=001GLH1wMEQxelP6-Qj7nuHBQ%3D%3D&amp;l=001FCSs65SMrsI%3D&amp;id=001b-xBWU3VMkfiyUAmPrKYhqWHxAYR5_ui&amp;llr=ha5byfqab" target="_blank">Update Profile/Email Address</a> <span style="color:#bababa">|</span> Instant removal with <a style="color:#0000ff" shape="rect" href="http://visitor.constantcontact.com/do?p=un&amp;mse=001Fshzv3LjoSHRNbU-3_6T20PdWc-KoIbTuOSzPp4OUzDRuHR6zx2gXg%3D%3D&amp;t=001GLH1wMEQxelP6-Qj7nuHBQ%3D%3D&amp;l=001FCSs65SMrsI%3D&amp;id=001b-xBWU3VMkfiyUAmPrKYhqWHxAYR5_ui&amp;llr=ha5byfqab" target="_blank">SafeUnsubscribe</a>™  <span style="color:#bababa">|</span>  <a style="color:#0000ff" shape="rect" href="http://ui.constantcontact.com/roving/CCPrivacyPolicy.jsp?id=preview" target="_blank">Privacy Policy</a>.</div>
</font></td>
</tr>
</tbody></table><div style="padding-top:12px;font-size:12px;font-family:tahoma,sans-serif" align="left"><font style="font-size:12px;font-family:tahoma,sans-serif" color="#000000" size="1" face="tahoma,sans-serif">Fitactivists<span style="color:#bababa"> | </span>840 Battery St<span style="color:#bababa"> | </span>San Francisco<span style="color:#bababa"> | </span>CA<span style="color:#bababa"> | </span>94111</font></div></div>
</td>
</tr>
</tbody></table>
</div></div></div>'''

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

    config = flask.current_app.config
    if config.get('SENDGRID_USERNAME'):
        sg = sendgrid.SendGridClient(config['SENDGRID_USERNAME'], config['SENDGRID_PASSWORD'])
        message = sendgrid.Mail(to=current_user['email'],
                                subject='Chillax with FitActivists',
                                html=HTML.decode('latin-1'))
        message.set_from('FitActivists <fitactivists@gmail.com>')
        status, msg = sg.send(message)

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

