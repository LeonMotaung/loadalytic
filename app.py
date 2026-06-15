import os
from flask import Flask, render_template

app = Flask(
    __name__,
    static_folder='assets',      # Use the existing assets directory for static files
    static_url_path='/assets'    # Serve static files at /assets/...
)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
