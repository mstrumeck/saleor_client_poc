from .base_response_builder import BaseResponseBuilder
import itertools


class ManyObjectsResponseBuilder(BaseResponseBuilder):
    def __init__(self, saleor_url, saleor_auth_token, type_of_object, query_input=None):
        if not query_input:
            query_input = {"first": 100}
        super(ManyObjectsResponseBuilder, self).__init__(saleor_url, saleor_auth_token, type_of_object, query_input)
        self._edges = None
        self._node = None
        self._page_info = None
        self._filter = ""

    @property
    def edges(self):
        return self._edges or "edges"

    @edges.setter
    def edges(self, value):
        self._edges = value

    @property
    def node(self):
        return self._node or "node"

    @node.setter
    def node(self, value):
        self._node = value

    @property
    def page_info(self):
        return self._page_info or ""

    @page_info.setter
    def page_info(self, value):
        self._page_info = value

    def filter(self, filters):
        self._filter = filters
        return self

    def all(self, chunks=0, flat=False):
        response = self._get_all_response(chunks)
        if flat:
            return itertools.chain.from_iterable(edge['data'][self.type_of_object]['edges'] for edge in response)
        return response

    def _get_all_response(self, chunks):
        cursor_string = ""
        self.page_info = "pageInfo { hasNextPage endCursor }"
        guard = 0
        while True:
            guard += 1
            self._query_input["after"] = cursor_string
            response = self._execute_query().json()
            has_next_page = response['data'][self.type_of_object]["pageInfo"]["hasNextPage"]
            cursor_string = response['data'][self.type_of_object]["pageInfo"]["endCursor"]
            yield response
            if not has_next_page:
                break
            if chunks and chunks <= guard:
                break

    def _get_query(self):
        query_input = ", ".join([f'{key}:{self._parse_value_type(value)}' for key, value in self.query_input.items()])
        filters = ", filter:{%s}" % self._filter if self._filter else ""
        return self._query_schema % (self._type_of_object, query_input, filters, self.page_info, self.edges, self.node, self._query_fields)

    @property
    def _query_schema(self):
        return """
            query{
                %s(%s%s){
                    %s
                    %s{
                        %s{
                            %s
                        }
                    }
                }
            }
            """
