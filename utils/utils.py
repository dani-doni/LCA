import pandas as pd
import streamlit as st
from googletrans import Translator
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

@st.cache_data
def download_example_file():
    example_path = "./utils/example.xlsx"
    with open(example_path, "rb") as file:
        content = file.read()
    return content

@st.cache_data
def material_list_from_uploaded_file(uploaded_file):
    df = pd.read_excel(uploaded_file)
    material_list = df.iloc[:, 0].tolist()
    return material_list

@st.cache_resource
def trans():
    trans = Translator()
    return trans

@st.cache_data
def translate_ITA_to_ENG(input):
    translator = trans()
    output = translator.translate(input, src='it', dest='en').text
    return output

@st.cache_data
def translate_ENG_to_ITA(input):
    translator = trans()
    output = translator.translate(input, src='en', dest='it').text
    return output

@st.cache_data
def CO2_dataset_upload():
    # Load the dataset from the CSV file
    dataset_path = "./utils/ITA_db_materials.csv"  # Replace with the actual path to your CSV file
    df = pd.read_csv(dataset_path, encoding='latin-1')
    df["combined_text"] = df["Name_ITA"] + " " + df["Description_ITA"]
    return df

@st.cache_resource
def vect():
    vect = TfidfVectorizer()
    return vect

@st.cache_data
def search_similarity(df, input):
    vectorizer = vect()
    tfidf_matrix = vectorizer.fit_transform(df["combined_text"])
    # Calculate cosine similarity between input and other materials
    query_vector = vectorizer.transform([input])
    cosine_similarities = np.dot(query_vector, tfidf_matrix.T).toarray().squeeze()

    # Sort materials by similarity in descending order
    # Add cosine similarities as a new column to the DataFrame
    
    df['similarity'] = cosine_similarities.tolist()
    df = df.sort_values(by="similarity", ascending=False)

    # Select top N most similar materials
    top_similar = df.head(5)

    return top_similar

