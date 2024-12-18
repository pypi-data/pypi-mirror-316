#coding=utf-8

import sys
root_dir = "/Users/yixin/workplace/yxwork/ktool/"
sys.path.append(root_dir)


import ktoolkits


"""
docker/api/browser/data
FUNCTION_TOOLS=[
    {"tool_name":"子域扫描","tool_func":k_tool_domain,"tool_desc":"可以帮助用户获取域名的子域名信息"},
    {"tool_name":"端口扫描","tool_func":k_tool_nmap,"tool_desc":"可以帮助用户对域名或IP进行端口扫描,并返回开放的端口"},
    {"tool_name":"敏感文件","tool_func":k_tool_dirb,"tool_desc":"可以帮助用户对域名或网站进行敏感文件或目录的检测，并返回敏感文件路径"},
    {"tool_name":"漏洞检测","tool_func":k_tool_nuclei,"tool_desc":"可以帮助用户对域名或网站进行漏洞检测，并返回漏洞结果"}, 
    {"tool_name":"生成报告","tool_func":k_pentest_report,"tool_desc":"可以帮助用户生成渗透测试报告"},  
]
"""

#面向外部开发者
tool_list = [
    {
        "tool_cate":"网络安全",
        "tool_name":"端口扫描",
        "tool_desc":"利用nmap对目标进行端口扫描，并将返回开放的端口信息",
        "tool_func":"k_docker_run",
        "tool_type":"docker",
        "tool_input":{"scan_target":"www.baidu.com"},
        "tool_output":{"code":"","message":"","output":{"tool_output":"###content##"}},
    },
    {
        "tool_cate":"网络安全",
        "tool_name":"安全报告",
        "tool_desc":"根据用户输入的信息，生成相应的渗透测试报告",
        "tool_func":"k_pentest_report",
        "tool_type":"api",
        "tool_input":{"scan_target":"www.baidu.com"},
        "tool_output":{"code":"","message":"","output":{"tool_output":"###content##"}},
    },
    {
        "tool_cate":"网络安全",
        "tool_name":"社交数据",
        "tool_desc":"根据账号、邮箱进行社交数据查询",
        "tool_func":"k_social_search",
        "tool_type":"data",
        "tool_input":{"query":""},
        "tool_output":{"code":"","message":"","output":{"tool_output":"###content##"}},
    }
]


__release_tool__=[
    #{"tool_name":"nmap","tool_args":"www.baidu.com","tool_type":"docker","call_type":"async"},
    {"tool_name":"nmap","tool_args":"www.baidu.com","tool_type":"docker"},
    #{"tool_name":"subfinder","tool_args":"yxqiche.com","tool_type":"docker"},
    #{"tool_name":"k_social_search","tool_args":"imiyoo","tool_type":"data"},
    #{"tool_name":"generate_and_save_pdf","tool_type":"local"}
    #{"tool_name":"generate_and_save_images","tool_type":"local"}
]


#dev
#ktool.base_http_api_url="http://192.168.216.148:8091/console/api/v1"
#ktool.api_key="6900ef3b-445d-4656-8a2e-2afba72a6a45"

#test
#ktool.base_http_api_url="http://192.168.144.96:8091/console/api/v1"
#ktool.api_key="0f74da19-88b6-488d-827b-43b945f49d0d"



#prd
ktoolkits.api_key="6900ef3b-445d-4656-8a2e-2afba72a6a45"

ktoolkits.debug = False

for item in __release_tool__:

    if item.get("tool_type")=="docker":
        #异步调用
        if item.get("call_type",False):
            output = ktoolkits.AsyncRunner.call(
                    tool_name="nmap",
                    tool_input="www.baidu.com",
                )
            print(output)
        else:
            #同步调用
            output = ktoolkits.Runner.call(
                    tool_name=item.get("tool_name"),
                    tool_input=item.get("tool_args"),
                )
            print(output)

    elif item.get("tool_type")=="data":
        output = ktoolkits.Runner.call(
                tool_name=item.get("tool_name"),
                tool_input=item.get("tool_args"),
            )
        print(output)


    elif item.get("tool_type")=="local":
        output = ktoolkits.Runner.call(
                    tool_name="generate_and_save_images",
                    tool_input={"query":"一辆飞驰的跑车"},
                )
        print(output)
        sys.exit()
        output = ktool.Runner.call(
                    tool_name="generate_and_save_pdf",
                    tool_input={
                        "sections": [
                            {
                            "title": "Introduction - Early Life",
                            "level": "h1",
                            "image": "https://picsum.photos/536/354",
                            "content": ("hello,the world"),
                            },
                        ]
                    },
                    tool_type="local",
                )
        print(output)
    
    elif item.get("tool_type")=="api":
        pass

    else:
        print("not support tool type")


sys.exit()
output = ktoolkits.Agent.chat(
        message="请帮我扫描下www.baidu.com"
        )