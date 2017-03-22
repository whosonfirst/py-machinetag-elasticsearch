# py-machinetag-elasticsearch

Python libraries for working with machinetags in Elasticsearch

## Install

```
sudo pip install -r requirements.txt .
```

## Usage

Too soon.

## Elasticsearch

### Mappings

```
{
  "settings": {
    "analysis": {
      "analyzer": {
        "machinetag-path-analyzer": {
          "type": "custom",
          "tokenizer": "machinetag-path-tokenizer"
        }
      },
      "tokenizer": {
        "machinetag-path-tokenizer": {
          "type": "path_hierarchy",
          "delimiter": "/"
        }
      }
    }
  },
  "mappings" : {
    "_default_": {
	"properties" : {
	    "categories_all": {
		"type" : "string",
		"index_analyzer": "machinetag-path-analyzer",
		"search_analyzer": "keyword"
	    },
	    "machinetags_all": {
		"type" : "string",
		"index_analyzer": "machinetag-path-analyzer",
		"search_analyzer": "keyword"
	    },
	    "wof:categories": {
		"type" : "string",
		"index_analyzer": "machinetag-path-analyzer",
		"search_analyzer": "keyword",
		"copy_to": "categories_all",
		"copy_to": "machinetags_all"
	    }
	}
    }
  }
}
```
