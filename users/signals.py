from django.dispatch import receiver
from django.template.loader import render_to_string
from django_rest_passwordreset.signals import reset_password_token_created

import constants
import utils


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'reset_password_url': "{}/generate-password?token={}".format(constants.SITE_URL, reset_password_token.key)
    }

    # render email html
    email_html_message = render_to_string('email_templates/user_reset_password.html', context)
    utils.send_email(subject="Password Reset for WallApp", recipient=[reset_password_token.user.email],
                     body=email_html_message)
