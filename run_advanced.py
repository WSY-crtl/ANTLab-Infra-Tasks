import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor

url = "http://localhost:8080/v1/chat/completions"

# 构造一个约 2000 token 的超长提示词，测试 8192 上下文的处理能力
long_prompt = "请总结以下内容的要点：" + "人工智能正在改变世界。" * 500

def send_long_request(index):
    start = time.time()
    payload = {
        "messages": [{"role": "user", "content": long_prompt}],
        "max_tokens": 100
    }
    try:
        res = requests.post(url, json=payload, timeout=180)
        end = time.time()
        return {"id": index, "status": res.status_code, "latency": round(end - start, 2)}
    except Exception as e:
        return {"id": index, "status": "error", "error": str(e)}

print("=== 长上下文测试（单个请求） ===")
print(send_long_request("long_context_1"))

print("\n=== 长上下文并发测试（3个并发） ===")
with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(send_long_request, f"adv_{i}") for i in range(3)]
    for f in futures:
        print(f.result())

print("\n✅ 进阶测试完成！")


