import streamlit as st
from ml_pipeline import extract_text_from_pdf, process_text, add_to_faiss, doc_id_map
from search import perform_search
from analytics import visualize_analytics

# Initialize session state
if "metadata" not in st.session_state:
    st.session_state.metadata = {}  # Stores document metadata (text, entities, keywords)
if "search_history" not in st.session_state:
    st.session_state.search_history = []  # Tracks user search queries and results

st.title("Enterprise Knowledge Hub")
st.write("Upload multiple documents, explore semantic search, and gain insights.")

# File upload (multiple documents)
uploaded_files = st.file_uploader("Upload PDF documents", type=["pdf"], accept_multiple_files=True)
if uploaded_files:
    with st.spinner("Processing documents..."):
        for uploaded_file in uploaded_files:
            text = extract_text_from_pdf(uploaded_file)
            doc_id = uploaded_file.name

            # Process text for metadata
            entities, keywords = process_text(text)

            # Add to FAISS index and metadata storage
            add_to_faiss(text, doc_id)
            st.session_state.metadata[doc_id] = {"text": text, "entities": entities, "keywords": keywords}

        st.success(f"Uploaded and processed {len(uploaded_files)} document(s).")

# Display uploaded documents with thumbnails
if st.session_state.metadata:
    st.write("### Uploaded Documents")
    for doc_id, doc_info in st.session_state.metadata.items():
        st.write(f"- **{doc_id}**")
        st.write(f"  - Keywords: {', '.join([kw[0] for kw in doc_info['keywords']])}")
        st.download_button("View Document", doc_info["text"], file_name=doc_id)

# Search functionality
search_query = st.text_input("Search documents")
if search_query:
    with st.spinner("Searching..."):
        results = perform_search(search_query, st.session_state.metadata)
        if results:
            st.write("### Search Results")
            for result in results:
                doc_id = result['doc_id']
                snippet = result['snippet']
                full_text = result['full_text']
                distance = result['distance']

                st.write(f"- **Document**: {doc_id}")
                st.write(f"  - Relevance Score: {1 / (1 + distance):.2f}")
                st.write(f"  - Snippet: {snippet}...")
                st.download_button("View Full Document", full_text, file_name=doc_id)
            
            st.session_state.search_history.append({"query": search_query, "results": [r['doc_id'] for r in results]})
        else:
            st.write("No results found.")

# Analytics visualization
if st.button("Show Analytics"):
    with st.spinner("Generating analytics..."):
        visualize_analytics(st.session_state.search_history, st.session_state.metadata)
