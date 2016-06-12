# https://pythonhosted.org/setuptools/setuptools.html#namespace-packages
__import__('pkg_resources').declare_namespace(__name__)

def escape(str):

    # If you need to use any of the characters which function as operators in
    # your query itself (and not as operators), then you should escape them
    # with a leading backslash. For instance, to search for (1+1)=2, you would
    # need to write your query as \(1\+1\)\=2.
    #
    # The reserved characters are: + - = && || > < ! ( ) { } [ ] ^ " ~ * ? : \ /
    #
    # Failing to escape these special characters correctly could lead to a
    # syntax error which prevents your query from running.
    #
    # A space may also be a reserved character. For instance, if you have a
    # synonym list which converts "wi fi" to "wifi", a query_string search for
    # "wi fi" would fail. The query string parser would interpret your query
    # as a search for "wi OR fi", while the token stored in your index is
    # actually "wifi". Escaping the space will protect it from being touched
    # by the query string parser: "wi\ fi"
    #
    # https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html
    
    # note the absence of "&" and "|" which are handled separately
    
    to_escape = [
        "+", "-", "=", ">", "<", "!", "(", ")", "{", "}", "[", "]", "^", '"', "~", "*", "?", ":", "\\", "/"
    ]
    
    escaped = []
    
    unistr = str.decode("utf-8")
    length = len(unistr)
    
    i = 0
    
    while i < length:
        
        char = unistr[i]
        
        if char in to_escape:
            char = "\%s" % char
            
        elif char in ("&", "|"):
            
            if (i + 1) < length and unistr[ i + 1 ] == char:
                char = "\%s" % char

        else:
            pass

        escaped.append(char)
        i += 1

    return "".join(escaped)
