import elasticsearch
import time

es = elasticsearch.Elasticsearch()
index_name = "bookstore"
type_name = "books"
try:
    es.indices.delete(index_name)
    es.cluster.health(wait_for_status="yellow")
    es.indices.delete_mapping(index_name, type_name)
    es.cluster.health(wait_for_status="yellow")
except Exception as ex:
    print("index not exists")

mapping_body = {
    "books": {
        "_source": {
            "enabled": True
        },
        "_all": {
            "enabled": True,
            "index_analyzer": "ik",
            "search_analyzer": "ik",
            "term_vector": "no",
            "store": "false"
        },
        "index_analyzer": "ik",
        "search_analyzer": "ik",
        "dynamic": True,
        "dynamic_templates": [
            {
                "string_analyze_template": {
                    "match": "*",
                    "match_mapping_type": "string",
                    "mapping": {
                        "type": "multi_field",
                        "fields": {
                            "{name}": {"type": "{dynamic_type}", "index": "analyzed"},
                            "Raw": {"type": "{dynamic_type}", "index": "not_analyzed"}
                        }
                    }
                }
            }
        ]
    }
}
es.indices.create(index_name)
es.cluster.health(wait_for_status="yellow")
r = es.indices.put_mapping(index=index_name, doc_type=type_name, body=mapping_body)
es.cluster.health(wait_for_status="yellow")

time.sleep(0.5)
print(r)
print("set mapping bookstore/books in ES !")
