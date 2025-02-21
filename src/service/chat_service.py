import os
import openai
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from ..repository.chat_repository import ChatRepository
from langchain_elasticsearch import ElasticsearchStore
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.chains import ConversationalRetrievalChain, LLMChain


class ChatService:
    def __init__(self):
        self.openai = openai.api_type = "azure"
        self.repository = ChatRepository()
        self.embedding = AzureOpenAIEmbeddings(
            api_version=os.getenv('OPENAI_API_VERSION_EMBEDDING'),
            api_key=os.getenv('OPENAI_API_KEY'),
            azure_endpoint=os.getenv('EMBEDDING'),
            azure_deployment="text-embedding-large",
            dimensions=3072,
            chunk_size=1
        )
        self.llm = AzureChatOpenAI(
            api_version=os.getenv('OPENAI_API_VERSION'),
            azure_deployment="gpt-4o",
            temperature=0.8,
            azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
            api_key=os.getenv('OPENAI_API_KEY')
        )

    async def process_chat(self, enterprise: str, question: str, chat_history: list[dict]) -> dict:
        """
        Processa a pergunta do usuário, busca no Elasticsearch e gera uma resposta.
        Salva a conversa no banco de dados.
        """
        index_name = enterprise.replace(" ", "").lower()

        db = ElasticsearchStore(
            es_cloud_id=os.getenv('ES_CLOUD_ID'),
            es_user=os.getenv('ES_USER'),
            es_password=os.getenv('ES_PASSWORD'),
            index_name=index_name,
            embedding=self.embedding,
        )

        # Preparar histórico do chat
        user_message = []
        if chat_history:
            last_messages = chat_history[-2:]  # Pegamos as duas últimas interações
            for message in last_messages:
                if message['role'] == 'user':
                    user_message.append(f"Pergunta anterior: {message['message']}")
                else:
                    user_message.append(f"Última Resposta: {message['message']}")

        user_message.append(f"Pergunta atual: {question}")
        messages_string = '\n'.join(user_message)

        # Seleciona o template correto
        template = """
        Você é um especialista em seguros e deve responder às perguntas do usuário com base no contexto fornecido. 
        Se o contexto não contiver uma resposta direta, elabore uma resposta fundamentada em princípios gerais sobre seguros. 
        Se a pergunta não estiver relacionada a seguros, gentilmente informe ao usuário que você só pode responder perguntas sobre esse tema.

        Seu objetivo é fornecer respostas completas, detalhadas e bem explicadas.

        ### Contexto ###
        {context}

        ### Pergunta ###
        {question}

        ### Resposta ###
        """

        QA_CHAIN_PROMPT = PromptTemplate(
            template=template,
            input_variables=["question", "context"]
        )
        # Configurar a cadeia de busca e resposta
        qa_chain = RetrievalQA.from_chain_type(
            self.llm,
            retriever=db.as_retriever(search_kwargs={"k": 5, "m": 10}),
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
            return_source_documents=True,
        )
        prompt = QA_CHAIN_PROMPT.format(question=messages_string, context="")
        response = qa_chain({"query": prompt})
        # Criar resposta formatada
        # Criar resposta formatada corretamente
        resposta_final = {
            "answer": response["result"],
            "documents": [
                {
                    "metadata": doc.metadata,
                    "content": doc.page_content
                } for doc in response["source_documents"]
            ]
        }

        # Salvar chat no banco
        await self.repository.save_chat({
            "enterprise": enterprise,
            "chat_history": chat_history + [{"role": "user", "message": question},
                                            {"role": "assistant", "message": resposta_final["answer"]}]
        })

        return resposta_final
