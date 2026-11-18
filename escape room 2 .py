import tkinter as tk
from tkinter import messagebox
import random
import time

# ==========================================
# CONFIGURATION
# ==========================================

WIDTH = 1000
HEIGHT = 700

CELL = 40

score = 0
temps = 1800
enigmes_resolues = 0
jeu_actif = True

# ==========================================
# BANQUE D'ENIGMES
# ==========================================

banque = [
    ("Plus on m'enlève, plus je deviens grand.",
     ["trou"], "On peut me trouver dans le sol."),

    ("Combien de mois ont 28 jours ?",
     ["12", "douze"], "Tous les mois ont au moins 28 jours."),

    ("Quel nombre vient ensuite : 2, 4, 8, 16 ?",
     ["32"], "Chaque nombre double."),

    ("Je possède des villes sans maisons.",
     ["carte"], "Je permets de me repérer."),

    ("Qu'est-ce qui a des dents mais ne mange pas ?",
     ["peigne"], "On m'utilise pour les cheveux."),

    ("Je disparais quand on prononce mon nom.",
     ["silence"], "On m'entend quand personne ne parle."),

    ("Quel nombre vient ensuite : 3, 6, 12, 24 ?",
     ["48"], "Multiplie par deux."),

    ("J'ai des aiguilles mais je ne couds pas.",
     ["horloge", "montre"], "Je donne l'heure."),

    ("Je suis toujours devant toi, mais invisible.",
     ["futur"], "Je concerne ce qui va arriver."),

    ("Je suis plein de trous mais je retiens l'eau.",
     ["eponge", "éponge"], "On m'utilise pour nettoyer."),

    ("Combien font 15 × 8 ?",
     ["120"], "15 fois 4, puis double."),

    ("Je peux être cassé sans être touché.",
     ["promesse"], "On peut me faire à quelqu'un."),

    ("Quel nombre vient ensuite : 1, 4, 9, 16 ?",
     ["25"], "Ce sont des carrés parfaits."),

    ("Qu'est-ce qui a des clés mais n'ouvre aucune porte ?",
     ["piano"], "On joue de la musique avec."),

    ("Je voyage autour du monde en restant dans un coin.",
     ["timbre"], "Je me trouve sur une enveloppe."),

    ("Quel est le tiers de  ninety ?",
     ["30", "trente"], "90 divisé par 3.")
]

enigmes = random.sample(banque, 4)

# ==========================================
# FENETRE
# ==========================================

root = tk.Tk()

root.title("ESCAPE ROOM 3.0")
root.geometry("1100x760")
root.configure(bg="#111827")
root.resizable(False, False)

# ==========================================
# INTERFACE
# ==========================================

titre = tk.Label(
    root,
    text="ESCAPE ROOM : LA CHAMBRE SECRETE",
    font=("Arial", 23, "bold"),
    fg="#38bdf8",
    bg="#111827"
)

titre.pack(pady=10)

# ==========================================
# CANVAS
# ==========================================

canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg="#263238",
    highlightthickness=0
)

canvas.pack()

# ==========================================
# SALLE
# ==========================================

canvas.create_rectangle(
    20, 20, 980, 680,
    fill="#455a64",
    outline="#90a4ae",
    width=8
)

# Sol
canvas.create_rectangle(
    40, 40, 960, 660,
    fill="#795548",
    outline=""
)

# Motifs du sol
for x in range(50, 960, 80):
    for y in range(50, 660, 80):
        canvas.create_rectangle(
            x, y, x+75, y+75,
            outline="#8d6e63"
        )

# ==========================================
# OBJETS
# ==========================================

objets = [
    {
        "nom": "BUREAU",
        "x": 180,
        "y": 160,
        "couleur": "#2196f3",
        "type": "enigme",
        "resolu": False
    },
    {
        "nom": "BIBLIOTHEQUE",
        "x": 750,
        "y": 150,
        "couleur": "#8d6e63",
        "type": "enigme",
        "resolu": False
    },
    {
        "nom": "COFFRE",
        "x": 180,
        "y": 480,
        "couleur": "#ff9800",
        "type": "enigme",
        "resolu": False
    },
    {
        "nom": "TABLEAU",
        "x": 750,
        "y": 480,
        "couleur": "#9c27b0",
        "type": "enigme",
        "resolu": False
    }
]

for obj in objets:

    x = obj["x"]
    y = obj["y"]

    canvas.create_rectangle(
        x-45, y-30,
        x+45, y+30,
        fill=obj["couleur"],
        outline="white",
        width=3
    )

    canvas.create_text(
        x, y,
        text=obj["nom"],
        fill="white",
        font=("Arial", 9, "bold")
    )

# ==========================================
# PORTE
# ==========================================

porte = canvas.create_rectangle(
    450, 20, 550, 55,
    fill="#b71c1c",
    outline="white",
    width=3
)

canvas.create_text(
    500, 37,
    text="SORTIE",
    fill="white",
    font=("Arial", 11, "bold")
)

# ==========================================
# JOUEUR
# ==========================================

player_x = 500
player_y = 350

joueur = canvas.create_oval(
    player_x-15,
    player_y-15,
    player_x+15,
    player_y+15,
    fill="#00e5ff",
    outline="white",
    width=3
)

# ==========================================
# PANNEAU D'INFORMATIONS
# ==========================================

panel = tk.Frame(root, bg="#111827")
panel.pack(fill="x")

info = tk.Label(
    panel,
    text="Explore la pièce et trouve les 4 énigmes.",
    font=("Arial", 12),
    fg="white",
    bg="#111827"
)

info.pack(pady=5)

stats = tk.Label(
    panel,
    text="Score : 0 | Énigmes : 0/4 | Temps : 30:00",
    font=("Arial", 12, "bold"),
    fg="#facc15",
    bg="#111827"
)

stats.pack()

question_label = tk.Label(
    panel,
    text="Déplace-toi avec ZQSD ou les flèches. Appuie sur E pour interagir.",
    font=("Arial", 12),
    fg="#38bdf8",
    bg="#111827",
    wraplength=900
)

question_label.pack(pady=8)

# ==========================================
# REPONSE
# ==========================================

entry = tk.Entry(
    panel,
    font=("Arial", 14),
    justify="center",
    width=35
)

entry.pack(pady=5)

# ==========================================
# VARIABLES DE JEU
# ==========================================

enigme_actuelle = None
indice_utilise = False

# ==========================================
# MISE A JOUR DES STATS
# ==========================================

def update_stats():

    minutes = temps // 60
    secondes = temps % 60

    stats.config(
        text=f"Score : {score} | Énigmes : {enigmes_resolues}/4 | Temps : {minutes:02}:{secondes:02}"
    )

# ==========================================
# DEPLACEMENT
# ==========================================

def deplacer(dx, dy):

    global player_x, player_y

    if not jeu_actif or enigme_actuelle is not None:
        return

    nx = player_x + dx
    ny = player_y + dy

    if 55 < nx < 945 and 65 < ny < 640:

        player_x = nx
        player_y = ny

        canvas.coords(
            joueur,
            player_x-15,
            player_y-15,
            player_x+15,
            player_y+15
        )

# ==========================================
# TOUCHES
# ==========================================

def touche(event):

    key = event.keysym.lower()

    if key in ("z", "up"):
        deplacer(0, -20)

    elif key in ("s", "down"):
        deplacer(0, 20)

    elif key in ("q", "left"):
        deplacer(-20, 0)

    elif key in ("d", "right"):
        deplacer(20, 0)

    elif key == "e":
        interaction()

root.bind("<KeyPress>", touche)

# ==========================================
# INTERACTION
# ==========================================

def interaction():

    global enigme_actuelle, indice_utilise

    if not jeu_actif or enigme_actuelle is not None:
        return

    for i, obj in enumerate(objets):

        distance = (
            (player_x - obj["x"])**2 +
            (player_y - obj["y"])**2
        )**0.5

        if distance < 85:

            if obj["resolu"]:
                question_label.config(
                    text="Tu as déjà résolu cette énigme."
                )
                return

            enigme_actuelle = i
            indice_utilise = False

            question_label.config(
                text="ÉNIGME : " + enigmes[i][0]
            )

            entry.focus_set()

            return

    # Interaction avec la porte

    if 430 < player_x < 570 and player_y < 90:

        if enigmes_resolues == 4:
            victoire()

        else:
            question_label.config(
                text="La porte est verrouillée. Résous les 4 énigmes !"
            )

# ==========================================
# INDICE
# ==========================================

def donner_indice():

    global indice_utilise

    if enigme_actuelle is not None:

        indice_utilise = True

        question_label.config(
            text="INDICE : " + enigmes[enigme_actuelle][2]
        )

# ==========================================
# VALIDATION
# ==========================================

def verifier():

    global enigme_actuelle
    global enigmes_resolues
    global score

    if enigme_actuelle is None or not jeu_actif:
        return

    tentative = entry.get().strip().lower()

    bonnes_reponses = enigmes[enigme_actuelle][1]

    if tentative in bonnes_reponses:

        objets[enigme_actuelle]["resolu"] = True

        enigmes_resolues += 1

        if indice_utilise:
            score += 50
        else:
            score += 100

        # Modifier la couleur de l'objet résolu

        obj = objets[enigme_actuelle]

        canvas.create_rectangle(
            obj["x"]-45,
            obj["y"]-30,
            obj["x"]+45,
            obj["y"]+30,
            fill="#2e7d32",
            outline="white",
            width=3
        )

        canvas.create_text(
            obj["x"],
            obj["y"],
            text="RESOLU",
            fill="white",
            font=("Arial", 10, "bold")
        )

        enigme_actuelle = None

        entry.delete(0, tk.END)

        question_label.config(
            text="Bonne réponse ! Continue ton exploration."
        )

        update_stats()

        if enigmes_resolues == 4:
            messagebox.showinfo(
                "Mission",
                "Toutes les énigmes sont résolues ! Trouve la porte."
            )

    else:

        messagebox.showwarning(
            "Erreur",
            "Mauvaise réponse ! Essaie encore."
        )

        entry.delete(0, tk.END)

# ==========================================
# VICTOIRE
# ==========================================

def victoire():

    global jeu_actif

    jeu_actif = False

    canvas.itemconfig(
        porte,
        fill="#00c853"
    )

    question_label.config(
        text="VICTOIRE ! TU AS REUSSI A T'ECHAPPER !"
    )

    messagebox.showinfo(
        "VICTOIRE",
        f"Tu as terminé le jeu !\nScore final : {score}/400"
    )

# ==========================================
# CHRONOMETRE
# ==========================================

def chronometre():

    global temps

    if not jeu_actif:
        return

    if temps > 0:

        temps -= 1

        update_stats()

        root.after(1000, chronometre)

    else:

        defaite()

# ==========================================
# DEFAITE
# ==========================================

def defaite():

    global jeu_actif

    jeu_actif = False

    question_label.config(
        text="GAME OVER ! Le temps est écoulé."
    )

    messagebox.showerror(
        "GAME OVER",
        "Tu n'as pas réussi à sortir à temps."
    )

# ==========================================
# BOUTONS
# ==========================================

boutons = tk.Frame(root, bg="#111827")
boutons.pack(pady=8)

tk.Button(
    boutons,
    text="VALIDER",
    command=verifier,
    bg="#16a34a",
    fg="white",
    font=("Arial", 11, "bold"),
    width=15
).grid(row=0, column=0, padx=10)

tk.Button(
    boutons,
    text="INDICE",
    command=donner_indice,
    bg="#d97706",
    fg="white",
    font=("Arial", 11, "bold"),
    width=15
).grid(row=0, column=1, padx=10)

# ==========================================
# LANCEMENT
# ==========================================

update_stats()
chronometre()

root.mainloop()