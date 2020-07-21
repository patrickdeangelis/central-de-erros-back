from django.shortcuts import render, HttpResponseRedirect
from django.conf import settings


def redirect_reset_password(request, uid, token):
    return HttpResponseRedirect(
        settings.EXTERNAL_RESET_CONFIRM_URL + "/" + uid + "/" + token + "/"
    )

