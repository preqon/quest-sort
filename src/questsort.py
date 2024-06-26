'''
This script allows you to write a general query on all quest arcs.
'''

# imports 
from constants import openai_api_key, tasks_directory_path
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
import warnings

# globals
# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = False
os.environ["OPENAI_API_KEY"] = openai_api_key

def main():

    #temporary: suppress warnings.
    warnings.filterwarnings("ignore")

    #optionally use query from command line argument.
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
        loader = DirectoryLoader(tasks_directory_path, glob='**/*.md')
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


    #I have 11 text files containing tasks, and using 1 text file as meta
    #context. You should set the k search_kwarg to total no. of documents to use
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=index.vectorstore.as_retriever(search_kwargs={"k": 12}),
        )

    # Keep prompting until "quit", "q", or "exit" received. 
    # Chat history is passed to LLM.
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

