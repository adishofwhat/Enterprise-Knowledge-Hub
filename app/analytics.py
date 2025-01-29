import matplotlib.pyplot as plt
import streamlit as st

def visualize_analytics(search_history, metadata):
    if not search_history:
        st.write("No searches performed yet. Analytics will appear here after some activity.")
        return
    
    st.write("### Analytics Dashboard")

    st.write("#### Most Searched Terms")
    search_terms = [item['query'] for item in search_history]
    term_counts = {term: search_terms.count(term) for term in set(search_terms)}
    sorted_terms = sorted(term_counts.items(), key=lambda x: x[1], reverse=True)

    fig, ax = plt.subplots()
    ax.bar([term[0] for term in sorted_terms], [term[1] for term in sorted_terms])
    ax.set_title("Search Term Frequency")
    ax.set_ylabel("Frequency")
    ax.set_xlabel("Search Terms")
    st.pyplot(fig)

    st.write("#### Most Relevant Documents")
    doc_counts = {}
    for search in search_history:
        for doc_id in search['results']:
            doc_counts[doc_id] = doc_counts.get(doc_id, 0) + 1
    sorted_docs = sorted(doc_counts.items(), key=lambda x: x[1], reverse=True)

    st.write("Most Retrieved Documents:")
    for doc_id, count in sorted_docs[:5]:
        st.write(f"- **{doc_id}**: Retrieved {count} times.")
