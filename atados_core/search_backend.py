from haystack.backends.solr_backend import SolrSearchBackend, SolrSearchQuery
from haystack.backends import BaseEngine, log_query

# TODO(mpomarole): Replace Solr backend to ElasticSearch

class SearchBackend(SolrSearchBackend):

    @log_query
    def search(self, *args, **kwargs):
        def exdt(facet_field):
            return '{!ex=%(facet_field)s}%(facet_field)s' % {'facet_field': facet_field}
        if 'facets' in kwargs:
            kwargs['facets'] = map(exdt, kwargs['facets'])
        return super(SearchBackend, self).search(*args, **kwargs)

class SearchQuery(SolrSearchQuery):

    def __init__(self, site=None, backend=None):
        backend = SearchBackend(site=site)
        super(SearchQuery, self).__init__(site, backend)

    def add_narrow_query(self, query):
        name, value = query.split(':')
        super(SearchQuery, self).add_narrow_query('{!tag=%s}%s' % (name, query))

class SearchEngine(BaseEngine):
    backend = SearchBackend
    query = SearchQuery
