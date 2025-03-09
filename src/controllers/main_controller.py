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

@main_bp.route('/get_policies/<source>')
def get_policies(source):
    policy_dir = os.path.join(os.getcwd(), 'src', 'data', 'llm_annotated_policies', source)
    policies = []
    for filename in os.listdir(policy_dir):
        if filename.endswith('.html'):
            policy_name = filename.replace('.html', '').split('_', 1)[-1]
            policies.append(policy_name)
    return jsonify({'policies': policies})

@main_bp.route('/view_policy/<source>/<policy>')
def view_policy(source, policy):
    policy_dir = os.path.join(os.getcwd(), 'src', 'data', 'llm_annotated_policies', source)
    for filename in os.listdir(policy_dir):
        if filename.endswith('.html') and filename.split('_', 1)[-1].replace('.html', '') == policy:
            return send_from_directory(policy_dir, filename)
    return "Policy not found", 404
