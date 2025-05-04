from flask import Flask, jsonify, request
import doubao
import threading
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 创建Flask应用实例
app = Flask(__name__)

# 模拟一个存储请求信息的字典，这里可以使用更合适的数据库或缓存来存储
request_storage = {}


# 定义一个简单的API端点，返回JSON数据
@app.route('/aligenie/836b3919a0dc16c18aa723d080719eed.txt', methods=['GET'])
def hello():
    return "Jfc4Z4Ur15JwUBuvUQD5wg7Nu8+l+HscqYlfofbyJdbEJ1SwqC6HnN5aPDx0ApX4"


# 定义一个接收POST请求的API端点，处理JSON数据
@app.route('/ai', methods=['POST'])
def weather():
    try:
        # 获取请求中的JSON数据
        data = request.get_json()
        logging.info(f"Received data: {data}")

        utterance = data.get('utterance', '你好')
        userOpenId = data.get('userOpenId', '123')

        # 启用多线程去调用AI的接口
        threading.Thread(target=doubao_send, args=(userOpenId, utterance)).start()

        if utterance == "AI回答" and userOpenId in request_storage:
            result = {
                "returnCode": "0",
                "returnErrorSolution": "",
                "returnMessage": "",
                "returnValue": {
                    "reply": request_storage[userOpenId],
                    "resultType": "RESULT",  # ASK_INF   RESULT
                    "executeCode": "SUCCESS"
                }
            }
            del request_storage[userOpenId]
        else:
            result = {
                "returnCode": "0",
                "returnErrorSolution": "",
                "returnMessage": "",
                "returnValue": {
                    "reply": '你可以说AI回答',
                    "resultType": "ASK_INF",  # ASK_INF   RESULT
                    "executeCode": "SUCCESS"
                }
            }

        logging.info(f"Sending response: {result}")
        return jsonify(result)
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"returnCode": "1", "returnErrorSolution": str(e), "returnMessage": "Error", "returnValue": {}})


def doubao_send(userOpenId, utterance):
    try:
        # 接口调用
        msgList = doubao.send(utterance)
        msg = "，".join(msgList)

        # 放入缓存
        request_storage[userOpenId] = msg
        logging.info(f"Stored message in cache for user {userOpenId}: {msg}")
    except Exception as e:
        logging.error(f"Error in doubao_send: {str(e)}")


if __name__ == '__main__':
    # 启动Flask应用，开启调试模式
    # app.run(debug=True)
    # 监听所有可用的网络接口，端口为80
    app.run(host='0.0.0.0', port=80, debug=True)
