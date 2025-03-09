from flask import Blueprint, render_template, request, jsonify, send_from_directory
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/process', methods=['POST'])
def process():
    data = request.json
    # icons = assign_privacy_icons(data['policy'])
    return

@main_bp.route('/view_policy/<source>')
def view_policy(source):
    policy_dir = os.path.join(os.getcwd(), 'src', 'data', 'llm_annotated_policies', source)
    return send_from_directory(policy_dir, '20_theatlantic.com.html')
