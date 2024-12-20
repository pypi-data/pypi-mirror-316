import requests
import json

class rgpt:
    url = "https://api.openai-hk.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer hk-yq2qv81000048809acf94a836973969faebd7edb4bf0664b"
    }

    @staticmethod
    def ru(message):
        data = {
            "max_tokens": 1200,
            "model": "gpt-3.5-turbo",
            "temperature": 0.8,
            "top_p": 1,
            "presence_penalty": 1,
            "messages": [
                {
                    "role": "system",
                    "content": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible."
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        }

        response = requests.post(RGPT.url, headers=RGPT.headers, data=json.dumps(data).encode('utf-8'))
        result = response.content.decode("utf-8")
        data_dict = json.loads(result)

        # 提取特定的内容
        content = data_dict['choices'][0]['message']['content']

        # 返回结果
        return content

# Example usage:
# print(RGPT.ru("信息"))
#print(RGPT.ru("判断下面这句话是否正确直接输出答案：在pyplot模块中，使用scatter()函数可以根据数据快速地绘制一个直方图。"))
