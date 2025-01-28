import PyPDF2
from sentence_transformers import SentenceTransformer
import faiss
import spacy
from keybert import KeyBERT

model = SentenceTransformer('all-MiniLM-L6-v2')
faiss_index = faiss.IndexFlatL2(384)
nlp = spacy.load('en_core_web_trf')
keybert_model = KeyBERT()

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def process_text(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    keywords = keybert_model.extract_keywords(text, top_n=5)
    return entities, keywords

doc_id_map = {}

def add_to_faiss(text, doc_id):
    embeddings = model.encode([text])
    start_index = faiss_index.ntotal  # Current size of the FAISS index
    faiss_index.add(embeddings)
    doc_id_map[start_index] = doc_id  # Map the FAISS index to the doc_id