# record_manager.py
import os
from datetime import datetime

def save_match_record(current_user_name, current_user_text, target_name, target_profile_text, match_result):
    """
    将匹配记录保存到本地 TXT 文件中
    """
    record_dir = "records"
    if not os.path.exists(record_dir):
        os.makedirs(record_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"匹配记录_{current_user_name}_vs_{target_name}_{timestamp}.txt"
    filepath = os.path.join(record_dir, filename)

    display_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report_content = f"""=========================================
HeartMatchAI 深度婚恋匹配报告
生成时间: {display_time}
=========================================

👩‍💼 【当前用户画像】
{current_user_text}

-----------------------------------------
🧑‍💼 【匹配对象画像】
{target_profile_text.strip()}

=========================================
❤️❤️ 【AI 匹配分析报告】 ❤️❤️
匹配对象：{target_name}
契合度得分：【{match_result.get('score', 0)} 分】

✅ 匹配优势 (Pros):
"""
    for p in match_result.get('pros', []):
        report_content += f" - {p}\n"

    report_content += "\n⚠️ 潜在挑战 (Cons):\n"

    for c in match_result.get('cons', []):
        report_content += f" - {c}\n"

    report_content += f"\n💌 AI 寄语:\n {match_result.get('summary', '')}\n"
    report_content += "=========================================\n"

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(report_content)
        return filepath
    except Exception as e:
        print(f"保存记录失败: {e}")
        return None