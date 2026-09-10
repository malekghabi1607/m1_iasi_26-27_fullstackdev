from src.models import Personne
from src.persistence import MoteurPersistence


def hello_world():
    print('Hello world')

    test_personne = Personne(id="42",
                             prenom='toto',
                             nom_famille='a la ferme')

    # Faire une fonction stockage qui prend une personne et qui écrit dans un JSON.
    MoteurPersistence.dump(test_personne)

    # TODO: Faire une fonction charge qui décharge un JSON vers un objet Personne.

if __name__ == '__main__':
    hello_world()
