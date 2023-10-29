import base64

import streamlit as st

from src.tabe_map import TabeMap


def main():
    st.title("Map Annot!")
    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file:
        st.write("You have uploaded a file!")

        tabe_map = TabeMap()
        try:
            tabe_map.run(uploaded_file)

            # 1. Prepare the file content for download
            with open('./static/map.html', 'rb') as file:
                file_content = file.read()
            b64 = base64.b64encode(file_content).decode()

            # 2. Create a download link for the file
            href = f'<a href="data:text/html;base64,{b64}" download="map.html">Download map.html</a>'

            st.markdown('### Download File')
            st.markdown(href, unsafe_allow_html=True)

        except Exception as e:
            st.write(e)


main()
