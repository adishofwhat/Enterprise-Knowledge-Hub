import streamlit as st
from ml_pipeline import extract_text_from_pdf, process_text, add_to_faiss, doc_id_map
from search import perform_search
from analytics import visualize_analytics

if "metadata" not in st.session_state:
    st.session_state.metadata = {}
if "search_history" not in st.session_state:
    st.session_state.search_history = []

st.sidebar.title("Uploaded Documents")

if st.session_state.metadata:
    for doc_id, doc_info in st.session_state.metadata.items():
        with st.sidebar:
            st.write(f"- **{doc_id}**")
            if st.sidebar.button(f"Download {doc_id}"):
                st.sidebar.download_button("Download", doc_info["text"], file_name=doc_id)

st.title("Enterprise Knowledge Hub")
st.write("Upload multiple documents, explore semantic search, and gain insights.")

uploaded_files = st.file_uploader("Upload PDF documents", type=["pdf"], accept_multiple_files=True, label_visibility="collapsed")
if uploaded_files:
    st.empty()

    with st.spinner("Processing documents..."):
        for uploaded_file in uploaded_files:
            text = extract_text_from_pdf(uploaded_file)
            doc_id = uploaded_file.name

            entities, keywords = process_text(text)

            add_to_faiss(text, doc_id)
            st.session_state.metadata[doc_id] = {"text": text, "entities": entities, "keywords": keywords}

        st.success(f"Uploaded and processed {len(uploaded_files)} document(s).")

if not uploaded_files:
    st.markdown("""
        <style>
            .stButton>button {
                width: 100%;
                height: 50px;
                font-size: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

search_query = st.text_input("Search documents", key="search_query")
if search_query:
    with st.spinner("Searching..."):
        results = perform_search(search_query, st.session_state.metadata)
        if results:
            st.write("### Search Results")
            seen_documents = set()
            for idx, result in enumerate(results):
                doc_id = result['doc_id']
                distance = result['distance']

                if doc_id not in seen_documents:
                    seen_documents.add(doc_id)
                    st.write(f"- **Document**: {doc_id}")
                    st.write(f"  - Relevance Score: {1 / (1 + distance):.2f}")

                    st.download_button(
                        label="View Full Document",
                        data=st.session_state.metadata[doc_id]["text"],
                        file_name=doc_id,
                        key=f"download_{doc_id}_{idx}"
                    )

            st.session_state.search_history.append({"query": search_query, "results": list(seen_documents)})
        else:
            st.write("No results found.")

analytics_button = st.button("Show Analytics", disabled=not bool(st.session_state.search_history))
if analytics_button:
    with st.spinner("Generating analytics..."):
        visualize_analytics(st.session_state.search_history, st.session_state.metadata)