import streamlit as st
import pandas as pd

def main():
    st.title('Excel File Upload and Read')

    # Upload Excel file
    uploaded_file = st.file_uploader("Upload Excel file", type=["xls", "xlsx"])

    if uploaded_file is not None:
        # Read Excel file
        df = pd.read_excel(uploaded_file)

        # Display DataFrame
        st.write(df)

if __name__ == '__main__':
    main()
