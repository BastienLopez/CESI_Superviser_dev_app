import unittest
from flask import Flask
from app.main import app
import requests
import docker
import time

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Crée un client Docker pour le test
        cls.docker_client = docker.from_env()

        # Lance le conteneur en mode détaché
        cls.container = cls.docker_client.containers.run(
            "cesi_superviser_dev_app-app",  # Nom de l'image Docker
            detach=True,
            ports={"8000/tcp": 8000}
        )
        # Attend quelques secondes pour que le conteneur soit prêt
        time.sleep(5)

    @classmethod
    def tearDownClass(cls):
        # Stoppe et supprime le conteneur Docker après le test
        cls.container.stop()
        cls.container.remove()
        cls.docker_client.close()

    def setUp(self):
        # Configure une application de test Flask
        self.app = app.test_client()
        self.app.testing = True

    def test_home_route(self):
        """
        Teste si la route principale ('/') retourne un statut 200 et le contenu attendu.
        """
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bienvenue sur Breizhsport!', response.data)

    def test_docker_container_running(self):
        """
        Vérifie que le conteneur Docker pour l'application tourne et répond.
        """
        response = requests.get("http://localhost:8000")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Bienvenue sur Breizhsport!", response.text)

if __name__ == "__main__":
    unittest.main()
