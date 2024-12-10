import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import json
from openai import OpenAI
import os
from qdrant_client import QdrantClient,models




def openai_embeddings(text):
    model="text-embedding-3-small"
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    embeddings = client.embeddings.create(input = [text], model=model).data[0].embedding
    return embeddings

# Mock function to simulate API call to Qdrant (Replace this with your actual API endpoint and logic)
def get_matching_jobs(embed_value):
    qdrant_client = QdrantClient(url=st.secrets["QDRANT_URL"], api_key=st.secrets["QDRANT_API_KEY"])
    response = qdrant_client.query_points(
        collection_name="skill-summary-mirambika",
        query=embed_value,
        limit=10
    )
    return response


def main():
   
    st.set_page_config(page_title="Job Finder", layout="wide")
    st.markdown("<h2 style='margin-top:0px;'>Discover Matching Jobs to your Skills</h2>", unsafe_allow_html=True)
    st.markdown("---")
    # Create two columns: Left for input, Right for results
    col_input, col_results = st.columns([2,3], gap="small")

    with col_input:
        st.subheader("Enter the Job Description")
        job_description = st.text_area("Paste or type the job description here", height=200)
        search_button = st.button("Search")
        

    # Placeholder for the results
    with col_results:
        st.subheader("Top 10 Matching Jobs")
        if search_button and job_description.strip():
            # Call the API to get matching jobs
            embed_value = openai_embeddings(job_description)

            matches = get_matching_jobs(embed_value)

            # Show top 10 results (assuming matches are returned sorted by similarity)
            for job in matches.points[:10]:
                
                with st.expander(f"**:blue[{job.payload['sector']}]**     {job.payload['job_name']}", expanded=False):
                    st.write(f"**Similarity Score:** {job.score}")
                    st.write(job.payload['summary'])
        else:
            st.write("No results to display. Please enter a job description and click Search.")

if __name__ == "__main__":
    main()
