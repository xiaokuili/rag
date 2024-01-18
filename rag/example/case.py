
import sys 
sys.path.append("/workspaces/rag/rag")
from demo import generator
def pprint(paths, query):
    print("[query]", query)
    print("[paths]", paths)

    rst = generator(paths, query)
    print("[generator]", rst)
# case1  基于新闻分析招商线索
# 向量库增长测试
case1 = {
    "paths": ["/workspaces/rag/rag/data/policy2.md","/workspaces/rag/rag/data/policy1.md"],
    "query": "四川在发展什么产业"
}

# case2 基于产业信息分析招商企业
# 从本地获取   
# 归一化 ， 
case2 = {
    "paths": ["/workspaces/rag/rag/data/company1.md"],
    "query": "给我大飞机产业的企业名称"
}

# 给我推荐四川可以进行招商的企业名称



# run 
pprint(**case1)
# pprint(**case2)

