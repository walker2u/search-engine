from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
vector = model.encode("Hello i am Mayank Kumar Prasad")

print(f"type : {type(vector)}, length : {len(vector)}")
