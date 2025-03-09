from flask import Flask, send_from_directory
from controllers.main_controller import main_bp
from ai_policy_annotation.llm import run_llm_agents
from ai_policy_annotation.copy_policies import main as copy_policies
from ai_policy_annotation.rag import initialize_rag_database
import os

app = Flask(__name__)
app.register_blueprint(main_bp)

@app.route('/privacy-icon-images/<path:filename>')
def serve_images(filename):
    return send_from_directory(os.path.join(app.root_path, 'data', 'privacy-icon-images'), filename)

if __name__ == '__main__':
    # copy_policies()
    run_llm_agents()
    # app.run(debug=True)