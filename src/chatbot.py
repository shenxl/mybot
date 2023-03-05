import openai
import json
import tiktoken

from src.conf.config import get_config
from src.logs.logger import Logger


# 设置日志
logger = Logger(__name__)
class chatbot:
    def __init__(self):
        openai.api_key = get_config().OPENAI_API_KEY
        self.model_engine = get_config().OPENAI_MODEL

    def chat(self, chat):
        # Set up the OpenAI API request
        request_body = {
            "messages": chat,
            "model": self.model_engine
        }
        response = openai.ChatCompletion.create(**request_body)
        # logger.info(json.dumps(response))
        
        if 'choices' in response and response['choices']:
            text = response['choices'][0]['message']['content']
            usage = response['usage']
            return ("success", text, usage)
        else:
            return("error", json.dumps(response),None)
        
    # 当内容过多的时候，进行主题提炼
    def get_topic_summary(self, message):
        # TODO 压缩方面需要进一步优化
        sum_prompt = {"role":"user","content":"对上述对话中涉及的所有内容进行提炼总结,并返回总结内容"}
        message.append(sum_prompt)
        return self.chat(message)

    def num_tokens_from_messages(self,messages):
        """Returns the number of tokens used by a list of messages."""
        model = self.model_engine
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        if model == "gpt-3.5-turbo":  # note: future models may deviate from this
            num_tokens = 0
            for message in messages:
                num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
                for key, value in message.items():
                    num_tokens += len(encoding.encode(value))
                    if key == "name":  # if there's a name, the role is omitted
                        num_tokens += -1  # role is always required and always 1 token
            num_tokens += 2  # every reply is primed with <im_start>assistant
            return num_tokens
        else:
            raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
    See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")