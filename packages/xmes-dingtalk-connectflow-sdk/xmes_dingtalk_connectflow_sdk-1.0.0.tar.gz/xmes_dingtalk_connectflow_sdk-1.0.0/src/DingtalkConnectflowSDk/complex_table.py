"""
Copyright (c) 2024-now LeslieLiang All rights reserved.
Build Date: 2024-12-18
Author: LeslieLiang
Description: 多维表连接流SDK
"""

from dataclasses import dataclass
from typing import Literal

from requests import post


@dataclass
class GetterFilter:
    field: str
    operator: Literal[
        'equal', 'notEqual', 'incontain', 'notContain', 'empty', 'notEmpty'
    ]
    value: list[str] = None


@dataclass
class Updater:
    record_id: str
    fields: dict[str, any]


class Table:
    __HEADERS = {
        'Content-Type': 'application/json',
    }

    def __init__(self, flow_url: str, did: str, tid: str):
        self.flow_url = flow_url
        self.did = did
        self.tid = tid
        self.global_reqdata = {
            'did': did,
            'tid': tid,
        }

    def get(
        self,
        size=20,
        cursor: str = '',
        combination: Literal['and', 'or'] = 'and',
        filters: list[GetterFilter] | None = None,
    ) -> dict:
        """
        获取表格数据
        Args:
            size: 每页数据条数, 默认为 20
            cursor: 分页游标, 首次请求可不传, 后续需传入上一次返回的 nextCursor 值
            combination: 组合方式
            filters: 过滤条件
        Returns:
            表格数据
        """

        reqdata = {
            **self.global_reqdata,
            'handle': 'GET',
            'handle_get': {
                'size': size,
                'cursor': cursor,
            },
        }

        if combination and combination in ['and', 'or']:
            filter_field = {}
            filter_field['combination'] = combination
            if filters and isinstance(filters, list):
                conditions = [
                    item.__dict__ for item in filters if isinstance(item, GetterFilter)
                ]
                filter_field['conditions'] = conditions
            reqdata['handle_get']['filter'] = filter_field

        resp = post(self.flow_url, json=reqdata, headers=self.__HEADERS)
        return resp.json().get('GET_RESULT')

    def add(self, records: list[dict]):
        """
        新增记录
        Args:
            records: 新增记录列表
        Returns:
            新增记录结果
        """

        if not records or not isinstance(records, list):
            raise ValueError('records must be a list')

        records_clean = [
            record for record in records if record and isinstance(record, dict)
        ]
        if not records_clean:
            raise ValueError('records must not be empty')

        reqdata = {
            **self.global_reqdata,
            'handle': 'ADD',
            'handle_add': {
                'records': records_clean,
            },
        }

        resp = post(self.flow_url, json=reqdata, headers=self.__HEADERS)
        return resp.json().get('ADD_RESULT')

    def update(self, records: list[Updater]):
        """
        更新记录
        Args:
            records: 更新记录列表
        Returns:
            更新记录结果
        """

        if not records or not isinstance(records, list):
            raise ValueError('records must be a list')

        records_clean = [
            record.__dict__
            for record in records
            if record and isinstance(record, Updater)
        ]
        if not records_clean:
            raise ValueError('records must not be empty')

        reqdata = {
            **self.global_reqdata,
            'handle': 'UPDATE',
            'handle_update': {
                'records': records_clean,
            },
        }

        resp = post(self.flow_url, json=reqdata, headers=self.__HEADERS)
        return resp.json().get('UPDATE_RESULT')

    def delete(self, record_ids: list[str]):
        """
        删除记录
        Args:
            record_ids: 记录 id 列表
        Returns:
            删除记录结果
        """

        if not record_ids or not isinstance(record_ids, list):
            raise ValueError('record_ids must be a list')

        record_ids_clean = [
            record_id
            for record_id in record_ids
            if record_id and isinstance(record_id, str)
        ]

        reqdata = {
            **self.global_reqdata,
            'handle': 'DELETE',
            'handle_delete': {
                'record_ids': record_ids_clean,
            },
        }

        resp = post(self.flow_url, json=reqdata, headers=self.__HEADERS)
        return resp.json().get('DELETE_RESULT')


class ComplexTable:
    def __init__(self, flow_url: str):
        """
        初始化 ComplexTable 类
        Args:
            flow_url: 连接流 url
        """

        self.flow_url = flow_url

    def get_table(self, did: str, tid: str) -> Table:
        """
        获取表格对象
        Args:
            did: 文档 id
            tid: 数据表 id
        Returns:
            Table 对象
        """

        return Table(self.flow_url, did, tid)
