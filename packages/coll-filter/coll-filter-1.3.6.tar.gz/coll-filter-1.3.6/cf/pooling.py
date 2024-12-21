#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""pool_coll_filter"""

import os
import time
import math
# from multiprocessing import Pool
from typing import Iterable, Tuple
from concurrent.futures import as_completed, ProcessPoolExecutor
from .base import BaseCollFilter
from . import default_similar_func, CFType, U, T
from .utils import print_cost_time, sort_similar, logger


PARALLEL_THRESHOLD = 4096


class PoolMultiProcessor:

    def __init__(self, n_jobs):
        cpu_count = os.cpu_count()
        self.n_jobs = cpu_count if n_jobs <= 1 else n_jobs
        # self.pool = Pool(cpu_count - 1) if self.n_jobs >= cpu_count else Pool(self.n_jobs - 1)
        self.executor = ProcessPoolExecutor(cpu_count - 1 if self.n_jobs >= cpu_count else self.n_jobs - 1)

    def cal_similar(self, dict1, items_list, cal_fn, similar_fn, verbose: bool):
        size = len(items_list)
        split_size = math.ceil(size / (self.n_jobs << 1))
        # results = [self.pool.apply_async(func=cal_fn, args=(dict1, items_list[i:i+split_size], similar_fn))
        #            for i in range(split_size, size, split_size)]
        
        results = [self.executor.submit(cal_fn, dict1, items_list[i:i+split_size], similar_fn, verbose)
                   for i in range(split_size, size, split_size)]

        similar = cal_fn(dict1, items_list[:split_size], similar_fn, verbose)

        for result in as_completed(results):
            # for key, items in result.get().items():
            for key, items in result.result().items():
                if key in similar:
                    for item, score in items.items():
                        similar[key][item] = similar[key].get(item, 0.0) + score
                else:
                    similar[key] = items

        return similar

    def cf(self, user_item_ratings, user_items_list, similar_dict, num_recalls, cf_fn, verbose: bool):
        size = len(user_item_ratings)
        split_size = math.ceil(size / (self.n_jobs << 1))
        # results = [self.pool.apply_async(func=cf_fn,
        #                                  args=(user_item_ratings,
        #                                        similar_dict,
        #                                        user_items_list[i:i + split_size],
        #                                        num_recalls
        #                                        )
        #                                  )
        #            for i in range(split_size, size, split_size)]
        
        results = [self.executor.submit(cf_fn, user_item_ratings, similar_dict, user_items_list[i:i + split_size], num_recalls, verbose)
                   for i in range(split_size, size, split_size)]

        cf_result = cf_fn(user_item_ratings, similar_dict, user_items_list[:split_size], num_recalls, verbose)

        for result in as_completed(results):
            # cf_result.update(result.get())
            cf_result.update(result.result())

        return cf_result

    def release(self):
        # self.pool.close()
        self.executor.shutdown(wait=True)


class PoolCollFilter(BaseCollFilter):

    def __init__(self, data: Iterable[Tuple[U, T, float]], n_jobs=0, row_unique=False,
                 similar_fn=default_similar_func, cache_similar: bool = False, verbose: bool = False):
        super().__init__(data, row_unique, similar_fn, cache_similar, verbose)
        self.processor = PoolMultiProcessor(n_jobs)

    def release(self):
        super().release()
        self.processor.release()

    def _cal_similar(self, cf_type: CFType, num_similar, similar_fn):
        """
        计算相似度

        @return dict{:dict}    {user1: {user2: similar}}
        """
        logger.info(f'开始{cf_type.value[:-2]}相似度计算, num_similar: {num_similar}')
        func_start_time = time.perf_counter()
        dict1, items_list, cal_similar_func = self._get_cal_similar_inputs(cf_type)
        items_list = list(items_list)
        similar_fn = similar_fn or self.similar_fn
        items_len = len(items_list)
        if (cf_type == CFType.UCF and items_len <= PARALLEL_THRESHOLD) or (cf_type == CFType.ICF and items_len <= 128):
            similar = cal_similar_func(dict1, items_list, similar_fn, self.verbose)
        else:
            similar = self.processor.cal_similar(dict1, items_list, cal_similar_func, similar_fn, self.verbose)
        similar = sort_similar(similar, num_similar)
        print_cost_time(f"完成{cf_type.value[:-2]}相似度计算, 当前进程<{os.getpid()}>, 总生成 {len(similar)} 条记录, 总耗时", func_start_time)
        logger.info("=" * 88)
        return similar

    def _cf(self, user_ids, similar_dict, num_recalls, cf_type: CFType):
        logger.info(f'开始{cf_type.value}推理, num_recalls: {num_recalls}')
        func_start_time = time.perf_counter()
        if user_ids:
            if not set(user_ids).intersection(self.user_item_ratings.keys()):
                return {user_id: [] for user_id in user_ids}

            user_items_list = list(map(lambda x: (x, self.user_item_ratings.get(x, [])), user_ids))
        else:
            user_items_list = list(self.user_item_ratings.items())

        user_items_len = len(user_items_list)
        cf_func = self._rating_user_cf if cf_type == CFType.UCF else self._rating_item_cf
        if (cf_type == CFType.UCF and user_items_len > PARALLEL_THRESHOLD) or (cf_type == CFType.ICF and user_items_len > 128):
            cf_result = self.processor.cf(self.user_item_ratings, user_items_list, similar_dict, num_recalls, cf_func, self.verbose)
        else:
            cf_result = cf_func(self.user_item_ratings, similar_dict, user_items_list, num_recalls, self.verbose)
        print_cost_time(f"完成{cf_type.value}推理, 当前进程<{os.getpid()}>, 生成{len(cf_result)}条记录, 总耗时", func_start_time)
        logger.info("=" * 88)
        return cf_result

