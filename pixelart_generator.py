
import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QSlider, QVBoxLayout, QWidget, QAction, QToolBar, QHBoxLayout, QLabel, QFileDialog,
                             QGridLayout, QComboBox, QPushButton, QDialog, QInputDialog, QMessageBox, QFrame, QStatusBar, QGroupBox)
from PyQt5.QtCore import Qt, QCoreApplication, QSize, QDir
from PyQt5.QtGui import QIcon, QPalette


class Fenetre(QMainWindow):
    def __init__(self):
        """
        Initialise la fenêtre principale et configure l'interface du générateur de PixelArt.
        """
        super().__init__()

        #-------- Configuration de la fenêtre principale --------
        self.setWindowTitle("Générateur de PixelArt")
        self.setWindowIcon(QIcon("icons/pixelart_logo.jpg"))
        self.setFixedSize(1200, 900)

        # Dossier des créations prédéfinies
        self.CREATIONS_FOLDER = os.path.join(QDir.currentPath(), "creations")
        if not os.path.exists(self.CREATIONS_FOLDER):
            os.makedirs(self.CREATIONS_FOLDER)

        # Constantes pour la taille de la palette
        self.PALETTE_ROWS = 3
        self.PALETTE_COLS = 3

        # Couleur par défaut : blanc
        self.couleur_rouge = 255
        self.couleur_verte = 255
        self.couleur_bleu = 255

        # Valeurs par défaut des sliders
        self.val_rouge = 255
        self.val_vert = 255
        self.val_bleu = 255

        #-------- Création du layout principal (horizontal) --------
        self.layout_principal = QHBoxLayout()      
        self.layout_principal.setContentsMargins(20, 20, 20, 20)
        self.layout_principal.setSpacing(20)

        #-------- Partie gauche : contrôles --------
        self.layout_gauche = QVBoxLayout()
        self.layout_gauche.setContentsMargins(20, 10, 20, 10)
        self.layout_gauche.setSpacing(15)

        #-------- Partie droite : grille de dessin --------
        self.layout_droite = QVBoxLayout() 
        self.affichage_grille = QGridLayout()
        self.affichage_grille.setSpacing(1)

        #-------- Layout horizontal pour ComboBox "Outils" et "Créations" --------
        self.layout_outils_predef = QHBoxLayout()
        self.layout_outils_predef.setSpacing(15)
        self.layout_outils_predef.setContentsMargins(5, 5, 5, 5)

        #-------- Configuration partie gauche : contrôles --------
        # Titre principal
        self.label_principal = QLabel("Générateur de PixelArt")
        self.label_principal.setStyleSheet("font-size: 26px; font-weight: bold; color: #222;")
        self.label_principal.setAlignment(Qt.AlignCenter)
        self.layout_gauche.addWidget(self.label_principal)

        # QGroupBox "Outils & Créations"
        self.group_outils_creations = QGroupBox("Outils && Créations")
        self.group_outils_creations.setStyleSheet(
            "QGroupBox { font-size: 18px; font-weight: bold; color: #555; margin-top: 8px;"
            "border: 2px solid #aaa; border-radius: 5px; padding: 10px; }"
            "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; }"
        )

        # Layout vertical interne au groupbox
        group_outils_layout = QVBoxLayout()
        group_outils_layout.setContentsMargins(10, 20, 10, 5)
        self.group_outils_creations.setLayout(group_outils_layout)

        # ComboBox "Outils"
        self.combo_outils = QComboBox()
        for outil in ["Stylo", "Gomme", "Baguette", "Pot"]:
            self.combo_outils.addItem(outil)
        self.combo_outils.setFixedSize(150, 30)
        self.combo_outils.setStyleSheet("font-size: 16px; border: 1px solid #aaa; border-radius: 5px; padding: 2px; background-color: white;")
        self.combo_outils.activated[str].connect(self.choix_tools)
        self.layout_outils_predef.addWidget(self.combo_outils)
        self.layout_outils_predef.addSpacing(20)

        # ComboBox "Créations"
        self.combo_predef = QComboBox()
        self.combo_predef.setFixedSize(150, 30)
        self.combo_predef.setStyleSheet("font-size: 16px; border: 1px solid #aaa; border-radius: 5px; padding: 2px; background-color: white;")
        self.remplirPredef()
        self.combo_predef.activated[str].connect(self.choix_predefs)
        self.layout_outils_predef.addWidget(self.combo_predef)

        group_outils_layout.addLayout(self.layout_outils_predef)
        self.layout_gauche.addWidget(self.group_outils_creations)

        # QGroupBox "Sélection & Palette"
        self.group_couleur_palette = QGroupBox("Sélection && Palette")
        self.group_couleur_palette.setStyleSheet(
            "QGroupBox { font-size: 18px; font-weight: bold; color: #555; margin-top: 10px;"
            "border: 2px solid #aaa; border-radius: 5px; padding: 10px; }"
            "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; }"
        )
        layout_couleur_palette = QVBoxLayout()
        layout_couleur_palette.setContentsMargins(10, 10, 10, 10)
        layout_couleur_palette.setSpacing(10)
        self.group_couleur_palette.setLayout(layout_couleur_palette)
        self.group_couleur_palette.setFixedHeight(320)

        # Label "Couleurs Sélectionnée"
        self.label_selectionnee = QLabel("Couleur Sélectionnée")
        self.label_selectionnee.setAlignment(Qt.AlignCenter)
        self.label_selectionnee.setStyleSheet("color: #333; font-size: 16px")
        layout_couleur_palette.addWidget(self.label_selectionnee)

        # Zone de la couleur actuelle   
        self.couleur_actuelle = QLabel()
        self.couleur_actuelle.setStyleSheet("background-color: white ; border: 2px solid grey; border-radius: 10px;")
        self.couleur_actuelle.setFixedSize(50, 50)
        layout_couleur_palette.addWidget(self.couleur_actuelle, alignment=Qt.AlignCenter)
        layout_couleur_palette.addSpacing(15)

        # Label "Palette de couleurs"
        self.couleurs_label = QLabel("Palette de couleurs")
        self.couleurs_label.setStyleSheet("color: #333; font-size: 16px")
        layout_couleur_palette.addWidget(self.couleurs_label, alignment=Qt.AlignCenter)
        layout_couleur_palette.addSpacing(5)

        # Grille de la palette
        self.palette_grid = QGridLayout()

        self.liste_couleurs_default = [
            (0, 0, 0), (147, 32, 255), (0, 0, 255), 
            (255, 153, 0), (255, 0, 0), (255, 255, 0), 
            (0, 104, 0), (171, 220, 244), (255, 255, 255)
        ]
        
        # Listes de filtres
        self.liste_filtre_rouge = [
            (255,0,0), (255, 94, 95), (255,51,94),
            (128,0,0), (220,20,60), (255, 97, 131),
            (255, 23, 131), (205,92,92), (240,128,128),
            (255, 124, 95)
        ]
        self.liste_filtre_vert = [
            (107,142,35), (85,107,47), (128,128,0),
            (46,139,87), (32,178,170), (60,179,113),
            (152,251,152), (0,255,0), (173,255,47),
            (34,139,34)
        ]
        self.liste_filtre_bleu = [
            (72,61,139), (230,230,250), (176,224,230),
            (135,206,250), (0,191,255), (30,144,255),
            (100,149,237), (123,104,238), (65,105,225),
            (0,0,205)
        ]
        self.liste_filtre_negatif = [
            (15,164,250), (0,255,247), (0,255,154),
            (220,232,255), (162,255,0), (0,204,204),
            (171,255,135), (192,192,192), (32,32,32),
            (0,153,153)
        ]
        self.liste_filtre_gris = [
            (121,128,129), (90,94,107), (220,220,220),
            (119,136,153), (112,128,144), (192,192,192),
            (209,197,197), (146,122,122), (131,113,113),
            (94,77,77)
        ]

        # Création des boutons de la palette par défaut
        indice = 0
        for i in range(self.PALETTE_ROWS):
            for j in range(self.PALETTE_COLS):
                bouton_couleur = QPushButton()
                bouton_couleur.setFixedSize(40, 40)
                bouton_couleur.setStyleSheet(
                    f"background-color:rgb{self.liste_couleurs_default[indice]}; border: 2px solid grey;"
                    "border-radius: 10px;"
                )
                bouton_couleur.clicked.connect(lambda event, row=i, col=j: self.recup_couleur_palette(row, col))
                self.palette_grid.addWidget(bouton_couleur, i, j)
                indice += 1

        layout_couleur_palette.addLayout(self.palette_grid)
        layout_couleur_palette.addStretch()

        self.layout_gauche.addSpacing(5)
        self.layout_gauche.addWidget(self.group_couleur_palette)

        # QGroupBox "Création de couleur"
        self.group_sliders = QGroupBox("Création de couleur")
        self.group_sliders.setStyleSheet(
            "QGroupBox { font-size: 18px; font-weight: bold; color: #555; margin-top: 10px; border: 2px solid #aaa; border-radius: 5px; padding: 10px; }"
            "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; }"
        )
        layout_sliders = QVBoxLayout()
        layout_sliders.setContentsMargins(10, 15, 0, 0)
        layout_sliders.setSpacing(10)
        self.group_sliders.setLayout(layout_sliders)
        self.group_sliders.setFixedHeight(250)

        # Sliders pour créer une nouvelle couleur (R, V, B)
        self.box_slider1 = QHBoxLayout()
        self.box_slider2 = QHBoxLayout()
        self.box_slider3 = QHBoxLayout()

        self.slider_rouge = QSlider(Qt.Horizontal)
        self.slider_vert = QSlider(Qt.Horizontal)
        self.slider_bleu = QSlider(Qt.Horizontal)

        # Configuration des sliders
        slider_config = [
            (self.slider_rouge, self.val_rouge),
            (self.slider_vert, self.val_vert),
            (self.slider_bleu, self.val_bleu),
        ]
        for slider, default_value in slider_config:
            slider.setMinimum(0)
            slider.setMaximum(255)
            slider.setValue(default_value)
            slider.valueChanged.connect(self.change_couleur)

        self.label_slider_rouge = QLabel("Rouge")
        self.label_slider_vert = QLabel("Vert")
        self.label_slider_bleu = QLabel("Bleu")

        # Configuration des labels des sliders
        slider_labels = [
            (self.label_slider_rouge, "red"),
            (self.label_slider_vert, "green"),
            (self.label_slider_bleu, "blue"),
        ]
        fixed_width = 80
        for label, color in slider_labels:
            label.setStyleSheet(f"color: {color}; font-size: 14px;")
            label.setAlignment(Qt.AlignRight)
            label.setFixedWidth(fixed_width)

        self.box_slider1.addWidget(self.slider_rouge)
        self.box_slider1.addWidget(self.label_slider_rouge)
        self.box_slider2.addWidget(self.slider_vert)
        self.box_slider2.addWidget(self.label_slider_vert)
        self.box_slider3.addWidget(self.slider_bleu)
        self.box_slider3.addWidget(self.label_slider_bleu)

        layout_sliders.addLayout(self.box_slider1)
        layout_sliders.addLayout(self.box_slider2)
        layout_sliders.addLayout(self.box_slider3)
        layout_sliders.addSpacing(5)

        # Label correspondant à la couleur créée
        self.ma_couleur_label = QLabel()
        self.ma_couleur_label.setStyleSheet(
        f"""
        background-color: rgb({self.val_rouge},{self.val_vert},{self.val_bleu});
        border: 2px solid black;
        border-radius: 10px;
        font-size: 16px;
        font-weight: bold;
        padding: 5px;
        color: white;
        """
        )
        self.change_couleur()
        layout_sliders.addWidget(self.ma_couleur_label, alignment=Qt.AlignCenter)
        self.layout_gauche.addSpacing(5)

        # Bouton "Ajouter à la palette"
        bouton_ajout = QPushButton("Ajouter à la palette")
        bouton_ajout.clicked.connect(self.afficher_popup)
        bouton_ajout.setFixedSize(225, 50)
        bouton_ajout.setStyleSheet(
            "font-size: 16px; font-weight: bold; background-color: #008CBA;" 
            "color: white; border-radius: 10px;"
        )
        layout_sliders.addWidget(bouton_ajout, alignment=Qt.AlignCenter)

        self.layout_gauche.addSpacing(10)
        self.layout_gauche.addWidget(self.group_sliders)
        self.layout_gauche.addStretch() 

        #-------- Configuration partie droite : grille de dessin --------
        self.lignes = 32
        self.colonnes = 32
        for i in range(self.lignes):
            for j in range(self.colonnes):
                case = QLabel()
                case.setStyleSheet("background-color:white; border: 1px solid black")
                case.mousePressEvent = lambda event, row=i, col=j: self.colorier(row, col)
                self.affichage_grille.addWidget(case, i, j)

        self.grid_widget = QWidget()
        self.grid_widget.setLayout(self.affichage_grille)
        self.grid_widget.setStyleSheet("background-color: #f0f0f0; border: 3px outset #ccc;")
        self.layout_droite.addWidget(self.grid_widget)
        
        # Séparateur vertical
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.VLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        self.separator.setStyleSheet("background-color: #ccc; width: 2px;")

        #-------- Assemblage final du layout principal --------
        self.layout_principal.addLayout(self.layout_gauche, 1)
        self.layout_principal.addWidget(self.separator)
        self.layout_principal.addLayout(self.layout_droite, 3)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.layout_principal)
        self.setCentralWidget(self.main_widget)

        #-------- Configuration de la Menu Bar --------
        self.menu = self.menuBar()

        # Menu "Grille"
        self.reinitialiser_action = QAction(QIcon("icons/reset.png"), "Réinitialiser", self)
        self.reinitialiser_action.triggered.connect(self.onReset)
        self.reinitialiser_action.setShortcut('Ctrl+D')

        self.reinitialiser_palette_action = QAction(QIcon("icons/reset_palette.png"), "Réinitialiser la palette", self)
        self.reinitialiser_palette_action.triggered.connect(self.onResetPalette)
        self.reinitialiser_palette_action.setShortcut('Ctrl+P')

        self.menuGrille = self.menu.addMenu("&Grille")
        self.menuGrille.addAction(self.reinitialiser_action)
        self.menuGrille.addSeparator()
        self.menuGrille.addAction(self.reinitialiser_palette_action)

        # Menu "Filtre"
        self.filtre_rouge = QAction(QIcon("icons/cercle_rouge.png"), "Filtre rouge", self)
        self.filtre_rouge.triggered.connect(self.filtration_rouge)
        self.filtre_rouge.setShortcut('Ctrl+R')

        self.filtre_vert = QAction(QIcon("icons/cercle_vert.png"), "Filtre vert", self)
        self.filtre_vert.triggered.connect(self.filtration_verte)
        self.filtre_vert.setShortcut('Ctrl+V')

        self.filtre_bleu = QAction(QIcon("icons/cercle_bleu.png"), "Filtre bleu", self)
        self.filtre_bleu.triggered.connect(self.filtration_bleu)
        self.filtre_bleu.setShortcut('Ctrl+B')

        self.filtre_negatif = QAction(QIcon("icons/cercle_negatif.png"), "Filtre négatif", self)
        self.filtre_negatif.triggered.connect(self.filtration_negatif)
        self.filtre_negatif.setShortcut('Ctrl+N')

        self.filtre_gris = QAction(QIcon("icons/cercle_gris.png"), "Filtre gris", self)
        self.filtre_gris.triggered.connect(self.filtration_gris)
        self.filtre_gris.setShortcut('Ctrl+G')

        self.menuFiltre = self.menu.addMenu("&Filtre")
        self.menuFiltre.addAction(self.filtre_rouge)
        self.menuFiltre.addSeparator()
        self.menuFiltre.addAction(self.filtre_vert)
        self.menuFiltre.addSeparator()
        self.menuFiltre.addAction(self.filtre_bleu)
        self.menuFiltre.addSeparator()
        self.menuFiltre.addAction(self.filtre_negatif)
        self.menuFiltre.addSeparator()
        self.menuFiltre.addAction(self.filtre_gris)

        # Menu "Effets"
        self.effet_noir_et_blanc = QAction(QIcon("icons/cercle_noir_et_blanc.png"), "Effet Noir et Blanc", self)
        self.effet_noir_et_blanc.triggered.connect(self.effet_n_et_b)
        self.effet_noir_et_blanc.setShortcut('Ctrl+E')

        self.menuEffet = self.menu.addMenu("&Effets")
        self.menuEffet.addAction(self.effet_noir_et_blanc)

        # Menu "Sauvegarder"
        self.sauvegarder_action = QAction(QIcon("icons/sauvegarde.png"), "Sauvegarder", self)
        self.sauvegarder_action.triggered.connect(self.on_save)
        self.sauvegarder_action.setShortcut('Ctrl+S')

        self.menuSauvegarder = self.menu.addMenu("&Sauvegarder")
        self.menuSauvegarder.addAction(self.sauvegarder_action)

        # Menu "Quitter"
        self.quitter_action = QAction(QIcon("icons/quitter.png"), "Quitter", self)
        self.quitter_action.triggered.connect(self.on_exit)
        self.quitter_action.setShortcut('Ctrl+Q')

        self.menuQuitter = self.menu.addMenu("&Quitter")
        self.menuQuitter.addAction(self.quitter_action)

        # Menu "Supprimer"
        self.supprimer_action = QAction(QIcon("icons/supprimer.png"), "Supprimer création", self)
        self.supprimer_action.triggered.connect(self.supprimer_creation)
        self.supprimer_action.setShortcut('Ctrl+X')

        self.menuSupprimer = self.menu.addMenu("&Supprimer")
        self.menuSupprimer.addAction(self.supprimer_action)

        #-------- Configuration de la Tool Bar --------
        self.toolbar = QToolBar("Ma toolbar")
        self.toolbar.setIconSize(QSize(36, 36))
        self.addToolBar(self.toolbar)

        # Ajout des actions à la toolbar avec des infobulles
        self.reinitialiser_action.setToolTip("Réinitialiser la grille")
        self.reinitialiser_palette_action.setToolTip("Réinitialiser la palette")
        self.filtre_rouge.setToolTip("Filtre rouge")
        self.filtre_vert.setToolTip("Filtre vert")
        self.filtre_bleu.setToolTip("Filtre bleu")
        self.filtre_negatif.setToolTip("Filtre négatif")
        self.filtre_gris.setToolTip("Filtre gris")
        self.effet_noir_et_blanc.setToolTip("Effet Noir et Blanc")
        self.sauvegarder_action.setToolTip("Sauvegarder")
        self.supprimer_action.setToolTip("Supprimer la création sélectionnée")
        self.quitter_action.setToolTip("Quitter")


        self.toolbar.addAction(self.reinitialiser_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.reinitialiser_palette_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.filtre_rouge)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.filtre_vert)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.filtre_bleu)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.filtre_negatif)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.filtre_gris)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.effet_noir_et_blanc)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.sauvegarder_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.supprimer_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.quitter_action)
        self.toolbar.addSeparator()

        #-------- Configuration de la StatusBar --------
        self.statusbar = QStatusBar()
        self.statusbar.setStyleSheet("font-size: 14px;")
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("🖌️ Prêt pour dessiner.")  


    #-------- Méthodes de Callback & Gestion des événements --------
    def change_couleur(self):
        """
        Met à jour la couleur en fonction des sliders et ajuste les labels correspondants.
        """        
        self.val_rouge = self.slider_rouge.value()
        self.val_vert = self.slider_vert.value()
        self.val_bleu = self.slider_bleu.value()

        self.label_slider_rouge.setText(f"Rouge : {self.val_rouge:03}")
        self.label_slider_vert.setText(f"Vert : {self.val_vert:03}")
        self.label_slider_bleu.setText(f"Bleu : {self.val_bleu:03}")

        brightness = (self.val_rouge * 0.299 + self.val_vert * 0.587 + self.val_bleu * 0.114)
        
        if brightness > 186:
            text_color = "black"

        else:
            text_color = "white"

        self.ma_couleur_label.setText(f"rgb({self.val_rouge:03},{self.val_vert:03},{self.val_bleu:03})")
        self.ma_couleur_label.setStyleSheet(
        f"""
        background-color: rgb({self.val_rouge},{self.val_vert},{self.val_bleu});
        border: 2px solid black;
        border-radius: 10px;
        font-size: 16px;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        padding: 5px;
        color: {text_color};
        """
        )
        self.ma_couleur_label.setFixedSize(178, 35)
        self.statusBar().showMessage(f"🧪 Couleur mise à jour : rgb({self.val_rouge:03}, {self.val_vert:03}, {self.val_bleu:03}).", 2000)


    def recup_couleur_palette(self, row, col):
        """
        Récupère la couleur du bouton situé à la position (row, col) dans la palette pour l'afficher comme couleur actuelle.
        """
        bouton = self.palette_grid.itemAtPosition(row, col).widget()
        couleur = bouton.palette().color(QPalette.Window)        
        
        # Récupère la valeur de la composante rouge, bleue et verte
        self.couleur_rouge = couleur.red()               
        self.couleur_verte = couleur.green()
        self.couleur_bleu = couleur.blue()

        self.couleur_actuelle.setStyleSheet(
            f"background-color: rgb({self.couleur_rouge},{self.couleur_verte},{self.couleur_bleu}); "
            "border: 2px solid grey; border-radius: 10px;"
        )
        self.statusBar().showMessage("🎨 Couleur sélectionnée dans la palette.", 2000)


    def colorier(self, row, col):
        """
        Colorie ou gomme une case de la grille en fonction de l'outil sélectionné.
        """
        case = self.affichage_grille.itemAtPosition(row, col).widget()
        outil = self.combo_outils.currentText()

        if outil == "Stylo":
            case.setStyleSheet(f"background-color: rgb({self.couleur_rouge},{self.couleur_verte},{self.couleur_bleu}); border: 1px solid black")
            self.statusBar().showMessage("🖌️ Case colorée.", 1500)

        elif outil == "Gomme":
            case.setStyleSheet(f"background-color:white; border: 1px solid black")
            self.statusBar().showMessage("🧽 Case effacée.", 1500)


    def choix_tools(self, text):
        """
        Applique le comportement correspondant à l'outil sélectionné dans la combo box.
        """
        if text == "Baguette":
            for i in range(self.lignes):
                for j in range(self.colonnes):
                    case = self.affichage_grille.itemAtPosition(i, j).widget()
                    col = case.palette().color(QPalette.Window)
                    if (self.couleur_rouge == col.red() and self.couleur_verte == col.green() and self.couleur_bleu == col.blue()):
                        case.setStyleSheet("background-color:white; border: 1px solid black")
            self.statusBar().showMessage("✨ Baguette sélectionnée.", 2000)

        elif text == "Pot":
            for i in range(self.lignes):
                for j in range(self.colonnes):
                    case = self.affichage_grille.itemAtPosition(i, j).widget()
                    col = case.palette().color(QPalette.Window)
                    if col.red() == 255 and col.green() == 255 and col.blue() == 255:
                        case.setStyleSheet(f"background-color: rgb({self.couleur_rouge},{self.couleur_verte},{self.couleur_bleu}); border: 1px solid black")
            self.statusBar().showMessage("🧺 Pot sélectionné.", 2000)

        else:
            if text == "Stylo":
                self.statusBar().showMessage("🖌️ Stylo sélectionné.", 2000)

            elif text == "Gomme":
                self.statusBar().showMessage("🧹 Gomme sélectionnée.", 2000)


    def choix_predefs(self, text):
        """
        Charge une configuration prédéfinie à partir d'un fichier texte.
        """
        try:
            with open(os.path.join(self.CREATIONS_FOLDER, text + ".txt"), "r") as pixelArtTxt:
                pixelArt = pixelArtTxt.readlines()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de charger la création : {e}")
            return

        for pixel in pixelArt:
            infos_pixel = pixel.split()
            btn = self.affichage_grille.itemAtPosition(int(infos_pixel[0]), int(infos_pixel[1])).widget()
            btn.setStyleSheet(f"background-color: rgb({infos_pixel[2]},{infos_pixel[3]},{infos_pixel[4]}); border: 1px solid black")
        self.statusBar().showMessage(f"🚀 Création '{text}' chargée.", 2000)


    def afficher_popup(self):
        """
        Affiche un popup pour choisir la couleur de la palette à remplacer par la nouvelle couleur.
        """
        self.popup = QDialog()
        self.popup.setWindowTitle("Remplacer couleur")
        self.popup.setWindowIcon(QIcon("icons/palette_logo.png"))
        self.popup.setFixedSize(300, 150)
        self.popup.setStyleSheet("background-color: #f7f7f7; font-size: 14px;")

        # Lyout vertical pour le popup
        sous_page_box = QVBoxLayout()
        sous_page_box.setContentsMargins(20, 20, 20, 20)
        sous_page_box.setSpacing(5)

        # Label centré
        label_popup = QLabel("Choisissez la couleur à remplacer: ")
        label_popup.setStyleSheet("color: #333; font-size: 16px")
        label_popup.setAlignment(Qt.AlignCenter)
        sous_page_box.addWidget(label_popup)

        # Layout horizontal pour les boutons de la palette
        pal_box = QHBoxLayout()
        pal_box.setSpacing(10)
        pal_box.setAlignment(Qt.AlignCenter)

        for i in range(self.PALETTE_ROWS):
            for j in range(self.PALETTE_COLS):
                coord = self.palette_grid.itemAtPosition(i, j).widget()
                couleur = coord.palette().color(QPalette.Window)
                button = QPushButton()
                button.setFixedSize(25, 25)
                button.setStyleSheet(f"background-color: {couleur.name()} ; border: 2px solid grey; border-radius: 10px;")
                button.clicked.connect(lambda event, row=i, col=j: self.couleur_a_remplacer(row, col))
                pal_box.addWidget(button)

        sous_page_box.addLayout(pal_box)
        self.popup.setLayout(sous_page_box)
        self.popup.exec()


    def onReset(self):
        """
        Réinitialise la grille de dessin en remplissant chaque case de blanc.
        """
        for i in range(self.lignes):
            for j in range(self.colonnes):
                case = self.affichage_grille.itemAtPosition(i, j).widget()
                case.setStyleSheet("background-color:white; border: 1px solid black")
        self.statusBar().showMessage("🔄 Grille réinitialisée.", 2000)


    def onResetPalette(self):
        """
        Réinitialise la palette avec les couleurs par défaut.
        """
        indice = 0
        for i in range(self.PALETTE_ROWS):
            for j in range(self.PALETTE_COLS):
                coord = self.palette_grid.itemAtPosition(i, j).widget()
                coord.setStyleSheet(f"background-color:rgb{self.liste_couleurs_default[indice]}; border: 2px solid grey; border-radius: 10px;")
                indice += 1
        self.statusBar().showMessage("🎨🔄 Palette réinitialisée.", 2000)


    def appliquer_filtre(self, liste_couleurs):
        """
        Applique un filtre à la palette en remplaçant chaque couleur par la liste fournie.
        """
        indice = 0
        for i in range(self.PALETTE_ROWS):
            for j in range(self.PALETTE_COLS):
                bouton = self.palette_grid.itemAtPosition(i, j).widget()
                bouton.setStyleSheet(f"background-color:rgb{liste_couleurs[indice]}; border: 1px solid black")
                indice += 1


    def filtration_rouge(self):
        """
        Applique le filtre rouge sur la palette.
        """
        self.appliquer_filtre(self.liste_filtre_rouge)
        self.statusBar().showMessage("🔴 Filtre Rouge appliqué.", 2000)


    def filtration_verte(self):
        """
        Applique le filtre vert sur la palette.
        """
        self.appliquer_filtre(self.liste_filtre_vert)
        self.statusBar().showMessage("🟢 Filtre Vert appliqué.", 2000)


    def filtration_bleu(self):
        """
        Applique le filtre bleu sur la palette.
        """
        self.appliquer_filtre(self.liste_filtre_bleu)
        self.statusBar().showMessage("🔵 Filtre Bleu appliqué.", 2000)


    def filtration_negatif(self):
        """
        Applique le filtre négatif sur la palette.
        """
        self.appliquer_filtre(self.liste_filtre_negatif)
        self.statusBar().showMessage("🌓 Filtre Négatif appliqué.", 2000)


    def filtration_gris(self):
        """
        Applique le filtre gris sur la palette.
        """
        self.appliquer_filtre(self.liste_filtre_gris)
        self.statusBar().showMessage("⚪️ Filtre Gris appliqué.", 2000)
    

    def couleur_a_remplacer(self, row, col):
        """
        Remplace la couleur de la palette par la couleur créée via les sliders.
        """
        coord = self.palette_grid.itemAtPosition(row, col).widget()
        coord.setStyleSheet(f"background-color: rgb({self.val_rouge},{self.val_vert},{self.val_bleu}); border: 2px solid grey; border-radius: 10px;")
        self.popup.accept()
        self.statusBar().showMessage("🎨⚙️ Palette mise à jour.", 2000)


    def on_save(self):
        """
        Sauvegarde la configuration de la grille dans un fichier texte.
        """
        options = QFileDialog.Options()
        fichier, _ = QFileDialog.getSaveFileName(self, "Enregistrer votre création", self.CREATIONS_FOLDER, "Fichiers texte (*.txt)", options=options)

        if fichier:
            nom_creation = os.path.basename(fichier).split('.')[0]          # On retire l'extension ".txt"

            if self.combo_predef.findText(nom_creation) == -1:
                self.combo_predef.addItem(nom_creation)

            with open(fichier, "w") as file:
                for i in range(self.lignes):
                    for j in range(self.colonnes):
                        case = self.affichage_grille.itemAtPosition(i, j).widget()
                        couleur = case.palette().color(QPalette.Window)
                        col_rouge, col_verte, col_bleu = couleur.red(), couleur.green(), couleur.blue()
                        file.write(f"{i} {j} {col_rouge} {col_verte} {col_bleu}\n")
            self.statusBar().showMessage("💾 Création sauvegardée.", 3000)    
    

    def supprimer_creation(self):
        """
        Supprime la création sélectionnée (du dossier des créations et de la combo box) après 
        confirmation de l'utilisateur et réinitialise la grille.
        """
        current_index = self.combo_predef.currentIndex()
        if current_index >= 0:
            nom_creation = self.combo_predef.currentText()

            # Affiche un pop-up de confirmation
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setWindowTitle("Confirmation de suppression")
            msgBox.setText(f"Êtes-vous sûr de vouloir supprimer la création '{nom_creation}' ?")
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msgBox.button(QMessageBox.Yes).setText("Oui")
            msgBox.button(QMessageBox.No).setText("Non")
            reply = msgBox.exec_()

            if reply == QMessageBox.Yes:
                chemin = os.path.join(self.CREATIONS_FOLDER, nom_creation + ".txt")
                if os.path.exists(chemin):
                    os.remove(chemin)
                self.combo_predef.removeItem(current_index)
                self.onReset()
                self.statusBar().showMessage("🗑️ Création supprimée.", 3000)


    def remplirPredef(self):                        
        """
        Remplit la combo box avec les créations existantes (fichiers .txt).
        """
        repertoire = self.CREATIONS_FOLDER
        for file in os.listdir(repertoire):          
            if file.endswith(".txt"):                
                self.combo_predef.addItem(file[:-4])       # Retire les 4 derniers caractères (".txt")


    def effet_n_et_b(self):
        """
        Applique un effet Noir et Blanc sur la grille en fonction de la luminosité de chaque case.
        """
        for i in range(self.lignes):
            for j in range(self.colonnes):
                case = self.affichage_grille.itemAtPosition(i, j).widget()
                col = case.palette().color(QPalette.Window)
                col_rouge = col.red()
                col_verte = col.green()
                col_bleu = col.blue()
                moy = (col_rouge + col_verte + col_bleu)//3
                if moy > 170 and moy != 255:
                    case.setStyleSheet("background-color:lightgray; border: 1px solid black")

                elif moy <= 170 and moy > 85:
                    case.setStyleSheet("background-color:grey; border: 1px solid black")

                elif moy <= 85:
                    case.setStyleSheet("background-color:black; border: 1px solid black")


    def on_exit(self):
        """
        Quitte l'application.
        """
        sys.exit()



# Programme principal
app = QCoreApplication.instance()
if app is None:
    app = QApplication(sys.argv)

window = Fenetre()
window.show()

app.exec_()
