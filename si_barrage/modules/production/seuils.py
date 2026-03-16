import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 1. Création des données de base (axe x)
x = np.linspace(0, 10, 500)

# 2. Définition de la fonction qui calcule la courbe à partir des seuils
def calculer_courbe(seuil1, seuil2):
    """Fonction linéaire par morceaux avec deux seuils."""
    y = np.piecewise(x,
                     [x < seuil1, (x >= seuil1) & (x <= seuil2), x > seuil2],
                     [0, lambda x: (x - seuil1) / (seuil2 - seuil1), 1])
    return y

# 3. Paramètres initiaux des seuils
seuil1_init = 2.0
seuil2_init = 7.0

# 4. Création de la figure et du graphique
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)  # laisser de l'espace pour les curseurs

# Tracé initial
y_init = calculer_courbe(seuil1_init, seuil2_init)
courbe, = ax.plot(x, y_init, lw=2)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Courbe modifiable avec seuils')
ax.grid(True)

# 5. Création des curseurs
# Position des curseurs : [left, bottom, width, height] en coordonnées figure
ax_seuil1 = plt.axes([0.15, 0.1, 0.65, 0.03])
ax_seuil2 = plt.axes([0.15, 0.05, 0.65, 0.03])

slider_seuil1 = Slider(ax_seuil1, 'Seuil 1', 0, 10, valinit=seuil1_init, valstep=0.1)
slider_seuil2 = Slider(ax_seuil2, 'Seuil 2', 0, 10, valinit=seuil2_init, valstep=0.1)

# 6. Fonction de mise à jour appelée quand un curseur bouge
def mise_a_jour(val):
    # Récupérer les valeurs actuelles des curseurs
    s1 = slider_seuil1.val
    s2 = slider_seuil2.val
    # Éviter que seuil1 soit supérieur ou égal à seuil2 (pour éviter division par zéro)
    if s1 >= s2:
        s2 = s1 + 0.1
        slider_seuil2.set_val(s2)  # correction automatique
    # Recalculer la courbe
    y_new = calculer_courbe(s1, s2)
    courbe.set_ydata(y_new)
    fig.canvas.draw_idle()  # rafraîchir l'affichage

# Connecter la fonction aux curseurs
slider_seuil1.on_changed(mise_a_jour)
slider_seuil2.on_changed(mise_a_jour)

plt.show()