from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/manifest.webapp')
def get_manifest():
    hash = request.host.split('.', 1)[0]
    return (render_template('manifest.webapp', hash=hash),
            200, {'Content-Type': 'application/x-web-app-manifest+json'})


@app.route('/')
def main():
    return 'yay'


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
