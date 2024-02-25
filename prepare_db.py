from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.document_loaders import CSVLoader
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings

loader = CSVLoader(file_path='/home/cuong/cuong/exe202_project_Medication_Prescription_Information_Extraction/LongChau_medicine.csv')
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

persist_directory = 'app/db'

embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

vectordb = Chroma.from_documents(documents,
                                 embedding=embedding,
                                 persist_directory=persist_directory)