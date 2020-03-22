from instance.generated.api.builtin.api_builtin import Interface
from instance.generated.models.stub import search_all
from instance.generated.models.builtin import SearchResponse


class APIBuiltin(Interface):
    @staticmethod
    def search(
        request,
):
        return SearchResponse(query=request.query, **search_all(request.query, request.tables))
