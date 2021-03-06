from flask import Blueprint, render_template, request, redirect
import os
import datetime
import officials
import services.result_creater
from services import result_creater, processor, downloader, mvp_analyzer
import badgelist

view = Blueprint('view', __name__, url_prefix='/')
today = datetime.date.today()
users = os.environ.get('ADMIN')
month_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]


def create_data_list():
    data_list = []
    year_list = [2017, 2018, 2019]
    for year in year_list:
        for month in month_list:
            data_list.append('%d/%d' % (year, month))
    return data_list


@view.route('/')
def view_index():
    title = 'homelog analytics'
    official_list = officials.namelist
    badge_list = badgelist.badge_list
    updated = services.result_creater.get_update_data()
    type_list = ['sending', 'receiving']
    try:
        u_date = updated['body']
    except:
        u_date = None
    return render_template(
        'index.html',
        title=title,
        list=official_list,
        year=create_data_list(),
        badge_list=badge_list,
        last_updated=u_date, type_list=type_list)


@view.route('/analytics/18_mvp')
def view_sender_and_receiver(year=None):
    year = 2018
    start_month = request.args.get('month')
    start_month = start_month[5::]
    fin_month = request.args.get('fin-month')
    fin_month = fin_month[5::]
    results = mvp_analyzer.mvp_analyze(year, start_month, fin_month)
    downloader.download_4q_mvp_analytics(results)
    print(results)
    return render_template('mvp_analytics.html', result=results, year=year, start_month=start_month, fin_month=fin_month)


@view.route('/analytics/12')
def view_badge_and_receiver():
    year = 2018
    month = request.args.get('month')
    month = month[5::]
    badge = request.args.get('badge')
    type = request.args.get('types')
    print(request.args)
    print('type: %s' % type)
    results = mvp_analyzer.mvp_analyze2(year, month, badge, type)
    downloader.download_12th_mvp_analytics(results, badge, type)
    return render_template(
        'badge_and_count.html',
        result=results,
        badge=badge,
        type=type,
        year=year,
        month=month
    )


@view.route('/result/<year>/<specified_month>')
def view_month_summary(year=None, specified_month=None):
    month = specified_month or '%s' % (today.month - 1)
    year = year or 2018
    result = result_creater.monthly_data_getter(year, month)
    print(result)
    return render_template('month_summary.html', result=result, year=year, month=month)


@view.route('/result/all')
def view_all_summary():
    result = result_creater.all_person_record_getter()
    print('result is :%s' % result)
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
    data = request.args.get('month')
    year = data[:4]
    print(year)
    month = data[5::]
    print(month)
    badge = request.args.get('badge')
    result = processor.badgekind_getter(year, month, badge)
    print(result)
    return render_template(
        'badgekind_summary.html',
        result=result,
        month=month,
        badge=request.args.get('badge'),
        count=len(result))


@view.route('/download/<year>/<month>')
def download_monthly_data(year=None, month=None):
    print(year)
    print(month)
    downloader.download_monthly_sheet(year, month)
    return redirect('/')


if __name__ == '__main__':
    # view_month_summary()
    # view_personal_sending()
    # view_all_summary()
    # view_personal_sending()
    # download_monthly_data(10)
    view_sender_and_receiver(year=2018)
