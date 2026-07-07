from flask import Blueprint, redirect, url_for, session, jsonify
from app import db, oauth
from app.models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login")
def login():
    redirect_uri = "http://127.0.0.1:5000/auth/callback"
    return oauth.google.authorize_redirect(redirect_uri)

@auth_bp.route("/callback")
def auth_callback():
    token = oauth.google.authorize_access_token()
    user_info = token["userinfo"]

    user = User.query.filter_by(google_sub=user_info["sub"]).first()

    if user is None:
        user = User(
            google_sub=user_info["sub"],
            email=user_info.get("email"),
            name=user_info.get("name"),
            picture=user_info.get("picture"),
        )
        db.session.add(user)
        db.session.commit()

    session["user_id"] = user.id
    return redirect(url_for("pages.home"))

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("pages.signin"))