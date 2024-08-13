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
    print(f"{Fore.RED}Erreur : la variable d'environnement TOKEN n'est pas définie.{Style.RESET_ALL}")
    exit()

URL_IMAGE_PROFIL = "https://tenor.com/fr/view/uwu-anime-perricoat-zorrita-chica-zorro-gif-7245679579972775597"
URL_IMAGE_BANNIÈRE = "https://tenor.com/fr/view/boop-fox-funny-animated-gif-24190579"

chargement = {}

FICHIER_DÉMARCHE = 'drapeau_mise_a_jour_profil.txt'

if os.path.exists(FICHIER_DÉMARCHE):
    print(f"{Fore.YELLOW}Le profil a déjà été mis à jour. Fin du programme.{Style.RESET_ALL}")
    exit()

statut_mise_a_jour_bannière = "Non Mis à Jour"
statut_mise_a_jour_avatar = "Non Mis à Jour"

if URL_IMAGE_PROFIL:
    reponse_image_profil = requests.get(URL_IMAGE_PROFIL)
    if reponse_image_profil.status_code == 200:
        image_profil_base64 = base64.b64encode(reponse_image_profil.content).decode('utf-8')
        chargement["avatar"] = f"data:image/gif;base64,{image_profil_base64}"
        statut_mise_a_jour_avatar = "Succès"
    else:
        print(f"{Fore.RED}Échec du téléchargement de la photo de profil.{Style.RESET_ALL}")

if URL_IMAGE_BANNIÈRE:
    reponse_image_banniere = requests.get(URL_IMAGE_BANNIÈRE)
    if reponse_image_banniere.status_code == 200:
        image_banniere_base64 = base64.b64encode(reponse_image_banniere.content).decode('utf-8')
        chargement["banner"] = f"data:image/gif;base64,{image_banniere_base64}"
        statut_mise_a_jour_bannière = "Succès"
    else:
        print(f"{Fore.RED}Échec du téléchargement de la bannière.{Style.RESET_ALL}")

if chargement:
    en_tetes = {
        'Authorization': f'Bot {DISCORD_BOT_TOKEN}',
        'Content-Type': 'application/json'
    }

    while True:
        reponse = requests.patch('https://discord.com/api/v10/users/@me', headers=en_tetes, json=chargement)

        if reponse.status_code == 200:
            break
        elif reponse.status_code == 429:
            retry_after = reponse.json().get('retry_after', 60)
            print(f"{Fore.YELLOW}Limite de taux dépassée. Nouvelle tentative après {retry_after} secondes...{Style.RESET_ALL}")
            time.sleep(retry_after)
        elif reponse.status_code == 401:
            print(f"{Fore.RED}Jeton invalide. Veuillez vérifier votre jeton et réessayer.{Style.RESET_ALL}")
            break
        elif reponse.status_code == 50035:
            print(f"{Fore.RED}Limite de taux pour l'avatar dépassée. Réessayez plus tard.{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Échec de la mise à jour du profil et/ou de la bannière : {reponse.text}{Style.RESET_ALL}")
            break
else:
    print(f"{Fore.YELLOW}Aucune mise à jour à effectuer. Les URL du profil et de la bannière étaient toutes deux vides.{Style.RESET_ALL}")

with open(FICHIER_DÉMARCHE, 'w') as f:
    f.write('Le script de mise à jour du profil a été exécuté.')

app = Flask(__name__)

@app.route('/')
def index():
    return "Le script de mise à jour du profil a été exécuté."

if __name__ == "__main__":
    # Supprimer les journaux de Flask
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    port = int(os.environ.get("PORT", 10000))

    print(f'\n{Fore.GREEN}🎨 Mise à jour de la bannière : {statut_mise_a_jour_bannière}{Style.RESET_ALL}')
    print(f'{Fore.GREEN}🎨 Mise à jour de l\'avatar : {statut_mise_a_jour_avatar}{Style.RESET_ALL}')
    print(f'{Fore.GREEN}🚀 Exécution sur le port : {port}{Style.RESET_ALL}')
    print(f'{Fore.GREEN}⚙️ Custom is alwais better{Style.RESET_ALL}')

    app.run(host='0.0.0.0', port=port, debug=False)

