import streamlit as st
import pandas as pd
from utils.utils import *

# Set page configuration
st.set_page_config(
    page_title="LCA",
    page_icon=":deciduous_tree:",
    layout="wide",  # Set layout to wide
)

if 'step' not in st.session_state:
    st.session_state.step = 1

def next_step():
    st.session_state.step += 1

def main():
    if st.session_state.step == 1:
        step1()
    elif st.session_state.step == 2:
        step2()
    elif st.session_state.step == 3:
        step3()

def step1():
    st.subheader('Fase 1: Carica il file excel con la lista dei materiali')
    st.write('Il file deve avere nella prima colonna la lista dei materiali con la descrizione completa da computo metrico. La colonna deve avere come intestazione: "Descrizione materiali"') 
    
    # ADD BUTTON TO DOWNLOAD EXAMPLE FILE
    file_content = download_example_file()
    st.download_button(
        label="Scarica file di esempio",
        data=file_content,
        file_name='example.xls', 
        mime='application/vnd.ms-excel'
    )

    # ADD BUTTON TO UPLOAD EXCEL FILE
    uploaded_file = st.file_uploader("Carica file excel", type=["xls", "xlsx"])
    if uploaded_file is not None:
        #st.session_state['input_materials'] = material_list_from_uploaded_file(uploaded_file)
        st.session_state['materials_table'] = pd.DataFrame(columns=['Input Material', 'Name', 'Name_ITA','Unit','Description', 'Description_ITA', 'Cut-Off Classification', 'CO2', 'selectbox_text'])
        st.session_state['materials_table']['Input Material'] = material_list_from_uploaded_file(uploaded_file)
        with st.expander("Apri e controlla lista materiali:"):
            for material in st.session_state['materials_table']['Input Material']:
                st.write({material})
        st.write('Ora che hai caricato il file e controllato che tutto sia corretto, clicca su "Vai alla fase succesiva"') 
        
        # Add button to proceed to Step 2
        st.button('Vai alla fase successiva', on_click=next_step)
            

def step2():
    all_materials = CO2_dataset_upload()

    # SELECT ALL THE CORRESPONDET MATERIALS FOR THE INPUTS
    st.subheader('Fase 2: seleziona la migliore corrispondenza')
    for index, material in enumerate(st.session_state['materials_table']['Input Material']):

        st.write(material)
        input_text = translate_ITA_to_ENG(material)
        similars = search_similarity(all_materials, input_text)

        st.selectbox('Seleziona il materiale corrispondente', similars['selectbox_text'], index = None, key=index)
        if st.session_state[index] is not None:
            materials_table_df = st.session_state['materials_table']
            filtered_similars = similars[similars['selectbox_text'] == st.session_state[index]]
            for column in materials_table_df.columns:
                if column in filtered_similars.columns and column in materials_table_df.columns:
                    materials_table_df.at[index, column] = filtered_similars.at[filtered_similars.index[0], column]
            st.success(f'Materiale associato: {st.session_state[index]}', icon="✅")
        st.divider()
    
    # Check if all session_state elements from 0 to index are not None
    if all(st.session_state.get(str(i)) is not None for i in range(index + 1)):
        st.session_state['materials_table'] = materials_table_df
        st.success('Tutti i materiali sono stati associati, vai alla fase successiva.', icon="✅")

        # Add button to proceed to Step 2
        st.button('Vai alla fase successiva', on_click=next_step)


def step3():
    st.subheader('Fase 3: scarica il report degli impatti ambientali')
    with st.expander("Apri e controlla la lista dei materiali associati:"):
        # Display the lists side by side
        col1, col2, col3, col4 = st.columns([0.4,0.4,0.1,0.1])
        with col1: st.caption("Materiale")
        with col2: st.caption("Materiale corrispondente")
        with col3: st.caption("udm")
        with col4: st.caption("CO2/udm")

        for i in range(len(st.session_state['materials_table'])):
            col1, col2, col3, col4 = st.columns([0.4,0.4,0.1,0.1])

            with col1:
                st.write(st.session_state['materials_table'].loc[i, "Input Material"])

            with col2:
                st.write(st.session_state['materials_table'].loc[i, "selectbox_text"])
            
            with col3:
                st.write(st.session_state['materials_table'].loc[i, "Unit"])
        
            with col4:
                st.write(st.session_state['materials_table'].loc[i, "CO2"])

            st.divider()
        
    materials_table = st.session_state['materials_table']
    excel_writer = pd.ExcelWriter('materials_table.xlsx', engine='xlsxwriter')
    materials_table.to_excel(excel_writer, index=False)
    materials_table.to_excel(excel_writer, index=False, sheet_name='Sheet1')
    excel_writer.close()

    # Create a download button for the output.xlsx file
    with open('materials_table.xlsx', 'rb') as f:
        file_data = f.read()
    st.download_button(
        label='Download Excel file',
        data=file_data,
        file_name='output.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


if __name__ == '__main__':
    main()
