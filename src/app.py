from flask import Flask
from controllers.main_controller import main_bp
from models.llm import run_llm_agents

app = Flask(__name__)
app.register_blueprint(main_bp)

if __name__ == '__main__':
    run_llm_agents()
    app.run(debug=True)
