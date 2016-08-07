# Setup
* Créer un virtualenv
* Installer les dépendences
   ```
   pip install -r requirements.txt
   ```
* Initialiser la base de données
  ```
  ./manage.py migrate
  ```
* Lancer le serveur développement
  ```
  ./manage.py runserver
  ```

# Usage

Il faut d'abord créer un compte (Create Account sur la page de login). Vous serez alors redirigé sur la page d'acceuil qui affiche un formulare pour uploader un modèle. Pour le test, les modèles sont juste des images.

Une fois qu'un modèle est uploadé, il est affiché sur la page d'acceuil. Vous pouvez cliquer dessus pour voir la page detail, ce qui va incrémenter son compteur de vue.

Les badges de l'utilisateur sont affichés dans la barre du haut. Pour simplifier les tests manuels, j'ai changé les limites:
 * star: 3 vues
 * collector: 4 modèles
 * pioneer: 1 minutes (ce badge est uniquement testé lors de la connection d'un utilisateur)

Vous pouvez lancer les tests avec :
```
./manage.py test
```
