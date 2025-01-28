from ml_pipeline import model, faiss_index, doc_id_map

def perform_search(query, metadata):
    """Perform semantic search using FAISS index."""
    query_embedding = model.encode([query])
    D, I = faiss_index.search(query_embedding, k=5)  # Retrieve top 5 matches
    results = []
    for i, distance in zip(I[0], D[0]):  # Pair index and distance
        if i != -1:  # Check for valid index
            doc_id = doc_id_map.get(i, "Unknown")  # Get the associated document ID
            if doc_id in metadata:
                document_text = metadata[doc_id]['text']
                snippet = document_text[:200]  # Take the first 200 characters as a preview
                results.append({
                    "doc_id": doc_id,
                    "snippet": snippet,
                    "full_text": document_text,
                    "distance": round(distance, 2)  # Round the distance to 2 decimal points
                })
    return results
