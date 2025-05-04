import requests
import os
import time
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 定义请求的URL
url1 = 'https://api.coze.cn/v3/chat/retrieve'
url = 'https://api.coze.cn/v3/chat'
url2 = 'https://api.coze.cn/v3/chat/message/list'

# 定义请求头
headers = {
    'Authorization': "Bearer pat_*************",
    'Content-Type': 'application/json'
}


def send(content):
    # 定义请求体数据
    data = {
        "bot_id": "7482190285729071139",
        "user_id": "123456789",
        "stream": False,
        "auto_save_history": True,
        "additional_messages": [
            {
                "role": "user",
                "content": content,
                "content_type": "text"
            }
        ]
    }
    try:
        # 发送POST请求
        response = requests.post(url, headers=headers, json=data)
        # 检查响应状态码
        response.raise_for_status()
        chat_id = response.json()['data']['id']
        conversation_id = response.json()['data']['conversation_id']
        while True:
            respList = requests.get(f"{url1}?chat_id={chat_id}&conversation_id={conversation_id}", headers=headers)
            status = respList.json()['data']['status']
            if status == 'completed':
                break
            time.sleep(0.5)
        respList = requests.get(f"{url2}?chat_id={chat_id}&conversation_id={conversation_id}", headers=headers)
        return [x['content'] for x in respList.json()['data'] if x['type'] == 'answer']
    except requests.exceptions.HTTPError as http_err:
        logging.error(f'HTTP error occurred: {http_err}')
        if response.status_code == 401:
            logging.error('可能是Authorization令牌错误，请检查令牌。')
        elif response.status_code == 404:
            logging.error('请求的资源未找到，请检查URL是否正确。')
    except Exception as err:
        logging.error(f'Other error occurred: {err}')


if __name__ == '__main__':
    msg = send("今天是几月几号，深圳天气怎么样")
    logging.info(f"获取到的聊天回复: {msg}")
