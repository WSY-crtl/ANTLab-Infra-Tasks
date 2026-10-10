import requests
import json
import time

url = "http://localhost:8080/v1/chat/completions"

payload = {
    "messages": [
        {"role": "user", "content": "你好，请用一句话介绍你自己。"}
    ],
    "max_tokens": 100
}

start_time = time.time()
response = requests.post(url, json=payload)
end_time = time.time()

print("状态码:", response.status_code)
print("耗时:", round(end_time - start_time, 2), "秒")
print("模型回复:", response.json()['choices'][0]['message']['content'])


