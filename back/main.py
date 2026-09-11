from src.models import Personne, ArbreGenealogiqe, Lien, LienType
from src.persistence import MoteurPersistence


def hello_world():
    print('Hello world')

    test_personne = Personne(id="42",
                             prenom='toto',
                             nom_famille='a la ferme')
    other_personne = Personne(id="44",
                              prenom='the other one',
                              nom_famille='lalalalalalla')
    link = Lien(id="1",
                source="42",
                destination="44",
                type=LienType.PARTENAIRE)

    arbre_personne = ArbreGenealogiqe(personnes=[test_personne, other_personne], liens=[link])
    print(arbre_personne)

    # Faire une fonction stockage qui prend une personne et qui écrit dans un JSON.
    MoteurPersistence.dump(arbre_personne)

    # Faire une fonction charge qui décharge un JSON vers un objet Personne.
    test: ArbreGenealogiqe = MoteurPersistence.load(MoteurPersistence.FICHIER)
    print(test)
    print(type(test))

if __name__ == '__main__':
    hello_world()
