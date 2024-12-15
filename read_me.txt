J'ai créé trois fichiers distincts pour une meilleure organisation du code :

log_parser.py : Contient la logique de parsing du fichier de log

- Parse les timestamps
- Extrait les noms d'hôtes
- Identifie les tâches et leur statut
- Calcule les durées d'exécution


report_generator.py : Gère l'affichage des résultats

- Formate les durées de manière lisible
- Génère un rapport détaillé par hôte
- Affiche les statistiques (tâches exécutées/ignorées)


main.py : Point d'entrée du programme

- Coordonne les différents modules
- Gère l'interaction avec l'utilisateur


Pour utiliser le script :

Rendez les fichiers exécutables :

chmod +x main.py log_parser.py report_generator.py
Exécutez le script principal :

./main.py
Le script va :

- Analyser le format spécifique de vos logs Ansible
- Calculer les temps d'exécution pour chaque tâche
- Afficher un rapport détaillé par hôte
- Identifier les tâches ignorées (skipped)
- Fournir des statistiques globales

Le rapport inclura :

- Le temps d'exécution de chaque tâche
- L'heure de début et de fin
- Le statut (exécuté ou ignoré)
- Un résumé par hôte avec le temps total
