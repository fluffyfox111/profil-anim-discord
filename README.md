# 🎨 Bannière/Avatar Animé,retire les status et à propos indesirables 

Bienvenue dans ce projet ! Suivez ces étapes pour personnaliser l'apparence de votre bot avec une bannière et/ou un avatar animé (et retirer les status indesirables des hebergeurs de bots gratuit tel que ghostbot ou shapes) . 🎉

## 🚀 Démarrage Rapide

1. **cloner le Projet**  
   Commencez par cloner le projet dans votre propre dépôt GitHub. 🍴

2. **Ajouter Votre Bannière/Avatar et configurer le fichier **  
   Téléchargez votre bannière et/ou avatar personnalisé dans dans discord et copier le lien. 🖼️

3. **Configurer sur Render**  
   - Allez sur [Render](https://render.com) et créez un nouveau service web. 
   - Ajoutez le lien de votre fork GitHub dans le champ du dépôt. 🔗
   - modifier le code dans la ligne 20 et 21 du code et ajouter un lien d'un gif provenant de discord 

4. **Configurer les Commandes de Build & de Démarrage**  
   - **Commande de Build :** `pip install -r requirements.txt` 
   - **Commande de Démarrage :** `python updateprofile.py` 

5. **Variables d'Environnement**  
   - Allez dans les paramètres "Environment". 🌿
   - Ajoutez une nouvelle variable :  
     - **Name :** `TOKEN`  
     - **Value :** Votre token de bot ici 🔑

6. **Déployer Votre Service Web**  
   Déployez le service web et attendez qu'il soit en ligne. 🏗️

7. **Vérifier les Changements**  
   Une fois le serveur en ligne, vérifiez le profil de votre bot pour voir si la bannière et/ou l'avatar ont été mis à jour. 🎯

8. **Nettoyage**  
   Si tout semble correct, vous pouvez supprimer le service web sur Render. 🗑️

## ❓ Dépannage

- **Vous avez une Erreur ?**  
   - Assurez-vous que le lien de votre bannière/avatar est correctement ajouté. 🖼️
   - Vérifiez que vous avez activé les intents nécessaires. 🔄
   - Vérifiez que votre token de bot est correct. 🔍
