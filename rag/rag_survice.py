"""
#总结服务,总结检索到的资料的工具吧
"""
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from rag.vector_store import  VectorStoreSurvice
from utils.prompt_loader import  load_rag_prompts
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model

def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)
    return prompt


class RagSummarizeService(object):
    def __init__(self):
        self.vector_store = VectorStoreSurvice()
        self.retriever = self.vector_store.get_retriever()
        self.prompt_text = load_rag_prompts()
        self.propmt_template = PromptTemplate.from_template(self.prompt_text)
        self.model =chat_model
        self.chain =self.init_chain()

    def init_chain(self):
        chain =self.propmt_template|print_prompt|self.model|StrOutputParser()
        return chain

    def retriever_docs(self,query:str)->list[Document]:
        return self.retriever.invoke(query)

    def rag_summarize(self,query:str)->str:
        context_docs = self.retriever_docs(query)

        context = ""
        counter = 0
        for doc in context_docs:
            counter += 1
            context += f"【参考资料{counter}】：参考资料：{doc.page_content}｜参考元数据：{doc.metadata}\n"
        #print(context)
        return self.chain.invoke(
            {
                "input":query,
                "context":context
            }
        )
if __name__ == "__main__":
    rag = RagSummarizeService()

    print(rag.rag_summarize("小户型适合哪些扫地机器人"))