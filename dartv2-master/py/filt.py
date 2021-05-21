import numpy as np
import scipy.stats as ss
import time
from scipy import signal


class SonarFilter():
    """Classe permettant de filtrer les sonars"""

    def __init__(self):
        self.mes = []  # Tableau des mesures
        self.filt = []  # Tableau des mesures filtrées
        self.no_wall = 0 # Compteur de non détection de mur


    def filtre(self, m):
        """Unique fonction de la classe permettant de filtrer une valeur m mesurée par le sonar, retourne la valeur filtrée (flottant)"""
        if m > 8000:
            self.no_wall += 1
            if self.no_wall >= 5:
                self.filt = []
                self.mes = []
            return float('inf')
        self.mes.append(m)
        # On ajoute la mesure m a la liste des mesures
        l = len(self.mes)
        if l < 3:
            # Initialisation : nos deux listes ne comportent pas assez de valeurs
            self.filt.append(m)
            return np.mean(np.array(self.filt))
        else:
            M = np.array(self.mes[-3:])
            # On considère les 3 dernières valeurs mesurées pour filtrer les pics de bruit
            # à l'aide de la technique de la médiane
            if m <= np.median(M):
                self.filt.append(np.mean(np.array(self.filt[-3:] + [m])))
                # On fait ensuite la moyenne de la mesure et des 3 dernières valeurs filtrées
        return self.filt[-1]
    
    
    def reset(self):
        self.mes = []
        self.filt = []
        self.no_wall = 0
