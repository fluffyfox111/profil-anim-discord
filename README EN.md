# 🎨 Animated Banner/Avatar, Remove Unwanted Statuses and About

Welcome to this project! Follow these steps to customize your bot's appearance with an animated banner and/or avatar (and remove unwanted statuses from free bot hosting services like Ghostbot or Shapes). 🎉

## 🚀 Quick Start

1. **Clone the Project**  
   Start by cloning the project into your own GitHub repository. 🍴

2. **Add Your Banner/Avatar and Configure the updateprofile.py File**  
   Upload your custom banner and/or avatar to Discord and copy the link.  
   In `updateprofile.py`, set true or false if you only want to change the banner/profile/status/about section. 🖼️  
   Modify the code and add a link to a GIF from Discord.

4. **Set Up on Render**  
   - Go to [Render](https://render.com) and create a new web service.  
   - Add the link to your GitHub fork in the repository field. 🔗

5. **Configure Build & Start Commands**  
   - **Build Command:** `pip install -r requirements.txt`  
   - **Start Command:** `python updateprofile.py`

6. **Environment Variables**  
   - Go to the "Environment" settings. 🌿  
   - Add a new variable:  
     - **Name:** `TOKEN`  
     - **Value:** Your bot token here 🔑

7. **Deploy Your Web Service**  
   Deploy the web service and wait for it to go live. 🏗️

8. **Verify Changes**  
   Once the server is live, check your bot’s profile to see if the banner and/or avatar has been updated. 🎯

9. **Clean Up**  
   If everything looks good, you can delete the web service on Render. 🗑️

## ❓ Troubleshooting

- **Got an Error?**  
   - Ensure that your banner/avatar link is correctly added. 🖼️  
   - Check that you have allowed the necessary intents. 🔄  
   - Verify that your bot token is correct. 🔍
