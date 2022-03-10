import hashlib
import hmac
import base64
import time
import json
import requests

from random import randint

from django.conf import settings
from rest_framework import status
from core.exceptions.exceptions import ValidateException

from .models import PhoneAuthLog
from .messages import PhoneMessages


class PhoneManager:
    def __init__(self):
        self.access_key = settings.SMS_ACCESS_KEY
        self.secret_key = settings.SMS_SECRET_KEY
        self.uri = f"/sms/v2/services/{settings.SMS_SERVICE_ID}/messages"

    def make_auth_number(self):
        """Create random auth number(10000~99999)"""
        auth_num = randint(10000, 99999)
        return auth_num

    def make_signature(self):
        """Encrypted signature with secert key"""
        timestamp = str(int(time.time() * 1000))
        access_key = f"{settings.SMS_ACCESS_KEY}"
        secret_key = f"{settings.SMS_SECRET_KEY}"
        secret_key = bytes(secret_key, "UTF-8")

        method = "POST"

        message = method + " " + self.uri + "\n" + timestamp + "\n" + access_key
        message = bytes(message, "UTF-8")
        signingKey = base64.b64encode(
            hmac.new(secret_key, message, digestmod=hashlib.sha256).digest()
        )
        return signingKey

    def send_sms(self, phone_num):
        """Call SMS api(SENS: Naver Cloud)"""
        timestamp = str(int(time.time() * 1000))
        signing_key = self.make_signature()
        auth_num = self.make_auth_number()
        sms_url = settings.SMS_URL + self.uri

        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "x-ncp-apigw-timestamp": timestamp,
            "x-ncp-iam-access-key": f"{settings.SMS_ACCESS_KEY}",
            "x-ncp-apigw-signature-v2": signing_key,
        }

        body = {
            "type": "SMS",
            "contentType": "COMM",
            "countryCode": "82",
            "from": settings.CUSTOMER_SERIVCE_NUMBER,
            "content": PhoneMessages.SMS_AUTH_COMMENT.format(auth_num),
            "messages": [{"to": f"{phone_num}"}],
        }

        encoded_data = json.dumps(body)
        res = requests.post(sms_url, headers=headers, data=encoded_data)

        if res.status_code == status.HTTP_202_ACCEPTED:
            PhoneAuthLog.objects.create(auth_num=auth_num, phone_num=phone_num)
        else:
            raise ValidateException(PhoneMessages.SMS_SEND_ERROR)
