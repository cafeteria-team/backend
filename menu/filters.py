from django_filters import rest_framework as drf_filters

from util.trans_date import TransDate


class MenuFilter(drf_filters.FilterSet):
    provide_at = drf_filters.DateFilter(
        method="filter_provide_at", help_text="메뉴 서비스 일자 / 2022-02-19"
    )

    def filter_provide_at(self, queryset, name, value):
        trans_date = TransDate(value)
        today_min = trans_date.get_today_min()
        today_max = trans_date.get_today_max()

        result = queryset.filter(provide_at__range=(today_min, today_max))
        return result
