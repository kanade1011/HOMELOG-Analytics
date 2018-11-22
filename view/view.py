from flask import Blueprint, render_template
import datetime
from api import result_getter

view = Blueprint("view", __name__, url_prefix="/result")
today = datetime.date.today()


@view.route('/')
def view_month_summry():
    result = result_getter.result_getter(month='10')
    # return (result)
    return render_template('month_summry.html', resul=result)


if __name__ == '__main__':
    view_month_summry()