from flask import request, jsonify, Blueprint, render_template, current_app
from .. import db, bcrypt
from ..models import User, RoleEnum
from ..services.mail_service import send_email
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from itsdangerous import URLSafeTimedSerializer
from email_validator import validate_email, EmailNotValidError
import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role_str = data.get('role')

    if not all([name, email, password, role_str]):
        return jsonify({"msg": "Missing required fields"}), 400

    try:
        role = RoleEnum[role_str]
    except KeyError:
        return jsonify({"msg": f"Invalid role '{role_str}'. Must be one of {[r.name for r in RoleEnum]}"}), 400

    try:
        # In a test environment, we don't want to check for real MX records
        is_testing = current_app.config.get("TESTING", False)
        validate_email(email, check_deliverability=not is_testing)
    except EmailNotValidError as e:
        return jsonify({"msg": str(e)}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already registered"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(
        name=name,
        email=email,
        password_hash=hashed_password,
        role=role
    )

    db.session.add(new_user)
    db.session.commit()

    ts = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    token = ts.dumps(email, salt='email-confirm-salt')
    confirm_url = f"/confirm/{token}"

    html = f"Hi, please confirm your email by clicking here: {confirm_url}"

    send_email(new_user.email, "Confirm Your Email", html)

    return jsonify({"msg": "User created. Please check your email to confirm."}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password_hash, password):
        if not user.is_verified:
            return jsonify({"msg": "Account not verified. Please check your email."}), 401

        access_token = create_access_token(identity=str(user.id), expires_delta=datetime.timedelta(hours=1))
        refresh_token = create_refresh_token(identity=str(user.id))
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200

    return jsonify({"msg": "Bad email or password"}), 401

@auth_bp.route('/confirm/<token>')
def confirm_email(token):
    ts = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = ts.loads(token, salt='email-confirm-salt', max_age=86400)
    except:
        return jsonify({"msg": "The confirmation link is invalid or has expired."}), 400

    user = User.query.filter_by(email=email).first()

    if user.is_verified:
        return jsonify({"msg": "Account already confirmed."}), 200

    user.is_verified = True
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "Account confirmed!"}), 200

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password_request():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"msg": "Email is required"}), 400

    user = User.query.filter_by(email=email).first()

    if user:
        ts = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        token = ts.dumps(email, salt='password-reset-salt')
        reset_url = f"/reset-password/{token}"

        html = f"Hi, reset your password by clicking here: {reset_url}"

        send_email(user.email, "Password Reset Request", html)

    return jsonify({"msg": "If your email is in our system, you will receive a password reset link."}), 200

@auth_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password_with_token(token):
    ts = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = ts.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        return jsonify({"msg": "The password reset link is invalid or has expired."}), 400

    data = request.get_json()
    new_password = data.get('password')

    if not new_password:
        return jsonify({"msg": "Password is required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
         return jsonify({"msg": "User not found"}), 404

    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    user.password_hash = hashed_password
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "Password has been updated."}), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id, expires_delta=datetime.timedelta(hours=1))
    return jsonify(access_token=new_access_token), 200