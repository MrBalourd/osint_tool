# Projet OSINT - Génération de profils à partir de données publiques

## Table des matières
1. [Introduction](#introduction)
2. [Fonctionnalités](#fonctionnalites)
3. [Installation](#installation)
4. [Utilisation](#utilisation)
5. [Exemples](#exemples)
6. [Contribuer](#contribuer)
7. [Licence](#licence)
8. [Remerciements](#remerciements)

---

## Introduction

Ce projet vise à créer un outil OSINT (Open Source Intelligence) capable de collecter, analyser et relier des informations publiques afin de générer un profil détaillé d'une personne. L'outil utilise plusieurs technologies, notamment la reconnaissance faciale, l'analyse linguistique et la gestion de graphes de connaissances, pour extraire des relations significatives entre des photos, des noms, des e-mails et des mots de passe compromis.

**Note importante** : Ce projet respecte strictement les lois locales et ne traite que des données disponibles publiquement. Il est destiné à des fins éducatives et professionnelles légales uniquement.

---

## Fonctionnalités

- **Reconnaissance faciale** : Comparez des visages pour identifier si plusieurs photos appartiennent à la même personne.
- **Extraction d'e-mails** : Recherchez des e-mails compromis dans des breaches publiques (ex. Have I Been Pwned).
- **Vérification de mots de passe** : Vérifiez si un mot de passe a été exposé dans une fuite de données.
- **Scraping web** : Collectez des informations à partir de réseaux sociaux publics ou de sites web.
- **Gestion des graphes de connaissances** : Représentez les relations entre les entités (personnes, photos, e-mails, etc.) sous forme de graphe.

---

## Installation

### Prérequis
- Python 3.8+ installé sur votre système.
- Une clé API pour Have I Been Pwned (HIBP) si vous utilisez cette fonctionnalité.

### Étapes d'installation

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/mrbalourd/osint_tool.git
   cd osint_tool
   ```

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

3. Configurez vos clés API :
   - Créez un fichier `.env` dans le répertoire racine avec le contenu suivant :
     ```
     HIBP_API_KEY=your_api_key_here
     NEO4J_URI=bolt://localhost:7687
     NEO4J_USER=neo4j
     NEO4J_PASSWORD=your_password
     ```

---

## Utilisation

### Reconnaissance faciale

Comparez deux images pour vérifier si elles contiennent le même visage :
```python
python scripts/compare_faces.py --image1 path/to/image1.jpg --image2 path/to/image2.jpg
```

### Vérification d'e-mails compromises

Vérifiez si un e-mail a été compromis dans une fuite de données :
```python
python scripts/check_email_breaches.py --email example@example.com
```

### Scraping web

Extrayez des informations à partir d'un profil LinkedIn public :
```python
python scripts/scrape_profile.py --url https://www.linkedin.com/in/example-profile
```

### Gestion des graphes de connaissances

Ajoutez une personne au graphe de connaissances :
```python
python scripts/manage_knowledge_graph.py --action add --name "John Doe" --email "john.doe@example.com"
```

---

## Exemples

### Comparaison de visages
Supposons que vous avez deux images `photo1.jpg` et `photo2.jpg`. Voici comment les comparer :
```bash
python scripts/compare_faces.py --image1 photo1.jpg --image2 photo2.jpg
```
Résultat attendu :
```
Les visages sont identiques : True
```

### Vérification d'e-mails compromises
Vérifiez si un e-mail a été compromis :
```bash
python scripts/check_email_breaches.py --email john.doe@example.com
```
Résultat attendu :
```
Breaches found: ['Adobe', 'LinkedIn', 'MySpace']
```

---

## Contribuer

Si vous souhaitez contribuer à ce projet, suivez ces étapes :

1. Fork ce dépôt.
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`).
3. Committez vos changements (`git commit -m "Ajout de nouvelle fonctionnalité"`).
4. Pousser vos changements (`git push origin feature/nouvelle-fonctionnalite`).
5. Soumettez une pull request.

---

## Licence

Ce projet est sous licence **MIT**. Consultez le fichier [LICENSE](LICENSE) pour plus de détails.

---

## Remerciements

- Merci à [Have I Been Pwned](https://haveibeenpwned.com/) pour leur API permettant de vérifier les breaches.
- Merci aux contributeurs de bibliothèques open-source comme OpenCV, Dlib, Beautiful Soup, Neo4j, etc., qui ont rendu ce projet possible.

---

### Auteur

- **MR.Balourd**
