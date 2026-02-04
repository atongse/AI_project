
from pathlib import Path
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import hashlib
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

all_docs = []
class CreateDB:
    embedding = OllamaEmbeddings(model="all-minilm")
    vector_store = Chroma(collection_name="data", embedding_function=embedding, persist_directory="./")
    
    def load_txt_file(self, root_dir: str):
        root = Path(root_dir)

        for path in root.rglob("*.txt"):
            text = path.read_text(encoding="utf-8")

            # stable, collision-safe document id
            doc_id = path.relative_to(root).as_posix()

            yield doc_id, text

    def hash_text(self, text:str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


    def chunk_txt(self, doc_id: str, text: str, chunk_size: int = 500, chunk_overlap:int = 50):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap)
        
        chunks = splitter.split_text(text)
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
                        "source" : text,
                    },
                )
            )
        return docs
    
    def add_docs(self):
        try:
            for doc_id , text in self.load_txt_file("C:\\Users\\AdityaTongse\\Desktop\\project\\AI_project\\phase_2_rag\\data"):
                all_docs.extend(self.chunk_txt(doc_id,text))
            
            ids = [d.metadata["chunk_id"] for d in all_docs]
            if len(all_docs) == 0 :
                self.vector_store.add_documents(
                    documents=all_docs,
                    ids=ids,
                    embedding=self.embedding
                )
                print("Added docs to vector db")
        except Exception as e:
            print(e) 
createdb = CreateDB()

# createdb.add_docs()