from django.shortcuts import render, HttpResponseRedirect
from django.conf import settings


def redirect_reset_password(request, redirect):
    return HttpResponseRedirect(settings.EXTERNAL_RESET_CONFIRM_URL + "/" + redirect)

