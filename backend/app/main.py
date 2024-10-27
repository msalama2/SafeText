
from flask import Flask, render_template

app = Flask(__name__, template_folder="frontend/public")  # Defaults to 'templates/' for templates

@app.route('/')
def home():
    return render_template('index.html')  # Now inside 'templates/'

if __name__ == '__main__':
    app.run(debug=True)