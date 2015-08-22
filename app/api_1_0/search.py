import elasticsearch
from ..models.mongo import MongoInstance
from . import api
from flask import jsonify, request
from pprint import pprint

import math


# Todo: it is just a draft
@api.route('/search', methods=['get'])
def search():
    try:
        es = elasticsearch.Elasticsearch()
    except Exception as ex:
        print(ex)
    keywords = request.args.get('keywords', '')
    print(keywords)
    index_name = "bookstore"
    type_name = "books"
    analyze_result = es.indices.analyze(
        index=index_name,
        body=keywords,
        analyzer="ik_smart"
    )
    keywords_tokens = []
    for item in analyze_result['tokens']:
        token = item['token']
        keywords_tokens.append(token)

    print(keywords_tokens)
    lkt = (len(keywords_tokens))
    if lkt <= 2:
        min_match = 1
    elif 2 < lkt < 6:
        min_match = math.ceil(lkt / 2.0)
    else:
        min_match = math.floor(lkt * 2 / 3.0)

    body = {
        "fields": ["name", "press", "author", "keywords"],
        "query": {
            "terms": {
                "_all": keywords_tokens,
                "minimum_match": min_match
            }
        }
    }
    body1 = {
        "fields": ["name", "press", "author", "keywords"],
        "query": {
            "terms": {
                "_all": keywords_tokens,
                "minimum_match": min_match
            }
        },
        "filter": {
            "bool": {
                "must": {
                    "term": {
                        "press": "人民"
                    }
                }
            }

        }
    }
    body2 = {
        "fields": ["name", "press", "author", "keywords"],
        "query": {
            "terms": {
                "_all": keywords_tokens,
                "minimum_match": min_match
            }
        },
        "filter": {
            "and": [
                {
                    "term": {"press": "人民"}
                },
                {
                    "term": {"name": "linux"}
                }
            ]
        }
    }

    body3 = {
        "fields": ["name", "press", "author", "keywords", "year"],
        "query": {
            "terms": {
                "_all": keywords_tokens,
                "minimum_match": min_match
            }
        },
        # "filter": {
        #     "and": [
        #         {
        #             "term": {"press": "出版社"}
        #         },
        #         {
        #             "term": {"year": "2012"}
        #         }
        #     ]
        # },
        "aggs":{
            "year_agg": {
                "terms": {
                    "field": "year"
                }
            },
            "press_agg": {
                "terms": {
                    "field": "press_id"
                }
            }
        }
    }
    body4 = {
        "fields": ["name", "press", "author", "keywords", "year"],
        "query": {
            "terms": {
                "_all": keywords_tokens,
                "minimum_match": min_match
            }
        },
        "filter": {
            "and": [
                {
                    "term": {"year": 2011}
                }
            ]
        },
        "aggs":{
            "year_agg": {
                "terms": {
                    "field": "year"
                }
            },
            "press_agg": {
                "terms": {
                    "field": "press_id"
                }
            }
        }
    }

    body4 = {
        "fields": ["name", "press", "author", "keywords", "year"],

        "query": {
            "filtered":{
                "query":{
                    "terms": {
                        "_all": keywords_tokens,
                        "minimum_match": min_match
                    }
                },
                "filter": {
                    "and": [
                        {
                            "term": {"year": 2011}
                        },
                        {
                            "term": {"press": "出版社"}
                        }
                    ]
                }
            }
        },

        "aggs":{
            "year_agg": {
                "terms": {
                    "field": "year"
                }
            },
            "press_agg": {
                "terms": {
                    "field": "press_id"
                }
            }
        }
    }
    print(min_match)
    try:
        search_result = es.search(
            index=index_name, doc_type=type_name,
            body=body4
            # explain=True
        )
    except Exception as ex:
        print(ex)
        return jsonify({'result': False}), 500

    print(search_result["hits"]["total"])
    return jsonify({'result': True, 'data': search_result})
