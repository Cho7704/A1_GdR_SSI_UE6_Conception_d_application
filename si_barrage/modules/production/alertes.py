import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 1. Données de base
x = np.linspace(0, 4*np.pi, 500)
y = np.sin(x)  # une courbe sinusoïdale

# 2. Paramètres initiaux des seuils (en y)
seuil_bas_init = -0.5
seuil_haut_init = 0.5

# 3. Création de la figure et du graphique
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.3)  # plus d'espace pour les curseurs

# Tracé initial (courbe en bleu)
courbe, = ax.plot(x, y, 'b-', lw=2, label='Courbe')
ax.axhline(seuil_bas_init, color='r', linestyle='--', alpha=0.7, label='Seuil bas')
ax.axhline(seuil_haut_init, color='g', linestyle='--', alpha=0.7, label='Seuil haut')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Alerte visuelle quand la courbe dépasse les seuils')
ax.legend()
ax.grid(True)

# 4. Création des curseurs pour seuils bas et haut
ax_seuil_bas = plt.axes([0.15, 0.15, 0.65, 0.03])
ax_seuil_haut = plt.axes([0.15, 0.1, 0.65, 0.03])

slider_bas = Slider(ax_seuil_bas, 'Seuil bas', -2, 2, valinit=seuil_bas_init, valstep=0.05)
slider_haut = Slider(ax_seuil_haut, 'Seuil haut', -2, 2, valinit=seuil_haut_init, valstep=0.05)

# Texte d'alerte (initialement vide)
alerte_text = ax.text(0.5, 0.95, '', transform=ax.transAxes, ha='center',
                      color='red', fontsize=12, weight='bold')

# 5. Fonction de mise à jour
def mise_a_jour(val):
    # Lire les valeurs des seuils
    bas = slider_bas.val
    haut = slider_haut.val
    
    # Éviter que bas > haut (correction automatique)
    if bas >= haut:
        haut = bas + 0.1
        slider_haut.set_val(haut)
    
    # Mettre à jour les lignes horizontales des seuils
    # On doit supprimer les anciennes lignes et en créer de nouvelles,
    # ou mieux : garder des références pour les modifier.
    # Solution simple : on nettoie les lignes existantes et on les redessine.
    ax.clear()
    ax.plot(x, y, 'b-', lw=2)
    ax.axhline(bas, color='r', linestyle='--', alpha=0.7)
    ax.axhline(haut, color='g', linestyle='--', alpha=0.7)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Alerte visuelle quand la courbe dépasse les seuils')
    ax.grid(True)
    ax.legend(['Courbe', 'Seuil bas', 'Seuil haut'])
    
    # Détection des dépassements
    depasse_bas = y < bas
    depasse_haut = y > haut
    
    if np.any(depasse_bas) or np.any(depasse_haut):
        # Colorier en rouge les parties qui dépassent
        # On trace par segments pour éviter de surcharger
        # Une méthode simple : tracer la courbe entière en rouge par-dessus là où ça dépasse
        # Mais pour une meilleure visualisation, on va tracer les points en rouge
        x_depasse_bas = x[depasse_bas]
        y_depasse_bas = y[depasse_bas]
        x_depasse_haut = x[depasse_haut]
        y_depasse_haut = y[depasse_haut]
        ax.scatter(x_depasse_bas, y_depasse_bas, color='red', s=10, zorder=5)
        ax.scatter(x_depasse_haut, y_depasse_haut, color='red', s=10, zorder=5)
        
        # Afficher le message d'alerte
        alerte = "ALERTE : dépassement de seuil !"
    else:
        alerte = ""
    
    # Mettre à jour le texte d'alerte
    # On doit recréer le texte car on a clear l'axe
    alerte_text = ax.text(0.5, 0.95, alerte, transform=ax.transAxes, ha='center',
                          color='red', fontsize=12, weight='bold')
    
    fig.canvas.draw_idle()

# Connecter les curseurs
slider_bas.on_changed(mise_a_jour)
slider_haut.on_changed(mise_a_jour)

plt.show()