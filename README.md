# Générateur de PixelArt avec PyQt

## Table des Matières
- [Description](#description)
- [Structure du Projet](#structure-du-projet)
- [Fonctionnalités Clés](#fonctionnalités-clés)
  - [Outils de Dessin](#outils-de-dessin)
  - [Palette de Couleurs & Création Personnalisée](#palette-de-couleurs--création-personnalisée)
  - [Grille Interactive](#grille-interactive)
  - [Filtres et Effets](#filtres-et-effets)
  - [Popups et Confirmations](#popups-et-confirmations)
- [Interface Graphique](#interface-graphique)
- [Sauvegarde, Chargement et Suppression de Créations](#sauvegarde-chargement-et-suppression-de-créations)
- [Architecture du Code](#architecture-du-code)
- [Exemple de flux d’utilisation](#exemple-de-flux-dutilisation)
- [Notes et Remarques](#notes-et-remarques)
- [Prérequis](#prérequis)

---

## Description

Le projet **PixelArt-Generator-PyQt** est une application développée en **Python** avec **PyQt5** qui permet de **créer**, **modifier** et **personnaliser** des dessins en Pixel Art. 
Son objectif principal est de fournir une **interface intuitive**, couplée à une **grille de 32×32 pixels**, pour dessiner librement et **sauvegarder** vos créations. 
Plusieurs **outils**, **filtres** et **effets** sont mis à disposition pour personnaliser la grille/palette et pour donner vie à votre Pixel Art.

---

## Structure du Projet

Voici l’arborescence générale du projet :

```bash
PixelArt-Generator-PyQt/
├── pixelart_generator.py     # Fichier principal (classe Fenetre(QMainWindow))
├── icons/                    # Icônes de la barre d’outils et des menus
│   ├── reset_palette.png
│   ├── sauvegarde.png
│   ├── supprimer.png
│   └── ...
└── creations/                # Dossier où sont stockés les fichiers .txt
    ├── exemple1.txt
    └── exemple2.txt
```

### `pixelart_generator.py`
- Contient la classe **`Fenetre(QMainWindow)`**, gérant **l’interface PyQt5**, les **outils de dessin**, la **palette**, les **filtres**, la **sauvegarde/chargement** et la **suppression** de créations.

### `icons/`
- Regroupe toutes les **icônes** (format `.png`/`.jpg`) utilisées dans la **barre d’outils** et **menus**.

### `creations/`
- Contient les **créations sauvegardées** (fichiers `.txt`).  
- Chaque fichier décrit la grille :  
  - **Coordonnées** (ligne, colonne)  
  - **Valeurs RVB** (R, G, B) de chaque pixel.

---

## Fonctionnalités Clés

### Outils de Dessin

1. **Stylo** 🖌️  
   - Colorie la case cliquée avec la couleur de la palette sélectionnée.
     
2. **Gomme** 🧽  
   - Efface la case cliquée en la remettant en blanc.
     
3. **Baguette** ✨  
   - Efface toutes les cases ayant la même couleur que celle sélectionnée.
     
4. **Pot** 🧺  
   - Remplit toutes les **cases blanches** avec la couleur actuelle.

### Palette de Couleurs & Création Personnalisée

- **Palette Initiale (3×3)** : 9 couleurs par défaut qui peut être réinitialisée ou modifiée.  
- **Aperçu Couleur Actuelle** : Affiche la couleur en cours d’utilisation.  
- **Sliders RGB** :  
  - Permettent de **créer** une nouvelle couleur (Rouge, Vert, Bleu).  
  - Un label affiche la valeur exacte `rgb(r, g, b)`.  
- **Bouton “Ajouter à la palette”** :  
  - Un popup permet de **remplacer** une couleur existante par celle nouvellement créée.

### Grille Interactive

- **Grille de 32×32** : Chaque case est cliquable et peut être colorée ou effacée.  
- **Réinitialisation** : Un menu permet de la remettre entièrement en blanc (Ctrl+D).
    
### Filtres et Effets

Les **filtres** ciblent la palette de couleurs, tandis que les **effets** agissent sur la grille.


- **Filtres sur la Palette** :  
  | Filtre            | Raccourci     | Effet                                                          |
  |-------------------|---------------|----------------------------------------------------------------|
  | **Rouge**    🔴   | Ctrl + R      | Convertit la palette en nuances de rouge.                      |
  | **Vert**     🟢   | Ctrl + V      | Convertit la palette en nuances de vert.                       |
  | **Bleu**     🔵   | Ctrl + B      | Convertit la palette en nuances de bleu.                       |
  | **Négatif**  🌗   | Ctrl + N      | Inverse les couleurs (effet négatif).                          |
  | **Gris**     ⚪   | Ctrl + G      | Désature la palette pour un rendu en niveaux de gris.          |

- **Effet Noir & Blanc** sur la Grille :  
  - **Ctrl + E** : Convertit chaque pixel en niveau de gris selon sa luminosité pour un rendu plus contrasté.
    
- **Réinitialiser la Palette** :  
  - **Ctrl + P** : Rétablit les 9 couleurs d’origine de la palette.
    
### Popups et Confirmations

- **Suppression** d’une création : demande confirmation (popup).
- **Remplacement** dans la palette : l’utilisateur choisit quelle couleur remplacer.
- **Erreurs** de chargement (fichier inexistant) : popup avertissant l’utilisateur.

---

## Interface Graphique

L’interface se divise en deux grandes zones :

1. **Panneau de Contrôle (à gauche)**  
   - Un label principal “Générateur de PixelArt”.  
   - Deux ComboBox :  
     - **Outils** (Stylo, Gomme, Baguette, Pot).  
     - **Créations** (liste des création prédéfinie/enregistrées disponibles dans `creations/`).  
   - **GroupBox “Sélection & Palette”** :
     - Palette initiale 3×3.  
     - Aperçu de la couleur actuelle.  
   - **GroupBox “Création de couleur”** :  
     - Sliders (Rouge, Vert, Bleu).  
     - Aperçu de la couleur générée. 
     - Bouton “Ajouter à la palette” (déclenche le popup de remplacement).
       
2. **Zone de Dessin (à droite)**  
   - **Grille 32×32** (chaque case est un `QLabel` cliquable).  

**Barre de Menu** :  
- Menu **Grille** :  
  - *Réinitialiser la grille* (Ctrl+D)
  - *Réinitialiser la palette* (Ctrl+P)
    
- Menu **Filtre** :  
  - Filtre rouge/vert/bleu/négatif/gris (Ctrl+R / Ctrl+V / Ctrl+B / Ctrl+N / Ctrl+G)
    
- Menu **Effets** :  
  - *Noir & Blanc* (Ctrl+E)
    
- Menu **Sauvegarder** :  
  - Enregistrer la grille (Ctrl+S)
    
- Menu **Supprimer** :  
  - Effacer la création sélectionnée (Ctrl+X)
    
- Menu **Quitter** :  
  - Fermer l’application (Ctrl+Q)  

**Barre d’Outils (ToolBar)** :  
- Icônes pour les mêmes actions (réinitialiser la grille/palette, filtres, etc.).  

**Barre d'État (StatusBar)** :  
- Bandeau d’information en bas permettant de confirmer les actions (changement d’outil, couleur mise à jour, succès de la sauvegarde, etc.).

---

## Sauvegarde, Chargement et Suppression de Créations

- **Sauvegarde** :  
  - Chaque création est enregistrée dans un fichier `.txt` placé dans le dossier `creations/`.
  - Chaque fichier contenant `(ligne, colonne, R, V, B)` pour les 32×32 pixels.
    
- **Chargement** :  
  - Via la ComboBox “Créations” : la grille se remplit automatiquement.
    
- **Suppression** :  
  - Effacement avec un **popup** de confirmation.  
  - Le fichier `.txt` correspondant est supprimé du dossier `creations/`, et la grille réinitialisée.

---

## Architecture du Code

Le projet est géré dans **une classe unique** : `Fenetre(QMainWindow)`.

1. **Initialisation & Configuration**  
   - Dimensions, titre, icône.  
   - Création des **layouts**.
   - Gestion des **raccourcis** (Ctrl+S, Ctrl+Q, etc.).  
   - Création du dossier `creations/` si inexistant.

2. **Panneau de Contrôle**  
   - GroupBox pour les **Outils**, la **Palette** et les **Sliders**.  
   - Popups (remplacement de couleur, suppression d’une création).

3. **Zone de Dessin**  
   - Grille 32×32 avec un `QGridLayout`. 
   - Méthode `colorier(row, col)` pour l’action de Stylo/Gomme.

4. **Palette de Couleurs**  
   - Liste de couleurs par défaut et listes spécialisées pour les filtres (rouge, vert, etc.).  
   - Méthodes pour appliquer rapidement un filtre ou réinitialiser la palette.

5. **Menus, ToolBar et StatusBar**  
   - Regrouper les actions (QAction) et leurs **raccourcis**.  
   - Afficher les icônes pour un accès rapide aux actions.
   - Gérer l’interaction (click + status bar) avec des messages d’état.

6. **Sauvegarde & Chargement**  
   - Écriture/Lecture des pixels dans des fichiers `.txt`, placés dans le répertoire `creations/`.
   - Gestion des erreurs (fichiers inexistants) via des `QMessageBox`.

7. **Effet Noir & Blanc**  
   - Convertit chaque pixel en nuance de gris selon la formule de luminosité.

8. **Suppression**  
   - Supprime le fichier `.txt` et retire la création de la ComboBox, après popup de confirmation.
     
---

## Exemple de flux d’utilisation

1. **Démarrer l’Application**  
   - Exécuter `pixelart_generator.py` : la fenêtre s’ouvre avec la grille (32×32) vide et la palette (3×3).

2. **Choisir un Outil**  
    - Par défaut, le “Stylo” est sélectionné.
    - Sélectionner “Gomme”, “Baguette” ou le “Pot” via la ComboBox.
           
3. **Sélectionner une Couleur**  
   - Cliquer sur une couleur de la palette (ex. rouge).  
   - *Optionnel* : Créer une **nouvelle couleur** via les sliders.
     - Utiliser “Ajouter à la palette” et sélectionner la couleur à remplacer via le **popup**.
            
4. **Dessiner / Effacer**  
   - Cliquer sur la grille pour appliquer la couleur ou effacer.  

5. **Appliquer un Filtre** (facultatif)  
   - Par exemple, Ctrl+V pour un **Filtre Vert** sur la palette.

6. **Sauvegarder la Création**  
   - Menu “Sauvegarder” (Ctrl+S), nommer le fichier.  
   - Un fichier `.txt` est créé dans `creations/`, ajouté à la ComboBox “Créations”.
  
7. **Charger ou Supprimer une Création**  
   - Sélectionner un nom dans la ComboBox “Créations” pour recharger.  
   - Ou Ctrl+X pour la supprimer (avec popup de confirmation).
     
8. **Appliquer l’Effet Noir & Blanc** (facultatif)  
   - Ctrl+E pour transformer le dessin en niveaux de gris, rendu plus contrasté.

9. **Quitter l’Application**  
   - Via le menu (Ctrl+Q).
     
---

## Notes et Remarques

- **Modification de la taille de la grille** :  
  Dans le code, vous pouvez changer :

```python
  self.lignes = 32
  self.colonnes = 32
```

  Adaptez ces valeurs (ex. 16×16, 64×64), et ajustez la taille de la fenêtre si nécessaire.
  *Vous pouvez également modifier la **taille des cases** ou la **couleur de fond** de la grille 
  en ajustant le style CSS des `QLabel`. Par exemple :*  

```python
  case.setStyleSheet("background-color: white; border: 1px solid black; min-width: 20px; min-height: 20px;")
```

  *pour définir des dimensions ou une couleur différentes.*

- **Icônes** :  
  Assurez-vous que le dossier `icons/` est présent et contient les fichiers requis (ex. `reset.png`, `filtre_rouge.png`).  
  Sinon, les icônes ne s’afficheront pas dans la barre d’outils / menus.

- **Compatibilité Python** :  
  Testé sous Python 3.7+. De légères différences peuvent exister avec des versions plus anciennes ou plus récentes.

- **Raccourcis Clavier** (rappel) :  
  - **Ctrl+D** : Réinitialiser la grille  
  - **Ctrl+P** : Réinitialiser la palette  
  - **Ctrl+R / Ctrl+V / Ctrl+B / Ctrl+N / Ctrl+G** : Filtres  
  - **Ctrl+E** : Effet Noir & Blanc sur la grille
  - **Ctrl+S** : Sauvegarder  
  - **Ctrl+X** : Supprimer la création sélectionnée
  - **Ctrl+Q** : Quitter  

---

## Prérequis

- **Python 3.x** (version ≥ 3.7 recommandée)  
- **PyQt5** (installation via pip) :
  
```bash
pip install PyQt5
```
