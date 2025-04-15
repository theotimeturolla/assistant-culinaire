# 🤝 Guide pour les collaborateurs du projet "Assistant Culinaire IA"

Bienvenue ! Ce guide a été rédigé pour vous aider à rejoindre le projet sur GitHub même si vous n’avez **jamais utilisé Git, GitHub ou Python**.

---

## 🧠 Pourquoi GitHub ?

GitHub est un site pour héberger du **code collaboratif**. Il permet de :
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

### 1. Créer un compte GitHub

👉 https://github.com/signup

### 2. M’envoyer votre pseudo GitHub pour que je vous ajoute comme **collaborateur**  
(Vous recevrez un mail d’invitation à accepter)

### 3. Installer Git

- Télécharger : https://git-scm.com/downloads
- Installer en cliquant sur "Next" à chaque étape (configuration par défaut)

### 4. Configurer Git (une seule fois)

Ouvrir un terminal (cmd ou PowerShell), puis :

git config --global user.name "Votre Nom"  
git config --global user.email "votre@email.com"

---

## 🛠️ Installer le projet sur votre ordi

### 1. Cloner le projet depuis GitHub

git clone https://github.com/theotime-projet/assistant-culinaire.git  
cd assistant-culinaire

### 2. Créer un environnement virtuel

python -m venv venv

### 3. L’activer (Windows)

.\venv\Scripts\Activate.ps1

(Si ça ne marche pas :)

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

### 4. Installer les dépendances

pip install -r requirements.txt

---

## 🔐 Comment obtenir une clé API Gemini (Google)

Pour utiliser l’assistant culinaire, il faut une **clé API** personnelle de Google. C’est cette clé qui donne accès au modèle d’IA (Gemini) dans le code.

### Étapes pour créer une clé :

1. Aller sur la page officielle de l'API Gemini :  
👉 https://makersuite.google.com/app/apikey

2. Se connecter avec un compte Google

3. Cliquer sur **"Create API key"** (ou "Créer une clé API")

4. Copier la clé générée (ressemble à `AIza...`)

5. Ouvrir VS Code et créer un fichier `.env` à la racine du projet  
(clic droit → Nouveau fichier → `.env`)

6. Y coller ceci (en remplaçant par votre propre clé) :

GOOGLE_GENERATIVE_AI_KEY=votre_clé_ici

💡 Ce fichier sert à **protéger la clé** : elle ne sera pas visible sur GitHub grâce au `.gitignore`.

🎯 Pourquoi cette clé est nécessaire ?

Elle permet au programme de se connecter à l'IA de Google pour **générer des recettes intelligentes**. Sans cette clé, le programme ne peut pas fonctionner.

❗ Attention : **ne partagez jamais votre clé en ligne** (ni sur GitHub, ni sur Discord). Elle est personnelle.

---

## ▶️ Lancer le programme

Dans le terminal, toujours dans le dossier du projet :

python PROJETV2.py

Ou simplement **double-cliquer sur le fichier `run.bat`** une fois que tout est prêt !

---

## 💬 Commandes Git utiles

Action : Commande  
- Vérifier les fichiers modifiés : git status  
- Ajouter des fichiers à valider : git add nom_du_fichier.py  
- Sauvegarder les changements : git commit -m "Votre message"  
- Envoyer les modifs sur GitHub : git push  
- Récupérer les modifs des autres : git pull

---

N’hésitez pas à me demander de l’aide si vous bloquez sur une étape 🙌  
Bon codage 👨‍🍳 !
