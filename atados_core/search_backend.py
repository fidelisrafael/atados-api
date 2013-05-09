from haystack.backends.solr_backend import SearchBackend as SolrBackend, SearchQuery as SolrQuery
from haystack.backends import log_query


BACKEND_NAME = 'search'

class SearchBackend(SolrBackend):

    @log_query
    def search(self, *args, **kwargs):
        def exdt(facet_field):
            return '{!ex=%(facet_field)s}%(facet_field)s' % {'facet_field': facet_field}
        if 'facets' in kwargs:
            kwargs['facets'] = map(exdt, kwargs['facets'])
        return super(SearchBackend, self).search(*args, **kwargs)

class SearchQuery(SolrQuery):

    def __init__(self, site=None, backend=None):
        backend = SearchBackend(site=site)
        super(SearchQuery, self).__init__(site, backend)

    def add_narrow_query(self, query):
        name, value = query.split(':')
        super(SearchQuery, self).add_narrow_query('{!tag=%s}%s' % (name, query))
