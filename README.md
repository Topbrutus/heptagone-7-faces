# Generateur du prisme heptagonal ouvert

**Auteur : Gabriel St-Pierre** (index bibliographique : St-Pierre, Gabriel).

Le programme `generateur_7_cotes_7_faces.py` construit les 7 faces laterales
d'un prisme droit a base heptagonale reguliere, sans face de dessus ni de dessous.

Formules classiques : angle central 2*pi/7 ; longueur du cote
s = 2*R*sin(pi/7) ; apotheme a = R*cos(pi/7) ;
perimetre P = 7*s ; aire laterale A = P*H.

Le maillage ouvert compte 14 sommets, 21 aretes et 7 faces;
la caracteristique d'Euler de la surface laterale ouverte est 0.

Pre-requis : Python 3, Tkinter, mpmath, matplotlib.
Installation : python -m pip install -r requirements.txt
Execution : python generateur_7_cotes_7_faces.py
Verification : python -m py_compile generateur_7_cotes_7_faces.py

Les identites utilisees sont classiques, non revendiquees comme une
decouverte de mathematiques. Les notes « Polyhector / polygone exact »
font l'objet d'une recherche distincte qui doit etre authentifiee.

**Licence de reutilisation : a choisir par l'auteur avant publication finale.**
La presente preparation ne publie aucun mot de passe ou jeton d'API.
