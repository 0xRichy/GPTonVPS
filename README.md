# GPTonVPS

GPTonVPS est un bot Python conçu pour être utilisé sur un VPS (Virtual Private Server). Le bot permet d'enregistrer et d'exécuter des commandes via une API Web. Il utilise la bibliothèque `paramiko` pour établir une connexion SSH avec le VPS et `flask` pour mettre en place l'API.

## Configuration requise

Avant d'exécuter le bot, assurez-vous d'avoir les éléments suivants configurés :

- Un VPS avec un accès SSH valide
- Python 3.x installé sur le VPS
- Les informations de connexion au VPS (adresse IP, nom d'utilisateur et mot de passe) doivent être mises à jour dans le fichier `GPT.py` avant l'exécution.

## Installation des dépendances

Pour installer les dépendances requises pour le bot, exécutez la commande suivante dans votre terminal :

```
pip install -r requirements.txt
```

Cela installera automatiquement les bibliothèques `paramiko` et `flask`.

## Utilisation

1. Mettez à jour les informations de connexion au VPS dans le fichier `GPT.py`.

2. Exécutez le bot en utilisant la commande suivante :

```
python GPT.py
```

3. Le bot démarre et est prêt à recevoir des commandes via une API.

## API

Le bot expose les endpoints suivants via l'API :

### `/command` (POST)

Permet de soumettre une commande à exécuter sur le VPS. Le corps de la requête POST doit être au format JSON avec la clé `"command"` contenant la commande à exécuter.

Exemple de requête :

```
POST /command
{
    "command": "ls -la"
}
```

### `/learn` (POST)

Permet d'apprendre des informations supplémentaires et de les enregistrer. Le corps de la requête POST doit être au format JSON avec les informations à apprendre.

Exemple de requête :

```
POST /learn
{
    "info": "Nouvelles informations à apprendre"
}
```

### `/internet` (GET)

Permet d'accéder à Internet en effectuant des requêtes HTTP. Il faut fournir une URL en tant que paramètre de requête.

Exemple de requête :

```
GET /internet?url=https://www.example.com
```

## Avertissement

GPTonVPS est conçu pour un usage expérimental uniquement. Assurez-vous de comprendre les risques liés à un tel bot, car il peut exposer votre VPS à des vulnérabilités de sécurité et à des abus. Utilisez-le avec prudence et mettez en œuvre les contrôles de sécurité appropriés pour protéger votre système.
