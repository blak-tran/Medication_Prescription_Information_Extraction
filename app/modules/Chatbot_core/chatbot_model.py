from app.core.base_model import UserDataBaseModel
from app.core.utils import create_base_model
import openai
import os, json
from app.core.utils import load_environments
from gpt_json import GPTMessage, GPTMessageRole
from gpt_json.gpt import GPTJSON, ListResponse
from app.core.base_model import MedicationBaseModel, MetaDataBaseModel

from langchain.vectorstores import Chroma
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain, LLMChain, RetrievalQA
import logging
from json.decoder import JSONDecodeError

logger = logging.getLogger(__name__)


# Load environment variables from the .env file in the specified root directory
load_environments()

os.environ["OPENAI_API_KEY"] = "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"
OPENAI_KEY = os.getenv("OPENAI_KEY")
DEFAULT_JSON_PATH = os.getenv("DEFAULT_JSON_PATH")
prompt_template_json_tracking_ = os.getenv("prompt_template_json_tracking_")
prompt_template_standardize_data_ = os.getenv("prompt_template_standardize_data_")
chromadb_path = os.getenv("chromadb_path")
embedding_model = os.getenv("embedding_model")

openai.api_key = os.getenv("OPENAI_KEY")

# Ensure the API key is available
if not openai.api_key:
    raise ValueError(
        "OpenAI API key is not set. Please check your environment variables.")


SYSTEM_PROMPT = """
Analyze the Medication Prescription Information of the given text. with vietnamese output.

Respond with the following JSON schema:

{json_schema}
"""
def load_chromadb(chromadb_path, embedding_model):
    embedding = SentenceTransformerEmbeddings(model_name=embedding_model)

    vectordb = Chroma(persist_directory=chromadb_path,
                  embedding_function=embedding)
    return vectordb


class CHATBOT:
    def __init__(self, OPENAI_KEY: str, 
                 DEFAULT_JSON_PATH: str,
                 prompt_template_json_tracking_: str,
                 prompt_template_standardize_data_: str):
        
        self.gpt_tracking_medication = GPTJSON[ListResponse[MedicationBaseModel]](
            api_key=OPENAI_KEY, model="gpt-3.5-turbo")
        
        self.gpt_tracking_metaData = GPTJSON[MetaDataBaseModel](
            api_key=OPENAI_KEY, model="gpt-3.5-turbo")
        
        # self.prompt_template_json_tracking_ = prompt_template_json_tracking_
        self.prompt_template_standardize_data_ = prompt_template_standardize_data_
        
    async def Json_tracking(self, user_id: str,
                            prescription_Id: str, 
                            data: str) -> UserDataBaseModel:
        prompt = data + " prescription_Id: " + prescription_Id + " user_id: " + user_id
        print("Json Tracking Prompt: ", prompt)
        
        try:
            payload_medications = await self.gpt_tracking_medication.run(
                    messages=[
                        GPTMessage(role=GPTMessageRole.SYSTEM, content=SYSTEM_PROMPT),
                        GPTMessage(role=GPTMessageRole.USER, content=prompt),
                    ]
                )

        except JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        
        print("Medication lists: ", payload_medications.response)
        
        payload_meta_data = await self.gpt_tracking_metaData.run(
            messages=[
                GPTMessage(
                    role=GPTMessageRole.SYSTEM,
                    content=SYSTEM_PROMPT,
                ),
                GPTMessage(
                    role=GPTMessageRole.USER,
                    content=prompt,
                )
            ]
        )
        
        print("MetaData Tracking: ", payload_meta_data.response)
        
        return create_base_model(payload_medications.response, payload_meta_data.response, prescription_Id)

    async def data_generator(self, data, vectordb) -> str:
        query = data + ":" + self.prompt_template_standardize_data_
        # prompt = self.prompt_template_standardize_data_ + " " + data
        # print("Request Chatbot for generalized data: ", prompt)
        
        # # Adjusting the method call for a chat model
        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo-1106",  # Specify the engine you want to use
        #     messages=[
        #         {"role": "system", "content": "Your system message, if any"},
        #         {"role": "user", "content": prompt}
        #     ],
        #     temperature=0.7  # The creativity temperature, higher values mean more creative responses
        # )

        # # Assuming the response structure aligns with ChatCompletion's output
        # # This may need adjustment based on actual response structure
        # print(response.choices[0].message['content'].strip())
        
        # return response.choices[0].message['content'].strip()
        retriever = vectordb.as_retriever()
        import pdb; pdb.set_trace()
        docs = retriever.get_relevant_documents("tên thuốc")
        retriever = vectordb.as_retriever(search_kwargs={"k": 2})
        # retriever.get_relevant_documents("paradon extra")
        qa_chain = RetrievalQA.from_chain_type(llm=ChatOpenAI(model_name="gpt-3.5-turbo-1106"), 
                                  chain_type="stuff", 
                                  retriever=retriever, 
                                  return_source_documents=True)
        
        def process_llm_response(llm_response):
            print(llm_response['result'])
            print('\n\nSources:')
            for source in llm_response["source_documents"]:
                print(source.metadata['source'])

        llm_response = qa_chain(query)
        return process_llm_response(llm_response)
        # template = """Answer the question based only on the following context:
        #         {context}
        #         Question: {question}
        #         """
        # prompt = ChatPromptTemplate.from_template(template)
        # model = ChatOpenAI(model_name="gpt-3.5-turbo-1106")
        # chain = (

        #     {"context": retriever, "question": RunnablePassthrough()}

        #     | prompt

        #     | model

        #     | StrOutputParser()

        # )
        # question_generator_chain = LLMChain(llm=model, prompt=prompt)
        # chain = ConversationalRetrievalChain.from_llm(llm=model,combine_docs_chain=docs,
        #                                                retriever=retriever,
        #                                               question_generator=question_generator_chain,
        #                                               max_tokens_limit=16385)
        # response = chain.invoke(query)
        return response
        
        
    
vectordb = load_chromadb(chromadb_path, embedding_model)
llm_model = CHATBOT(OPENAI_KEY, DEFAULT_JSON_PATH, prompt_template_json_tracking_, prompt_template_standardize_data_)


if __name__ == "__main__":
    data = " trần tuân đạt, bệnh lý, nhức đầu, thuốc paradon extra: uống 1 ngày 2 lần mỗi lần một viên, pradone cetamon uống 2 lần 1 ngày sáng tối mỗi lần 1 ống, bác sĩ: lê thị hoa, bệnh viện hùng vương. lưu ý không dùng quá liều ảnh hưởng đến sức khỏe, uống từ ngày 18/2/2024 29/2/2024"
    data_gen = llm_model.data_generator(data, vectordb)
    data_final = llm_model.Json_tracking("dattran", "0001", data_gen)
    print("Data final: ", data_final)
    