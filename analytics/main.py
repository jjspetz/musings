from flask import Flask, render_template, jsonify, request, redirect, url_for
import get_analytics as analytics
app = Flask(__name__)

VIEW_ID = '163519985'
TIME_FRAME = '30'
COMPARE = False

def home():
    data = analytics.main(VIEW_ID, TIME_FRAME, COMPARE)
    account_data = analytics.get_account_info()
    site = {}
    for account in account_data.get('items', []):
        for property in account.get('webProperties', []):
            name = property.get('name')
            for props in property.get('profiles', []):
                site[name] = props.get('id')
    return render_template('index.html', data=data, account=site)

@app.route('/json')
def return_json():
    return jsonify(analytics.main(VIEW_ID, TIME_FRAME, COMPARE))

@app.route('/account')
def return_account():
    return jsonify(analytics.get_account_info())

@app.route('/')
def home():
    data = analytics.main(VIEW_ID, TIME_FRAME, COMPARE)
    account_data = analytics.get_account_info()
    site = {}
    for account in account_data.get('items', []):
        for property in account.get('webProperties', []):
            name = property.get('name')
            for props in property.get('profiles', []):
                site[name] = props.get('id')
    return render_template('index.html', data=data, account=site)

@app.route('/change', methods=['POST'])
def set_project():
    global VIEW_ID
    global TIME_FRAME
    VIEW_ID = dict(request.form).get('site')[0]
    TIME_FRAME = dict(request.form).get('time')[0]
    return redirect(url_for('home'))

@app.route('/hello/<name>')
def hello(name):
    # show the user profile for that user
    return ('Hello %s' % name)
