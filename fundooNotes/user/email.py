from django.core.mail import send_mail


class Email:

    @staticmethod
    def send_email(token, email_id):
        """
        this method is use for sending email
        :param token: jwt token
        :param email_id: sender email_id
        :return:
        """
        url = "http://127.0.0.1:8000/user/validate/" + token
        print(url)
        # send_mail(subject, message, from_email, [to_email], fail_silently=False)
        send_mail("register", url, email_id, ["dhugkar95@gmail.com"], fail_silently=False)
