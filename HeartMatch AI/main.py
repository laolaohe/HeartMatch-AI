# main.py
from user_profile import UserProfile
from llm_analysis import analyze_user_profile
from matchmaker import calculate_match 
from record_manager import save_match_record 

def profile_to_text(profile_json: dict) -> str:
    text = ""
    for key, values in profile_json.items():
        if key == "raw": continue
        if isinstance(values, list) and len(values) > 0:
            text += f"{key}: {', '.join(values)}\n"
        elif isinstance(values, str) and values.strip():
            text += f"{key}: {values.strip()}\n"
    return text.strip()

def collect_basic_info():
    name = input("你的名字: ")
    age = input("年龄: ")
    gender = input("性别: ")
    mbti = input("MBTI类型（如INTJ）: ")
    zodiac = input("星座: ")
    return UserProfile(name, age, gender, mbti, zodiac)

def collect_free_answers(user):
    questions = [
                
        "【生活方式】抛开工作和压力，你理想中完美的周末一天是怎么度过的？（越具体越好，比如：睡到自然醒点个辣外卖、和朋友去山里徒步、在咖啡馆看一天书等）",
        
        
        "【社交画像】在朋友聚会或团队中，你通常扮演什么样的角色？（比如：活跃气氛的显眼包、默默倾听的树洞、负责做攻略拿主意的大佬）",
        
        
        "【价值底线】在人际交往或恋爱中，对方的什么行为会瞬间踩到你的“雷区”，让你立刻下头？",
        
        
        "【冲突应对】如果你们因为意见不合发生激烈争吵，你习惯的处理方式是什么？（比如：需要独处冷静一晚、必须当天当面辩论清楚、习惯先服软哄人等）",
        
        
        "【情感需求】在感情里，你更希望伴侣多给你哪方面的反馈？是情绪上的陪伴安慰，还是实际生活中的规划和解决问题？"
    ]
    print("\n请回答以下问题：\n")
    for q in questions:
        ans = input(q + "\n> ")
        user.add_answer(q, ans)

def main():
    print("欢迎使用 HeartMatch AI 用户数据收集 Demo！\n")

    current_user = collect_basic_info()
    collect_free_answers(current_user)

    print("\n=== 正在生成你的 AI 深度画像，请稍候... ===")
    
    current_user_analysis = analyze_user_profile(current_user)
    current_user_text = profile_to_text(current_user_analysis)
    
    print("\n你的画像标签提取完毕！")
    print(current_user_text)

    # 模拟匹配环节 (这里我们直接虚构一个数据库里的异性/同性)
    # 实际项目中，你会从数据库中拉取另一个人的 profile_text

    target_profile_text = """
    姓名: 何姥姥
    性别: 男
    MBTI: ENFJ
    性格: 阳光开朗, 目标导向型，探索型人格，焦虑型成长人格
    兴趣: F1, 看电影，听音乐，各种运动
    价值观: 自由至上,快乐至上
    生活习惯: 晚睡晚起, 周末喜欢往外跑，有时候也喜欢当宅男
    恋爱风格: 慢热型选手
    对伴侣看重的品质: 温柔, 善良，能包容
    """

    print("\n=== 正在为你匹配数据库中的最佳人选，请稍候... ===")
    
    # 匹配打分
    match_result = calculate_match(current_user_text, target_profile_text)

    # 匹配结果
    print("\n❤️❤️ 匹配报告出炉 ❤️❤️")
    print(f"匹配对象：何姥姥")
    print(f"契合度得分：【{match_result.get('score', 0)} 分】")
    
    print("\n✅ 匹配优势 (Pros):")
    for p in match_result.get('pros', []):
        print(f" - {p}")
        
    print("\n⚠️ 潜在挑战 (Cons):")
    for c in match_result.get('cons', []):
        print(f" - {c}")
        
    print("\n💌 AI 寄语:")
    print(f" {match_result.get('summary', '')}")

    # 保存匹配记录
    
    print("\n=== 正在保存报告到本地... ===")
    saved_path = save_match_record(
        current_user_name=current_user.name, 
        current_user_text=current_user_text, 
        target_name="何姥姥", 
        target_profile_text=target_profile_text, 
        match_result=match_result
    )
    
    if saved_path:
        print(f"✅ 报告已成功保存至: {saved_path}")
        print("快去文件夹里看看吧！")

if __name__ == "__main__":
    main()

