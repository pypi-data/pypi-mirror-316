#coding=utf-8
import os
import time
import pprint
import autogen
from autogen import Cache
#import autogenstudio

import logging as logger

"""
https://zhuanlan.zhihu.com/p/705964550
"""

#配置大模型
llm_proxy_config = {
    "config_list": [
        {
        #"model": "gpt-4",
        "model":"qwen-turbo",
        "api_key": "sk-IND5uEfmsC2g8SK24b1892C1De0d4a3e9e4a5a293e365bF8",
        "base_url":"http://ai.imiyoo.com/",
        "cache_seed": 42,
        }
    ],
}

llm_config = {
    "config_list": [
        {
        "model":"qwen-turbo",
        "api_key": "sk-a44fabdf02834335a70b9c9c0ba8d539",
        "base_url":"https://dashscope.aliyuncs.com/compatible-mode/v1",
        "cache_seed": 42,
        "price":[0.0003,0.0006],
        }
    ],
}

# Start logging with logger_type and the filename to log to
logging_session_id = autogen.runtime_logging.start(logger_type="file", config={"filename": "runtime.log"})
print("Logging session ID: " + str(logging_session_id))

"""
创建用户代理
"""
user_proxy = autogen.UserProxyAgent(
    name="用户代理",
    #human_input_mode="NEVER",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "last_n_messages": 10,
        "work_dir": "code",
        "use_docker": False,
    }
)
"""
创建AI助理
"""
engineer = autogen.AssistantAgent(
    name="工程师",
    system_message="""你遵循已批准的计划。你编写 Python 或 Shell 代码来解决任务。
    将代码包裹在一个指定脚本类型的代码块中。用户不能修改你的代码，因此不要建议不完整的代码，这些代码需要他人修改。如果不打算由执行器执行，则不要使用代码块。
    在一个回应中不要包含多个代码块。不要要求其他人复制和粘贴结果。检查执行器返回的执行结果。
    如果结果显示存在错误，请修复错误并再次输出代码。建议完整的代码而不是部分代码或代码更改。
    如果无法修复错误，或者即使代码成功执行后任务仍未解决，请分析问题，重新审视你的假设，收集你需要的额外信息，并考虑尝试不同的方法。
""",
)

planner = autogen.AssistantAgent(
    name="规划者",
    system_message="""提出一个计划。根据管理员和批评者的反馈修订计划，直到获得管理员的批准。
该计划可能涉及一名能够编写代码的工程师和一名不编写代码的科学家。
首先解释计划。明确哪些步骤是由工程师执行的，哪些步骤是由科学家执行的。
""",
)

executor = autogen.UserProxyAgent(
    name="执行者",
    system_message="执行工程师编写的代码并报告结果。",
    human_input_mode="NEVER",
    code_execution_config={
        "last_n_messages": 3,
        "work_dir": "code",
        "use_docker": False,
    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
)

critic = autogen.AssistantAgent(
    name="批评者",
    system_message="仔细检查其他代理提出的计划、声明和代码，并提供反馈。检查计划是否包括添加可验证的信息，例如来源URL。",
)

groupchat = autogen.GroupChat(
    agents=[user_proxy, engineer, planner, executor, critic], messages=[], max_round=10
)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

"""
发起对话
"""
"""
序列化任务
chat_results = autogen.initiate_chats(
    [
        {
            "sender":user_proxy,
            "recipient": pentest_assitant,
            "message": pentest_tasks[0],
            "clear_history": True,
            "summary_method":"last_msg",
        },
    ]
)
"""
from autogen import register_function

def read_file(filename: str):
    with open(filename, 'r', encoding='utf-8') as file:
        # 读取整个文件内容
        content = file.read()
        return content

import sys
root_dir = "/Users/yixin/workplace/yxwork/ktool/"
sys.path.append(root_dir)
import ktool
import inspect

ktool.base_http_api_url="http://192.168.216.148:8091/console/api/v1"
ktool.api_key="6900ef3b-445d-4656-8a2e-2afba72a6a45"


#ktool.Agent.role("渗透测试专家")


#ktool.api_key="6900ef3b-445d-4656-8a2e-2afba72a6a45"
tool = ktool.FunctionCall.create_tool(tool_name="nmap")
print(tool)
#获取函数参数
print(inspect.signature(tool.get("tool_func")))

#role_pentest = read_file("渗透测试专家.md")


tasks=[
    """请对www.baidu.com进行端口扫描""",
]

assistant = autogen.AssistantAgent(
    name="渗透测试专家",
    #system_message=role_pentest,
    llm_config=llm_config
    )

register_function(
    f=tool.get("tool_func"),
    description=tool.get("tool_desc"),
    caller=assistant,
    executor=user_proxy,
)

# reset the assistant. Always reset the assistant before starting a new conversation.
assistant.reset()

#assitant_msg = {"role": "assistant", "content": "hello"}
#assistant.send(assitant_msg,user_proxy)


def custome_before_message_func(sender, message,recipient,silent):
    chat_message = {}
    chat_message["sender"] = sender.name
    chat_message["recipient"] = recipient.name
    chat_message["content"] = message
    chat_message["silent"] = silent
    chat_message["create_at"] = int(time.time())
    return message

#user_proxy.register_hook("process_message_before_send",custome_before_message_func)
#assistant.register_hook("process_message_before_send",custome_before_message_func)


chat_result = user_proxy.initiate_chat(assistant,message=tasks[0])
print(chat_result.cost)

#with Cache.redis(redis_url="redis://:difyai123456@localhost:6379/0") as cache:
    #chat_result = user_proxy.initiate_chat(assistant,message=tasks[0],cache=cache,silent=True)
    #pprint.pprint(chat_result.chat_history)
    #pprint.pprint(chat_result.cost)

