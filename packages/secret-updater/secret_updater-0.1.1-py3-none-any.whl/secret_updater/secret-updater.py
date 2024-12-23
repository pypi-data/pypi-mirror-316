import argparse
import os
from base64 import b64encode
from nacl import encoding, public
import requests



def get_public_key(environment_url, token):
    header = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28"
    }
    response = requests.get(environment_url, headers=header)
    if response.status_code != 200:
        raise Exception(f"Failed to get public key: {response.text}")
    response_json = response.json()
    return response_json["key_id"], response_json["key"]

def write_secret(update_secret_url, token, encrypted_value, public_key_id):
    header = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28"
    }
    payload = {"encrypted_value": encrypted_value, "key_id": public_key_id}
    response = requests.put(update_secret_url, headers=header, json=payload)
    if response.status_code == 201:
        print(f"Secret created in {update_secret_url}")
        return
    if response.status_code == 204:
        print(f"Secret updated for {update_secret_url}")
        return
    
    print(f"Error in updating secret, api response: \n{response}")

def encrypt(public_key: str, secret_value: str) -> str:
  """Encrypt a Unicode string using the public key."""
  public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
  sealed_box = public.SealedBox(public_key)
  encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
  return b64encode(encrypted).decode("utf-8")


def update_secret(secret, value, repo, token):
    print(f'Updating secret {secret} in repo {repo}')
    base_url = "https://api.github.com"
    public_key_url = f"{base_url}/repos/{repo}/actions/secrets/public-key"
    public_key_id, public_key = get_public_key(public_key_url, token)
    encrypted_value = encrypt(public_key, value)
    update_secret_url = f"{base_url}/repos/{repo}/actions/secrets/{secret}"
    write_secret(update_secret_url, token, encrypted_value, public_key_id)

def update_secrets_from_env_file(env_file, repo, token):
    with open(env_file, "r") as f:
        for line in f:
            if line.startswith("#"):
                continue
            if line.startswith("\n"):
                continue
            if line.startswith("export"):
                line = line[7:]
            secret_name, value = line.strip().split("=")
            if secret_name and value:
                update_secret(secret_name, value, repo, token)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update secrets in GitHub')
    parser.add_argument('--secret', type=str, help='Name of the secret to update')
    parser.add_argument('--value', type=str, help='Value of the secret to update')
    parser.add_argument('--repo', type=str, help='Name of the repo to update')
    parser.add_argument('--token', type=str, default = os.environ.get("GH_TOKEN"), help='GitHub token')
    parser.add_argument('--env-file', type=str, help='Path to the file containing secrets (recommended filename: .env)')


    args = parser.parse_args()
    try:
        if args.env_file:
            update_secrets_from_env_file(args.env_file, args.repo, args.token)
        else:
            update_secret(args.secret, args.value, args.repo, args.token)
        exit(0)
    except Exception as e:
        print(e)
        exit(1)
    