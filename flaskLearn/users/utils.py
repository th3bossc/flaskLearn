from flask import url_for, current_app
from flaskLearn import mail 
from flask_mail import Message
from PIL import Image 
import secrets
import os


def send_reset_email(user):
    print(user)
    token = user.get_reset_token()
    print(token)
    message = Message('PassWord Reset Request', 
                      sender = "noreply@demo.com", 
                      recipients = [user.email],
    )

    message.body = f''' To reset your password, visit the following link:
{url_for('users.reset_password', token = token, _external = True)}
The following message was intended for:
    user: {user.username}
The link expires in 30 minutes

If you didn't request a password reset, feel free to ignore this message    
'''
    mail.send(message)
    

def save_picture(form_picture):
    print(form_picture)
    random_hex = secrets.token_hex(8) 
    _, file_ext = os.path.splitext(form_picture.filename)
    save_path = os.path.join(current_app.root_path, 'static/profile_pics', random_hex + file_ext) 

    img = Image.open(form_picture)
    img.thumbnail((125, 125))
    img.save(save_path) 

    return random_hex + file_ext