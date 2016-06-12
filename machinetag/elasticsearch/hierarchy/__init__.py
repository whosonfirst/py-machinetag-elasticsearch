# https://pythonhosted.org/setuptools/setuptools.html#namespace-packages
__import__('pkg_resources').declare_namespace(__name__)

import machinetag.elasticsearch

def query_filters(**kwargs):

    # https://stackoverflow.com/questions/24819234/elasticsearch-using-the-path-hierarchy-tokenizer-to-access-different-level-of
    # https://www.elastic.co/guide/en/elasticsearch/reference/1.7/search-aggregations-bucket-terms-aggregation.html
    # https://github.com/whosonfirst/py-mapzen-whosonfirst-machinetag/blob/master/mapzen/whosonfirst/machinetag/__init__.py

    # these are used to prune the initial ES dataset

    rsp_filter = None

    # these are appended to aggrs['hierarchies']['terms']

    include_filter = None
    exclude_filter = None

    if kwargs.get('filter', False) == 'namespaces':

        rsp_filter = query_filter_namespaces

        # all the namespaces for a predicate and value

        if kwargs.get('predicate', None) and kwargs.get('value', None):

            esc_pred = machinetag.elasticsearch.escape(kwargs['predicate'])
            esc_value = machinetag.elasticsearch.escape(kwargs['value'])

            # include_filter = '.*\.' + esc_pred + '\.' + esc_value + '$'
            include_filter = '.*\/' + esc_pred + '\/' + esc_value + '$'

        # all the namespaces for a predicate

        elif kwargs.get('predicate', None):

            esc_pred = machinetag.elasticsearch.escape(kwargs['predicate'])

            # include_filter = '^.*\.' + esc_pred
            # exclude_filter = '.*\/.*\/.*'

            include_filter = '^.*\/' + esc_pred
            exclude_filter = '.*\/.*\/.*'

        # all the namespaces for a value 
            
        elif kwargs.get('value', None):

            esc_value = machinetag.elasticsearch.escape(kwargs['value'])

            # include_filter = '.*\..*\.' + esc_value + '$'
            include_filter = '.*\/.*\/' + esc_value + '$'

        # all the namespaces
        
        else:

            # exclude_filter = '.*\..*'
            exclude_filter = '.*\/.*'

    elif kwargs.get('filter', None) == 'predicates':

        rsp_filter = query_filter_predicates

        # all the predicates for a namespace and value

        if kwargs.get('namespace', None) and kwargs.get('value', None):

            esc_ns = machinetag.elasticsearch.escape(kwargs['namespace'])
            esc_value = machinetag.elasticsearch.escape(kwargs['value'])

            # include_filter = '^' + esc_ns + '\..*\.' + esc_value + '$'
            include_filter = '^' + esc_ns + '\/.*\.' + esc_value + '$'

        # all the predicates for a namespace

        elif kwargs.get('namespace', None):

            esc_ns = machinetag.elasticsearch.escape(kwargs['namespace'])

            # include_filter = '^' + esc_ns + '\.[^\.]+'
            # exclude_filter = '.*\..*\..*'

            include_filter = '^' + esc_ns + '\/[^\/]+'
            exclude_filter = '.*\/.*\/.*'

        # all the predicates for a value

        elif kwargs.get('value', None):

            esc_value = machinetag.elasticsearch.escape(kwargs['value'])

            # include_filter = '.*\..*\.' + esc_value + '$'
            include_filter = '.*\/.*\/' + esc_value + '$'
            
        # all the predicates

        else:

            # include_filter = '.*\..*'
            # exclude_filter = '.*\..*\..*'

            include_filter = '.*\/.*'
            exclude_filter = '.*\/.*\/.*'
        
    elif kwargs.get('filter', None) == 'values':

        rsp_filter = query_filter_values

        # all the values for namespace and predicate

        if kwargs.get('namespace', None) and kwargs.get('predicate', None):

            esc_ns = machinetag.elasticsearch.escape(kwargs['namespace'])
            esc_pred = machinetag.elasticsearch.escape(kwargs['predicate'])

            include_filter = '^' + esc_ns + '\.' + esc_pred + '\..*'

        # all the values for a namespace

        elif kwargs.get('namespace', None):

            esc_ns = machinetag.elasticsearch.escape(kwargs['namespace'])

            # include_filter = '^' + esc_ns + '\..*\..*'
            include_filter = '^' + esc_ns + '\/.*\/.*'

        # all the values for a predicate
    
        elif kwargs.get('predicate', None):
            
            esc_pred = machinetag.elasticsearch.escape(kwargs['predicate'])

            # include_filter = '^.*\.' + esc_pred + '\..*'
            include_filter = '^.*\/' + esc_pred + '\/.*'

        # all the values

        else:

            # include_filter = '.*\..*\..*'
            include_filter = '.*\./*\/.*'

    else:
        pass

    return include_filter, exclude_filter, rsp_filter

def sort_filtered(raw):

    sorted = []
    tmp = {}
    
    for b in raw:
        key = b['key']
        count = b['doc_count']
        
        bucket = tmp.get(count, [])
        bucket.append(key)
        
        tmp[count] = bucket
        
    counts = tmp.keys()
    counts.sort()
    counts.reverse()

    for count in counts:
        for key in tmp[count]:
            sorted.append({'doc_count': count, 'key': key })

    return sorted

def query_filter_namespaces(raw):

    filtered = []
    tmp = {}

    predicates = {}
    values = {}

    for b in raw:
        key = b['key']
        count = b['doc_count']

        key = key.split(".")
        ns = key[0]

        total = tmp.get(ns, 0)
        total += count
        
        tmp[ns] = total
        
    for pred, count in tmp.items():
        filtered.append({'doc_count': count, 'key': pred})
        
    return sort_filtered(filtered)

def query_filter_predicates(raw):

    filtered = []
    tmp = {}

    for b in raw:
        key = b['key']
        count = b['doc_count']

        key = key.split(".")
        pred = key[1]

        total = tmp.get(pred, 0)
        total += count

        tmp[pred] = total

    for pred, count in tmp.items():
        filtered.append({'doc_count': count, 'key': pred})
        
    return sort_filtered(filtered)

def query_filter_values(raw):

    filtered = []
    tmp = {}

    for b in raw:
        key = b['key']
        count = b['doc_count']
        
        key = key.split(".")
        value = key[2]

        total = tmp.get(value, 0)
        total += count

        tmp[value] = total

    for pred, count in tmp.items():
        filtered.append({'doc_count': count, 'key': pred})

    return sort_filtered(filtered)
