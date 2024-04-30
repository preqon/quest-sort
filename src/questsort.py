'''
This script allows you to write a general query on all quest arcs.
'''

# imports 
from constants import openai_api_key, vault_path
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders.directory import DirectoryLoader 
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.chains import ConversationalRetrievalChain
import sys
import os
from langchain_community.document_loaders import UnstructuredMarkdownLoader

# globals
# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = False
documents_path = "arcs/"
os.environ["OPENAI_API_KEY"] = openai_api_key

def main():
    query = None
    if len(sys.argv) == 2: 
        query = sys.argv[1]

    if PERSIST and os.path.exists("persist"):
        print("Reusing index...\n")
        vectorstore = Chroma(
            persist_directory="persist",
            embedding_function=OpenAIEmbeddings())
        index = VectorStoreIndexWrapper(vectorstore=vectorstore) 
    else:
        loader = DirectoryLoader(vault_path+documents_path, glob='**/*.md')
        loader_meta = TextLoader("meta_context.md")
        if PERSIST:
            index = VectorstoreIndexCreator(
                vectorstore_kwargs={"persist_directory":"persist"}
                ).from_loaders([loader, loader_meta])
        else:
            index = VectorstoreIndexCreator().from_loaders([loader_meta,loader])

    llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=index.vectorstore.as_retriever(search_kwargs={"k": 12}),
        )
    
    chat_history = []
    while True:
        if not query:
            query = input("Prompt: ")
        if query.strip() in ['quit', 'q', 'exit']:
            sys.exit()
        result = chain({"question": query, "chat_history": chat_history})
        print(result['answer'])

        chat_history.append((query, result['answer']))
        query = None
    
if __name__ == "__main__":
    main()

