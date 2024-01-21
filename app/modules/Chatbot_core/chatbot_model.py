from app.core.base_model import user_data_basemodel
from app.core.utils import create_base_model
from openai import OpenAI
import os, json
from app.core.utils import load_environments

# Load environment variables from the .env file in the specified root directory
load_environments()

OPENAI_KEY = os.getenv("OPENAI_KEY")
DEFAULT_JSON_PATH = os.getenv("DEFAULT_JSON_PATH")
prompt_template_json_tracking_ = os.getenv("prompt_template_json_tracking_")
prompt_template_standardize_data_ = os.getenv("prompt_template_standardize_data_")

class CHATBOT:
    def __init__(self, OPENAI_KEY: str, 
                 DEFAULT_JSON_PATH: str,
                 prompt_template_json_tracking_: str,
                 prompt_template_standardize_data_: str):
        
        self.llm_client = OpenAI(
            api_key = OPENAI_KEY
        )
        with open(DEFAULT_JSON_PATH, "r") as json_file:
            self.default_json_format = json.load(json_file)
        self.prompt_template_json_tracking_ = prompt_template_json_tracking_
        self.prompt_template_standardize_data_ = prompt_template_standardize_data_
        
        
        
    def Json_tracking(self, data: str) -> user_data_basemodel:
        prompt = self.prompt_template_json_tracking_ + " " + data
        print("Reqest Chatbot for parse json: ", prompt)
        chat_completion = self.llm_client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={"type":"json_object"},
            messages=[
                {"role":"system","content":"Cung cấp đầu ra ở dạng JSON hợp lệ với mỗi medication là một loại thuốc với những thông tin như được cung cấp trên. Lược đồ dữ liệu phải như thế này:"+json.dumps(self.default_json_format)},
                {"role":"user","content":prompt}
            ]
        )

        finish_reason = chat_completion.choices[0].finish_reason

        if finish_reason == "stop":
            data = chat_completion.choices[0].message.content
            medication = json.loads(data)
            print(medication)
        else :
            print("Error! provide more tokens please")
            
        return {"user_data": create_base_model(form_json=medication)}
    
    def standardize_data(self, data) -> str:
        prompt = self.prompt_template_standardize_data_ + " " + data
        print("Reqest Chatbot for generalize data: ", prompt)
        chat_completion = self.llm_client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        finish_reason = chat_completion.choices[0].finish_reason

        if finish_reason == "stop":
            data = chat_completion.choices[0].message.content
        else:
            print("Error! provide more tokens please")
            
        return data
    
    
llm_model = CHATBOT(OPENAI_KEY, DEFAULT_JSON_PATH, prompt_template_json_tracking_, prompt_template_standardize_data_)