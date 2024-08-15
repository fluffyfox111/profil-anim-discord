import requests
import base64
import os
import time
from dotenv import load_dotenv
from flask import Flask
from colorama import Fore, Style, init
import logging

init()

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('TOKEN')

if not DISCORD_BOT_TOKEN:
    print(f"{Fore.RED}Error: TOKEN non défini.{Style.RESET_ALL}")
    exit()
#lien du gif discord ici
PROFILE_IMAGE_URL = "lien"
BANNER_IMAGE_URL = "lien"

payload = {}

FLAG_FILE = 'profile_update_flag.txt'

if os.path.exists(FLAG_FILE):
    print(f"{Fore.YELLOW}Le profil a été mis à jour.{Style.RESET_ALL}")
    exit()

banner_update_status = "Non mis à jour"
avatar_update_status = "Non mis à jour"

if PROFILE_IMAGE_URL:
    profile_image_response = requests.get(PROFILE_IMAGE_URL)
    if profile_image_response.status_code == 200:
        profile_image_base64 = base64.b64encode(profile_image_response.content).decode('utf-8')
        payload["avatar"] = f"data:image/gif;base64,{profile_image_base64}"
        avatar_update_status = "Succès"
    else:
        print(f"{Fore.RED}Échec du téléchargement de la photo de profil.{Style.RESET_ALL}")

if BANNER_IMAGE_URL:
    banner_image_response = requests.get(BANNER_IMAGE_URL)
    if banner_image_response.status_code == 200:
        banner_image_base64 = base64.b64encode(banner_image_response.content).decode('utf-8')
        payload["banner"] = f"data:image/gif;base64,{banner_image_base64}"
        banner_update_status = "Succès"
    else:
        print(f"{Fore.RED}Échec du téléchargement de la bannière.{Style.RESET_ALL}")

if payload:
    headers = {
        'Authorization': f'Bot {DISCORD_BOT_TOKEN}',
        'Content-Type': 'application/json'
    }

    while True:
        response = requests.patch('https://discord.com/api/v10/users/@me', headers=headers, json=payload)

        if response.status_code == 200:
            break
        elif response.status_code == 429:
            retry_after = response.json().get('retry_after', 60)
            print(f"{Fore.YELLOW}Limite de débit dépassée. Réessayer après {retry_after} secondes...{Style.RESET_ALL}")
            time.sleep(retry_after)
        elif response.status_code == 401:
            print(f"{Fore.RED}TOKEN invalide. Veuillez vérifier votre TOKEN et réessayer.{Style.RESET_ALL}")
            break
        elif response.status_code == 50035:
            print(f"{Fore.RED}Limite de taux d'avatar dépassée. Réessayez plus tard.{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Échec de la mise à jour du profil et/ou de la bannière :{response.text}{Style.RESET_ALL}")
            break
else:
    print(f"{Fore.YELLOW}Aucune mise à jour à effectuer. Les URL du profil et de la bannière étaient vides.{Style.RESET_ALL}")

with open(FLAG_FILE, 'w') as f:
    f.write('Le script de mise à jour du profil a été exécuté.')

app = Flask(__name__)

@app.route('/')
def index():
    return "Le script de mise à jour du profil a été exécuté."

if __name__ == "__main__":
    # Suppress Flask's logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    port = int(os.environ.get("PORT", 10000))

    print(f'\n{Fore.GREEN}Banniere: {banner_update_status}{Style.RESET_ALL}')
    print(f'{Fore.GREEN}Avatar: {avatar_update_status}{Style.RESET_ALL}')
    print(f'{Fore.GREEN}créé par NY{Style.RESET_ALL}')
    print(f'{Fore.GREEN}rejoins mon serveur discord:https://discord.gg/aEHqZFTYGw{Style.RESET_ALL}')
    print(f'{Fore.GREEN}https://discord.gg/aEHqZFTYGw{Style.RESET_ALL}')

    app.run(host='0.0.0.0', port=port, debug=False)
