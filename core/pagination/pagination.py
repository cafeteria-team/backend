from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        return Response(
            {
                "page": {
                    "links": {
                        "next": self.get_next_link(),
                        "previous": self.get_previous_link(),
                    },
                    "current_page": self.page.number,
                    "page_size": self.page.paginator.per_page,
                    "total_count": self.page.paginator.count,
                },
                "results": data,
            }
        )
