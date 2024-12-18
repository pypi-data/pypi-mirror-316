from django.apps import AppConfig
from django.core.checks import Tags, register

from django5_recaptcha_admin_login.recaptcha.captcha.checks import recaptcha_key_check


class CaptchaConfig(AppConfig):
    name = "django5_recaptcha_admin_login.recaptcha.captcha"
    verbose_name = "Django reCAPTCHA"

    def ready(self):
        register(recaptcha_key_check, Tags.security)
