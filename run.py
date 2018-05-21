from app.views import bp
from flask import Flask

app = Flask(__name__)
app.register_blueprint(bp)
app.run()
