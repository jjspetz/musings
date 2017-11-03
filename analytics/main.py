from flask import Flask, render_template, jsonify, request, redirect, url_for
import get_analytics as analytics
app = Flask(__name__)

VIEW_ID = '163519985'

def home():
    data = analytics.main(VIEW_ID)
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
    return jsonify(analytics.main(VIEW_ID))

@app.route('/account')
def return_account():
    return jsonify(analytics.get_account_info())

@app.route('/')
def home():
    data = analytics.main(VIEW_ID)
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
    results = dict(request.form).get('site')[0]
    VIEW_ID = results
    return redirect(url_for('home'))

@app.route('/hello/<name>')
def hello(name):
    # show the user profile for that user
    return ('Hello %s' % name)
