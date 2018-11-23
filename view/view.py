from flask import Blueprint, render_template
import datetime
from api import result_getter

view = Blueprint("view", __name__, url_prefix="/")
today = datetime.date.today()


@view.route('/')
def view_index():
    title = 'homelog analytics'
    return render_template('index.html', title=title)


@view.route('/result/<specified_month>')
def view_month_summary(specified_month=None):
    month = specified_month or '%s' % (today.month - 1)
    result = result_getter.result_getter(month=month)
    print(result)
    return render_template('month_summry.html', result=result, month=month)


@view.route('/result')
def view_this_month_summary():
    month = '%s' % (today.month - 1)
    result = result_getter.result_getter(month=month)
    print(result)
    return render_template('month_summry.html', result=result, month=month)


@view.route('/result/person/<person>', methods=['POST'])
def view_personal_sending(person=None):
    person = person or '小澤 健治'
    result = result_getter.person_record_getter(person=person)
    print(result)
    return render_template(
        'personal_summary.html', result=result, person=person)


if __name__ == '__main__':
    # view_month_summary()
    view_personal_sending()
