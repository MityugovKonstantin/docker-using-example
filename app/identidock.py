from flask import Flask, Response, request
import requests as req
import hashlib as hl
import redis
import html

app = Flask(__name__)
cache = redis.StrictRedis(host='redis', port=6379, db=0)
default_name = 'Mityugov Konstantin'
salt = "UNIQUE_SALT"

@app.route('/', methods=['GET', 'POST'])
def mainpage():
    
    name = default_name

    if request.method == 'POST':
        name = html.escape(request.form['name'], quote=True)

    salted_name = salt + name
    name_hash = hl.sha256(salted_name.encode()).hexdigest()

    header = '<html><head><title>Identidock</title></head><body>'
    
    body = '''
    <form method="POST">
    Hello <input type="text" name="name" value="{0}">
    <input type="submit" value="submit">
    </form>
    <p>You look like a:
    <img src="/monster/{1}"/>
    '''.format(name, name_hash)

    footer = '</body></html>'

    return header + body + footer

@app.route('/monster/<name>')
def get_identicon( name ):
    name = html.escape(name, quote=True)
    image = cache.get(name)

    if image is None:
        print("Cache miss", flush=True)
        r = req.get('http://dnmonster:8080/monster/' + name + '?size=80')
        image = r.content
        cache.set(name, image)

    return Response(image, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
