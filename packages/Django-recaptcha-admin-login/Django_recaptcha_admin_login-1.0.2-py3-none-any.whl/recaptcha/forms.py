from django.contrib.admin import forms

from django5_recaptcha_admin_login.recaptcha.captcha.fields import ReCaptchaField


class AdminAuthenticationForm(forms.AdminAuthenticationForm):
    captcha = ReCaptchaField()
