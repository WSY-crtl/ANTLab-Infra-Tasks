import requests
import json
import time
import os

# 1. 读取任务列表
with open("tasks/test_tasks.json", "r", encoding="utf-8") as f:
    tasks = json.load(f)

# 2. 创建结果目录
os.makedirs("results", exist_ok=True)

url = "http://localhost:8080/v1/chat/completions"
all_results = []

for task in tasks:
    print(f"正在执行任务 {task['id']} ({task['type']})...")
    
    payload = {
        "messages": [
            {"role": "system", "content": "你是一个专业的AI助手，请准确、完整地回答问题。"},
            {"role": "user", "content": task["prompt"]}
        ],
        "max_tokens": 512,
        "temperature": 0.1
    }
    
    start_time = time.time()
    try:
        response = requests.post(url, json=payload, timeout=120)
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            output = data['choices'][0]['message']['content']
            status = "success"
        else:
            output = f"Error: HTTP {response.status_code}"
            status = "failed"
    except Exception as e:
        end_time = time.time()
        output = f"Exception: {str(e)}"
        status = "timeout"
    
    elapsed = round(end_time - start_time, 2)
    
    # 保存单条结果
    result_item = {
        "task_id": task["id"],
        "type": task["type"],
        "prompt": task["prompt"],
        "output": output,
        "status": status,
        "elapsed_seconds": elapsed
    }
    all_results.append(result_item)
    
    print(f"  -> 状态: {status}, 耗时: {elapsed}s")
    print(f"  -> 回复: {output[:50]}...\n")

# 3. 把所有结果保存到 JSON 文件
with open("results/test_results.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)

print("✅ 全部测试完成！结果已保存到 results/test_results.json")


