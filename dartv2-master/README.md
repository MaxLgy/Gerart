Projet réalisé par LEGEAY Maxime, ODORICO Nicolas et ORLHAC Baptiste.

Pour lancer le programme mettant en fonctionnement le robot :

- Dans le dossier py, exécuter le fichier robot_cmd_1.py à l'aide d'une IDE Python.

- Au lancement, le programme vous laissera le choix entre trois modes d'exécution :

 -> Le mode circuit, qui lance la machine à états finis qui permet au robot de faire le circuit demandé.

 -> L'option de calibration, qui permet de calibrer les odomètres et les sonars afin d'obtenir une meilleure précision lors des virages.

Odomètres : Cette option fait faire des tours au robot sur lui-même, vous devrez indiquer de façon successives si le robot est revenu
dans son orientation de départ après 1,2,3,4 tours, ou s'il a trop ou pas assez tourné sur lui-même.

Sonars : En posant le robot au milieu d'une allée du circuit, le programme écrit les deux distances au murs perçues par les sonars, afin d'ensuite corriger
les potentielles erreurs de mesure liées à une différence dans cette distance perçue.

 -> L'option Quitter, qui ferme le programme et coupe les moteurs du robot.

ATTENTION : AVANT LE PREMIER LANCEMENT EN MODE CIRCUIT, IL FAUT LANCER LE ROBOT UNE PREMIERE FOIS EN MODE CALIBRATION ET SUIVRE LES INSTRUCTIONS POUR EFFECTUER LES DEUX CALIBRATIONS.

- En mode circuit, le robot effectue ensuite le chemin complet sans besoin d'intervention humaine, et enregistre des données de sonars afin de retracer sa position par la suite.
- Pour retracer son parcours, il faut exécuter afficherparcours.py à l'aide d'une ide python, en ayant au préalable édité dans la première ligne de code le nom du fichier dans
lequel les données ont été écrites par le robot lors de son exécution.

Pour information :

Les fichiers importants pour l'exécution du programme sont situés dans le dossier py :
- robot_cmd_1.py, programme gérant l'exécution initiale de la machine à états finis, et qui propose les options de lancement à l'utilisateur.
- fsm.py, qui gère la machine à états finis en elle-même.
- dartv2b.py, qui contient les fonctions se servant des drivers pour lire les capteurs et actionner les moteurs.