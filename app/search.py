from ml_pipeline import model, faiss_index, doc_id_map

def perform_search(query, metadata):
    query_embedding = model.encode([query])
    D, I = faiss_index.search(query_embedding, k=5)
    results = []
    for i, distance in zip(I[0], D[0]):
        if i != -1:
            doc_id = doc_id_map.get(i, "Unknown") 
            if doc_id in metadata:
                document_text = metadata[doc_id]['text']
                snippet = document_text[:200]
                results.append({
                    "doc_id": doc_id,
                    "snippet": snippet,
                    "full_text": document_text,
                    "distance": round(distance, 2)
                })
    return results