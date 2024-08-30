from flask import Flask, render_template, send_from_directory
from waitress import serve
import pandas as pd
import os

app = Flask(__name__)

metadata = pd.read_csv('metadata.csv')

metadata.columns = metadata.columns.str.strip()

metadata['link'] = metadata['link'].str.strip()

if isinstance(metadata, pd.DataFrame):
    latest_images = metadata.sort_values(by='datetime', ascending=False).head(10).to_dict(orient='records')
else:
    latest_images = []

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', metadata=latest_images)

@app.route('/art')
def art():
    metadata_list = metadata.to_dict(orient='records')

    metadata_list.sort(key=lambda x: x['datetime'], reverse=True)
    
    return render_template('art.html', metadata=metadata_list)

@app.route('/commissions')
def commissions():
    return render_template('commissions.html')

@app.route('/robots.txt')
def robots():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'robots.txt')

if __name__ == "__main__":
    serve(app, listen='127.0.0.1:5000')
