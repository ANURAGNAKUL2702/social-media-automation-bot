
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Social Media Automation Bot is up and running!'

if __name__ == '__main__':
    app.run(debug=True)
