from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain.chains import create_retrieval_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
from utils import build_history_aware_retriever, build_qa_chain
from services.llm_service import get_llm
from services.db_service import get_db

class ChatService:
    def __init__(self):
        self.store = {}
        
    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]
    
    async def process_message(self, message: str, session_id: str = "default"):
        try:
            llm = get_llm()
            db = get_db()
            retriever = db.as_retriever()
            
            history_aware_retriever = build_history_aware_retriever(llm, retriever)
            qa_chain = build_qa_chain(llm)
            history_rag_chain = create_retrieval_chain(history_aware_retriever, qa_chain)
            
            conversational_rag_chain = RunnableWithMessageHistory(
                history_rag_chain,
                self.get_session_history,
                input_messages_key="input",
                history_messages_key="chat_history",
                output_messages_key="answer",
            )
            
            response = conversational_rag_chain.invoke(
                {"input": message},
                config={"configurable": {"session_id": session_id}},
            )
            
            return response["answer"]
        except Exception as e:
            raise Exception(f"Error processing message: {str(e)}")