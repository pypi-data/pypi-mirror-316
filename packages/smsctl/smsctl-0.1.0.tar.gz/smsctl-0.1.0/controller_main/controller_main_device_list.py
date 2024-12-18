import requests

from sms_client import settings


def controller_main_device_list():
    url = settings.url_prefix + "sms/device/list"
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception(resp.status_code)
    return resp.json()
