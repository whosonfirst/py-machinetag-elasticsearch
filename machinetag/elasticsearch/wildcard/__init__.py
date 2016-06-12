# https://pythonhosted.org/setuptools/setuptools.html#namespace-packages
__import__('pkg_resources').declare_namespace(__name__)

import machinetag
import machinetag.elasticsearch

def query_filter_from_string(str_mt, **kwargs):

    mt = machinetag.from_string(str_mt, allow_wildcards=True)
        
    if not mt.is_machinetag():
        return None

    ns = mt.namespace()
    pred = mt.predicate()
    value = mt.value()
    
    esc_ns = None
    esc_pred = None
    esc_value = None
    
    if ns:
        esc_ns = machinetag.elasticsearch.escape(ns)
        
    if pred:
        esc_pred = machinetag.elasticsearch.escape(pred)
        
    if value:
        esc_value = machinetag.elasticsearch.escape(value)
        
    query_filter = None

    # https://www.elastic.co/guide/en/elasticsearch/reference/1.7/query-dsl-regexp-query.html#regexp-syntax
    
    if ns != None and pred != None and value != None:
        
        # is machine tag
        # query_filter = esc_ns + '\.' + esc_pred + '\.' + esc_value
        query_filter = esc_ns + '\/' + esc_pred + '\/' + esc_value
        
    elif ns != None and pred == None and value == None:
        
        # sg:*=
        # query_filter = esc_ns + '\..*\\.*'
        query_filter = esc_ns + '\/[^\/]+\/.*'
        
    elif ns != None and pred != None and value == None:

        # sg:services=
        # query_filter = esc_ns + '\.' + esc_pred + '\..*'
        query_filter = esc_ns + '\/' + esc_pred + '\/.*'
                
    elif ns != None and pred == None and value != None:

        # sg:*=personal
        # query_filter = esc_ns + '\.[^\.]+\.' + esc_value
        query_filter = esc_ns + '\/[^\/]+\/' + esc_value

    elif ns == None and pred != None and value != None:

        # *:services=personal
        # query_filter = '[^\.]+\.' + esc_pred + '\.' + esc_value
        query_filter = '[^\/]+\.' + esc_pred + '\/' + esc_value
        
    elif ns == None and pred != None and value == None:
            
        # *:services=
        # query_filter = '[^\.]+\.' + esc_pred + '\..*'
        query_filter = '[^\/]+\/' + esc_pred + '\/.*'

    elif ns == None and pred == None and value != None:
        
        # *:*=personal
        # query_filter = '[^\.]+\.[^\.]+\.' + esc_value
        query_filter = '[^\/]+\/[^\/]+\/' + esc_value

    else:
        # WTF?
        pass

    return query_filter

