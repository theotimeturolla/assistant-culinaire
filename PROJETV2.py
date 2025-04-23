import google.generativeai as genai
import json
import os
from typing import List, Dict, Optional
import time
from dotenv import load_dotenv

load_dotenv()

# Configuration de l'API (idéalement, la clé devrait être dans un fichier .env)
API_KEY = os.getenv('GOOGLE_GENERATIVE_AI_KEY') # À remplacer par votre clé dans un environnement sécurisé

if not API_KEY:
    raise ValueError("La clé d'API n'a pas été trouvée. Veuillez vérifier votre configuration.")

genai.configure(api_key=API_KEY)

class AssistantCulinaire:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.preferences = {
            "regime": "standard",
            "allergies": [],
            "preferences": [],
            "aversions": [],
            "nb_personnes": 1
        }
        self.historique_recettes = []
    
    def saluer_utilisateur(self) -> str:
        """Affiche un message d'accueil personnalisé"""
        print("\n" + "="*60)
        print("🍽️  ASSISTANT CULINAIRE PERSONNEL  🍽️")
        print("="*60)
        print("Bonjour ! Je suis votre assistant culinaire personnel.")
        print("Je peux vous aider à trouver des recettes avec les ingrédients")
        print("que vous avez ou créer des menus adaptés à vos préférences.")
        print("="*60 + "\n")
    
    def configurer_preferences(self) -> None:
        """Permet à l'utilisateur de configurer ses préférences culinaires"""
        print("\n📋 Configuration de vos préférences culinaires")
        
        # Nombre de personnes
        try:
            nb = int(input("Pour combien de personnes cuisinez-vous habituellement? "))
            self.preferences["nb_personnes"] = max(1, nb)
        except ValueError:
            print("Nombre invalide, je vais considérer 1 personne par défaut.")
            self.preferences["nb_personnes"] = 1
            
        # Régime alimentaire
        print("\nQuel type de régime suivez-vous?")
        regimes = ["standard", "végétarien", "végétalien", "sans gluten", "paléo", "cétogène", "autre"]
        for i, regime in enumerate(regimes, 1):
            print(f"{i}. {regime}")
        
        try:
            choix = int(input("Votre choix (numéro): "))
            if 1 <= choix <= len(regimes):
                if choix == len(regimes):  # "autre"
                    self.preferences["regime"] = input("Précisez votre régime: ")
                else:
                    self.preferences["regime"] = regimes[choix-1]
            else:
                print("Choix invalide, régime standard par défaut.")
        except ValueError:
            print("Entrée invalide, régime standard par défaut.")
            
        # Allergies
        allergies = input("\nAvez-vous des allergies alimentaires? (séparées par des virgules): ")
        if allergies.strip():
            self.preferences["allergies"] = [a.strip() for a in allergies.split(",")]
            
        # Préférences alimentaires
        preferences = input("\nQuels sont vos ingrédients ou plats préférés? (séparés par des virgules): ")
        if preferences.strip():
            self.preferences["preferences"] = [p.strip() for p in preferences.split(",")]
            
        # Aversions alimentaires
        aversions = input("\nQuels ingrédients n'aimez-vous pas? (séparés par des virgules): ")
        if aversions.strip():
            self.preferences["aversions"] = [a.strip() for a in aversions.split(",")]

        # Budget
        budget = input("\nQuel est votre budget moyen par personne pour un repas? (en euros): ")
        if budget.strip():
            self.preferences["budget"] = float(budget)
        
        # Temps de préparation
        temps = input("\nQuel est le temps de préparation maximum que vous souhaitez pour une recette? (en minutes): ") 
        if temps.strip():
            self.preferences["temps_preparation"] = int(temps)
            
        print("\n✅ Vos préférences ont été enregistrées!")
        self._afficher_resume_preferences()
    
    def _afficher_resume_preferences(self) -> None:
        """Affiche un résumé des préférences actuelles"""
        print("\n📌 Vos préférences actuelles:")
        print(f"• Nombre de personnes: {self.preferences['nb_personnes']}")
        print(f"• Régime alimentaire: {self.preferences['regime']}")
        
        if self.preferences["allergies"]:
            print(f"• Allergies: {', '.join(self.preferences['allergies'])}")
        else:
            print("• Allergies: Aucune")
            
        if self.preferences["preferences"]:
            print(f"• Préférences: {', '.join(self.preferences['preferences'])}")
        else:
            print("• Préférences: Aucune spécifiée")
            
        if self.preferences["aversions"]:
            print(f"• Aversions: {', '.join(self.preferences['aversions'])}")
        else:
            print("• Aversions: Aucune spécifiée")

        if self.preferences.get("budget"):
            print(f"• Budget moyen par personne: {self.preferences['budget']} €")
        else:
            print("• Budget moyen par personne: Non spécifié")
        
        if self.preferences.get("temps_preparation"):
            print(f"• Temps de préparation maximum: {self.preferences['temps_preparation']} minutes")
        else:
            print("• Temps de préparation maximum: Non spécifié")
    
    def generer_recette(self, ingredients: List[str]) -> str:
        """Génère une recette basée sur les ingrédients disponibles et les préférences"""
        print("\n🔍 Recherche de la meilleure recette possible...")
        
        # Construction du prompt avec les préférences
        prompt = f"""
        Génère une recette détaillée avec les ingrédients suivants: {', '.join(ingredients)}.
        
        Informations importantes:
        - Pour {self.preferences['nb_personnes']} personne(s)
        - Régime alimentaire: {self.preferences['regime']}
        """
        
        if self.preferences["allergies"]:
            prompt += f"- Allergies à éviter: {', '.join(self.preferences['allergies'])}\n"
            
        if self.preferences["aversions"]:
            prompt += f"- Ingrédients à éviter: {', '.join(self.preferences['aversions'])}\n"
            
        if self.preferences["preferences"]:
            prompt += f"- Préférences culinaires: {', '.join(self.preferences['preferences'])}\n"
        
        if self.preferences.get("budget"):
            prompt += f"- Budget moyen par personne: {self.preferences['budget']} €\n"
        
        if self.preferences.get("temps_preparation"):
            prompt += f"- Temps de préparation maximum: {self.preferences['temps_preparation']} minutes\n"  

            
        prompt += """
        Format de la recette:
        1. Nom de la recette (créatif et attractif)
        2. Temps de préparation et de cuisson
        3. Liste des ingrédients avec quantités précises
        4. Instructions détaillées étape par étape
        5. Conseils de présentation
        6. Valeurs nutritionnelles approximatives
        """
        
        try:
            # Animation de chargement
            for _ in range(3):
                print(".", end="", flush=True)
                time.sleep(0.5)
            print("\n")
            
            response = self.model.generate_content(prompt)
            recette = response.text
            
            # Enregistrement dans l'historique
            self.historique_recettes.append({
                "ingredients": ingredients,
                "recette": recette[:100] + "..." if len(recette) > 100 else recette
            })
            
            return recette
        except Exception as e:
            return f"Erreur lors de la génération de la recette: {str(e)}"
    
    def generer_menu(self, jours: int) -> str:
        """Génère un menu pour plusieurs jours en fonction des préférences"""
        print(f"\n📆 Génération d'un menu pour {jours} jours...")
        
        # Construction du prompt avec les préférences
        prompt = f"""
        Génère un menu détaillé pour {jours} jours pour {self.preferences['nb_personnes']} personne(s).
        
        Informations importantes:
        - Régime alimentaire: {self.preferences['regime']}
        """
        
        if self.preferences.get("budget"):
            prompt += f"- Budget moyen par personne: {self.preferences['budget']} €\n"
        
        if self.preferences.get("temps_preparation"):
            prompt += f"- Temps de préparation maximum: {self.preferences['temps_preparation']} minutes\n"
        
        if self.preferences["allergies"]:
            prompt += f"- Allergies à éviter: {', '.join(self.preferences['allergies'])}\n"
            
        if self.preferences["aversions"]:
            prompt += f"- Ingrédients à éviter: {', '.join(self.preferences['aversions'])}\n"
            
        if self.preferences["preferences"]:
            prompt += f"- Préférences culinaires: {', '.join(self.preferences['preferences'])}\n"
            
        prompt += """
        Format du menu:
        1. Pour chaque jour: petit-déjeuner, déjeuner, dîner (et collations éventuelles)
        2. Liste de courses complète à la fin, organisée par catégories d'aliments
        3. Estimations des coûts approximatifs du menu
        4. Conseils pour la préparation à l'avance et l'organisation
        """
        
        try:
            # Animation de chargement
            for _ in range(5):
                print(".", end="", flush=True)
                time.sleep(0.5)
            print("\n")
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Erreur lors de la génération du menu: {str(e)}"
    
    def sauvegarder_preferences(self, fichier: str = "preferences_culinaires.json") -> None:
        """Sauvegarde les préférences dans un fichier JSON"""
        try:
            with open(fichier, 'w', encoding='utf-8') as f:
                json.dump(self.preferences, f, ensure_ascii=False, indent=4)
            print(f"\n✅ Préférences sauvegardées dans {fichier}")
        except Exception as e:
            print(f"\n❌ Erreur lors de la sauvegarde des préférences: {str(e)}")
    
    def charger_preferences(self, fichier: str = "preferences_culinaires.json") -> bool:
        """Charge les préférences depuis un fichier JSON"""
        try:
            if os.path.exists(fichier):
                with open(fichier, 'r', encoding='utf-8') as f:
                    self.preferences = json.load(f)
                print(f"\n✅ Préférences chargées depuis {fichier}")
                self._afficher_resume_preferences()
                return True
            else:
                print("\nAucun fichier de préférences trouvé.")
                return False
        except Exception as e:
            print(f"\n❌ Erreur lors du chargement des préférences: {str(e)}")
            return False

def afficher_menu_principal():
    """Affiche le menu principal de l'application"""
    print("\n" + "-"*60)
    print("🍳  MENU PRINCIPAL  🍳")
    print("-"*60)
    print("1. Créer mon profil culinaire")
    print("2. Trouver une recette avec mes ingrédients")
    print("3. Générer un menu pour plusieurs jours")
    print("4. Afficher mes préférences actuelles")
    print("5. M'identifier (charger un profil)")
    print("0. Quitter")
    print("-"*60)
    return input("Votre choix? ")

def main():
    assistant = AssistantCulinaire()
    assistant.saluer_utilisateur()
    
    # Essai de chargement des préférences existantes
    assistant.charger_preferences()
    
    while True:
        choix = afficher_menu_principal()
        
        if choix == "1":
            # Configurer les préférences et sauvegarder automatiquement
            assistant.configurer_preferences()
            
            # Demander un nom de profil pour la sauvegarde
            while True:
                nom_profil = input("\n📝 Voulez-vous sauvegarder ce profil ? Entrez votre prénom (ou 'non' pour ignorer) : ")
                
                if nom_profil.lower() == 'non':
                    break
                
                if nom_profil:
                    # Ajouter l'extension .json si non présente
                    nom_fichier = nom_profil if nom_profil.endswith('.json') else f"{nom_profil}.json"
                    
                    try:
                        assistant.sauvegarder_preferences(nom_fichier)
                        print(f"✅ Profil sauvegardé sous {nom_fichier}")
                        break
                    except Exception as e:
                        print(f"❌ Erreur lors de la sauvegarde : {e}")
                else:
                    print("⚠️ Veuillez entrer un nom de profil valide.")
        
        elif choix == "2":
            print("\n🥕 Quels ingrédients avez-vous à disposition?")
            print("(séparés par des virgules, ex: poulet, riz, carottes)")
            ingredients_input = input("> ")
            if ingredients_input.strip():
                ingredients = [i.strip() for i in ingredients_input.split(",")]
                recette = assistant.generer_recette(ingredients)
                print("\n" + "="*60)
                print("🍽️  VOTRE RECETTE PERSONNALISÉE  🍽️")
                print("="*60)
                print(recette)
                print("="*60)
                
                # Option de sauvegarde
                if input("\nSouhaitez-vous sauvegarder cette recette dans un fichier? (o/n): ").lower() == 'o':
                    nom_fichier = input("Nom du fichier (sans extension): ") or "ma_recette"
                    try:
                        with open(f"{nom_fichier}.txt", 'w', encoding='utf-8') as f:
                            f.write(recette)
                        print(f"✅ Recette sauvegardée dans {nom_fichier}.txt")
                    except Exception as e:
                        print(f"❌ Erreur de sauvegarde: {str(e)}")
            else:
                print("⚠️ Veuillez spécifier au moins un ingrédient.")
        
        elif choix == "3":
            try:
                jours = int(input("\nPour combien de jours souhaitez-vous un menu? (1-14): "))
                if 1 <= jours <= 14:
                    menu = assistant.generer_menu(jours)
                    print("\n" + "="*60)
                    print(f"📆  VOTRE MENU POUR {jours} JOURS  📆")
                    print("="*60)
                    print(menu)
                    print("="*60)
                    
                    # Option de sauvegarde
                    if input("\nSouhaitez-vous sauvegarder ce menu dans un fichier? (o/n): ").lower() == 'o':
                        nom_fichier = input("Nom du fichier (sans extension): ") or "mon_menu"
                        try:
                            with open(f"{nom_fichier}.txt", 'w', encoding='utf-8') as f:
                                f.write(menu)
                            print(f"✅ Menu sauvegardé dans {nom_fichier}.txt")
                        except Exception as e:
                            print(f"❌ Erreur de sauvegarde: {str(e)}")
                else:
                    print("⚠️ Veuillez entrer un nombre de jours entre 1 et 14.")
            except ValueError:
                print("⚠️ Veuillez entrer un nombre valide.")
        
        elif choix == "4":
            assistant._afficher_resume_preferences()
        
        elif choix == "5":
    # Option pour s'identifier et charger un profil existant
            nom_profil = input("\n📂 Entrez le nom du profil à charger (sans l'extension .json) : ")
    
            if not nom_profil:
                print("⚠️ Veuillez entrer un nom de profil valide.")
            else:
        # Construire le nom de fichier
                nom_fichier = nom_profil if nom_profil.endswith('.json') else f"{nom_profil}.json"
        
        # Tenter de charger le profil
                try:
                    if assistant.charger_preferences(nom_fichier):
                        print(f"✅ Cool {nom_profil} ! Votre profil est chargé avec succès!")
                    else:
                        print(f"❌ {nom_profil}, votre profil n'existe pas.")
                        if input("Souhaitez-vous créer un nouveau profil? (o/n): ").lower() == 'o':
                            assistant.configurer_preferences()
                    # Proposer de sauvegarder sous ce nom
                            if input(f"\nSouhaitez-vous sauvegarder ce profil sous le nom '{nom_profil}'? (o/n): ").lower() == 'o':
                                assistant.sauvegarder_preferences(nom_fichier)
                                print(f"✅ Profil sauvegardé sous {nom_fichier}")
                except Exception as e:
                    print(f"❌ Erreur lors du chargement du profil: {str(e)}")
                    print("Retour au menu principal...")
        
        elif choix == "0":
            print("\n👋 Merci d'avoir utilisé l'Assistant Culinaire! À bientôt!")
            break
        
        else:
            print("⚠️ Option invalide, veuillez réessayer.")

if __name__ == "__main__":
    main()
