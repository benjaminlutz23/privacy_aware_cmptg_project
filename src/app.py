from flask import Flask
from controllers.main_controller import main_bp
from models.llm import run_llm_agents, print_first_three_sections
from models.copy_policies import main as copy_policies

app = Flask(__name__)
app.register_blueprint(main_bp)

if __name__ == '__main__':
    # copy_policies()
    print_first_three_sections()
    app.run(debug=True)
