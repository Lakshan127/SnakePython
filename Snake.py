import tkinter
import random

# Spielfeldgröße
REIHEN = 25
SPALTEN = 25
KACHEL_GROESSE = 25

FENSTER_BREITE = SPALTEN * KACHEL_GROESSE
FENSTER_HOEHE = REIHEN * KACHEL_GROESSE

class Kachel:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Fenster erstellen
fenster = tkinter.Tk()
fenster.title("Snake")
fenster.resizable(False, False)

leinwand = tkinter.Canvas(fenster, bg='gray', width=FENSTER_BREITE, height=FENSTER_HOEHE, borderwidth=0, highlightthickness=0)
leinwand.pack()
fenster.update()

# Fenster zentrieren
fenster_breite = fenster.winfo_width()
fenster_hoehe = fenster.winfo_height()
bildschirm_breite = fenster.winfo_screenwidth()
bildschirm_hoehe = fenster.winfo_screenheight()

fenster_x = int((bildschirm_breite / 2) - (fenster_breite / 2))
fenster_y = int((bildschirm_hoehe / 2) - (fenster_hoehe / 2))

fenster.geometry(f"{fenster_breite}x{fenster_hoehe}+{fenster_x}+{fenster_y}")

# Spiel-Initialisierung
schlange = Kachel(5 * KACHEL_GROESSE, 5 * KACHEL_GROESSE)  # Kopf der Schlange
essen = Kachel(10 * KACHEL_GROESSE, 10 * KACHEL_GROESSE)
schlangen_koerper = []  # Liste für den Körper der Schlange
bewegung_x = 0
bewegung_y = 0
spiel_vorbei = False
spiel_gestartet = False
punktzahl = 0

def spiel_neu_starten():
    global schlange, essen, schlangen_koerper, bewegung_x, bewegung_y, spiel_vorbei, spiel_gestartet, punktzahl
    schlange = Kachel(5 * KACHEL_GROESSE, 5 * KACHEL_GROESSE)
    essen = Kachel(10 * KACHEL_GROESSE, 10 * KACHEL_GROESSE)
    schlangen_koerper = []
    bewegung_x = 0
    bewegung_y = 0
    spiel_vorbei = False
    spiel_gestartet = False
    punktzahl = 0

def richtung_aendern(e):
    """Ändert die Bewegungsrichtung der Schlange basierend auf der gedrückten Pfeiltaste."""
    global bewegung_x, bewegung_y, spiel_vorbei, spiel_gestartet

    if spiel_vorbei and e.keysym == 'space':
        spiel_neu_starten()
        return

    if not spiel_gestartet and e.keysym in ['Up', 'Down', 'Left', 'Right']:
        spiel_gestartet = True

    if spiel_vorbei:
        return

    if e.keysym == 'Up' and bewegung_y != 1:
        bewegung_x = 0
        bewegung_y = -1
    elif e.keysym == 'Down' and bewegung_y != -1:
        bewegung_x = 0
        bewegung_y = 1
    elif e.keysym == 'Left' and bewegung_x != 1:
        bewegung_x = -1
        bewegung_y = 0
    elif e.keysym == 'Right' and bewegung_x != -1:
        bewegung_x = 1
        bewegung_y = 0

def bewegen():
    """Bewegt die Schlange und überprüft auf Kollisionen."""
    global schlange, essen, schlangen_koerper, spiel_vorbei, punktzahl

    if spiel_vorbei or not spiel_gestartet:
        return
    
    # Kollision mit der Wand
    if schlange.x < 0 or schlange.x >= FENSTER_BREITE or schlange.y < 0 or schlange.y >= FENSTER_HOEHE:
        spiel_vorbei = True
        return
    
    # Kollision mit sich selbst
    for kachel in schlangen_koerper:
        if schlange.x == kachel.x and schlange.y == kachel.y:
            spiel_vorbei = True
            return 

    # Kollision mit dem Essen
    if schlange.x == essen.x and schlange.y == essen.y:
        schlangen_koerper.append(Kachel(essen.x, essen.y))  # Neues Segment hinzufügen
        essen.x = random.randint(0, SPALTEN - 1) * KACHEL_GROESSE
        essen.y = random.randint(0, REIHEN - 1) * KACHEL_GROESSE
        punktzahl += 1

    # Schlange bewegen (Körperteile verschieben)
    for i in range(len(schlangen_koerper) - 1, -1, -1):
        kachel = schlangen_koerper[i]
        if i == 0:
            kachel.x = schlange.x
            kachel.y = schlange.y
        else:
            vorherige_kachel = schlangen_koerper[i - 1]
            kachel.x = vorherige_kachel.x
            kachel.y = vorherige_kachel.y

    # Kopf der Schlange weiterbewegen
    schlange.x += bewegung_x * KACHEL_GROESSE
    schlange.y += bewegung_y * KACHEL_GROESSE

def zeichnen():
    """Zeichnet das Spielfeld neu nach jeder Bewegung."""
    global schlange, essen, schlangen_koerper, spiel_vorbei, punktzahl

    bewegen()
    leinwand.delete('all')

    # Essen zeichnen
    leinwand.create_rectangle(essen.x, essen.y, essen.x + KACHEL_GROESSE, essen.y + KACHEL_GROESSE, fill='red')

    # Schlange zeichnen
    leinwand.create_rectangle(schlange.x, schlange.y, schlange.x + KACHEL_GROESSE, schlange.y + KACHEL_GROESSE, fill='lime green')

    for kachel in schlangen_koerper:
        leinwand.create_rectangle(kachel.x, kachel.y, kachel.x + KACHEL_GROESSE, kachel.y + KACHEL_GROESSE, fill='lime green')

    if spiel_vorbei:
        leinwand.create_text(FENSTER_BREITE / 2, FENSTER_HOEHE / 2, font="Arial 20", text=f"Game Over: {punktzahl} (Leertaste für Neustart)", fill="white")
    elif not spiel_gestartet:
        leinwand.create_text(FENSTER_BREITE / 2, FENSTER_HOEHE / 2, font="Arial 15", text="Drücke ←↑↓→ Starten", fill="white")
    else:
        leinwand.create_text(30, 20, font='Arial 10', text=f"Punkte: {punktzahl}", fill='white')
    
    fenster.after(100, zeichnen)

zeichnen()
fenster.bind("<KeyRelease>", richtung_aendern)
fenster.mainloop()
