#用户信息收集 + 数据类
# user_profile.py

class UserProfile:
    def __init__(self, name, age, gender, mbti, zodiac):
        self.name = name
        self.age = age
        self.gender = gender
        self.mbti = mbti
        self.zodiac = zodiac
        self.answers = {} 

    def add_answer(self, question, answer):
        self.answers[question] = answer

    def summary(self):
        """返回用户信息和回答概览"""
        summary = {
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "mbti": self.mbti,
            "zodiac": self.zodiac,
            "answers": self.answers
        }
        return summary