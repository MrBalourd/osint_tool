import face_recognition
import os
import numpy as np
from sklearn.cluster import DBSCAN
from deepface import DeepFace
import shutil
import argparse
import json

def cluster_faces(image_folder):
    """
    Regroupe des visages similaires dans un ensemble d'images.
    """
    encodings = []
    image_paths = []

    # Extraire les encodages faciaux
    for filename in os.listdir(image_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(image_folder, filename)
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)

            print(f"Image : {filename}")
            print(f"Nombre de visages détectés : {len(face_encodings)}")

            for encoding in face_encodings:
                encodings.append(encoding)
                image_paths.append(image_path)

    if not encodings:
        print("Aucun visage détecté dans les images fournies.")
        return {}, []

    # Appliquer DBSCAN pour regrouper les visages
    encodings = np.array(encodings)
    clustering = DBSCAN(metric="euclidean", eps=0.5, min_samples=1)
    labels = clustering.fit_predict(encodings)

    # Organiser les clusters
    clusters = {}
    for i, label in enumerate(labels):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(image_paths[i])

    return clusters, labels

def analyze_face_attributes(image_path):
    """
    Analyse les attributs d'un visage dans une image.
    """
    try:
        # Analyser le visage
        analysis = DeepFace.analyze(img_path=image_path, actions=['age', 'gender', 'emotion'])

        # Vérifier si les résultats sont dans une liste ou un dictionnaire
        if isinstance(analysis, list):  # Si c'est une liste, prendre le premier résultat
            analysis = analysis[0]

        # Extraire le genre dominant
        gender_probs = analysis.get("gender", {})
        dominant_gender = max(gender_probs, key=gender_probs.get) if gender_probs else "Non détecté"
        if dominant_gender == "Man":
            dominant_gender = "Homme"
        elif dominant_gender == "Woman":
            dominant_gender = "Femme"

        return {
            "age": analysis.get("age", "Non détecté"),
            "gender": dominant_gender,
        }
    except Exception as e:
        print(f"Erreur lors de l'analyse du visage : {e}")
        return None

def organize_photos_by_person(clusters, output_folder):
    """
    Organise les photos dans des dossiers distincts pour chaque personne.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    person_id = 0
    results = {}

    for cluster_id, images in clusters.items():
        if cluster_id == -1:  # Ignorer les outliers
            continue

        person_folder = os.path.join(output_folder, f"person_{person_id}")
        os.makedirs(person_folder, exist_ok=True)

        # Copier les images dans le dossier correspondant
        for image_path in images:
            shutil.copy(image_path, person_folder)

        # Analyser les attributs du premier visage du cluster
        attributes = analyze_face_attributes(images[0])
        results[f"person_{person_id}"] = {
            "folder": person_folder,
            "attributes": attributes
        }

        person_id += 1

    return results

def display_clusters(clusters):
    """
    Affiche les clusters sous forme de liste de visages et photos associées.
    """
    print("\nRésultats des clusters :")
    face_id = 1
    for cluster_id, images in clusters.items():
        if cluster_id == -1:  # Ignorer les outliers
            continue

        print(f"\nVisage {face_id} :")
        for image in images:
            print(f"- {os.path.basename(image)}")
        face_id += 1

def export_results_to_json(results, output_file):
    """
    Exporte les résultats dans un fichier JSON.
    """
    json_data = {}
    for person, data in results.items():
        json_data[person] = {
            "Dossier": data["folder"],
            "Attributs": {
                "Âge estimé": data["attributes"]["age"],
                "Genre": data["attributes"]["gender"],
                "Émotion dominante": data["attributes"]["dominant_emotion"]
            }
        }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)
    print(f"Résultats exportés dans {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyse un dossier de photos et regroupe les visages similaires.")
    parser.add_argument("--input", required=True, help="Dossier contenant les images à analyser.")
    parser.add_argument("--output", required=True, help="Dossier de sortie pour organiser les photos.")
    args = parser.parse_args()

    # Étape 1 : Regrouper les visages
    print("Regroupement des visages...")
    clusters, _ = cluster_faces(args.input)

    # Étape 2 : Organiser les photos et analyser les attributs
    print("Organisation des photos et analyse des attributs...")
    results = organize_photos_by_person(clusters, args.output)

    # Étape 3 : Afficher les résultats
    display_clusters(clusters)

    # Étape 4 : Exporter les résultats en JSON
    json_output_file = os.path.join(args.output, "results.json")
    export_results_to_json(results, json_output_file)