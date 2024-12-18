from django.contrib.admin import sites

from .forms import AdminAuthenticationForm


class AdminSite(sites.AdminSite):
    login_form = AdminAuthenticationForm
    login_template = 'admin/recaptcha_login.html'
