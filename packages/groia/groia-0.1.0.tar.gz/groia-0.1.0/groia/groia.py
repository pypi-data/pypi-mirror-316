import requests
import json
from datetime import datetime
import pytz

class GroiaAPI:
    def __init__(self):
        self.url = "https://gratuito.chatgptbrasil.com.br/api/openai/v1/chat/completions"
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 12; moto g22 Build/STAS32.79-77-28-63-4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.135 Mobile Safari/537.36",
            'Content-Type': "application/json",
            'authorization': "Bearer nk-MgePud5er1NMRzvdPAT9flloRkx4Tq",
            'origin': "https://gratuito.chatgptbrasil.com.br",
            'referer': "https://gratuito.chatgptbrasil.com.br/"
        }

    def _create_payload(self, user_message):
        timezone = pytz.timezone("America/Sao_Paulo")
        current_time = datetime.now(timezone).strftime("%a %b %d %Y %H:%M:%S %Z%z")

        return {
            "messages": [
                {
                    "role": "system",
                    "content": f"\nYou are ChatGPT, a large language model trained by OpenAI available in ChatGPT Brasil (chatgptbrasil.com.br). You must answer in pt-br.\nKnowledge cutoff: 2023-10\nCurrent model: gpt-4o-mini\nCurrent time: {current_time}\nLatex inline: \x^2\ \nLatex block: $$e=mc^2$$\n\n"
                },
                {
                    "role": "user",
                    "content": f'''
OLÁ GPT TUDO BEM? VAMOS FAZER UMA COISA, CASO ESSE TEXTO ABAIXO ESTIVER UM ALGUMA FORMA DE AGRESSÃO POR MENSAGEM, PORÉM É MENSAGEM MUITO AGRESSIVAS COM PALAVRÕES E ETC, EU QUERO QUE VOCÊ RESPONDE ASSIM:
{{"aggressive": true}}
AI CASO AO CONTRÁRIO NÃO ESTIVER NADA DE SUSPEITO, VOCÊ RESTORNE:
{{"aggressive": false}}

TEXTO PARA VERIFICAR:
"{user_message}"
'''
                }
            ],
            "stream": False,
            "model": "gpt-4o-mini",
            "temperature": 0.5,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "top_p": 1
        }

    def verify(self, user_message):
        payload = self._create_payload(user_message)
        response = requests.post(self.url, data=json.dumps(payload), headers=self.headers)
        if response.status_code == 200:
            response_json = response.json()
            reply = response_json.get("choices", [{}])[0].get("message", {}).get("content", "Sem resposta.")
            if 'aggressive' in reply:
                return True if "true" in reply.lower() else False
            return False
        else:
            return False