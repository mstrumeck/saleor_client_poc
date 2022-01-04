from response_builder.many_objects_response import ManyObjectsResponseBuilder
from response_builder.single_object_response import SingleObjectResponseBuilder
import os


class SaleorClient:
    def __init__(self, saleor_url, saleor_token=None):
        super(SaleorClient, self).__init__()
        self._saleor_url = saleor_url or os.getenv("SALEOR_ENDPOINT")
        self._token = saleor_token or os.getenv("SALEOR_TOKEN")
        self._type_request = None

    @property
    def query(self):
        self._type_request = "query"
        return self

    @property
    def mutation(self):
        self._type_request = "mutation"
        return self

    def product(self, **kwargs):
        return self._assign_builder(SingleObjectResponseBuilder, "product", kwargs)

    def products(self, **kwargs):
        return self._assign_builder(ManyObjectsResponseBuilder, "products", kwargs)

    def order(self, **kwargs):
        return self._assign_builder(SingleObjectResponseBuilder, "order", kwargs)

    def orders(self, **kwargs):
        return self._assign_builder(ManyObjectsResponseBuilder, "orders", kwargs)

    def variant(self, **kwargs):
        return self._assign_builder(SingleObjectResponseBuilder, "productVariant", kwargs)

    def variants(self, **kwargs):
        return self._assign_builder(ManyObjectsResponseBuilder, "productVariants", kwargs)

    def _assign_builder(self, builder, type_of_object, kwargs):
        builder_kwargs = {"saleor_url": self._saleor_url, "saleor_auth_token": self._token, "type_of_object": type_of_object}
        if kwargs:
            builder_kwargs["query_input"] = kwargs
        return builder(**builder_kwargs)


token = "YOUR TOKEN!"
url = "http://localhost:8000/graphql/"

#TESTING!

saleor_query = SaleorClient(url, token).query
print(saleor_query.product(id="UHJvZHVjdDo3Mg==").fields("id, name"))  # Get product with given ID and fields

print(saleor_query.orders().fields("id, status"))  # Get all orders with given fields and default pagination

print(list(saleor_query.orders().all(flat=True)))  # Get flat list of all orders in iterator with ID field

print(saleor_query.products().fields("id, name").filter('ids: ["UHJvZHVjdDo3Mg==", "UHJvZHVjdDo3NA=="]'))

print(list(saleor_query.variants(first=1).all(chunks=1, flat=True)))

print(saleor_query.variant(id="UHJvZHVjdFZhcmlhbnQ6MzE0"))

