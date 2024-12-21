#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import math
from enum import Enum
from typing import Iterable, Tuple, List, Mapping, Collection, Generic, TypeVar

from .utils import fusion


U = TypeVar('U')
T = TypeVar('T')


class CFType(Enum):
    UCF = 'UserCF'
    ICF = 'ItemCF'


def default_similar_func(items: List, other: List) -> float:
    """两个item并集数

    以用户相似度为例，遍历item_users，每行用户间拥有共同的item，避免遍历userTtems大量用户间没有共同的item：
    item1: user1, user2, user3

    user1和user2共同有item1:
    user1: item1, item2, item3
    user2: item1, item4, item5

    传入此方法的参数为:
    items: [item1, item2, item3]
    other: [item1, item4, item5]
    """
    return 1.0 / float(len(set(items + other)))


def sqrt_similar_func(items: List, other: List) -> float:
    """两个item数相乘开根"""
    return 1.0 / math.sqrt(len(items) * len(other))


class CollFilter(Generic[U, T]):
    """
    Collaborative filter

    Examples
    --------
    >>> from cf import CollFilter
    >>> data = read_data('file_path')
    >>> data = pre_process(data)  # return List[(user_id: Any, item_id: Any, rating: float)]
    >>> cf = CollFilter(data)
    >>> ucf = cf.user_cf()  # return {user_id: [(item_id, score),],}
    >>> icf = cf.item_cf()  # return {user_id: [(item_id, score),],}
    >>> recommend = cf.recommend(user_id, num_recalls=5) # return [(item_id, score),]
    >>> recommends = cf.recommends(user_ids, num_recalls=5) # return {user_id: [(item_id, score),],}
    >>> cf.release()
    """

    def __init__(self, data: Iterable[Tuple[U, T, float]], n_jobs=2 * os.cpu_count(), row_unique=False,
                 similar_fn=default_similar_func, cache_similar: bool = False, verbose: bool = False):
        if n_jobs > 1:
            from cf.pooling import PoolCollFilter
            self._coll_filter = PoolCollFilter(data, n_jobs, row_unique, similar_fn, cache_similar, verbose)
        else:
            from cf.base import BaseCollFilter
            self._coll_filter = BaseCollFilter(data, row_unique, similar_fn, cache_similar, verbose)

    def user_cf(self,
                num_recalls=64,
                num_similar=256,
                user_ids: Collection[U] = None,
                user_similar: Mapping[U, Mapping[U, float]] = None,
                similar_fn=None
                ) -> Mapping[U, List[Tuple[T, float]]]:
        """
        基于用户的协同过滤
        @param num_recalls  每个用户最大召回个数
        @param num_similar  每个用户最大相似用户个数
        @param user_ids  要推荐的用户列表
        @param user_similar  用户相似矩阵
        @param similar_fn  相似度计算函数
        @return {user_id: [(item_id, score),],}
        """
        assert num_recalls > 0, "'num_recalls' should be a positive number."
        return self._coll_filter.user_cf(num_recalls, num_similar, user_ids, user_similar, similar_fn)

    def item_cf(self,
                num_recalls=64,
                num_similar=256,
                user_ids: Collection[U] = None,
                item_similar: Mapping[T, Mapping[T, float]] = None,
                similar_fn=None
                ) -> Mapping[U, List[Tuple[T, float]]]:
        """
        基于物品的协同过滤
        @param num_recalls  每个用户最大召回个数
        @param num_similar  每个物品最大相似物品个数
        @param user_ids  要推荐的用户列表
        @param item_similar  物品相似矩阵
        @param similar_fn  相似度计算函数
        @return {user_id: [(item_id, score),],}
        """
        assert num_recalls > 0, "'num_recalls' should be a positive number."
        return self._coll_filter.item_cf(num_recalls, num_similar, user_ids, item_similar, similar_fn)

    def recommend(self, user_id: U, num_recalls=64, num_similar=8, similar_fn=None, ratio=0.5, return_score=False) \
            -> List[Tuple[T, float]]:
        """
        给一个用户推荐
        @param user_id  要推荐的用户
        @param num_recalls  每个用户最大召回个数
        @param num_similar  每个物品最大相似物品个数
        @param similar_fn  相似度计算函数
        @param ratio  推荐结果中item_cf所占比例
        @param return_score 是否返回分数
        @return [item_id,] or [(item_id, score),]
        """
        result = self._recommend(user_id, num_recalls, num_similar, similar_fn, ratio)
        return result if return_score else [item[0] for item in result]

    def _recommend(self, user_id: U, num_recalls, num_similar, similar_fn, ratio) -> List[Tuple[T, float]]:
        """
        给一个用户推荐
        @param user_id  要推荐的用户
        @param num_recalls  每个用户最大召回个数
        @param num_similar  每个物品最大相似物品个数
        @param similar_fn  相似度计算函数
        @param ratio  推荐结果中item_cf所占比例
        @return [(item_id, score),]
        """
        icf = self.item_cf(num_recalls, num_similar, [user_id], None, similar_fn)
        icf_items = icf[user_id]
        if num_recalls == 1:
            if icf_items:
                return icf_items
            else:
                return self.user_cf(num_recalls, num_similar, [user_id], None, similar_fn)[user_id]
        else:
            ucf_items = self.user_cf(num_recalls, num_similar, [user_id], None, similar_fn)[user_id]
            return fusion(icf_items, ucf_items, num_recalls, ratio)

    def recommends(self,
                   user_ids: Collection[U] = None,
                   num_recalls: int = 64,
                   num_similar: int = 8,
                   similar_fn=None,
                   ratio: float = 0.5
                   ) -> Mapping[U, List[Tuple[T, float]]]:
        """
        给一批用户推荐
        @param user_ids  要推荐的用户列表，如果为空给所有用户推荐
        @param num_recalls  每个用户最大召回个数
        @param num_similar  每个物品最大相似物品个数
        @param similar_fn  相似度计算函数
        @param ratio  推荐结果中item_cf所占比例
        @return {user_id: [(item_id, score),],}
        """
        icf = self.item_cf(num_recalls, num_similar, user_ids, None, similar_fn)
        if num_recalls == 1:
            user_similar = self.get_user_similar(num_similar, similar_fn)
            for user_id, items in icf.items():
                if not items:
                    icf[user_id] = self.user_cf(num_recalls, num_similar, [user_id], user_similar, similar_fn)[user_id]
        else:
            ucf = self.user_cf(num_recalls, num_similar, user_ids, None, similar_fn)
            for user_id, icf_items in icf.items():
                ucf_items = ucf[user_id]
                icf[user_id] = fusion(icf_items, ucf_items, num_recalls, ratio)

        return icf

    def get_user_similar(self, num_similar=256, similar_fn=None) -> Mapping[U, Mapping[U, float]]:
        """
        用户相似矩阵
        """
        return self._coll_filter.cal_similar(CFType.UCF, num_similar, similar_fn)

    def get_item_similar(self, num_similar=256, similar_fn=None) -> Mapping[T, Mapping[T, float]]:
        """
        物品相似矩阵
        """
        return self._coll_filter.cal_similar(CFType.ICF, num_similar, similar_fn)

    def release(self):
        self._coll_filter.release()
