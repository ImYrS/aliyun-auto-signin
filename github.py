import requests
from os import environ
from base64 import b64encode
from nacl import encoding, public

def encrypt(public_key, secret_value) -> str:
  """Encrypt a Unicode string using the public key."""
  public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder)
  sealed_box = public.SealedBox(public_key)
  encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
  return b64encode(encrypted).decode("utf-8")


def getpubkey(repos, token):
    url = 'https://api.github.com/repos/{}/actions/secrets/public-key'.format( repos)
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer {}'.format(token),
        'X-GitHub-Api-Version': '2022-11-28'
    }

    r = requests.get(url, headers=headers)
    return r.json()["key"], r.json()["key_id"]

def update_secret(name, value):
    repos = environ['GITHUB_REPOS']
    token = environ['GP_TOKEN']
    if token == "":
        print("未配置GP_TOKEN， 更新refresh_tokens失败")
        return
    key, key_id = getpubkey(repos, token)
    url = 'https://api.github.com/repos/{}/actions/secrets/{}'.format(repos, name)
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer {}'.format(token),
        'X-GitHub-Api-Version': '2022-11-28'
    }
    payload = {
        "encrypted_value" : encrypt(key, value),
        "key_id" : key_id
    }
    requests.put(url, headers=headers, json=payload)
