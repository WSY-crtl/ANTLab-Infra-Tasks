import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor

url = "http://localhost:8080/v1/chat/completions"

# 任务书要求的测试提示词（我们选一个通用的，跑多轮）
test_payload = {
    "messages": [
        {"role": "user", "content": "请用一句话介绍量子纠缠。"}
    ],
    "max_tokens": 100
}

def send_request(index):
    start = time.time()
    try:
        res = requests.post(url, json=test_payload, timeout=120)
        end = time.time()
        return {
            "request_id": index,
            "status_code": res.status_code,
            "latency": round(end - start, 2)
        }
    except Exception as e:
        return {"request_id": index, "status_code": "error", "error": str(e)}

# --- 1. 单并发测试（连续3轮）---
print("=== 单并发测试 ===")
single_results = []
for i in range(3):
    result = send_request(f"single_{i+1}")
    single_results.append(result)
    print(f"第 {i+1} 轮: {result}")

# --- 2. 多并发测试（一次发5个请求）---
print("\n=== 多并发测试（5个并发） ===")
concurrent_results = []
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(send_request, f"concurrent_{i+1}") for i in range(5)]
    for future in futures:
        res = future.result()
        concurrent_results.append(res)
        print(f"请求 {res['request_id']}: {res}")

# --- 保存数据 ---
output = {
    "single_concurrency": single_results,
    "multi_concurrency": concurrent_results
}

with open("results/concurrency_results.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("\n✅ 并发测试完成！数据已保存到 results/concurrency_results.json")


