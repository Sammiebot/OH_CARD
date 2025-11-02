import json
import random
from http.server import BaseHTTPRequestHandler

# 加载OH卡牌数据
oh_cards = [
    {"image_card": "房子", "word_card": "家", "combination": "房子·家", "guide_question": "这张卡让你想到什么样的家庭氛围？"},
    {"image_card": "树木", "word_card": "成长", "combination": "树木·成长", "guide_question": "你目前在哪个方面正在成长？"},
    {"image_card": "钥匙", "word_card": "解决", "combination": "钥匙·解决", "guide_question": "你生活中最需要解锁的问题是什么？"},
    {"image_card": "桥梁", "word_card": "连接", "combination": "桥梁·连接", "guide_question": "你目前生活中最需要连接的是什么？"},
    {"image_card": "书本", "word_card": "知识", "combination": "书本·知识", "guide_question": "什么知识对你现在最重要？"},
    {"image_card": "灯塔", "word_card": "指引", "combination": "灯塔·指引", "guide_question": "谁或什么是你生活中的指引？"},
    {"image_card": "雨伞", "word_card": "保护", "combination": "雨伞·保护", "guide_question": "你感觉自己在保护什么？"},
    {"image_card": "礼物", "word_card": "惊喜", "combination": "礼物·惊喜", "guide_question": "生活最近给了你什么惊喜？"},
    {"image_card": "门", "word_card": "机会", "combination": "门·机会", "guide_question": "什么机会正在向你敞开？"},
    {"image_card": "心", "word_card": "爱", "combination": "心·爱", "guide_question": "这张卡让你联想到什么样的爱？"}
]

class Handler(BaseHTTPRequestHandler):
    
    def do_OPTIONS(self):
        # 处理预检请求
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        try:
            # 读取请求数据
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            # 获取抽牌数量，默认为1
            count = request_data.get('count', 1)
            
            # 随机抽取卡牌
            if count == 1:
                drawn_cards = [random.choice(oh_cards)]
            else:
                drawn_cards = random.sample(oh_cards, min(count, len(oh_cards)))
            
            # 构建响应
            response = {
                "return_code": 0,
                "return_message": "success",
                "result": {
                    "drawn_cards": drawn_cards
                }
            }
            
            # 发送响应
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            # 错误处理
            error_response = {
                "return_code": 1,
                "return_message": f"Error: {str(e)}",
                "result": {}
            }
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))