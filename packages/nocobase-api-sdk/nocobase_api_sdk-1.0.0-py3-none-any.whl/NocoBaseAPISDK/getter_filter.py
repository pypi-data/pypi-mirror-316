import json
from dataclasses import dataclass
from typing import Any, Literal


@dataclass
class FilterCondition:
    field: str
    operator: Literal[
        'includes', 'notIncludes', 'eq', 'ne', 'empty', 'notEmpty', 'isTruly', 'isFalsy'
    ]
    value: Any = None

    def __post_init__(self):
        if self.operator in ['isTruly', 'isFalsy']:
            self.value = True


@dataclass
class Filter:
    combination: Literal['and', 'or'] = 'and'
    conditions: list[FilterCondition] = None

    def __post_init__(self):
        if self.combination not in ['and', 'or']:
            self.combination = 'and'

        if not isinstance(self.conditions, list):
            self.conditions = []


@dataclass
class Sort:
    field: str
    order: Literal['asc', 'desc'] = 'asc'

    def __post_init__(self):
        if self.order not in ['asc', 'desc']:
            self.order = 'asc'


@dataclass
class GetterFilter:
    filterByTk: str | int = None
    filter_: Filter = None
    """过滤条件"""
    sort: list[Sort] = None
    fields: list[str] = None
    """需要的字段"""
    except_fields: list[str] = None
    """不需要的字段"""

    def get_query(self, flatten=False):
        """
        获取查询参数

        Args:
            flatten: 是否展平查询参数变成单层结构, 默认为 False
        """

        query = {}

        if isinstance(self.filterByTk, (str, int)):
            query['filterByTk'] = self.filterByTk

        if self.filter_ and isinstance(self.filter_, Filter):
            filters = [
                {item.field: {f'${item.operator}': item.value}}
                for item in self.filter_.conditions
                if isinstance(item, FilterCondition)
            ]
            if filters:
                query['filter'] = {f'${self.filter_.combination}': filters}

        if self.sort and isinstance(self.sort, list):
            sorts = [
                f'-{sort.field}' if sort.order == 'desc' else sort.field
                for sort in self.sort
                if isinstance(sort, Sort)
            ]
            query['sort'] = ','.join(sorts)

        if self.fields and isinstance(self.fields, list):
            query['fields'] = ','.join(
                [field for field in self.fields if field and isinstance(field, str)]
            )

        if self.except_fields and isinstance(self.except_fields, list):
            query['except'] = ','.join(
                [
                    field
                    for field in self.except_fields
                    if field and isinstance(field, str)
                ]
            )

        if flatten is True:
            for key, value in query.items():
                if isinstance(value, (list, dict)):
                    query[key] = json.dumps(value, ensure_ascii=False)

        return query
