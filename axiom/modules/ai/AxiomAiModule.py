# author https://github.com/MIrrox27/Axiom
# Ai Module
# AxiomAiModule.py

from openai import OpenAI
import requests
import os, time

from axiom.modules.ai.api import MODEL_URL, MODEL_TOKEN, MODEL_NAME # токен и url


"""
    Список функций для реализации:
        
        - загрузка модели в формате ONNX (`var model = `)
        - функция с определенным количеством запросов
        
            # текстовые модели
        - отправка запросов модели и получение ответа
        - создание контекста 
        - очистка контекста 
        
            
            # изображения 
        - 
        -
"""



class Error:
    def __init__(self, module):
        self.module = module

    def raise_error(self,  msg, func):
        raise Exception(f'[{self.module}]: [{func}] {msg}')


class AiModule:
    error = Error('AiModule')
    def __repr__(self):
        return ""



class Ai(AiModule):
    def __init__(self, model, temperature=0.5, max_tokens=250, stream=False):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.stream = stream



class Client(AiModule): # класс для отправки запросов, хранения контекста
    def __init__(self, api, base_url, context, ai):
        self.api = api
        self.base_url = base_url
        self.context = context

        self.model = ai.model
        self.temperature = ai.temperature
        self.max_tokens = ai.max_tokens
        self.stream = ai.stream

        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api
        )




class Response(Client):
    def __init__(self, client, msg):
        self.client = client
        self.msg = msg



    def send_response(self):
        func = 'send_response'


        if isinstance(self.msg, (int, str, float)):
            self.client.context.append({
            'role': 'user',
            'content': str(self.msg)
            })

        elif isinstance(self.msg, dict):
            self.client.context.append(self.msg)

        else:
            self.error.raise_error(f'Invalid message format: {self.msg}', func=func)


        response = self.client.client.chat.completions.create( # отправляем
            model=self.client.model,
            messages=self.client.context,
            temperature=self.client.temperature,
            stream=self.client.stream
        )


        bot_answer = response.choices[0].message.content

        while True:
            time.sleep(0.1)
            if bot_answer != None:
                break

        self.client.context.append({
            'role': 'assistant',
            'content': str(bot_answer)
            })

        return bot_answer
















