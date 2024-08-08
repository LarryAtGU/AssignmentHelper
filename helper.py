import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import ChatOpenAI

key  = st.secrets["OPENAI_API_KEY"]

st.header("2805ICT/3815ICT/7805ICT Milestone One Helper")

training_file = "train.md"

if 'qa_history' not in st.session_state:
    st.session_state['qa_history'] = []


# Button to read and process the input

with open(training_file,"r") as file:
    text = file.read()
    spliter = RecursiveCharacterTextSplitter(
        separators="\n",
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len
    )
    chunks = spliter.split_text(text)
    # st.write(chunks)
    embeddings = OpenAIEmbeddings(openai_api_key=key)
    vector_store = FAISS.from_texts(chunks,embeddings)

    # question = st.text_input("Please input your question")
    question = st.text_input("Please input your question:")

    if question:
        matches = vector_store.similarity_search(question)
        llm = ChatOpenAI(
            openai_api_key=key,
            temperature=0,
            max_tokens=1000,
            model = 'gpt-4o-mini'
            # model='gpt-3.5-turbo-0125'
        )
        chain = load_qa_chain(llm, chain_type="stuff")
        # answer = chain.run(input_documents=matches,question=question)
        input_data = {
            "input_documents": matches,
            "question": question
        }

        # Use the invoke method with the input dictionary
        answer = chain.invoke(input=input_data)        
        st.session_state.qa_history.insert(0,(question, answer["output_text"]))

        # st.write(answer["output_text"])
        
for i, (question, answer) in enumerate(st.session_state['qa_history']):
    st.write(f"**Q:** {question}")
    st.write(f"**A:** {answer}")
    st.write("------------")
