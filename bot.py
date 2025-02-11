import discord
import random
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
import os
from flask import Flask
from threading import Thread
import logging
import socket
import sys
import time

# Configuration des logs
logging.basicConfig(level=logging.DEBUG,  # Changé en DEBUG pour plus de détails
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Mécanisme de verrouillage pour une seule instance
def obtain_lock():
    try:
        # Force la suppression du verrou si le processus n'existe plus
        if os.path.exists('.bot.lock'):
            try:
                with open('.bot.lock', 'r') as f:
                    old_pid = int(f.read().strip())
                try:
                    os.kill(old_pid, 0)
                    logger.error(f"Une autre instance du bot est déjà en cours d'exécution (PID: {old_pid})")
                    return False
                except ProcessLookupError:
                    # Le processus n'existe plus, on peut supprimer le fichier
                    logger.info("Suppression du verrou obsolète")
                    os.remove('.bot.lock')
            except (ValueError, OSError) as e:
                logger.warning(f"Suppression du verrou invalide: {e}")
                os.remove('.bot.lock')

        # Crée un nouveau fichier de verrouillage
        with open('.bot.lock', 'w') as f:
            f.write(str(os.getpid()))
        return True
    except Exception as e:
        logger.error(f"Erreur lors de la création du verrou: {e}")
        if os.path.exists('.bot.lock'):
            try:
                os.remove('.bot.lock')
            except OSError:
                pass
        return False

# Flask app pour le keep-alive
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def find_free_port():
    ports_to_try = [8080, 8081, 8082, 8083, 8084, 8085]
    for port in ports_to_try:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('0.0.0.0', port))
            sock.close()
            return port
        except OSError:
            continue
    raise RuntimeError("Aucun port disponible trouvé")

def run_flask():
    try:
        port = find_free_port()
        app.run(host='0.0.0.0', port=port)
    except Exception as e:
        logger.exception(f"Erreur critique lors du démarrage du serveur Flask: {e}")

def keep_alive():
    try:
        server = Thread(target=run_flask, daemon=True)
        server.start()
    except Exception as e:
        logger.exception(f"Erreur critique lors du démarrage du thread keep-alive: {e}")

# Listes des Atouts et Défauts restent inchangées
atouts = [
    "L'un de vos sens est exceptionnellement développé. (Vue, ouïe, odorat… à vous de choisir.)",
    "Votre corps est d'une résistance impressionnante. (Vous encaissez mieux les coups et la fatigue.)",
    "Vous êtes particulièrement souple. (Passer dans des espaces exigus ou esquiver est plus aisé.)",
    "Vos réflexes sont d'une précision remarquable. (Votre corps réagit plus vite que votre pensée.)",
    "Votre musculature est bien au-dessus de la moyenne. (Force physique accrue.)",
    "Vous êtes incroyablement endurant. (Fatigue physique retardée, courses prolongées possibles.)",
    "Votre corps se remet vite des blessures. (Cicatrisation accélérée, douleurs moins handicapantes.)",
    "Vous avez une coordination parfaite. (Aucune maladresse, mouvements fluides et précis.)",
    "Votre respiration est maîtrisée. (Plongée en apnée, endurance en conditions difficiles.)",
    "Votre voix est captivante et autoritaire. (Difficile à ignorer, parfait pour imposer sa présence.)"
]

defauts = [
    "L'un de vos sens est particulièrement faible. (Vision trouble, mauvaise ouïe, odorat quasi inexistant…)",
    "Votre corps est fragile et supporte mal les blessures. (Moins de résistance aux coups et chocs.)",
    "Vous êtes étonnamment maladroit. (Vos gestes manquent de précision, risque accru de rater des actions fines.)",
    "Vous souffrez d'un handicap physique léger. (Boiterie, bras moins fonctionnel, manque de mobilité…)",
    "Votre force est anormalement basse. (Difficulté à soulever, porter, ou utiliser des objets lourds.)",
    "Votre endurance est limitée. (Vous vous fatiguez plus vite que la normale.)",
    "Votre corps guérit très lentement. (Les blessures, même mineures, mettent du temps à disparaître.)",
    "Vous manquez de coordination. (Vos mouvements sont parfois imprécis ou hésitants.)",
    "Votre respiration est faible. (Difficulté en altitude, en apnée, ou lors d'efforts prolongés.)",
    "Votre voix est faible ou monotone. (Difficile à entendre ou à rendre captivante.)"
]

# Historique des tirages et systèmes de verrouillage
recent_tirages = {}
command_lock = {}
processed_messages = set()  # Pour la déduplication des messages

def nettoyer_historique():
    maintenant = time.time()
    a_supprimer = []
    for tirage, timestamp in recent_tirages.items():
        if maintenant - timestamp > 3600:
            a_supprimer.append(tirage)
    for tirage in a_supprimer:
        del recent_tirages[tirage]

def tirage_unique(liste, historique):
    nettoyer_historique()
    maintenant = time.time()
    candidats = [item for item in liste if item not in historique.keys()]
    if not candidats:
        temps_restant = int(3600 - (maintenant - min(historique.values())))
        minutes = temps_restant // 60
        secondes = temps_restant % 60
        raise ValueError(f"Tous les éléments sont en cooldown. Veuillez attendre {minutes}m {secondes}s.")

    choix = random.choice(candidats)
    historique[choix] = maintenant
    return choix

# Configuration du bot avec des intents minimaux
load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logger.info(f'Bot connecté en tant que {bot.user}')

@bot.command()
async def lucie(ctx):
    # Déduplication des messages
    message_id = f"{ctx.message.id}"
    if message_id in processed_messages:
        logger.warning(f"Message {message_id} déjà traité, ignoré")
        return
    processed_messages.add(message_id)

    # Nettoyage périodique des messages traités
    if len(processed_messages) > 1000:
        processed_messages.clear()

    # Vérifications de base
    if not ctx.guild:
        logger.debug(f"Commande ignorée car envoyée en DM par {ctx.author.name}")
        return

    user_id = str(ctx.author.id)
    logger.info(f"Nouvelle commande lucie de {ctx.author.name} (ID: {user_id}, Message ID: {message_id})")

    if user_id in command_lock and command_lock[user_id]:
        logger.warning(f"Commande déjà en cours pour {ctx.author.name}")
        await ctx.send("Une commande est déjà en cours pour vous. Veuillez attendre.")
        return

    try:
        command_lock[user_id] = True
        logger.debug(f"Verrou activé pour {ctx.author.name}")

        try:
            atout = tirage_unique(atouts, recent_tirages)
            defaut = tirage_unique(defauts, recent_tirages)
            await ctx.send(f"🎲 **Résultat du tirage :**\n🎭 **Atout :** {atout}\n⚠️ **Défaut :** {defaut}")
            logger.info(f"Tirage réussi pour {ctx.author.name} (Message ID: {message_id})")
        except ValueError as ve:
            await ctx.send(str(ve))
            return

    except Exception as e:
        logger.exception(f"Erreur lors de l'exécution de la commande lucie: {e}")
        await ctx.send("Une erreur s'est produite lors du tirage. Veuillez réessayer.")
    finally:
        command_lock[user_id] = False
        logger.debug(f"Verrou désactivé pour {ctx.author.name}")

if __name__ == '__main__':
    if obtain_lock():
        try:
            keep_alive()
            token = os.getenv('DISCORD_TOKEN')
            if not token:
                logger.error("Token Discord non trouvé dans les variables d'environnement")
                sys.exit(1)
            bot.run(token)
        except Exception as e:
            logger.exception(f"Erreur critique lors du démarrage du bot: {e}")
        finally:
            try:
                os.remove('.bot.lock')
                logger.info("Fichier de verrouillage supprimé")
            except OSError:
                pass
    else:
        logger.error("Impossible d'obtenir le verrou. Une autre instance est peut-être déjà en cours d'exécution.")
        sys.exit(1)