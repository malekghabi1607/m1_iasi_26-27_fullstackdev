from src.models import Personne


def hello_world():
    print('Hello world')

    test_personne = Personne(identifiant=42,
                             prenom='toto',
                             nom_famille='a la ferme')


if __name__ == '__main__':
    hello_world()
