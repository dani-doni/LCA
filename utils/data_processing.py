import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from googletrans import Translator
import numpy as np

def find_top_matches(input_description_italian):
    # Load the dataset from the CSV file
    dataset_path = "./db_materials.csv"  # Replace with the actual path to your CSV file
    df = pd.read_csv(dataset_path, encoding='latin-1')

    # Extract relevant columns
    materials = df["Reference Product Name"].tolist()
    descriptions = df["Product Information"].tolist()
    values = df["Product UUID"].tolist()  

    # Translate input description to English
    translator = Translator()
    input_description_english = translator.translate(input_description_italian, src='it', dest='en').text

    # Combine material names and descriptions
    all_materials = [f"{name} {desc}" for name, desc in zip(materials, descriptions)]
    input_data = f"{input_description_english}"
    all_materials.append(input_data)

    # Vectorize the data
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_materials)

    # Calculate cosine similarity
    similarities = cosine_similarity(tfidf_matrix[:-1], tfidf_matrix[-1])

    # Get the indices of the top 5 matches
    top_indices = np.argsort(similarities.flatten())[:-6:-1]

    # Output the top 5 matches
    top_matches = []
    for idx in top_indices:
        match_name = materials[idx]
        match_value = values[idx]
        match_similarity = similarities[idx]
        top_matches.append((match_name, match_value, match_similarity))

    return top_matches

