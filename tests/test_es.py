import pymongo
import elasticsearch
from pprint import pprint
import time

# client = pymongo.MongoClient()
# client.drop_database('boleplusdb')
# print("Drop database <boleplusdb> ")
# time.sleep(0.5)

es = elasticsearch.Elasticsearch()
# company_id = 10086
# es.delete_by_query(
#     index="profiles", doc_type=str(company_id),
#     body={
#         "query":
#             {
#                 "match_all": {}
#             }
#     }
# )
#
# print("delete es <profiles/10086> ")
r = es.indices.analyze(
    index="profiles",
    body="NVIDIA and AMD Video Card master 招聘 嵌入式软件工程师",
    analyzer="max_word",
    pretty=True
)
pprint(r)
y= []
for x in r['tokens']:
    t=x['token']
    y.append(t)

print(y)