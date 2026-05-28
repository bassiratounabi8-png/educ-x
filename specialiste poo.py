from abc import ABC, abstractmethod

class Question(ABC):
    def __init__(self, id, enonce, matiere, difficulte=1, auteur=None, explication=None):
        self.id = id
        self.enonce = enonce
        self.matiere = matiere
        self.difficulte = difficulte
        self.auteur = auteur
        self.explication = explication
        self.historique = []  # [True, False, True] pour suivre les réponses

    @abstractmethod
    def verifier_reponse(self, reponse):
        pass

    @abstractmethod
    def afficher(self):
        pass

    def ajouter_resultat(self, correct):
        self.historique.append(correct)

    @staticmethod
    def style_texte(texte, rouge=False, souligner=False):
        codes = []
        if rouge:
            codes.append("31")
        if souligner:
            codes.append("4")
        if not codes:
            return texte
        return f"\033[{';'.join(codes)}m{texte}\033[0m"

    def afficher_entete(self):
        entete = f"{self.matiere} — Difficulté {self.difficulte}"
        if self.auteur:
            entete += f" — Auteur: {self.auteur}"
        return entete

    def afficher_explication(self):
        return f"\nExplication : {self.explication}" if self.explication else ""

    def score(self):
        if not self.historique:
            return "Aucun résultat"
        correct = sum(self.historique)
        total = len(self.historique)
        return f"{correct}/{total} ({correct * 100 / total:.0f}%)"

    def __str__(self):
        return f"[{self.id}] {self.enonce} ({self.matiere})"

class QCM(Question):
    def __init__(self, id, enonce, matiere, choix, bonne_rep, difficulte=1, auteur=None, explication=None):
        super().__init__(id, enonce, matiere, difficulte, auteur=auteur, explication=explication)
        self.choix = choix  # ["Paris", "Lyon", "Marseille"]
        self.bonne_rep = bonne_rep  # index 0, 1, 2...

    def afficher(self, surbrillance=None):
        texte = f"\n{self.afficher_entete()}\n{self.enonce}\n"
        for i, c in enumerate(self.choix):
            indice = f"{i}."
            if surbrillance is not None and surbrillance == i:
                indice = self.style_texte(indice, rouge=True, souligner=True)
            ligne = f"  {indice} {c}"
            texte += f"{ligne}\n"
        return texte

    def verifier_reponse(self, reponse):
        try:
            valeur = int(reponse)
            est_correct = valeur == self.bonne_rep
        except (ValueError, TypeError):
            est_correct = str(reponse).strip().lower() == str(self.choix[self.bonne_rep]).strip().lower()
        self.ajouter_resultat(est_correct)
        return est_correct

class VraiFaux(Question):
    def __init__(self, id, enonce, matiere, reponse, difficulte=1, auteur=None, explication=None):
        super().__init__(id, enonce, matiere, difficulte, auteur=auteur, explication=explication)
        self.reponse = bool(reponse)  # True ou False

    def afficher(self, surbrillance=None):
        texte = f"\n{self.afficher_entete()}\n{self.enonce}\nVrai ou Faux ?"
        if surbrillance == 'vrai':
            texte = self.style_texte(texte, rouge=True, souligner=True)
        return texte

    def verifier_reponse(self, reponse):
        rep = str(reponse).strip().lower()
        vrai = rep in ["vrai", "v", "true", "t", "1", "oui", "o"]
        faux = rep in ["faux", "f", "false", "0", "non", "n"]
        if vrai:
            choix = True
        elif faux:
            choix = False
        else:
            choix = None
        est_correct = choix is not None and choix == self.reponse
        self.ajouter_resultat(est_correct)
        return est_correct
