from instance.generated.api.builtin.api_builtin import Interface
from instance.generated.models.stub import search_all
from instance.generated.models.builtin import SearchResponse


class APIBuiltin(Interface):
    @staticmethod
    def search(
        request,
):
        data = search_all(request.query, request.tables)
        for x in data['person']:
            x.avas
        return SearchResponse(query=request.query, **data)
