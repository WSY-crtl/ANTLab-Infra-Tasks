import gradio as gr
import requests
import json

# 调用本地 8080 端口的推理服务
def chat_with_model(message, history):
    url = "http://localhost:8080/v1/chat/completions"
    payload = {
        "messages": [{"role": "user", "content": message}],
        "max_tokens": 512
    }
    try:
        response = requests.post(url, json=payload, timeout=120)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"请求出错: {str(e)}"

# 读取之前跑出来的测试数据，展示在表格里
def load_results():
    try:
        with open("results/test_results.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return [[d["task_id"], d["type"], d["status"], d["elapsed_seconds"]] for d in data]
    except:
        return [["数据未找到", "-", "-", "-"]]

# 搭建网页界面
with gr.Blocks(title="ANTLab 推理服务前端") as demo:
    gr.Markdown("# 本地大模型推理服务前端展示")
    
    with gr.Tab("对话"):
        gr.ChatInterface(chat_with_model)
    
    with gr.Tab("测试结果统计"):
        gr.Dataframe(
            headers=["任务ID", "类型", "状态", "耗时(秒)"],
            value=load_results(),
            label="10个规定任务测试结果"
        )

# 启动网页，端口 7860
demo.launch(server_name="0.0.0.0", server_port=7860)

