# 🤝 Guide pour les collaborateurs du projet "Assistant Culinaire IA"

Bienvenue ! Ce guide a été rédigé pour vous aider à rejoindre le projet sur GitHub même si vous n’avez jamais utilisé Git ou GitHub

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

### 5. Créer un fichier `.env` (à la racine du projet)

Contenu du fichier :

GOOGLE_GENERATIVE_AI_KEY=ma_clé_personnelle

(Demandez-moi votre clé si vous ne l'avez pas.)

---

## ▶️ Lancer le programme

Dans le terminal, toujours dans le dossier du projet :

python PROJETV2.py

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
