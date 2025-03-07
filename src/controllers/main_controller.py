from flask import Blueprint, render_template, request, jsonify
# from ai_policy_annotation.llm import assign_privacy_icons

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/process', methods=['POST'])
def process():
    data = request.json
    # icons = assign_privacy_icons(data['policy'])
    return
