import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import json

# Mock function to simulate API call to Qdrant (Replace this with your actual API endpoint and logic)
def get_matching_jobs(job_description):
    # In real scenario, you'd send job_description to an API endpoint and get results
    # Here we return a mock response
    # read from response.jon and put it in response_json
    
    with open('response.json', 'r') as file:
        response_json = json.load(file)
    
    return response_json


def main():
    # Set Page config
    st.set_page_config(page_title="Job Finder", layout="wide")

    # Load a logo image (Optional: Replace with your image path or URL)
    # For demonstration, we will create a placeholder image in memory.
    # Replace this section with something like:
    # image = Image.open("path_to_your_logo_image.png")
    #img = Image.new('RGB', (200, 50), color = 'black')
    #logo = img

    # Header Section with Image and Title
    #col_logo, col_title = st.columns([1,4])
    #with col_logo:
     #   st.image(logo, use_column_width=True)
    #with col_title:
    st.markdown("<h1 style='margin-top:0px;'>Discover Matching Jobs to your Skills</h1>", unsafe_allow_html=True)

    st.markdown("---")

    # Create two columns: Left for input, Right for results
    col_input, col_results = st.columns([1,2], gap="large")

    with col_input:
        st.subheader("Enter the Job Description")
        job_description = st.text_area("Paste or type the job description here", height=200)
        search_button = st.button("Search")

    # Placeholder for the results
    with col_results:
        st.subheader("Matching Jobs")
        if search_button and job_description.strip():
            # Call the API to get matching jobs
            matches = get_matching_jobs(job_description)

            # Show top 10 results (assuming matches are returned sorted by similarity)
            for job in matches[:10]:
                
                with st.expander(f"**:blue[{job['sector']}]**     {job['job_name']}", expanded=False):
                    st.write(f"**Similarity Score:** {job['similarity_score']:.2f}")
                    st.write(job["description"])
        else:
            st.write("No results to display. Please enter a job description and click Search.")

if __name__ == "__main__":
    main()
