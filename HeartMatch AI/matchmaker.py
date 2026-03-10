# matchmaker.py
import requests
import json
import os
import re

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "your API_KEY")
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"

def calculate_match(profile_text_a: str, profile_text_b: str) -> dict:
    """
    调用 DeepSeek 接口，直接对比两个用户的 profile_text，返回匹配分数和分析。
    """
    prompt = f"""
你是一个顶级的 AI 婚恋匹配专家。你的任务是评估两位用户的契合度。
请不仅考虑他们的“相似性”（如共同爱好），更要考虑他们的“互补性”（如性格互补、生活习惯契合）。

【用户 A 画像】
{profile_text_a}

【用户 B 画像】
{profile_text_b}

请深度分析这两位用户在性格、价值观、生活习惯、恋爱观等方面的匹配程度。
必须输出 JSON 格式，包含以下字段：
- "score": 一个 0 到 100 的整数，代表综合匹配度（分数越高越匹配）。
- "pros": 一个数组，列出他们相处的 2-3 个核心优势。
- "cons": 一个数组，列出他们相处可能面临的 1-2 个潜在矛盾或挑战。
- "summary": 一段 50 字左右的综合评价，作为给他们的匹配寄语。
"""

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5, 
        "response_format": {"type": "json_object"} 
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        
        result_text = response.json()["choices"][0]["message"]["content"]
        
        result_text = re.sub(r"```json\s*", "", result_text)
        result_text = re.sub(r"```\s*", "", result_text)
        
        return json.loads(result_text.strip())
        
    except Exception as e:
        print(f"匹配计算失败: {e}")
        return {"score": 0, "pros": [], "cons": [], "summary": "匹配分析服务暂时不可用。"}