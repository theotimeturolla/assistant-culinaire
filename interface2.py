import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, font
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
from typing import List
from PIL import Image, ImageTk
import webbrowser
from datetime import datetime
import tkinter.filedialog as filedialog
from reportlab.pdfgen import canvas
import tempfile
import os

# Charger la clé API
load_dotenv()
API_KEY = os.getenv('GOOGLE_GENERATIVE_AI_KEY')

if not API_KEY:
    raise ValueError("La clé d'API n'a pas été trouvée. Veuillez vérifier votre configuration.")

genai.configure(api_key=API_KEY)

# Définition des couleurs et du thème
COULEURS = {
    "primary": "#FF6B6B",        # Rouge corail
    "secondary": "#4ECDC4",      # Turquoise
    "accent": "#FFD166",         # Jaune doré
    "dark": "#292F36",           # Gris foncé
    "light": "#F7FFF7",          # Blanc cassé
    "success": "#6BCB77",        # Vert menthe
    "warning": "#FFD166",        # Jaune
    "error": "#FF6B6B",          # Rouge
    "text_dark": "#292F36",      # Couleur de texte foncée
    "text_light": "#F7FFF7"      # Couleur de texte claire
}

class CustomStyle:
    """Classe pour gérer le style personnalisé de l'application"""
    @staticmethod
    def apply_style():
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configuration des styles généraux
        style.configure('TFrame', background=COULEURS["light"])
        style.configure('TLabel', background=COULEURS["light"], foreground=COULEURS["text_dark"], font=('Helvetica', 10))
        style.configure('TButton', background=COULEURS["primary"], foreground=COULEURS["text_light"], 
                      font=('Helvetica', 10, 'bold'), borderwidth=1, focusthickness=3, focuscolor='none')
        style.map('TButton', 
              background=[('active', COULEURS["primary"]), ('pressed', COULEURS["dark"])],
              foreground=[('pressed', COULEURS["text_light"]), ('active', COULEURS["text_light"])])
        
        # Style pour les titres
        style.configure('Title.TLabel', font=('Helvetica', 18, 'bold'), foreground=COULEURS["primary"])
        
        # Style pour les boutons d'action
        style.configure('Action.TButton', background=COULEURS["secondary"], foreground=COULEURS["text_light"])
        style.map('Action.TButton', 
                background=[('active', COULEURS["accent"]), ('pressed', COULEURS["dark"])])
        
        # Style pour les boutons de menu
        style.configure('Menu.TButton', background=COULEURS["dark"], foreground=COULEURS["text_light"])
        style.map('Menu.TButton',
                background=[('active', COULEURS["primary"]), ('pressed', COULEURS["primary"])])
                
        # Style pour les champs de saisie
        style.configure('TEntry', foreground=COULEURS["text_dark"], fieldbackground=COULEURS["light"])
        
        # Style pour les combobox
        style.configure('TCombobox', foreground=COULEURS["text_dark"], fieldbackground=COULEURS["light"])
        
        # Style pour le menu des options
        style.configure('Option.TLabel', background=COULEURS["secondary"], foreground=COULEURS["text_light"], 
                        font=('Helvetica', 10, 'bold'), padding=5)

class TooltipManager:
    """Gestionnaire d'infobulles pour les widgets"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        
        widget.bind("<Enter>", self.on_enter)
        widget.bind("<Leave>", self.on_leave)
    
    def on_enter(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = ttk.Label(self.tooltip, text=self.text, justify=tk.LEFT,
                        background=COULEURS["dark"], foreground=COULEURS["text_light"],
                        relief="solid", borderwidth=1, padding=(5, 3))
        label.pack()
    
    def on_leave(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class AssistantCulinaireGUI:
    """Version graphique de l'assistant culinaire"""
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.preferences = {
            "regime": "standard",
            "allergies": [],
            "preferences": [],
            "aversions": [],
            "nb_personnes": 1,
            "budget": None,
            "temps_preparation": None
        }
        self.historique_recettes = []
    
    def saluer_utilisateur(self) -> str:
        """Retourne un message d'accueil personnalisé"""
        heure = datetime.now().hour
        if 5 <= heure < 12:
            salutation = "Bonjour"
        elif 12 <= heure < 18:
            salutation = "Bon après-midi"
        else:
            salutation = "Bonsoir"
            
        return f"{salutation} ! Je suis votre assistant culinaire personnel.\nJe peux vous aider à trouver des recettes avec les ingrédients que vous avez ou créer des menus adaptés à vos préférences."
    
    def configurer_preferences(self, root):
        """Configure les préférences via des boîtes de dialogue graphiques"""
        # Fenêtre de configuration des préférences
        pref_window = tk.Toplevel(root)
        pref_window.title("Configuration des préférences")
        pref_window.geometry("600x700")
        pref_window.resizable(False, False)
        pref_window.configure(background=COULEURS["light"])
        
        # Icône de la fenêtre si disponible
        try:
            pref_window.iconbitmap("cuisine_icon.ico")
        except:
            pass
        
        # Titre principal
        titre_frame = ttk.Frame(pref_window)
        titre_frame.pack(fill=tk.X, padx=20, pady=20)
        
        titre_label = ttk.Label(titre_frame, text="Personnalisez votre expérience culinaire", style="Title.TLabel")
        titre_label.pack()
        
        soustitre = ttk.Label(titre_frame, text="Configurez vos préférences pour des suggestions adaptées à vos goûts")
        soustitre.pack(pady=5)
        
        # Ligne de séparation
        separator = ttk.Separator(pref_window, orient='horizontal')
        separator.pack(fill=tk.X, padx=20)
        
        # Cadre principal avec scrollbar
        canvas = tk.Canvas(pref_window, background=COULEURS["light"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(pref_window, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)
        
        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y", pady=20)
        
        # ===== Formulaire de préférences =====
        # Nombre de personnes
        nb_frame = ttk.Frame(scroll_frame)
        nb_frame.pack(fill=tk.X, pady=10)
        
        nb_label = ttk.Label(nb_frame, text="Nombre de personnes:", width=25, anchor="w")
        nb_label.pack(side=tk.LEFT, padx=5)
        
        nb_personnes_var = tk.StringVar(value=str(self.preferences["nb_personnes"]))
        nb_spinbox = ttk.Spinbox(nb_frame, from_=1, to=20, textvariable=nb_personnes_var, width=5)
        nb_spinbox.pack(side=tk.LEFT, padx=5)
        
        TooltipManager(nb_label, "Pour combien de personnes cuisinez-vous généralement?")
        
        # Régime alimentaire
        regime_frame = ttk.Frame(scroll_frame)
        regime_frame.pack(fill=tk.X, pady=10)
        
        regime_label = ttk.Label(regime_frame, text="Régime alimentaire:", width=25, anchor="w")
        regime_label.pack(side=tk.LEFT, padx=5)
        
        regimes = ["standard", "végétarien", "végétalien", "sans gluten", "paléo", "cétogène", "autre"]
        regime_var = tk.StringVar(value=self.preferences["regime"])
        regime_dropdown = ttk.Combobox(regime_frame, textvariable=regime_var, values=regimes, width=15)
        regime_dropdown.pack(side=tk.LEFT, padx=5)
        
        TooltipManager(regime_label, "Quel type de régime suivez-vous?")
        
        # Allergies
        allergies_frame = ttk.Frame(scroll_frame)
        allergies_frame.pack(fill=tk.X, pady=10)
        
        allergies_label = ttk.Label(allergies_frame, text="Allergies alimentaires:", width=25, anchor="w")
        allergies_label.pack(side=tk.LEFT, padx=5)
        
        allergies_var = tk.StringVar(value=", ".join(self.preferences["allergies"]))
        allergies_entry = ttk.Entry(allergies_frame, textvariable=allergies_var, width=30)
        allergies_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        TooltipManager(allergies_label, "Entrez vos allergies alimentaires séparées par des virgules")
        
        # Préférences alimentaires
        preferences_frame = ttk.Frame(scroll_frame)
        preferences_frame.pack(fill=tk.X, pady=10)
        
        preferences_label = ttk.Label(preferences_frame, text="Ingrédients préférés:", width=25, anchor="w")
        preferences_label.pack(side=tk.LEFT, padx=5)
        
        preferences_var = tk.StringVar(value=", ".join(self.preferences["preferences"]))
        preferences_entry = ttk.Entry(preferences_frame, textvariable=preferences_var, width=30)
        preferences_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        TooltipManager(preferences_label, "Entrez vos ingrédients ou plats préférés séparés par des virgules")
        
        # Aversions alimentaires
        aversions_frame = ttk.Frame(scroll_frame)
        aversions_frame.pack(fill=tk.X, pady=10)
        
        aversions_label = ttk.Label(aversions_frame, text="Ingrédients à éviter:", width=25, anchor="w")
        aversions_label.pack(side=tk.LEFT, padx=5)
        
        aversions_var = tk.StringVar(value=", ".join(self.preferences["aversions"]))
        aversions_entry = ttk.Entry(aversions_frame, textvariable=aversions_var, width=30)
        aversions_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        TooltipManager(aversions_label, "Entrez les ingrédients que vous n'aimez pas séparés par des virgules")
        
        # Budget
        budget_frame = ttk.Frame(scroll_frame)
        budget_frame.pack(fill=tk.X, pady=10)
        
        budget_label = ttk.Label(budget_frame, text="Budget par personne (€):", width=25, anchor="w")
        budget_label.pack(side=tk.LEFT, padx=5)
        
        budget_var = tk.StringVar(value=str(self.preferences.get("budget", "")))
        budget_entry = ttk.Entry(budget_frame, textvariable=budget_var, width=10)
        budget_entry.pack(side=tk.LEFT, padx=5)
        
        TooltipManager(budget_label, "Quel est votre budget moyen par personne pour un repas?")
        
        # Temps de préparation
        temps_frame = ttk.Frame(scroll_frame)
        temps_frame.pack(fill=tk.X, pady=10)
        
        temps_label = ttk.Label(temps_frame, text="Temps max. de préparation (min):", width=25, anchor="w")
        temps_label.pack(side=tk.LEFT, padx=5)
        
        temps_var = tk.StringVar(value=str(self.preferences.get("temps_preparation", "")))
        temps_entry = ttk.Entry(temps_frame, textvariable=temps_var, width=10)
        temps_entry.pack(side=tk.LEFT, padx=5)
        
        TooltipManager(temps_label, "Quel est le temps de préparation maximum que vous souhaitez?")
        
        # Ligne de séparation
        separator2 = ttk.Separator(scroll_frame, orient='horizontal')
        separator2.pack(fill=tk.X, pady=20)
        
        # Zone d'information
        info_frame = ttk.Frame(scroll_frame, padding=10)
        info_frame.pack(fill=tk.X, pady=10)
        
        info_text = "💡 Ces préférences seront utilisées pour personnaliser vos recettes et menus.\nVous pourrez les modifier à tout moment."
        info_label = ttk.Label(info_frame, text=info_text, foreground=COULEURS["secondary"], justify=tk.LEFT)
        info_label.pack(fill=tk.X)
        
        # Boutons d'action
        buttons_frame = ttk.Frame(scroll_frame)
        buttons_frame.pack(fill=tk.X, pady=20)
        
        # Fonction pour sauvegarder les préférences
        def save_preferences():
            try:
                self.preferences["nb_personnes"] = max(1, int(nb_personnes_var.get()))
            except ValueError:
                self.preferences["nb_personnes"] = 1
                
            self.preferences["regime"] = regime_var.get()
            
            allergies = allergies_var.get().strip()
            self.preferences["allergies"] = [a.strip() for a in allergies.split(",")] if allergies else []
            
            prefs = preferences_var.get().strip()
            self.preferences["preferences"] = [p.strip() for p in prefs.split(",")] if prefs else []
            
            aversions = aversions_var.get().strip()
            self.preferences["aversions"] = [a.strip() for a in aversions.split(",")] if aversions else []
            
            try:
                budget = budget_var.get().strip()
                self.preferences["budget"] = float(budget) if budget else None
            except ValueError:
                self.preferences["budget"] = None
                
            try:
                temps = temps_var.get().strip()
                self.preferences["temps_preparation"] = int(temps) if temps else None
            except ValueError:
                self.preferences["temps_preparation"] = None

            # On demande maintenant le nom du fichier AVANT de fermer la fenêtre
            filename = simpledialog.askstring("Nom du profil", "Sous quel nom souhaitez-vous enregistrer vos préférences ?")
            if filename:
                filename = filename.strip()
                if not filename.endswith('.json'):
                    filename += ".json"
                try:
                    self.sauvegarder_preferences(filename)
                    messagebox.showinfo("Sauvegarde réussie", f"Préférences sauvegardées sous {filename}")
                    pref_window.destroy()
                except Exception as e:
                    messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde : {str(e)}")
            else:
                messagebox.showwarning("Aucun nom saisi", "Les préférences n'ont pas été sauvegardées.")


        # Bouton d'annulation
        cancel_button = ttk.Button(buttons_frame, text="Annuler", command=pref_window.destroy)
        cancel_button.pack(side=tk.LEFT, padx=10)
        
        # Bouton de sauvegarde
        save_button = ttk.Button(buttons_frame, text="Enregistrer", command=save_preferences, style="Action.TButton")
        save_button.pack(side=tk.RIGHT, padx=10)
    
    def generer_recette(self, ingredients: List[str]) -> str:
        """Génère une recette basée sur les ingrédients disponibles et les préférences"""
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
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Erreur lors de la génération du menu: {str(e)}"
    
    def sauvegarder_preferences(self, filename):
        """Sauvegarder les préférences sous un nom choisi par l'utilisateur."""
        if filename:
            filename = filename.strip()
            if not filename.endswith('.json'):
                filename += ".json"
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.preferences, f, ensure_ascii=False, indent=4)
                messagebox.showinfo("Sauvegarde réussie", f"Préférences sauvegardées sous {filename}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde : {str(e)}")
        else:
            messagebox.showwarning("Aucun nom saisi", "Les préférences n'ont pas été sauvegardées.")


    def charger_preferences(self, fichier: str = "preferences_culinaires.json") -> bool:
        """Charge les préférences depuis un fichier JSON"""
        try:
            if os.path.exists(fichier):
                with open(fichier, 'r', encoding='utf-8') as f:
                    self.preferences = json.load(f)
                return True
            else:
                messagebox.showwarning("Fichier non trouvé", "Aucun fichier de préférences trouvé.")
                return False
        except Exception as e:
            messagebox.showerror("Erreur de chargement", f"Erreur lors du chargement des préférences: {str(e)}")
            return False

class HoverButton(tk.Button):
    """Bouton avec effet de survol"""
    def __init__(self, master, **kw):
        self.default_bg = kw.get('background', 'SystemButtonFace')
        self.hover_bg = kw.get('activebackground', 'SystemButtonFace')
        tk.Button.__init__(self, master, **kw)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self.hover_bg

    def on_leave(self, e):
        self['background'] = self.default_bg

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Chef Assistant - Votre compagnon culinaire")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
        
        # Définir les couleurs et les styles
        CustomStyle.apply_style()
        
        # Créer une instance de l'assistant culinaire
        self.assistant = AssistantCulinaireGUI()
        
        # Icône de l'application si disponible
        try:
            self.root.iconbitmap("cuisine_icon.ico")
        except:
            pass
            
        # Création des images (placeholder si l'image n'existe pas)
        try:
            self.logo_img = ImageTk.PhotoImage(Image.open("logo_cuisine.png").resize((100, 100)))
        except:
            self.logo_img = None
        
        # Couleur d'arrière-plan principale
        self.root.configure(background=COULEURS["light"])
        
        # Création de l'interface
        self.create_widgets()
        
        # Charger les préférences au démarrage si le fichier existe
        try:
            if os.path.exists("preferences_culinaires.json"):
                self.assistant.charger_preferences("preferences_culinaires.json")
        except:
            pass

    def create_widgets(self):
        """Créer tous les éléments de l'interface"""
        # Utiliser un PanedWindow pour créer une interface divisée
        self.main_pane = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True)
        
        # Créer le panneau de gauche (menu)
        self.left_frame = ttk.Frame(self.main_pane, style='TFrame')
        self.left_frame.pack(fill=tk.BOTH, expand=False)
        
        # Créer le panneau de droite (contenu principal)
        self.right_frame = ttk.Frame(self.main_pane)
        self.right_frame.pack(fill=tk.BOTH, expand=True)
        
        # Ajouter les panneaux au PanedWindow
        self.main_pane.add(self.left_frame, weight=1)
        self.main_pane.add(self.right_frame, weight=4)
        
        # === PANNEAU DE GAUCHE (MENU) ===
        self.left_frame.configure(padding=(10, 10, 10, 10))
        
        # Logo et titre
        if self.logo_img:
            logo_label = ttk.Label(self.left_frame, image=self.logo_img, background=COULEURS["light"])
            logo_label.pack(pady=10)
        
        title_label = ttk.Label(self.left_frame, text="Chef Assistant", style="Title.TLabel")
        title_label.pack(pady=5)
        subtitle_label = ttk.Label(self.left_frame, text="Votre compagnon culinaire", foreground=COULEURS["secondary"])
        subtitle_label.pack(pady=(0, 20))
        
        # Séparateur
        separator = ttk.Separator(self.left_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=10)
        
        # Menu de navigation
        menu_frame = ttk.Frame(self.left_frame)
        menu_frame.pack(fill=tk.X, pady=10)
        
        # Boutons de menu avec icônes (textuelles en attendant les vraies icônes)
        buttons_data = [
            ("🏠 Accueil", self.saluer_utilisateur),
            ("⚙️ Préférences", self.configurer_preferences),
            ("🍽️ Générer recette", self.generer_recette),
            ("📋 Générer menu", self.generer_menu),
            ("👤 Mes préférences", self.afficher_preferences),
            ("📂 S'identifier", self.charger_preferences)
        ]
        
        # Création des boutons de menu
        self.menu_buttons = []
        for text, command in buttons_data:
            btn = HoverButton(menu_frame, text=text, command=command,
                           background=COULEURS["dark"], foreground=COULEURS["text_light"],
                           activebackground=COULEURS["primary"], activeforeground=COULEURS["text_light"],
                           relief=tk.FLAT, borderwidth=0, 
                           font=('Helvetica', 10),
                           width=20, height=2)
            btn.pack(fill=tk.X, pady=5)
            self.menu_buttons.append(btn)
        
        # Informations en bas du menu
        footer_frame = ttk.Frame(self.left_frame)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        version_label = ttk.Label(footer_frame, text="Version 1.0", font=('Helvetica', 8), foreground=COULEURS["dark"])
        version_label.pack(side=tk.BOTTOM)
        
        # === PANNEAU DE DROITE (CONTENU PRINCIPAL) ===
        # Accueil / Zone de bienvenue
        self.content_frame = ttk.Frame(self.right_frame, padding=(20, 20, 20, 20))
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre de bienvenue
        welcome_frame = ttk.Frame(self.content_frame)
        welcome_frame.pack(fill=tk.X, pady=20)
        
        welcome_title = ttk.Label(welcome_frame, text="Bienvenue dans votre assistant culinaire", 
                                style="Title.TLabel", font=('Helvetica', 22, 'bold'))
        welcome_title.pack()
        
        welcome_subtitle = ttk.Label(welcome_frame, 
                                  text="Découvrez des recettes personnalisées et des menus sur mesure",
                                  font=('Helvetica', 12))
        welcome_subtitle.pack(pady=5)
        
        # Séparateur
        separator2 = ttk.Separator(self.content_frame, orient='horizontal')
        separator2.pack(fill=tk.X, pady=10)
        
        # Contenu principal - Cartes des fonctionnalités
        cards_frame = ttk.Frame(self.content_frame)
        cards_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Configurer un grid layout pour les cartes
        cards_frame.columnconfigure(0, weight=1)
        cards_frame.columnconfigure(1, weight=1)
        cards_frame.rowconfigure(0, weight=1)
        cards_frame.rowconfigure(1, weight=1)
        
        # Créer les cartes de fonctionnalités
        self.create_feature_card(cards_frame, 0, 0, "Recettes personnalisées", 
                              "Trouvez des recettes avec les ingrédients que vous avez sous la main.",
                              "🍽️", self.generer_recette)
                              
        self.create_feature_card(cards_frame, 0, 1, "Menus hebdomadaires", 
                              "Créez des menus équilibrés pour toute la semaine.",
                              "📋", self.generer_menu)
                              
        self.create_feature_card(cards_frame, 1, 0, "Préférences alimentaires", 
                              "Personnalisez vos préférences pour des recommandations adaptées.",
                              "⚙️", self.configurer_preferences)
        self.create_feature_card(cards_frame, 1, 1, "Sauvegarde de recettes", 
                              "Enregistrez vos recettes préférées pour les consulter plus tard.",
                              "💾", lambda: messagebox.showinfo("En développement", "Cette fonctionnalité sera disponible prochainement!"))                            
        # Pied de page
        footer_main = ttk.Frame(self.content_frame)
        footer_main.pack(fill=tk.X, side=tk.BOTTOM, pady=10)
        
        footer_text = ttk.Label(footer_main, text="Commencez par configurer vos préférences pour une expérience personnalisée.", 
                             foreground=COULEURS["secondary"])
        footer_text.pack(side=tk.LEFT)
        
        help_btn = ttk.Button(footer_main, text="Aide", width=8, command=self.afficher_aide)
        help_btn.pack(side=tk.RIGHT)
    
    def create_feature_card(self, parent, row, col, title, description, icon, command):
        """Crée une carte de fonctionnalité avec un style uniforme"""
        # Cadre de la carte
        card = ttk.Frame(parent, relief="raised", borderwidth=1)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Style de la carte
        card.configure(style='TFrame')
        
        # Contenu de la carte
        icon_label = ttk.Label(card, text=icon, font=('Helvetica', 24), foreground=COULEURS["primary"])
        icon_label.pack(pady=(20, 10))
        
        title_label = ttk.Label(card, text=title, font=('Helvetica', 14, 'bold'))
        title_label.pack(pady=(0, 10))
        
        desc_label = ttk.Label(card, text=description, wraplength=200, justify=tk.CENTER)
        desc_label.pack(pady=(0, 20), padx=15)
        
        # Bouton d'action
        action_btn = ttk.Button(card, text="Utiliser", command=command, style="Action.TButton")
        action_btn.pack(pady=(0, 20))

    def saluer_utilisateur(self):
        """Afficher un message de bienvenue dans une fenêtre stylisée"""
        # Fenêtre de bienvenue
        welcome_window = tk.Toplevel(self.root)
        welcome_window.title("Bienvenue")
        welcome_window.geometry("500x300")
        welcome_window.configure(background=COULEURS["light"])
        welcome_window.resizable(False, False)
        
        try:
            welcome_window.iconbitmap("cuisine_icon.ico")
        except:
            pass
        
        # Titre
        title_frame = ttk.Frame(welcome_window)
        title_frame.pack(fill=tk.X, pady=20)
        
        if self.logo_img:
            logo_small = self.logo_img.subsample(2, 2)  # Réduire la taille du logo
            logo_label = ttk.Label(title_frame, image=logo_small, background=COULEURS["light"])
            logo_label.image = logo_small  # Garder une référence
            logo_label.pack()
        
        title_label = ttk.Label(title_frame, text="Chef Assistant", style="Title.TLabel")
        title_label.pack(pady=10)
        
        # Message
        message_frame = ttk.Frame(welcome_window, padding=20)
        message_frame.pack(fill=tk.BOTH, expand=True)
        
        message_text = self.assistant.saluer_utilisateur()
        message_label = ttk.Label(message_frame, text=message_text, wraplength=400, 
                               justify=tk.CENTER, font=('Helvetica', 12))
        message_label.pack(fill=tk.BOTH, expand=True)
        
        # Bouton de fermeture
        btn_frame = ttk.Frame(welcome_window)
        btn_frame.pack(fill=tk.X, pady=20)
        
        close_btn = ttk.Button(btn_frame, text="Commencer", command=welcome_window.destroy,
                            style="Action.TButton", width=15)
        close_btn.pack()
        
        # Centrer la fenêtre sur l'écran
        welcome_window.update_idletasks()
        width = welcome_window.winfo_width()
        height = welcome_window.winfo_height()
        x = (welcome_window.winfo_screenwidth() // 2) - (width // 2)
        y = (welcome_window.winfo_screenheight() // 2) - (height // 2)
        welcome_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Rendre modale
        welcome_window.transient(self.root)
        welcome_window.grab_set()
        self.root.wait_window(welcome_window)

    def configurer_preferences(self):
        """Ouvrir la fenêtre de configuration des préférences"""
        self.assistant.configurer_preferences(self.root)

    def afficher_loader(self, message="Génération en cours..."):
        """Affiche une fenêtre d'attente animée"""
        loader = tk.Toplevel(self.root)
        loader.title("Chargement")
        loader.geometry("400x150")
        loader.configure(background=COULEURS["light"])
        loader.resizable(False, False)
        
        try:
            loader.iconbitmap("cuisine_icon.ico")
        except:
            pass
        
        # Centrer la fenêtre
        loader.update_idletasks()
        width = loader.winfo_width()
        height = loader.winfo_height()
        x = (loader.winfo_screenwidth() // 2) - (width // 2)
        y = (loader.winfo_screenheight() // 2) - (height // 2)
        loader.geometry(f'{width}x{height}+{x}+{y}')
        
        # Contenu
        frame = ttk.Frame(loader, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        msg_label = ttk.Label(frame, text=message, 
                          wraplength=350, justify=tk.CENTER, 
                          font=('Helvetica', 12))
        msg_label.pack(pady=10)
        
        # Barre de progression animée
        progress = ttk.Progressbar(frame, mode='indeterminate', length=300)
        progress.pack(pady=20)
        progress.start(10)
        
        # Rendre modale
        loader.transient(self.root)
        loader.grab_set()
        
        # Mettre à jour l'interface
        loader.update()
        
        return loader

    def generer_recette(self):
        """Générer une recette à partir des ingrédients"""
        ingredients = simpledialog.askstring("Ingrédients", 
                                         "Entrez vos ingrédients séparés par des virgules:")
        if not ingredients:
            return
            
        ingredients_list = [ingredient.strip() for ingredient in ingredients.split(",")]
        
        # Afficher un loader
        loader = self.afficher_loader("Génération de votre recette personnalisée en cours...\nVeuillez patienter.")
        
        # Mettre à jour l'interface pour afficher le loader
        self.root.update()
        
        # Générer la recette
        recette = self.assistant.generer_recette(ingredients_list)
        
        # Fermer le loader
        loader.destroy()
        
        # Afficher la recette dans une fenêtre stylisée
        self.afficher_resultat(f"Recette avec {', '.join(ingredients_list)}", recette)

    def generer_menu(self):
        """Générer un menu pour plusieurs jours"""
        try:
            jours = simpledialog.askinteger("Nombre de jours", 
                                       "Pour combien de jours souhaitez-vous générer un menu ?",
                                       minvalue=1, maxvalue=14)
            if not jours:
                return
                
            # Afficher un loader
            loader = self.afficher_loader(f"Génération de votre menu pour {jours} jours...\nVeuillez patienter.")
            
            # Mettre à jour l'interface pour afficher le loader
            self.root.update()
            
            # Générer le menu
            menu = self.assistant.generer_menu(jours)
            
            # Fermer le loader
            loader.destroy()
            
            # Afficher le menu
            self.afficher_resultat(f"Menu pour {jours} jours", menu)            
        
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue lors de la génération du menu : {str(e)}")

    def afficher_resultat(self, titre, contenu):
        """Afficher un résultat dans une fenêtre stylisée"""
        # Créer la fenêtre de résultat
        result_window = tk.Toplevel(self.root)
        result_window.title(titre)
        result_window.geometry("800x600")
        result_window.configure(background=COULEURS["light"])
        
        try:
            result_window.iconbitmap("cuisine_icon.ico")
        except:
            pass
        
        # Frame principal
        main_frame = ttk.Frame(result_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Titre
        title_label = ttk.Label(main_frame, text=titre, style="Title.TLabel")
        title_label.pack(pady=10)
        
        # Ligne de séparation
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=10)
        
        # Créer le widget Text avec scrollbar pour le contenu
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_content = tk.Text(text_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, 
                            background=COULEURS["light"], foreground=COULEURS["text_dark"],
                            font=('Helvetica', 11), padx=10, pady=10,
                            relief="flat", borderwidth=0)
        text_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=text_content.yview)
        
        text_content.insert(tk.END, contenu)
        text_content.config(state=tk.DISABLED)  # Rendre le texte non modifiable
        
        # Frame pour les boutons d'action
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        def save_content():
            """Enregistrer le contenu affiché dans un fichier choisi par l'utilisateur."""
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("Fichiers PDF", "*.pdf"), ("Tous les fichiers", "*.*")],
                title="Enregistrer le fichier",
                initialdir=os.path.dirname(__file__)
            )
            if file_path:
                try:
                    # Créer un fichier texte temporaire encodé UTF-8
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w', encoding='utf-8') as temp_file:
                        temp_file.write(contenu)
                        temp_filename = temp_file.name

                    # Créer un PDF
                    c = canvas.Canvas(file_path)
                    c.setFont("Helvetica-Bold", 18)

                    titre = "Votre menu personnalisé"
                    page_width = c._pagesize[0]
                    c.drawCentredString(page_width / 2, 800, titre)

                    # Position de départ
                    current_y = 750
                    line_height = 14  # espace entre lignes

                    with open(temp_filename, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            line = line.replace('**', '')
                            if line.startswith('*'):
                                line = line.lstrip('*').strip()

                            if not line:
                                continue  # ignorer les lignes vides

                            # ➔ Si la ligne est un titre de section (Jour ou Liste de courses)
                            if line.lower().startswith('jour') or 'liste de courses' in line.lower():
                                c.setFont("Helvetica-Bold", 14)
                                c.drawString(50, current_y, line)

                                # ➔ Ajouter un trait de séparation
                                c.line(45, current_y-2, page_width-45, current_y-2)

                                current_y -= (line_height + 10)  # espace après les titres
                                c.setFont("Helvetica", 12)
                            else:
                                # Texte normal
                                c.setFont("Helvetica", 12)
                                c.drawString(50, current_y, line)
                                current_y -= line_height

                            # Si on arrive en bas de page, créer une nouvelle page
                            if current_y < 50:
                                c.showPage()
                                current_y = 800

                    c.save()

                    os.remove(temp_filename)

                    messagebox.showinfo("Sauvegarde réussie", f"Contenu sauvegardé dans {file_path}", parent=result_window)

                except Exception as e:
                    messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde : {str(e)}", parent=result_window)
            else:
                messagebox.showwarning("Aucun fichier sélectionné", "Le contenu n'a pas été sauvegardé.", parent=result_window)


  
        # Bouton pour imprimer
        def print_content():
            messagebox.showinfo("Impression", 
                        "Fonctionnalité d'impression en cours de développement.", 
                        parent=result_window)
            
        # Bouton pour fermer
        close_btn = ttk.Button(btn_frame, text="Fermer", command=result_window.destroy)
        close_btn.pack(side=tk.RIGHT, padx=5)
            
        # Bouton pour imprimer
        print_btn = ttk.Button(btn_frame, text="Imprimer", command=print_content)
        print_btn.pack(side=tk.RIGHT, padx=5)
            
        # Bouton pour sauvegarder
        save_btn = ttk.Button(btn_frame, text="Sauvegarder", command=save_content, style="Action.TButton")
        save_btn.pack(side=tk.RIGHT, padx=5)

    def afficher_preferences(self):
        """Afficher un résumé des préférences dans une fenêtre stylisée"""
        preferences = self.assistant.preferences
        
        # Créer la fenêtre
        pref_window = tk.Toplevel(self.root)
        pref_window.title("Mes préférences")
        pref_window.geometry("500x400")
        pref_window.configure(background=COULEURS["light"])
        pref_window.resizable(False, False)
        
        try:
            pref_window.iconbitmap("cuisine_icon.ico")
        except:
            pass
        
        # Frame principal
        main_frame = ttk.Frame(pref_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        title_label = ttk.Label(main_frame, text="Mes préférences culinaires", style="Title.TLabel")
        title_label.pack(pady=10)
        
        # Ligne de séparation
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=10)
        
        # Contenu des préférences
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Affichage organisé des préférences
        row = 0
        
        # Fonction pour ajouter une ligne
        def add_pref_row(label_text, value, row):
            label = ttk.Label(content_frame, text=label_text, width=25, anchor="w")
            label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
            
            val_text = value if value else "Non spécifié"
            value_label = ttk.Label(content_frame, text=val_text)
            value_label.grid(row=row, column=1, padx=10, pady=5, sticky="w")
            
            return row + 1
        
        # Nombre de personnes
        row = add_pref_row("Nombre de personnes:", str(preferences['nb_personnes']), row)
        
        # Régime alimentaire
        row = add_pref_row("Régime alimentaire:", preferences['regime'], row)
        
        # Allergies
        allergies_text = ", ".join(preferences['allergies']) if preferences['allergies'] else "Aucune"
        row = add_pref_row("Allergies:", allergies_text, row)
        
        # Préférences alimentaires
        prefs_text = ", ".join(preferences['preferences']) if preferences['preferences'] else "Aucune spécifiée"
        row = add_pref_row("Préférences:", prefs_text, row)
        
        # Aversions alimentaires
        aversions_text = ", ".join(preferences['aversions']) if preferences['aversions'] else "Aucune"
        row = add_pref_row("Aversions:", aversions_text, row)
        
        # Budget
        budget_text = f"{preferences['budget']} €" if preferences.get('budget') else "Non spécifié"
        row = add_pref_row("Budget par personne:", budget_text, row)
        
        # Temps de préparation
        temps_text = f"{preferences['temps_preparation']} minutes" if preferences.get('temps_preparation') else "Non spécifié"
        row = add_pref_row("Temps de préparation max:", temps_text, row)

        # Boutons d'actions
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        # Bouton pour fermer
        close_btn = ttk.Button(btn_frame, text="Fermer", command=pref_window.destroy)
        close_btn.pack(side=tk.RIGHT, padx=5)

        # Bouton pour sauvegarder
        save_btn = ttk.Button(btn_frame, text="Sauvegarder", command=lambda: [pref_window.destroy(), self.sauvegarder_preferences()], style="Action.TButton")
        save_btn.pack(side=tk.RIGHT, padx=5)

        # Bouton pour modifier
        edit_btn = ttk.Button(btn_frame, text="Modifier", command=lambda: [pref_window.destroy(), self.configurer_preferences()])
        edit_btn.pack(side=tk.RIGHT, padx=5)        

    
    def sauvegarder_preferences(self):
        """Sauvegarder les préférences dans un fichier"""
        filename = simpledialog.askstring("Sauvegarder les préférences", 
                                      "Nom du fichier (sans extension):")
        if filename:
            filename = filename if filename.endswith('.json') else filename + '.json'
            self.assistant.sauvegarder_preferences(filename)
    
    def charger_preferences(self):
        """Charger les préférences depuis un fichier"""
        filename = simpledialog.askstring("Charger les préférences",
                                      "Nom du fichier (sans extension):")
        if filename:
            filename = filename if filename.endswith('.json') else filename + '.json'
            if self.assistant.charger_preferences(filename):
                messagebox.showinfo("Chargement réussi", f"Préférences chargées depuis {filename}")
    
    def afficher_aide(self):
        """Affiche une fenêtre d'aide"""
        aide_window = tk.Toplevel(self.root)
        aide_window.title("Aide - Chef Assistant")
        aide_window.geometry("600x500")
        aide_window.configure(background=COULEURS["light"])
        
        try:
            aide_window.iconbitmap("cuisine_icon.ico")
        except:
            pass
        
        # Frame principal
        main_frame = ttk.Frame(aide_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        title_label = ttk.Label(main_frame, text="Guide d'utilisation", style="Title.TLabel")
        title_label.pack(pady=10)
        
        # Ligne de séparation
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=10)
        
        # Contenu de l'aide avec scrollbar
        help_frame = ttk.Frame(main_frame)
        help_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(help_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        help_text = tk.Text(help_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set,
                         background=COULEURS["light"], foreground=COULEURS["text_dark"],
                         font=('Helvetica', 11), padx=10, pady=10)
        help_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=help_text.yview)
        
        # Contenu de l'aide
        aide_content = """
# Comment utiliser Chef Assistant

## Fonctionnalités principales

### 1. Générer une recette
Utilisez cette fonction pour obtenir une recette personnalisée à partir des ingrédients que vous avez à disposition. 
- Cliquez sur "Générer recette"
- Entrez vos ingrédients séparés par des virgules
- Attendez pendant la génération de votre recette
- Vous pourrez consulter et sauvegarder la recette générée

### 2. Générer un menu
Créez un menu complet pour plusieurs jours adapté à vos préférences.
- Cliquez sur "Générer menu"
- Indiquez le nombre de jours (entre 1 et 14)
- Attendez pendant la génération de votre menu
- Vous pourrez consulter et sauvegarder le menu généré

### 3. Configurer les préférences
Personnalisez votre expérience en précisant:
- Nombre de personnes
- Régime alimentaire
- Allergies alimentaires
- Préférences et goûts
- Aversions alimentaires
- Budget moyen par personne
- Temps de préparation maximum

### 4. Sauvegarder et charger des préférences
Vous pouvez enregistrer vos préférences dans un fichier pour les réutiliser ultérieurement.

## Conseils d'utilisation
- Pour des résultats optimaux, configurez vos préférences avant de générer des recettes ou des menus
- Plus vous fournissez d'informations précises, plus les recettes seront adaptées à vos besoins
- N'hésitez pas à sauvegarder les recettes intéressantes pour les consulter ultérieurement
        """
        
        help_text.insert(tk.END, aide_content)
        help_text.config(state=tk.DISABLED)  # Rendre le texte non modifiable
        
        # Bouton pour fermer
        close_btn = ttk.Button(main_frame, text="Fermer", command=aide_window.destroy)
        close_btn.pack(side=tk.RIGHT, pady=10)

def main():
    # Création de la fenêtre principale
    root = tk.Tk()
    
    # Création de l'application
    app = Application(root)
    
    # Lancement de la boucle principale
    root.mainloop()

if __name__ == "__main__":
    main()
