from flask import Blueprint, render_template, request
import os
import datetime
import officials
from services import result_creater
import badgelist

view = Blueprint("view", __name__, url_prefix="/")
today = datetime.date.today()
users = os.environ.get("ADMIN")
month_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]


@view.route('/')
def view_index():
    title = 'homelog analytics'
    official_list = officials.namelist
    badge_list = badgelist.badge_list
    return render_template(
        'index.html',
        title=title,
        list=official_list,
        year=month_list,
        badge_list=badge_list)


@view.route('/result/<specified_month>')
def view_month_summary(specified_month=None):
    month = specified_month or '%s' % (today.month - 1)
    result = result_creater.monthly_data_getter(month)
    print(result)
    return render_template('month_summary.html', result=result, month=month)


@view.route('/result/all')
def view_all_summary():
    result = result_creater.all_person_record_getter()
    print("result is :%s" % result)
    return render_template('all_summary.html', result=result, year=month_list)


@view.route('/result/person/<person>')
def view_personal_sending(person=None):
    person = person or '小澤 健治'
    result = result_creater.person_record_getter(person=person)
    print(result)
    return render_template(
        'personal_summary.html', result=result, person=person)


@view.route('/result/badge_kind/')
def view_sender_receiver_badgekind():
    month = request.args.get('month')
    badge = request.args.get('badge')
    result = result_creater.badgekind_getter(month, badge)
    print(result)
    return render_template(
        'badgekind_summary.html',
        result=result,
        month=month,
        badge=request.args.get('badge'),
        count=len(result))


if __name__ == '__main__':
    # view_month_summary()
    # view_personal_sending()
    # view_all_summary()
    view_personal_sending()
