from .base_response_builder import BaseResponseBuilder


class SingleObjectResponseBuilder(BaseResponseBuilder):
    def __init__(self, saleor_url, saleor_auth_token, type_of_object, query_input):
        super(SingleObjectResponseBuilder, self).__init__(saleor_url, saleor_auth_token, type_of_object, query_input)

    @property
    def _query_schema(self):
        return """
            query {
            %s(%s) {
                %s
                }
            }
            """

