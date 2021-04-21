import os
import sys
import json
import collections

class FEGardening(object):
    def __init__(self, seeds_pool_dict, seeds_rank_dict, seeds_grade_dict, required_seeds_sub_combs_list):
        self.seeds_pool = seeds_pool_dict
        self.seeds_rank = seeds_rank_dict
        self.seeds_grade = seeds_grade_dict
        self.required_seeds_sub_combs = required_seeds_sub_combs_list

        # assume we have {A:2, B:3}
        # when to delete an iterated elem? 
        # 0. need to recover it back for the parent stack, otherwise after setting A = 1, 
        # we invoke another layer of backtrace, deleting B from the dict permanenty, we then would lose all comb with A = 2
        # and B > 0
        # 1. cannot set it back before the next elem get iterated through, otherwise, there would be duplicate.

    def _back_trace(self, seeds_num, seeds_pool, seeds_rank, seeds_grade, accum, candidates, required_seeds = []):
        if seeds_num <= 0 or not seeds_pool:
            return
        seeds_list = list(seeds_pool.keys())
        if required_seeds:
            first_required_seed = required_seeds[0]
            required_seeds = required_seeds[1:]
            seeds_list = [first_required_seed]
        pool_this_layer = {k: v for k, v in seeds_pool.items()}
        for s in seeds_list:
            sn = pool_this_layer[s]
            pool_this_layer.pop(s)
            for n in range(1, min(seeds_num, sn) + 1):
                accum[s] = n
                curr_comb = {k: v for k, v in accum.items() if v > 0}
                candidates.add(tuple(curr_comb.items()))
                self._back_trace(seeds_num - n, pool_this_layer, seeds_rank, seeds_grade, accum, candidates, required_seeds)
            accum.pop(s, -1)

    def enum_top_combs(self, capacity, required_seeds_sub_combs = [[]]):
        accum = {}
        candidates = set()
        for required_sub_comb in required_seeds_sub_combs:
            self._back_trace(capacity, self.seeds_pool, self.seeds_rank, self.seeds_grade, accum, candidates, required_sub_comb)
        return [dict(t) for t in candidates]

    def calculate_score(self, comb):
        A = (12 - sum(comb[s] * self.seeds_rank[s] for s in comb) % 12) * 5
        B = sum(comb[s] * self.seeds_grade[s] for s in comb) * 4 // 5
        return A + B
    
    def rank_comb(self, capacity):
        combs = self.enum_top_combs(capacity, self.required_seeds_sub_combs)
        comb_scores = {json.dumps(comb): self.calculate_score(comb) for comb in combs}
        return sorted(comb_scores.items(), key=lambda x: x[1], reverse = True)

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        seeds_info = json.load(f)
    garden = FEGardening(seeds_info["pool"], seeds_info["rank"], seeds_info["grade"], seeds_info["required_seeds"])
    seeds_combs_rank = garden.rank_comb(int(sys.argv[2]))
    seeds_combs_yield_3 = [(k, v) for k, v in seeds_combs_rank if v > int(sys.argv[3])]
    with open(sys.argv[4], "w") as f:
        for combs, score in seeds_combs_yield_3:
            f.write("{}{}\n".format(score, combs))