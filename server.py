from flask import Flask, jsonify, render_template, request
import connexion
import os

from graph import plotChamps
from fetchData import makeData
# Create the application instance
app = connexion.App(__name__, specification_dir="./")

# screen -r
# screen ctrl-a ctrl-d
# source env/bin/activate

# Read the yaml file to configure the endpoints
app.add_api("master.yml")

# create a URL route in our application for "/"
@app.route("/")
def home():
    return render_template("test.html", mimetype = 'text/html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    if not os.path.exists(f'src/data/{text}.h5'):
        makeData(text)
    return plotChamps(text)
    # return render_template("test.html", user_image = plotChamps(text), mimetype = 'text/html')

if __name__ == '__main__':
    app.run(debug=True, port=20000, host='0.0.0.0')