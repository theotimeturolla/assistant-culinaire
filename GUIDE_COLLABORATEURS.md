# 🤝 Guide pour les collaborateurs du projet "Assistant Culinaire IA"

Bienvenue ! Ce guide a été rédigé pour vous aider à rejoindre le projet sur GitHub même si vous n’avez jamais utilisé Git, GitHub ou Python.

---

## 🧠 Pourquoi GitHub ?

GitHub est un site pour héberger du code collaboratif. Il permet de :
- Travailler ensemble sur un même projet
- Sauvegarder les modifications
- Revenir en arrière en cas d’erreur
- Ajouter des idées sans casser le code principal

---

## 📦 Ce projet : c’est quoi ?

Ce projet est un assistant culinaire IA qui :
- Pose des questions à l’utilisateur sur ses goûts
- Génère des recettes et des menus personnalisés
- Utilise l’IA Gemini de Google

---

## 👣 Étapes pour collaborer

1. Créer un compte GitHub : https://github.com/signup  
2. M’envoyer votre pseudo GitHub pour que je vous ajoute comme collaborateur (vous recevrez un mail d’invitation)  
3. Installer Git : https://git-scm.com/downloads  
   - Cliquez sur "Next" à chaque étape (config par défaut)  
4. Configurer Git (à faire une fois) :  
   git config --global user.name "Votre Nom"  
   git config --global user.email "votre@email.com"

---

## 🛠️ Installer le projet sur votre ordi

1. Cloner le projet :  
   git clone https://github.com/theotime-projet/assistant-culinaire.git  
   cd assistant-culinaire

2. Créer un environnement virtuel :  
   python -m venv venv

3. L’activer (Windows) :  
   .\venv\Scripts\Activate.ps1  
   Si ça ne marche pas :  
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

4. Installer les dépendances :  
   pip install -r requirements.txt

---

## 🔐 Obtenir une clé API Gemini (Google)

1. Aller sur : https://makersuite.google.com/app/apikey  
2. Se connecter avec un compte Google  
3. Cliquer sur "Create API key"  
4. Copier la clé générée (type AIza...)  
5. Créer un fichier .env à la racine du projet  
6. Y coller :  
   GOOGLE_GENERATIVE_AI_KEY=votre_clé_ici

⚠️ Ne partagez jamais cette clé en ligne. Elle est personnelle. Le fichier .env est protégé et ignoré par GitHub automatiquement.

---

## ▶️ Lancer le programme

Dans le terminal (après avoir activé l’environnement virtuel) :  
python PROJETV2.py

💡 Ou plus simple : double-cliquez sur le fichier run.bat  
→ Il active l’environnement automatiquement et lance le programme.

---

## 🌿 Modifier le code sans casser le projet (branches)

1. Créez une branche avant de coder :  
   git checkout -b nom-de-votre-branche  
   Exemple : git checkout -b interface-graphique

2. Modifiez le code, testez vos idées…

3. Enregistrez vos changements :  
   git add .  
   git commit -m "Ajout fonctionnalité X"

4. Envoyez votre branche sur GitHub :  
   git push origin nom-de-votre-branche

5. Allez sur GitHub → cliquez sur "Compare & pull request"  
Ajoutez un titre et une petite description → je pourrai valider les changements.

---

## 💬 Commandes Git utiles

git status → voir les fichiers modifiés  
git add nomdufichier.py → ajouter un fichier  
git add . → ajouter tous les fichiers  
git commit -m "message" → enregistrer localement  
git push → envoyer sur GitHub  
git pull → récupérer les mises à jour  
git checkout -b nouvelle-branche → créer une nouvelle branche  
git checkout main → revenir à la branche principale

---

N’hésitez pas à me demander de l’aide si vous bloquez. Bon code les chefs 👨‍🍳
