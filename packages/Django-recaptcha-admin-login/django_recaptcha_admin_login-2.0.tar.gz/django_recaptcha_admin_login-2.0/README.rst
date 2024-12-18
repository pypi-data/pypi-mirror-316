Django Recaptcha Admin Login
============================

Features
--------

- Adds Google reCAPTCHA to the Django admin login page.
- Easy to configure and customize.
- Compatible with Django 4.2 and later.

Quick Start
-----------

1. Install the package:

   .. code-block:: bash

      pip install django5-recaptcha-admin-login

2. Add ``django5_recaptcha_admin_login.recaptcha`` and ``django5_recaptcha_admin_login.recaptcha.captcha`` to your ``INSTALLED_APPS`` in your ``settings.py``:

   .. code-block:: python

      INSTALLED_APPS = [
          ...
          "django5_recaptcha_admin_login.recaptcha",
          "django5_recaptcha_admin_login.recaptcha.captcha",
      ]

3. Add the Google reCAPTCHA keys to your settings:

   .. code-block:: python

      RECAPTCHA_PUBLIC_KEY = "your-public-key"
      RECAPTCHA_PRIVATE_KEY = "your-private-key"

4. Update your base URLs to use the custom admin:

   .. code-block:: python

      from django5_recaptcha_admin_login.recaptcha import admin

      urlpatterns = [
            path('admin/', admin.site.urls),
      ]
