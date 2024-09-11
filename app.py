from flask import Flask, request, render_template, redirect, url_for
import os
import base64
import requests
import time
from dotenv import load_dotenv

# Initialize Flask and load environment variables
app = Flask(__name__)
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('TOKEN')

# Default values
PROFILE_IMAGE_URL = "https://cdn.discordapp.com/attachments/1273650008692101181/1273663264537968683/senko.gif?ex=66bf6ed9&is=66be1d59&hm=9efe7609a031eef00343b292b9896e111bb4b208829349da1cc02f2c0cc1ce3f&"
BANNER_IMAGE_URL = "https://cdn.discordapp.com/attachments/1273650008692101181/1273663289943130172/fox-mad.gif?ex=66bf6edf&is=66be1d5f&hm=0085d34ae44aebb98eb173514bd1adf9265a6c93735aa51976e2dd3afe458304&"
ABOUT_ME_TEXT = "I'm a cool bot with a shiny new GIF profile picture!"
STATUS_TEXT = "i have a gif pfp"

@app.route('/', methods=['GET', 'POST'])
def index():
    global PROFILE_IMAGE_URL, BANNER_IMAGE_URL, ABOUT_ME_TEXT, STATUS_TEXT, DISCORD_BOT_TOKEN
    
    if request.method == 'POST':
        # Update the variables from the form
        PROFILE_IMAGE_URL = request.form.get('profile_image_url', PROFILE_IMAGE_URL)
        BANNER_IMAGE_URL = request.form.get('banner_image_url', BANNER_IMAGE_URL)
        ABOUT_ME_TEXT = request.form.get('about_me_text', ABOUT_ME_TEXT)
        STATUS_TEXT = request.form.get('status_text', STATUS_TEXT)
        DISCORD_BOT_TOKEN = request.form.get('token', DISCORD_BOT_TOKEN)
        
        # Save the updated token to .env file (optional)
        with open('.env', 'w') as f:
            f.write(f'TOKEN={DISCORD_BOT_TOKEN}\n')
        
        update_profile()
        return redirect(url_for('index'))
    
    return render_template('index.html', 
                           profile_image_url=PROFILE_IMAGE_URL, 
                           banner_image_url=BANNER_IMAGE_URL, 
                           about_me_text=ABOUT_ME_TEXT, 
                           status_text=STATUS_TEXT, 
                           token=DISCORD_BOT_TOKEN)

def update_profile():
    payload = {}

    if PROFILE_IMAGE_URL:
        response = requests.get(PROFILE_IMAGE_URL)
        if response.status_code == 200:
            profile_image_base64 = base64.b64encode(response.content).decode('utf-8')
            payload["avatar"] = f"data:image/gif;base64,{profile_image_base64}"

    if BANNER_IMAGE_URL:
        response = requests.get(BANNER_IMAGE_URL)
        if response.status_code == 200:
            banner_image_base64 = base64.b64encode(response.content).decode('utf-8')
            payload["banner"] = f"data:image/gif;base64,{banner_image_base64}"

    if ABOUT_ME_TEXT:
        payload["bio"] = ABOUT_ME_TEXT

    headers = {
        'Authorization': f'Bot {DISCORD_BOT_TOKEN}',
        'Content-Type': 'application/json'
    }

    if payload:
        response = requests.patch('https://discord.com/api/v10/users/@me', headers=headers, json=payload)
        if response.status_code != 200:
            print(f"Failed to update profile: {response.text}")

    status_payload = {
        "activities": [{"name": STATUS_TEXT, "type": 0}],  # 0 corresponds to "Playing"
        "status": "dnd"  # "Do Not Disturb"
    }
    
    response = requests.patch('https://discord.com/api/v10/users/@me/settings', headers=headers, json=status_payload)
    if response.status_code != 200:
        print(f"Failed to update status: {response.text}")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
