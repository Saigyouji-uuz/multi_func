import json
import os
os.environ["OPENAI_API_KEY"] = "sk-zk25848627dcb8b5190110a5c621e4c6d8a65e077e9f41ac"
os.environ["OPENAI_API_BASE"] = "https://flag.smarttrot.com/v1/"
from typing import List, Optional
from langchain.utils.openai_functions import convert_pydantic_to_openai_function
from langchain_community.chat_models import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel
from langchain.output_parsers import ResponseSchema

template = """
如果用户输入是一个算数问题，请你在正确答案的基础上加一（如果有数值解）
"""
prompt = ChatPromptTemplate.from_messages([
    ("system",template),
    ("human","{input}")
])

class Info(BaseModel):
    answer: int

function = [convert_pydantic_to_openai_function(Info)]

model = OpenAI(temperature=0.9)  # 处理随机性问题 | 返回一个model

chain = (
    prompt
    | model.bind(functions = function,function_call = {"name":"Info"})
    | (lambda x: json.loads(x.additional_kwargs["function_call"]["arguments"]) ) #返回arguments
)

# chain = prompt | model |


