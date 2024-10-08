from dotenv import load_dotenv
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
import tiktoken
import os
from elasticsearch import Elasticsearch
from langchain_elasticsearch import ElasticsearchStore

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
INDEX_NAME = os.getenv('INDEX_NAME')
# CHAT_MODEL_NAME = os.getenv('CHAT_MODEL_NAME')

model_name = "gpt-4o"
embeddings = HuggingFaceEmbeddings(model_name='intfloat/multilingual-e5-large')
encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)
vectorstore = PineconeVectorStore(index=index, embedding=embeddings)

es = Elasticsearch("http://172.16.28.205:9200", verify_certs=False)

elastic_index = "faizan_e_ramadan_v2"

index_mapping = {
    "mappings": {
        "properties": {
            "title": {"type": "text"},
            "source": {"type": "text"},
            "page": {"type": "integer"},
            "embedding": {
                "type": "dense_vector",
                "dims": 1024
            }
        }
    }
}

if not es.indices.exists(index=elastic_index):
    es.indices.create(index=elastic_index, body=index_mapping)

elasticstore = ElasticsearchStore(
    index_name=elastic_index, embedding=embeddings, es_connection=es
)

# index_mapping = {
#     "mappings": {
#         "properties": {
#             "title": {"type": "text"},
#             "source": {"type": "text"},
#             "page": {"type": "integer"},
#             "embedding": {
#                 "type": "dense_vector",
#                 "dims": 1024
#             }
#         }
#     }
# }

# if not es.indices.exists(index=elastic_index):
#     es.indices.create(index=elastic_index, body=index_mapping)
