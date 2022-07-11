import os
from secrets import token_hex
from PIL import Image
from flask import url_for, current_app
from FlaskBlog import mail
from flask_mail import Message


def save_picture(form_picture):
    random_hex = token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    print(token)
    msg = Message('Password reset request',
                  sender='badrhymes@yandex.ru',
                  recipients=[user.email])
    print(f'msg{msg}')
    msg.body = f'''To reset you passsword please click the link and follow 
                                    instructions: {url_for('users.reset_token',
                                    token=token, _external=True)}. If you have
                                    not requested password change, please
                                    ignore this message.'''
    print(msg.body)
    mail.send(msg)
    print('mail sent')

