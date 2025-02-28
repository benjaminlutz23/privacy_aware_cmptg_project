from flask import Flask
from controllers.main_controller import main_bp

app = Flask(__name__)
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)
