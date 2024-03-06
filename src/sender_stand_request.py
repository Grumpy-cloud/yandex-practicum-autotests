import requests

from src import configuration as cfg
from src import data


# ======POST====== #
def create_new_user(body):
    requests.post(cfg.URL + cfg.CREATE_USER,
                  json=body,
                  headers=data.headers)


def create_new_kit(body, headers=data.headers):
    requests.post(cfg.URL + cfg.CREATE_KIT,
                  json=body,
                  headers=headers)
# ================ #
