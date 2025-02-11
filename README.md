git clone [votre-url-github]
cd [nom-du-dossier]
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurez les variables d'environnement :
   - Copiez le fichier `.env.example` vers `.env`
   - Modifiez le fichier `.env` avec vos paramètres :
     ```
     DISCORD_TOKEN=votre_token_discord
     BOT_PREFIX=!
     DEBUG_MODE=False
     ```

## Utilisation

1. Démarrez le bot :
```bash
python bot.py
```

2. Dans Discord, utilisez la commande :
```
!lucie
```

Le bot tirera aléatoirement un atout et un défaut. Chaque élément tiré sera en cooldown pendant 1 heure.

## Structure du Projet

```
.
├── bot.py                 # Point d'entrée principal du bot
├── run_tests.py          # Script d'exécution des tests
├── tests/                # Tests automatisés
├── .env.example          # Exemple de configuration
├── .gitignore           # Fichiers à ignorer par Git
└── README.md            # Documentation (ce fichier)
```

## Tests

Pour exécuter les tests :
```bash
python run_tests.py