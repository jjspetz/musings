from flask import Flask, render_template, jsonify, request, redirect, url_for
import get_analytics as analytics
from box import Box
app = Flask(__name__)

# TODO
# 1) add current stats to display
# 2) add compare toggle

VIEW_ID = '163519985'
TIME_FRAME = '30'
COMPARE = True

@app.route('/json')
def return_json():
    return jsonify(analytics.main(VIEW_ID, TIME_FRAME, COMPARE))

# used for testing purposes only
# @app.route('/account')
# def return_account():
#     return jsonify(analytics.get_account_info())

@app.route('/')
def home():
    data = analytics.main(VIEW_ID, TIME_FRAME, COMPARE)
    other = Box(data)
    account_data = analytics.get_account_info()
    site = {}
    total_val = []
    metric_val = []

    for account in account_data.get('items', []):
        for property in account.get('webProperties', []):
            name = property.get('name')
            for props in property.get('profiles', []):
                site[name] = props.get('id')

    values = []
    # data.reports[0].data.totals[0].values()
    for total in other.reports[0].data.totals:
        for val in total.values():
            for num in val:
                values.append(num)

    for i in range(int(len(values)/2)):
        total_val.append([values[i], values[i+10], calc_percent(values[i], values[i+10])])


    # data.reports[0].data.rows.metrics[0].values()
    for row in other.reports[0].data.rows:
        name = row.dimensions[0]
        values = []
        for metric in row.metrics:
            for val in metric.values():
                for num in val:
                    values.append(num)
        for i in range(int(len(values)/2)):
            metric_val.append([values[i], values[i+10], calc_percent(values[i], values[i+10]), name])

    return render_template('index.html', data=data, account=site, total=total_val, metric=metric_val, compare=COMPARE)

@app.route('/change', methods=['POST'])
def set_project():
    global VIEW_ID
    global TIME_FRAME
    global COMPARE
    VIEW_ID = dict(request.form).get('site')[0]
    TIME_FRAME = dict(request.form).get('time')[0]
    COMPARE = dict(request.form).get('compare')
    return redirect(url_for('home'))


# functions
def calc_percent(a, b):
    a = float(a)
    b = float(b)
    if a == 0 and b == 0:
        return 0
    elif b > 0:
        return ((a - b) / b)*100
    else:
        return 100
