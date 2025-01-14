from datetime import datetime, timedelta, timezone
import jwt
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from werkzeug.security import check_password_hash, generate_password_hash
from flask import request, render_template, g
from flask_mail import Message
from config.config import Config
from api.users.user_model import User
from api.mail_manager import mail

class AuthDAO:
    def __init__(self, session):
        self.session = session

    def generate_csrf_token(self):
        serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
        csrf_token = serializer.dumps(Config.CSRFTOKEN, salt=Config.SALT)
        return csrf_token

    def verify_csrf_token(self, csrf_token):
        serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
        try:
            data = serializer.loads(csrf_token, salt=Config.SALT)
            return data == Config.CSRFTOKEN
        except (BadSignature, SignatureExpired):
            return False

    def get_session(self):
        user_id = g.user_id
        user = self.session.query(User).filter_by(id=user_id).first()
        return user.is_auth if user and user.is_auth else False

    def user_login(self, data, lang):
        email = data.get('email').lower()
        password = data.get('password')
        user = self.session.query(User).filter(User.email == email).first()

        if user and check_password_hash(user.password, password):
            access_token = jwt.encode({
                'sub': {'user_id': user.id},
                'exp': datetime.now(timezone.utc) + timedelta(seconds=3600)
            }, Config.SECRET_KEY, algorithm='HS256')

            user.is_auth = True
            self.session.commit()
            return access_token, 200

        return {'message': 'Incorrect email or password'}, 401

    def send_mail(data):
        try:
            subject = data.get("subject", "Notification")
            recipients = data.get("recipients", [])

            if not recipients:
                return {"message": "Recipients not specified"}, 400

            # HTML şablonunu birbaşa string olaraq daxil edirik
            html_template = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{data.get("title", "Notification")}</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f9f9f9;
                        margin: 0;
                        padding: 0;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 20px auto;
                        background-color: #fff;
                        padding: 20px;
                        border-radius: 5px;
                        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                    }}
                    h2 {{
                        color: #333;
                    }}
                    p {{
                        font-size: 14px;
                        color: #555;
                    }}
                    a.button {{
                        display: inline-block;
                        margin-top: 20px;
                        padding: 10px 15px;
                        background-color: #007BFF;
                        color: white;
                        text-decoration: none;
                        border-radius: 4px;
                    }}
                    a.button:hover {{
                        background-color: #0056b3;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>{data.get("title", "Hello!")}</h2>
                    <p>{data.get("message", "This is a notification email.")}</p>
                    {f'<a href="{data.get("link")}" class="button">{data.get("link_text", "Click Here")}</a>' if data.get("link") else ""}
                </div>
            </body>
            </html>
            """

            msg = Message(
                subject=subject,
                sender="noreply@example.com",  # Neutral sender email
                recipients=recipients
            )

            msg.body = data.get("msg", "This is a notification email.")
            msg.html = html_template

            mail.send(msg)
            return {"message": "Email sent successfully"}, 200
        except Exception as e:
            return {"message": f"Error sending email: {e}"}, 400

    def recovery_pass(self, data):
        email = data['email']
        password = data['password']

        user = self.session.query(User).filter(User.email == email).first()

        if not user:
            return {'message': 'User with this email does not exist'}, 400

        user.temporary_password = generate_password_hash(password)
        self.session.commit()

        reset_token = jwt.encode({
            'sub': {'email': email},
            'exp': datetime.now(timezone.utc) + timedelta(hours=1)
        }, Config.SECRET_KEY, algorithm='HS256')

        reset_link = f'{request.url_root}api/auth/recovery_pass/{reset_token}/'

        html = render_template(
            'mail_confirm.html',
            first_name=user.first_name,
            last_name=user.last_name,
            email=email,
            reset_link=reset_link
        )

        msg = {'recipients': [email], "msg": 'Password Recovery'}
        self.send_mail(msg, html)
        return user.email

    def confirm_recovery_pass(self, token: str):
        try:
            decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            email = decoded_token.get('sub').get('email')

            user = self.session.query(User).filter(User.email == email).first()

            if user and user.temporary_password:
                user.password = user.temporary_password
                user.temporary_password = None
                self.session.commit()
                return 200

            return {'message': 'Invalid or expired link'}, 400
        except jwt.ExpiredSignatureError:
            return {'message': 'Token has expired'}, 400
        except jwt.InvalidTokenError:
            return {'message': 'Invalid Token'}, 400

    def logout(self):
        user_id = g.user_id
        user = self.session.query(User).filter_by(id=user_id).first()

        if user:
            user.is_auth = False
            self.session.commit()
            return user.is_auth
        return {"message": "User not found"}, 404
