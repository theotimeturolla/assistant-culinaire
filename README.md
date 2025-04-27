Assistant Culinaire - Projet Python

## 1. Présentation du projet

Ce projet a été développé dans le cadre d'un travail de groupe visant à construire une application Python fonctionnelle.  
L'objectif était de créer un assistant culinaire interactif, capable de :

- Générer des recettes adaptées aux préférences alimentaires d'un utilisateur.
- Proposer un menu personnalisé pour plusieurs jours.
- Sauvegarder et charger les préférences dans des fichiers.
- Permettre une interaction utilisateur simple via une interface graphique.

Le projet repose sur une architecture en classes claires, séparant la logique métier de l'interface utilisateur.

---

## 2. Fonctionnalités du programme

Le programme propose les fonctionnalités suivantes :

- Configuration détaillée des préférences utilisateur :
  - Nombre de personnes
  - Régime alimentaire (standard, végétarien, végan, etc.)
  - Allergies
  - Préférences spécifiques
  - Aversions alimentaires
  - Budget maximum
  - Temps maximal de préparation souhaité

- Génération automatique :
  - Une recette adaptée aux contraintes saisies
  - Un menu complet pour plusieurs jours consécutifs

- Gestion des profils utilisateurs :
  - Sauvegarde des préférences sous forme de fichiers `.json`
  - Chargement et utilisation d'un profil existant

- Export des menus :
  - Enregistrement d'un menu généré au format PDF
  
- Interface graphique conviviale avec Tkinter.

---

## 3. Technologies utilisées

- Python 3.11
- Tkinter (interface graphique)
- ReportLab (génération de PDF)

---

## 4. Installation et lancement

### a) Cloner le projet

```bash
git clone https://github.com/ton_compte/ton_projet.git
```

### b) Installer les bibliothèques nécessaires

```bash
pip install reportlab
```

Tkinter est normalement inclus d'office avec Python.

### c) Lancer l'application

```bash
python interface2.py
```

---

## 5. Utilisation de l'application

1. Lancer l'application `interface2.py`.
2. Configurer les préférences utilisateur.
3. Enregistrer les préférences sous un profil.
4. Générer une recette ou un menu.
5. Sauvegarder les résultats en format PDF si souhaité.
6. Charger un profil existant si besoin.

---

## 6. Organisation du code

Le projet est structuré en plusieurs classes principales, avec une séparation claire entre la logique métier, l'interface graphique et le point d'entrée de l'application.

### 6.1. `AssistantCulinaire`

Cette classe regroupe toute la logique métier de l'assistant culinaire. Elle est indépendante de l'interface utilisateur et peut être utilisée séparément.

**Rôles principaux :**
- Génération de recettes : propose des recettes basées sur les préférences de l'utilisateur (régime alimentaire, allergies, préférences, aversions, budget, temps de préparation).
- Création d'un menu : génère un menu complet sur plusieurs jours en respectant les contraintes définies.
- Gestion des préférences :
  - Chargement d'un profil utilisateur depuis un fichier `.json`.
  - Sauvegarde des préférences dans un fichier `.json` personnalisé.
- Stockage de l'historique : conserve l'historique des recettes proposées pour un éventuel export ou pour éviter les doublons.

Cette classe est le cœur fonctionnel du projet et peut être enrichie facilement avec de nouvelles fonctionnalités (exemple : ajout de nouvelles contraintes alimentaires).

---

### 6.2. `AssistantCulinaireGUI`

Cette classe s'occupe de toute la partie interface utilisateur à l'aide de Tkinter.

**Rôles principaux :**
- Affichage des préférences :
  - Permet à l'utilisateur de saisir son régime, ses allergies, ses préférences alimentaires, ses aversions, son budget et son temps disponible.
- Interaction :
  - Boutons pour générer une recette ou un menu.
  - Bouton pour sauvegarder ses préférences sous un profil personnalisé.
  - Bouton pour charger un profil existant.
  - Bouton pour exporter le menu en PDF.
- Affichage des résultats :
  - Présente les recettes ou menus générés dans une nouvelle fenêtre dédiée.
  - Propose un bouton pour sauvegarder le contenu généré.

**Principes de conception respectés :**
- Séparation claire entre affichage (GUI) et logique métier (`AssistantCulinaire`).
- Retour utilisateur immédiat avec affichage de boîtes de dialogue (`messagebox`) pour confirmer les actions ou signaler des erreurs.
- Utilisation d'un style simple et épuré pour l'interface.

---

### 6.3. `Application`

Cette classe représente le point d'entrée du projet.

**Rôles principaux :**
- Crée une instance de l'interface graphique (`AssistantCulinaireGUI`).
- Lance la boucle principale Tkinter (`mainloop`) pour démarrer l'interface.
- Coordonne l'ensemble des interactions utilisateur.

**Pourquoi séparer `Application` ?**
- Cela permet de centraliser le lancement du projet.
- Cela facilite les extensions futures (par exemple, ajouter un autre mode de démarrage comme un mode console).

---

### 6.4. Architecture générale (vue schématique)

```
[Application]
     ↓
[AssistantCulinaireGUI] → (affiche) → Interface graphique
     ↓
[AssistantCulinaire] → (génère) → Recettes, menus, profils
```

Chaque classe a une responsabilité bien définie, ce qui rend le projet :
- Facile à comprendre
- Facile à maintenir
- Facile à faire évoluer

---

## 7. Points techniques particuliers

- Les profils utilisateurs sont stockés sous forme de fichiers `.json`, facilitant la réutilisation et la personnalisation.
- Les menus générés sont exportés en PDF avec un formatage amélioré.
- L'application sépare clairement la logique de traitement de l'interface utilisateur.
- Des messages d'information et d'erreurs accompagnent l'utilisateur tout au long de son expérience.

---

## 8. Auteurs

Projet réalisé par :

- Lucien BAUER-EBERSPECHER, Mona GRAMDI, Théotime TUROLLA

Dans le cadre du projet Python de l'année universitaire 2024-2025.
