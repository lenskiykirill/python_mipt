from flask import render_template, escape, request
from app import app, db_logic

import json

@app.route('/api/token-<token>')
def api (token):
    return f"Token: {escape(token)}"

app.route('/api')(lambda : "Nice api")

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/api/register', methods=['POST', 'GET'])
def api_register():
    if request.method != "POST":
        return "API only supports POST-requests"

#    print (request.form)

    username = request.form.get('username')
    password = request.form.get('password')

    res = db_logic.create_user (username, password)
    return res[0]

@app.route('/api/get_username', methods=['POST'])
def api_get_username():
    user_id = request.form.get("id")

    username = db_logic.get_username (int(user_id))
    return username[1]

@app.route('/api/login', methods=['POST'])
def api_login():
    pass

@app.route('/api/articles', methods=['POST'])
def api_articles():
    articles = db_logic.get_articles()
    articles = articles[1]

    res = []
    for i in range(len(articles)):
        res.append((articles[i][0],
                    articles[i][1].strftime("%d-%b-%Y (%H:%M:%S.%f)"),
                    articles[i][2]))
    return json.dumps(res)

@app.route('/api/create_article', methods=['POST'])
def api_create_article():

    user_id = request.form.get("id")
    text = request.form.get("text")

    db_logic.create_article (int(user_id), text)
    return ""


