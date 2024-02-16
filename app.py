import streamlit as st
import pandas as pd
from utils.data_processing import find_top_matches

# Define session state to manage page state
class _SessionState:
    def __init__(self):
        self.page = "step1"

# Create a session state instance
session_state = _SessionState()

def main():
    if session_state.page == "step1":
        st.write({session_state.page})
    elif session_state.page == "step2":
        st.write({session_state.page})

def step1():
    st.subheader('Fase 1: Carica il file excel con la lista dei materiali')
    st.caption('Il file deve avere nella prima colonna la lista dei materiali con la descrizione completa da computo metrico. Nella prima cella scrivete "Descrizione materiali". Scarica un esempio di file usando il bottone sottostante ') 
    # Add button to download template file
    #example_path = "./utils/example.xls" 
    #st.markdown(f"[Scarica esempio file]({example_path})", unsafe_allow_html=True)

    # Upload Excel file
    uploaded_file = st.file_uploader("Carica file excel", type=["xls", "xlsx"])

    # Display DataFrame if file uploaded
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        st.write(df)
        st.caption('Ora che hai caricato il file controlla che tutto sia corretto e poi clicca su "Vai alla fase successiva" in fondo alla pagina ') 

        # Add button to proceed to Step 2
        if st.button("Vai alla fase successiva"):
            session_state.page = "step2"

def step2():
    st.title('Fase 2: seleziona la migliore corrispondenza')

    # Retrieve uploaded Excel file from Step 1
    uploaded_file = st.session_state.uploaded_file

    # Process the uploaded file if it exists
    if uploaded_file is not None:
        # Load the uploaded Excel file into a DataFrame
        df = pd.read_excel(uploaded_file)

        # Iterate over each row in the DataFrame
        for index, row in df.iterrows():
            # Get the Italian description from the DataFrame
            italian_description = row['Descrizione materiali']  # Adjust column name accordingly

            # Find top matches for the Italian description
            top_matches = find_top_matches(italian_description)

            # Display top matches for the current row
            st.write(f"Top matches for row {index + 1}:")
            for i, (match_name, match_value, match_similarity) in enumerate(top_matches, 1):
                st.write(f"Match {i}: {match_name} (Value: {match_value}, Similarity: {match_similarity})")
    else:
        st.warning("Please upload an Excel file in Step 1.")

if __name__ == '__main__':
    main()
