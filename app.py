from flask import Flask, render_template
from connect_db import select_table

app = Flask(__name__)

@app.route('/')
def index():
    schedule_data = select_table('schedule_D1150459')

    return render_template('index.html', schedule=schedule_data)

if __name__ == '__main__':
    app.run(debug=True)
