# llm_analysis.py
import json
import requests
import re  

DEEPSEEK_API_KEY = "your API_KEY" 
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"

def analyze_user_profile(user):
    """
    输入 UserProfile 对象
    输出 扩展版 JSON 用户画像
    """
    # 拼接用户基本信息 + 回答
    basic_info = f"姓名: {user.name}\n年龄: {user.age}\n性别: {user.gender}\nMBTI: {user.mbti}\n星座: {user.zodiac}"
    answers_text = "\n".join([f"{q}: {a}" for q, a in user.answers.items()])
#角色设定prompt
    prompt = f"""
你是心理学+社交分析专家。
用户基本信息：
{basic_info}

用户回答：
{answers_text}

请根据用户回答及基本信息，分析以下维度：
- 性格 (personality)
- 兴趣 (interests)
- 价值观 (values)
- 生活习惯 (lifestyle)
- 社交偏好 (social_preference)
- 情绪倾向 (emotion_tendency)
- 学习/工作风格 (work_study_style)
- 幽默感/聊天风格 (humor_chat_style)
- 目标/追求 (goals)
- 偏好话题 (favorite_topics)
- 约会/恋爱风格 (dating_style)

输出 JSON 格式，确保每个字段都是数组。不要输出任何多余的解释文字。
"""

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",  
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "response_format": {"type": "json_object"} 
    }

    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"DeepSeek API请求失败: {response.status_code} {response.text}")

    result_text = response.json()["choices"][0]["message"]["content"]

    
    result_text = re.sub(r"```json\s*", "", result_text)
    result_text = re.sub(r"```\s*", "", result_text)
    result_text = result_text.strip()

    
    try:
        result_json = json.loads(result_text)
    except json.JSONDecodeError as e:
        print(f"\n[警告] JSON 解析失败: {e}\n模型原始输出: {result_text}\n") 
        result_json = {
            "personality": [],
            "interests": [],
            "values": [],
            "lifestyle": [],
            "social_preference": [],
            "emotion_tendency": [],
            "work_study_style": [],
            "humor_chat_style": [],
            "goals": [],
            "favorite_topics": [],
            "dating_style": [],
            "raw": result_text
        }

    return result_json