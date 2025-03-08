from flask import Flask
from controllers.main_controller import main_bp
from ai_policy_annotation.llm import run_llm_agents
from ai_policy_annotation.copy_policies import main as copy_policies
from ai_policy_annotation.rag import initialize_rag_database

app = Flask(__name__)
app.register_blueprint(main_bp)

if __name__ == '__main__':
    copy_policies()
    initialize_rag_database()
    # run_llm_agents()
    # app.run(debug=True)