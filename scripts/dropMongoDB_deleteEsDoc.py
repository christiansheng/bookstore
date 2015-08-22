import pymongo
import elasticsearch
import time

client = pymongo.MongoClient()
r = client.drop_database('xxx')
print("\nDrop database <xxxb> start ! ")
print("\t" + str(r))
print("Drop database <xxx> done ! ")
time.sleep(0.5)

es = elasticsearch.Elasticsearch()
company_id = 10086
r = es.delete_by_query(
    index="profiles", doc_type=str(company_id),
    body={
        "query":
            {
                "match_all": {}
            }
    }
)
print("\ndelete es  start !")
print("\t" + str(r))
print("delete es  done !")
