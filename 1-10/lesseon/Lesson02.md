---
marp: true
theme: default
header: 'LangGraph 开发课程'
footer: '小马技术 - https://youtube.com/@deeplearncloud'
style: |
  header {
    color: #00ced1;
    font-weight: bold;
    font-size: 18px !important;
  }
  footer {
    color: #50fa7b;
    font-weight: bold;
    font-size: 18px !important;
  }
  footer a {
    font-size: 18px !important;
    color: #009dd5;
  }
  h1 {
    color: #f8f8f2;
    font-size: 64px;
  }
  section {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    background-color: #154360;
    color: #f8f8f2;
    font-size: 24px;
    font-family: Yuanti SC;
  }
  a {
    color: #8be9fd;
  }
  img {
    background-color: transparent!important;
  }
  code {
    font-family: JetBrains Mono;
  }

---
<style scoped>
  section {
    align-items: center;
    justify-content: center;
  }
  h1 {
    color: #f8f8f2;
    font-size: 120px;
    margin: 0;
  }
  h2 {
    margin: 0;
    font-size: 42px;
  }
</style>

![width:300px drop-shadow:0,5px,10px,rgba(f,f,f,.4)](./images/langchain.png)

# LangGraph

## 构建复杂的 AI 应用程序

---
<style scoped>
  section {
    font-size: 40px;
  }
  h1 {
    font-size: 50px;
    color: #f8f8f2;
  }
  li {
    font-family: JetBrains Mono;
    font-size: 32px;
  }
</style>

# :books: 初始化开发环境

操作步骤

+ 建立本地的开发环境
+ 开发测试应用程序

---
<style scoped>
  section {
    align-items: center;
    justify-content: center;
  }
  h1 {
    color: #f8f8f2;
    font-size: 200px;
    margin: 0;
  }
  img {
    border: 10px solid #f8f8f2;
    border-radius: 20%;
    margin: 0;
  }
</style>

![width:200px](../images/step-by-step-operation.webp)

# 操作演示

---
<style scoped>
  h3 {
    margin-top: 0;
  }
</style>
## 课堂实验

### 执行脚本

```bash
$ mkdir lesson_langgraph && cd $_
$ python3 -V
$ python3 -m venv _pvenv_
$ source _pvenv_/bin/activate
$ python3 -m pip install --upgrade pip
```

---
<style scoped>
  h3 {
    margin-top: 0;
  }
</style>
### 安装课程依赖包

```bash
# 安装库
$ pip install \
  langchain==0.2.12 \
  langchain-community==0.2.11 \
  langchain-aws==0.1.16 \
  langchain-openai==0.1.21 \
  langchain-anthropic==0.1.22 \
  langchainhub==0.1.21 \
  langgraph==0.2.4 \
  langsmith==0.1.99 \
  langchain_fireworks==0.1.7 \
  langchain_experimental==0.0.64 \
  langchain-ollama==0.1.1 \
  langchain-chroma==0.1.2 \
  pandas==2.2.2 \
  matplotlib==3.9.1 \
  wikipedia==1.4.0 \
  tavily-python==0.3.7 \
  lxml==5.3.0 \
  python-dotenv==1.0.1
```

---
<style scoped>
  h3 {
    margin-top: 0;
  }
</style>
### 设置环境

```bash
# 生成环境文件
cat << EOF > .env
OPENAI_API_KEY=123
TAVILY_API_KEY=456
ANTHROPIC_API_KEY=789
GOOGLE_API_KEY=XYZ
#LANGCHAIN_TRACING_V2=true
#LANGCHAIN_API_KEY=ABC
#LANGCHAIN_PROJECT=lesson_langgraph
USER_AGENT=Mozilla/5.0
EOF

# 编辑程序
$ nano common.py
$ nano main.py
# 运行程序
$ python main.py
```

---
<style scoped>
  h3 {
    margin-top: 0;
  }
</style>
### common.py

```python
import os
import time
from dotenv import load_dotenv

load_dotenv()  # 读取.env文件

def printENV():
    # 获取所有环境变量
    env_vars = os.environ
    # 打印所有环境变量
    for key, value in env_vars.items():
        if key in ["OPENAI_API_KEY", "TAVILY_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY"]:
            print(f"{key}: {value}")

def evalEndTime(start_time):
    end_time = time.time()  # 获取结束时间
    execution_time = "(程序运行时间：%.2f 秒)" % (
        end_time - start_time
    )  # 计算程序运行时间
    return execution_time
```

---
<style scoped>
  h3 {
    margin-top: 0;
  }
</style>
### main.py

```python
import os, pprint, json, time
from common import *
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

print("=" * 100)

start_time = time.time()  # 获取开始时间

load_dotenv()

printENV()

print(evalEndTime(start_time))
```

---
<style scoped>
  section {
    align-items: center;
    justify-content: center;
  }
  h1 {
    color: #f8f8f2;
    font-size: 200px;
  }
</style>

# 下课时间

