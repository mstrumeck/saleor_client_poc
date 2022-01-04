import abc

import requests


class BaseResponseBuilder(abc.ABC):
    def __init__(self, saleor_url, saleor_auth_token, type_of_object, query_input=None):
        self._saleor_url = saleor_url
        self._auth_token = saleor_auth_token
        self._type_of_object = type_of_object
        self._query_input = query_input
        self._query_fields = "id"
        self._response = None

    @property
    def _query_schema(self):
        raise NotImplementedError()

    @property
    def type_of_object(self):
        return self._type_of_object

    @type_of_object.setter
    def type_of_object(self, value):
        self._type_of_object = value

    @property
    def query_input(self):
        return self._query_input

    @query_input.setter
    def query_input(self, value):
        self._query_input = value

    @property
    def query_fields(self):
        return self._query_fields

    @query_fields.setter
    def query_fields(self, value):
        self._query_fields = value

    def fields(self, fields):
        self._query_fields = fields
        return self

    def _execute_query(self):
        response = requests.post(url=self._saleor_url, data={"query": self._get_query()}, headers={"Authorization": self._auth_token})
        response.raise_for_status()
        return response

    def _get_query(self):
        query_input = ", ".join([f'{key}:{self._parse_value_type(value)}' for key, value in self.query_input.items()])
        return self._query_schema % (self._type_of_object, query_input, self._query_fields)

    def _get_or_create_response(self):
        if not self._response:
            self._response = self._execute_query()

    def _parse_value_type(self, value):
        type_map = {
            str: '"{}"',
            int: '{}'
        }
        return type_map.get(type(value)).format(value)

    def __getitem__(self, item):
        self._get_or_create_response()
        return self._response.json()[item]

    def __str__(self):
        self._get_or_create_response()
        return self._response.content.decode("utf-8")
