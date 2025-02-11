import discord
import random
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
import os

# Listes des Atouts et Défauts
atouts = [
    "L’un de vos sens est exceptionnellement développé. (Vue, ouïe, odorat… à vous de choisir.)",
    "Votre corps est d’une résistance impressionnante. (Vous encaissez mieux les coups et la fatigue.)",
    "Vous êtes particulièrement souple. (Passer dans des espaces exigus ou esquiver est plus aisé.)",
    "Vos réflexes sont d’une précision remarquable. (Votre corps réagit plus vite que votre pensée.)",
    "Votre musculature est bien au-dessus de la moyenne. (Force physique accrue.)",
    "Vous êtes incroyablement endurant. (Fatigue physique retardée, courses prolongées possibles.)",
    "Votre corps se remet vite des blessures. (Cicatrisation accélérée, douleurs moins handicapantes.)",
    "Vous avez une coordination parfaite. (Aucune maladresse, mouvements fluides et précis.)",
    "Votre respiration est maîtrisée. (Plongée en apnée, endurance en conditions difficiles.)",
    "Votre voix est captivante et autoritaire. (Difficile à ignorer, parfait pour imposer sa présence.)",
    "Vos gestes sont d’une précision chirurgicale. (Idéal pour les manipulations délicates.)",
    "Votre démarche est naturelle et discrète. (Déplacements silencieux instinctifs.)",
    "Votre sens de l’équilibre est parfait. (Difficile à déséquilibrer ou à faire chuter.)",
    "Votre résistance aux toxines est accrue. (Alcool, drogues ou poisons ont un effet réduit.)",
    "Vous êtes capable de supporter des températures extrêmes. (Froid et chaleur vous affectent moins.)",
    "Votre corps est taillé pour l’escalade et l’agilité. (Saisir, grimper, bondir semble naturel.)",
    "Vous possédez une force impressionnante dans une partie du corps. (Main, jambes, dos… à vous de choisir.)",
    "Votre peau est particulièrement résistante. (Coupures superficielles et ecchymoses ont peu d’effet.)",
    "Vous avez une capacité pulmonaire hors norme. (Sprint, endurance ou résistance aux gaz.)",
    "Votre perception du mouvement est aiguisée. (Difficile de vous surprendre en combat ou en infiltration.)",
    "Vous êtes naturellement rapide. (Vos déplacements sont fulgurants.)",
    "Votre souplesse vous permet d’exécuter des postures improbables. (Contorsionniste, esquives fluides.)",
    "Votre peau ne marque presque jamais. (Bleus, coups, cicatrices disparaissent vite.)",
    "Vous récupérez étonnamment bien du manque de sommeil. (Moins de besoin de repos immédiat.)",
    "Votre endurance nerveuse est inébranlable. (Résistance accrue au stress et aux douleurs prolongées.)",
    "Votre corps s’adapte rapidement aux changements. (Altitude, plongée, pression, mouvement rapide.)",
    "Votre instinct de survie est aiguisé. (Votre corps réagit instinctivement face au danger.)",
    "Vous possédez une dextérité naturelle. (Manipulations fines et précises, gestes rapides.)",
    "Votre posture et votre prestance imposent le respect. (Aucune hésitation dans votre démarche.)",
    "Votre corps semble fonctionner avec une efficience parfaite. (Coordination, réactivité et énergie optimale.)",
    "Vous possédez une arme de qualité. (Une arme tranchante, une arme à feu, ou autre… à définir.)",
    "Vous avez un équipement de protection efficace. (Armure, gilet pare-balles, combinaison renforcée…)",
    "Vous êtes en possession d’un outil multifonction. (Couteau suisse, pied-de-biche, laser de découpe…)",
    "Vous avez des documents d’identité solides. (Parfait pour passer les contrôles sans encombre.)",
    "Vous avez un accès à un moyen de transport fiable. (Cheval, voiture, moto, vaisseau…)",
    "Vous transportez une somme d’argent confortable. (Assez pour acheter ce dont vous avez besoin sur place.)",
    "Vous possédez une clé/un badge/un code d’accès précieux. (Vers un lieu sécurisé.)",
    "Vous portez des vêtements de grande qualité. (Élégants, résistants, ou parfaitement adaptés à l’environnement.)",
    "Vous disposez d’un appareil technologique avancé. (Communicateur, drone, analyseur de données…)",
    "Vous avez des vivres et provisions en quantité. (Nourriture, eau, rations de survie.)",
    "Vous possédez un carnet de notes rempli d’informations utiles. (Indices, noms, plans d’accès…)",
    "Vous avez un animal dressé. (Chien de garde, faucon messager, monture bien entraînée…)",
    "Vous transportez un kit médical de bonne qualité. (De quoi soigner des blessures légères à moyennes.)",
    "Vous possédez un plan détaillé du lieu où vous vous trouvez. (Avec des annotations précises.)",
    "Vous avez un dispositif de communication efficace. (Radio, talkie-walkie, réseau clandestin.)",
    "Vous possédez un moyen d’éclairage performant. (Lampe torche, briquet, pierre à feu, lumigel.)",
    "Vous avez des explosifs improvisés. (Grenades artisanales, charges de démolition, poudre noire.)",
    "Vous transportez un document compromettant. (Preuve d’un complot, information ultra-sensible.)",
    "Vous avez une potion, drogue ou stimulant rare. (Effet temporaire : force, endurance, résistance…)",
    "Vous êtes en possession d’un livre ancien précieux. (Informations cachées, artefact mystique ou technologique.)",
    "Vous avez une arme dissimulée indétectable. (Lame de botte, pistolet miniature, aiguilles empoisonnées.)",
    "Vous possédez un appareil d’enregistrement sophistiqué. (Pour collecter des preuves audio/vidéo.)",
    "Vous avez un uniforme/localement reconnu. (Permet de se faire passer pour quelqu’un d’autre.)",
    "Vous transportez un message important. (Lettre scellée, mission secrète, coordonnées d’un lieu.)",
    "Vous possédez une monnaie d’échange rare. (Or, pierres précieuses, artefact convoité.)",
    "Vous avez une trousse à outils complète. (De quoi forcer des serrures, bricoler, réparer.)",
    "Vous êtes équipé d’un détecteur spécial. (Détecte chaleur, métaux, radiations, énergie magique.)",
    "Vous avez en votre possession un antidote. (Peut neutraliser un poison spécifique.)",
    "Vous transportez une carte de contacts influents. (Réseau souterrain, accès à des informations privilégiées.)",
    "Vous avez un mot de passe/un code secret. (Permet d’ouvrir des portes… au sens propre ou figuré.)",
]

defauts = [
    "L’un de vos sens est particulièrement faible. (Vision trouble, mauvaise ouïe, odorat quasi inexistant…)",
    "Votre corps est fragile et supporte mal les blessures. (Moins de résistance aux coups et chocs.)",
    "Vous êtes étonnamment maladroit. (Vos gestes manquent de précision, risque accru de rater des actions fines.)",
    "Vous souffrez d’un handicap physique léger. (Boiterie, bras moins fonctionnel, manque de mobilité…)",
    "Votre force est anormalement basse. (Difficulté à soulever, porter, ou utiliser des objets lourds.)",
    "Votre endurance est limitée. (Vous vous fatiguez plus vite que la normale.)",
    "Votre corps guérit très lentement. (Les blessures, même mineures, mettent du temps à disparaître.)",
    "Vous manquez de coordination. (Vos mouvements sont parfois imprécis ou hésitants.)",
    "Votre respiration est faible. (Difficulté en altitude, en apnée, ou lors d’efforts prolongés.)",
    "Votre voix est faible ou monotone. (Difficile à entendre ou à rendre captivante.)",
    "Votre équilibre est instable. (Facile à déséquilibrer ou à faire chuter.)",
    "Votre peau est particulièrement sensible. (Marque facilement, réactions aux agressions extérieures.)",
    "Vous êtes sujet aux tremblements. (Mains, jambes, voire tout le corps, en fonction du stress ou de l’effort.)",
    "Votre résistance à la douleur est faible. (Vous ressentez les blessures plus intensément.)",
    "Vous ne supportez pas bien les températures extrêmes. (Chaleur et froid vous affectent rapidement.)",
    "Votre vitesse de déplacement est réduite. (Vous êtes plus lent que la moyenne.)",
    "Vos réflexes sont anormalement lents. (Difficile de réagir rapidement à une menace.)",
    "Votre posture est inhabituelle. (Marche peu naturelle, attitude étrange qui attire l’attention.)",
    "Votre métabolisme est imprévisible. (Vous avez souvent faim, soif, ou des réactions physiologiques anormales.)",
    "Vous êtes sujet à des douleurs chroniques. (Migraine, douleurs articulaires, crampes inexpliquées…)",
    "Votre système immunitaire est faible. (Vulnérable aux maladies, infections ou poisons.)",
    "Vous êtes incapable de courir longtemps. (Même une courte course vous épuise rapidement.)",
    "Vos mains sont rigides ou peu précises. (Difficulté à manier des outils ou armes fines.)",
    "Votre champ de vision est réduit. (Problèmes de perception périphérique ou vision tunnel.)",
    "Vous êtes facilement sujet aux vertiges. (Déséquilibre fréquent, peur du vide, troubles de l’orientation.)",
    "Votre force dans un membre est réduite. (Un bras ou une jambe est plus faible que l’autre.)",
    "Votre respiration est irrégulière. (Tendance à s’essouffler sans raison apparente.)",
    "Vous êtes sujet à des crampes musculaires. (Effort prolongé = crampe imprévisible.)",
    "Vous avez une condition médicale non soignée. (Asthme léger, arythmie, douleurs articulaires chroniques…)",
    "Votre corps est étrangement froid ou chaud au toucher. (Sans raison apparente, ce qui peut attirer l’attention.)",
    "Vous êtes totalement désarmé. (Aucune arme, même improvisée.)",
    "Votre équipement est en très mauvais état. (Rouillé, abîmé, dysfonctionnel.)",
    "Vos vêtements sont inadaptés à votre environnement. (Trop légers, trop chauds, mal ajustés.)",
    "Vous n’avez aucun moyen de communication. (Impossible de contacter qui que ce soit.)",
    "Vous n’avez pas un sou en poche. (Aucun argent, ni objet de valeur échangeable.)",
    "Votre seule arme est peu efficace. (Lame émoussée, munitions limitées, arme improvisée.)",
    "Vous avez un équipement incomplet. (Il manque un élément crucial.)",
    "Vos documents d’identité sont incohérents. (Nom erroné, statut suspect, origine douteuse.)",
    "Votre sac est rempli d’objets inutiles. (Des choses sans valeur ou hors de propos.)",
    "Votre équipement est trop encombrant. (Difficile à transporter discrètement ou rapidement.)",
    "Vous avez un objet compromettant sur vous. (Preuve d’un crime, faux papiers, substance interdite.)",
    "Vous êtes en possession d’un objet dangereux… sans en connaître l’usage. (Technologie inconnue, substance douteuse.)",
    "Votre seule source de lumière est défaillante. (Lampe qui clignote, torche qui s’éteint au moindre mouvement.)",
    "Votre nourriture et votre eau sont contaminées ou insuffisantes. (Vous risquez de tomber malade.)",
    "Votre moyen de transport est en panne ou inutilisable. (Bloqué, saboté, sans carburant.)",
    "Votre matériel électronique est hors service. (Batterie morte, circuits grillés.)",
    "Votre trousse médicale est presque vide. (Pas de bandages, antiseptique épuisé, médications manquantes.)",
    "Vous avez une clé/un code d’accès, mais il ne fonctionne plus. (Obsolète, erreur de cryptage, mauvaise porte.)",
    "Vous possédez une arme, mais aucune munition. (Ou des munitions incompatibles.)",
    "Votre équipement de protection est inefficace. (Armure trouée, casque fissuré, bouclier fendu.)",
    "Vous avez un appareil high-tech… mais vous ne savez pas l’utiliser. (Technologie étrangère ou trop avancée.)",
    "Votre tenue vous rend très visible. (Trop colorée, trop reconnaissable.)",
    "Vos chaussures sont inadaptées. (Trop grandes, trop petites, usées, glissantes.)",
    "Votre sac ou conteneur principal est déchiré. (Risque de perdre du matériel.)",
    "Votre carte ou plan est erroné. (Mauvaises indications, zones non mises à jour.)",
    "Vous avez un objet de valeur… mais il est faussement authentifié. (Risque de trahison si découvert.)",
    "Votre matériel de camouflage ne fonctionne pas. (Tissu déchiré, peinture qui s’efface, bruit trop élevé.)",
    "Vos menottes, cordes ou attaches ne tiennent pas. (Difficile de sécuriser un captif.)",
    "Votre équipement de survie est incomplet. (Pas de feu, pas d’eau potable, pas de trousse d’urgence.)",
    "Vous avez un objet inconnu sur vous. (Vous ignorez son usage et s’il est dangereux.)",
]

# Historique des tirages
recent_tirages = []

def tirage_unique(liste, historique):
    candidats = [item for item in liste if item not in historique]
    if not candidats:
        historique.clear()  # Réinitialiser si tous ont été tirés récemment
        candidats = liste
    choix = random.choice(candidats)
    historique.append(choix)
    return choix

# Création du bot
load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user}')

@bot.command()
async def atoutdefaut(ctx):
    atout = tirage_unique(atouts, recent_tirages)
    defaut = tirage_unique(defauts, recent_tirages)
    await ctx.send(f"🎲 **Résultat du tirage :**\n🎭 **Atout :** {atout}\n⚠️ **Défaut :** {defaut}")
    await asyncio.sleep(3600)  # Attendre 1 heure avant de libérer l'entrée
    recent_tirages.remove(atout)
    recent_tirages.remove(defaut)

# Lancement du bot avec le token depuis .env
bot.run(os.getenv('DISCORD_TOKEN'))