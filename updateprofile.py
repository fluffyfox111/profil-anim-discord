import requests
import base64
import os
import time
from dotenv import load_dotenv
from flask import Flask
from colorama import Fore, Style, init
import logging

# Initialisation de Colorama pour la coloration du texte dans la console
init()

load_dotenv()

# Récupération du token du bot Discord
DISCORD_BOT_TOKEN = os.getenv('TOKEN')

if not DISCORD_BOT_TOKEN:
    print(f"{Fore.RED}Error: TOKEN non défini.{Style.RESET_ALL}")
    exit()

# URLs des images et texte "About Me"
PROFILE_IMAGE_URL = "https://cdn.discordapp.com/attachments/1273650008692101181/1273663264537968683/senko.gif?ex=66bf6ed9&is=66be1d59&hm=9efe7609a031eef00343b292b9896e111bb4b208829349da1cc02f2c0cc1ce3f&"
BANNER_IMAGE_URL = "https://cdn.discordapp.com/attachments/1273650008692101181/1273663289943130172/fox-mad.gif?ex=66bf6edf&is=66be1d5f&hm=0085d34ae44aebb98eb173514bd1adf9265a6c93735aa51976e2dd3afe458304&"
ABOUT_ME_TEXT = "I'm a cool bot with a shiny new GIF profile picture!"
STATUS_TEXT = "i have a gif pfp"

# Variables booléennes pour décider quelles parties mettre à jour
UPDATE_PROFILE_IMAGE = True
UPDATE_BANNER_IMAGE = True
UPDATE_ABOUT_ME = True
UPDATE_STATUS = True

payload = {}

# Fichier utilisé pour vérifier si la mise à jour a déjà été effectuée
FLAG_FILE = 'profile_update_flag.txt'

if os.path.exists(FLAG_FILE):
    print(f"{Fore.YELLOW}Le profil a été mis à jour.{Style.RESET_ALL}")
    exit()

# Initialisation des statuts des mises à jour
banner_update_status = "Non mis à jour"
avatar_update_status = "Non mis à jour"
bio_update_status = "Non mis à jour"
status_update_status = "Non mis à jour"

# Télécharger et encoder l'image de profil en base64 si nécessaire
if UPDATE_PROFILE_IMAGE and PROFILE_IMAGE_URL:
    profile_image_response = requests.get(PROFILE_IMAGE_URL)
    if profile_image_response.status_code == 200:
        profile_image_base64 = base64.b64encode(profile_image_response.content).decode('utf-8')
        payload["avatar"] = f"data:image/gif;base64,{profile_image_base64}"
        avatar_update_status = "Succès"
    else:
        print(f"{Fore.RED}Échec du téléchargement de la photo de profil.{Style.RESET_ALL}")

# Télécharger et encoder la bannière en base64 si nécessaire
if UPDATE_BANNER_IMAGE and BANNER_IMAGE_URL:
    banner_image_response = requests.get(BANNER_IMAGE_URL)
    if banner_image_response.status_code == 200:
        banner_image_base64 = base64.b64encode(banner_image_response.content).decode('utf-8')
        payload["banner"] = f"data:image/gif;base64,{banner_image_base64}"
        banner_update_status = "Succès"
    else:
        print(f"{Fore.RED}Échec du téléchargement de la bannière.{Style.RESET_ALL}")

# Ajouter le texte "About Me" au payload si nécessaire
if UPDATE_ABOUT_ME and ABOUT_ME_TEXT:
    payload["bio"] = ABOUT_ME_TEXT
    bio_update_status = "Succès"

# Effectuer la requête de mise à jour du profil
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

# Mettre à jour le statut du bot si nécessaire
if UPDATE_STATUS and STATUS_TEXT:
    headers = {
        'Authorization': f'Bot {DISCORD_BOT_TOKEN}',
        'Content-Type': 'application/json'
    }

    status_payload = {
        "activities": [{"name": STATUS_TEXT, "type": 0}],  # 0 correspond à "Playing"
        "status": "dnd"  # Statut "Do Not Disturb"
    }

    response = requests.patch('https://discord.com/api/v10/users/@me/settings', headers=headers, json=status_payload)

    if response.status_code == 200:
        status_update_status = "Succès"
    else:
        print(f"{Fore.RED}Échec de la mise à jour du statut : {response.text}{Style.RESET_ALL}")

# Enregistrement de l'état d'exécution du script dans un fichier
with open(FLAG_FILE, 'w') as f:
    f.write('Le script de mise à jour du profil a été exécuté.')

# Création de l'application Flask pour une interface web basique
app = Flask(__name__)

@app.route('/')
def index():
    return "Le script de mise à jour du profil a été exécuté."

if __name__ == "__main__":
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    port = int(os.environ.get("PORT", 10000))

    # Affichage des statuts de mise à jour dans la console
    print(f'\n{Fore.GREEN}Banniere: {banner_update_status}{Style.RESET_ALL}')
    print(f'{Fore.GREEN}Avatar: {avatar_update_status}{Style.RESET_ALL}')
    print(f'{Fore.GREEN}About Me: {bio_update_status}{Style.RESET_ALL}')
    print(f'{Fore.GREEN}Statut: {status_update_status}{Style.RESET_ALL}')
    print(f'{Fore.GREEN}créé par NY{Style.RESET_ALL}')
    print(f'{Fore.GREEN}rejoins mon serveur discord:{Style.RESET_ALL}')
    print(f'{Fore.GREEN}https://discord.gg/aEHqZFTYGw{Style.RESET_ALL}')

    app.run(host='0.0.0.0', port=port, debug=False)
