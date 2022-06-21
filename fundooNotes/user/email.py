from django.core.mail import send_mail


class Email:

    @staticmethod
    def send_email(token, email_id):
        url = "http://127.0.0.1:8000/user/validate/" + token
        msg = f'click on link to verify user. \n{url}'
        # send_mail(subject, message, from_email, [to_email], fail_silently=False)
        send_mail("welcome to fundoonote", msg, "Tenznz01@gmail.com", [email_id], fail_silently=False)
