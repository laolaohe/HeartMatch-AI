# HeartMatch AI
💖 HeartMatch-AI：基于大模型的深度婚恋性格匹配系统 (LLM-as-a-Judge)

📌 项目简介
HeartMatch-AI 是一个探索性的 AI 婚恋匹配 Demo。传统的交友软件往往依赖浅层的标签（如年龄、收入）或简单的向量检索（Embedding）来进行匹配，难以捕捉到两人在性格互补性、价值观底线、冲突解决方式等深层次的契合度。
本项目打破了传统的“相似度匹配”逻辑，采用了 LLM-as-a-Judge（大模型作为裁判） 的创新架构。通过引导用户进行结构化的“行为式提问”，利用 DeepSeek 大模型对用户的自然语言回答进行深度剖析，提取高维度的性格特征（MBTI、生活习惯、情感需求等），并最终由 LLM 直接对比双方画像，输出详尽的契合度得分、相处优势 (Pros)、潜在挑战 (Cons) 以及针对性的恋爱建议。
✨ 核心功能与亮点
🧠 深度用户画像抽取 (Profile Extraction)：
不再依赖用户枯燥地勾选表单，而是通过情境化、行为化的开放式问题（如冲突处理方式、理想周末安排），利用 LLM 的阅读理解能力，自动提取出包含 11 个维度的结构化 JSON 画像（性格、兴趣、社交偏好、雷区等）。
⚖️ 突破向量检索的 LLM 裁判机制 (LLM-as-a-Judge)：
放弃了传统的文本 Embedding 相似度计算（因为性格相似不代表适合在一起，互补往往更重要）。直接让大模型扮演“心理学+社交分析专家”，综合评估两人的“相似性”与“互补性”。
📊 细粒度、结构化的输出控制：
利用了 DeepSeek API 的 response_format: json_object 特性，并通过正则清理、异常回退等机制，确保 LLM 稳定输出可供程序解析的结构化数据，极大提升了系统的鲁棒性。
📝 自动化匹配报告生成 (Local Record Management)：
每次匹配结束后，系统会自动将双方画像及详细的匹配分析（得分、Pros、Cons、AI寄语）打包保存为带时间戳的 .txt 报告，便于后续的产品化扩展（如生成 PDF 发送给用户）。
🛠️ 技术栈与架构设计
语言: Python 3.8+
大模型服务: DeepSeek Chat API (deepseek-chat 模型)
核心库: requests (API 调用), json (数据解析), re (数据清洗)


架构流转图:
Mermaid
graph LR
A[用户基础信息+开放式问答] -->|Prompt Engineering| B(LLM 画像抽取分析)
B -->|正则清洗+JSON解析| 
C[标准化文本画像 Profile_Text]
D[数据库目标用户画像] --> E(LLM-as-a-Judge 匹配打分)
C --> E
E -->|结构化输出| F[生成匹配分数、Pros、Cons]
F --> G[持久化保存为 TXT 报告]
(注：如果你的 GitHub 不支持 Mermaid 渲染，可以把上面这段流程用文字或截图替代)

🚀 快速开始 (Quick Start)

1. 克隆项目
git clone (https://github.com/laolaohe/HeartMatch-AI.git)
cd HeartMatch

2. 配置 API Key
本项目依赖 DeepSeek API。请前往 DeepSeek 开放平台 申请 API Key。
出于安全考虑，请不要将 Key 硬编码在代码中。建议通过环境变量配置：
Windows:
code
Cmd
set DEEPSEEK_API_KEY=你的_API_KEY
Mac/Linux:
code
Bash
export DEEPSEEK_API_KEY="你的_API_KEY"
(或者，你也可以在本地测试时临时在 llm_analysis.py 和 matchmaker.py 中替换为你的真实 Key，但切记不要提交到公共仓库)

3. 运行程序
code
Bash
python main.py

4. 体验流程
根据终端提示，输入你的基本信息和情境问答。
程序会自动分析你的性格，并生成结构化画像。
程序会拉取预设的虚拟人物（如：热情阳光的 ENFP “李雷”）与你进行深度匹配。
匹配完成后，可在项目根目录下的 records 文件夹中查看生成的完整 .txt 匹配报告。

🔍 项目难点与踩坑记录
LLM 输出不稳定导致 JSON 解析崩溃的问题：
痛点： 即使在 Prompt 里强调了输出 JSON，大模型依然习惯性地在输出前后包裹 Markdown 代码块（如 ```json），导致 Python 的 json.loads() 抛出异常。
解决方案： 除了启用官方的 response_format: {"type": "json_object"} 外，我在代码中加入了正则清洗逻辑 (re.sub)，强制剥离多余符号；并增加了异常捕获与回退机制，确保哪怕解析彻底失败，系统也能保留原始文本（"raw" 字段）继续流转，不至于引发服务宕机。
为何弃用 Embedding 而转向 LLM 打分？
思考： 在项目初期，我尝试将用户画像转化为纯文本并调用 Embedding API 计算余弦相似度。但在测试中发现，对于婚恋场景，高度相似的向量并不等同于高匹配度（例如两个脾气暴躁的人向量极度相似，但相处起来是灾难）。
迭代： 我果断重构了架构，引入了 matchmaker.py，让 LLM 直接“读懂”两个人的画像，重点分析“互补性”（如一方喜欢倾诉，另一方善于倾听）。这使得系统不仅能给出干瘪的分数，还能输出真实可落地的恋爱建议。
🤝 未来优化方向 (TODO)

前端可视化: 使用 FastAPI + Vue.js 或 Streamlit 将目前的 CLI 界面升级为 Web 交互界面。

数据持久化: 接入 MySQL/PostgreSQL 或 MongoDB 存储真实用户画像。

异步调用优化: 目前两个 LLM 请求是串行同步阻塞的，未来可引入 asyncio 和 aiohttp 减少 API 等待时间。


<img width="1457" height="864" alt="1" src="https://github.com/user-attachments/assets/0352b5bc-2d41-4f24-95c1-c68059b05b28" /><img width="1494" height="406" alt="屏幕截图 2026-03-10 130300" src="https://github.com/user-attachments/assets/2422a2a8-f54b-4d51-9c7e-3045264da8da" />


<img width="1259" height="700" alt="屏幕截图 2026-03-10 130251" src="https://github.com/user-attachments/assets/b107ad5d-ead9-4f07-bd57-d2140552bfe9" />

