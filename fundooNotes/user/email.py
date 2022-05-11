from django.core.mail import send_mail

from .utils import EncodeDecodeToken


class Email:

    @staticmethod
    def send_email(data):
        """
        this method is use for sending email
        :param data:
        :return:
        """
        token = EncodeDecodeToken.encode_token(payload=data['id'])
        url = "http://127.0.0.1:8000/user/validate/" + token
        send_mail("register", url, data['email'], ["dhugkar95@gmail.com"], fail_silently=False)
