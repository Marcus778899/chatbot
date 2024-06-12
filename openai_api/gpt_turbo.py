import json
from pathlib import Path
from docx import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.chains.retrieval_qa.base import RetrievalQA

class ChatOpenAPI:
    def __init__(self, query:str) -> None:
        self.work_dir = Path(__file__).parent.parent
        self.query = query
        self.API_KEY,self.BASE_URL = self.login_info()

    def login_info(self):
        with open(f"{self.work_dir}/login_info/openai_token.json","r") as file:
            login_info = json.load(file)
        return login_info['api_key'],login_info['base_url']
    
    # rule about dress
    def rule_dress(self) -> str:
        word = Document(f"{self.work_dir}/openai_api/服裝儀容規範.docx")
        full_text = [para.text for para in word.paragraphs]
        return '\n'.join(full_text)
    
    def vectorstore(self) -> Chroma:
        text_splitter = CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=0
        )
        texts = text_splitter.split_text(self.rule_dress())

        embedding = OpenAIEmbeddings(api_key = self.API_KEY, base_url=self.BASE_URL)
        vectorstore = Chroma.from_texts(texts, embedding)

        return vectorstore

    def main(self) -> str:
        '''
        return answer from gpt-3.5-turbo
        '''
        retriever = self.vectorstore().as_retriever()
        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo", 
            temperature=0, 
            openai_api_key=self.API_KEY, 
            base_url=self.BASE_URL
            )

        qa = RetrievalQA.from_chain_type(
            llm=llm, 
            chain_type="stuff", 
            retriever=retriever
            )
        response = qa({"query": self.query})
        return response['result']

if __name__ == "__main__":
    action = ChatOpenAPI('如何選擇服裝')
    print(action.main())