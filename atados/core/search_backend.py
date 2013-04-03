from haystack.backends.solr_backend import SearchBackend as SolrBackend, SearchQuery as SolrQuery
from haystack.backends import log_query


BACKEND_NAME = 'search'

class SearchBackend(SolrBackend):

    @log_query
    def search(self, *args, **kwargs):
        def tagdt(facet_field):
            return '{!tag=dt}' + facet_field
        def exdt(facet_field):
            return '{!ex=dt}' + facet_field
        kwargs['narrow_queries'] = set(map(tagdt, kwargs['narrow_queries']))
        kwargs['facets'] = map(exdt, kwargs['facets'])
        return super(SearchBackend, self).search(*args, **kwargs)

class SearchQuery(SolrQuery):

    def __init__(self, site=None, backend=None):
        backend = SearchBackend(site=site)
        super(SearchQuery, self).__init__(site, backend)
