
from pathlib import Path
from langchain_chroma import Chroma
import hashlib
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from phase_2_rag.shared.embeddings.embedding_service import EmbeddingService
import tiktoken

tokenizer = tiktoken.get_encoding("cl100k_base")

def token_len(text: str) -> int:
    return len(tokenizer.encode(text))


all_docs = []
class CreateDB:
    def __init__(self):
        self.embedding = EmbeddingService()
        self.vector_store = Chroma(collection_name="data", persist_directory="./")
        self.DATA_DIR = "C:\\Users\\AdityaTongse\\Desktop\\project\\AI_project\\phase_2_rag\\data"
    
    def load_txt_file(self, root_dir: str):
        root = Path(root_dir)
        print("loading data")

        for path in root.rglob("*.txt"):
            text = path.read_text(encoding="utf-8")

            # stable, collision-safe document id
            doc_id = path.relative_to(root).as_posix()

            yield doc_id, text

    def hash_text(self, text:str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


    def split_token_safe(self, text: str):
        MAX_TOKENS = 128  
        words = text.split()
        chunks = []
        current = []

        for word in words:
            current.append(word)
            if token_len(" ".join(current)) >= MAX_TOKENS:
                chunks.append(" ".join(current[:-1]))
                current = [word]

        if current:
            chunks.append(" ".join(current))

        return chunks


    def chunk_txt(self, doc_id: str, text: str, chunk_size: int = 256, chunk_overlap:int = 15):
        
        print("chunking docs")
        
        chunks = self.split_token_safe(text)
        docs = []

        for i, chunk in enumerate(chunks):
            chunk_id = f"{doc_id}::{self.hash_text(chunk)}"

            docs.append(
                Document(
                    page_content=chunk, 
                    metadata = {
                        "doc_id": doc_id,
                        "chunk_id": chunk_id,
                        "chunk_index" : i,
                        "source" : doc_id,
                    },
                )
            )
        return docs
    
    def add_docs(self):
        all_docs = []

        for doc_id, text in self.load_txt_file(self.DATA_DIR):
            chunks = self.chunk_txt(doc_id, text)
            all_docs.extend(chunks)

        print("Number of chunks:", len(all_docs))
        print("Max chunk length:",
            max(len(d.page_content) for d in all_docs))

        texts = [d.page_content for d in all_docs]

        embeddings = []
        for i, t in enumerate(texts):
            print(f"Embedding chunk {i+1}/{len(texts)} | len={len(t)}")
            embeddings.append(self.embedding.embed([t])[0])

        self.vector_store.add_texts(
            texts=texts,
            embeddings=embeddings,
            metadatas=[d.metadata for d in all_docs],
            ids=[d.metadata["chunk_id"] for d in all_docs]
        )


createdb = CreateDB()

createdb.add_docs()