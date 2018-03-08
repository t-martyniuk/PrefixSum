import multiprocessing
from math import log

def seq_prefix_sum(lst):
    length = len(lst)
    lst.insert(0,0)
    for i in range(length):
        lst[i + 1] = lst[i] + lst[i + 1]
    return lst

def up_sum(array, depth, core, num_per_core):
    left = num_per_core * core
    right = num_per_core * (core + 1)
    step = pow(2, depth)
    for idx in range(left + step - 1, right, step):
        array[idx] = array[idx] + array[idx - int(step / 2)]

def down_sum(array, depth, core, num_per_core):
    left = num_per_core * core
    right = num_per_core * (core + 1)
    step = pow(2, depth)
    for idx in range(left + step - 1, right, step):
        element = array[idx]
        array[idx] = array[idx] + array[idx - int(step / 2)]
        array[idx - int(step / 2)] = element


def parallel_prefix_sum(array):
    length = len(array) - 1
    max_cores = multiprocessing.cpu_count()
    jobs = []

    def parallelize(level, direction):
        processing_field = pow(2, level)
        core_number = int(length / processing_field)
        if core_number > max_cores:
            core_number = max_cores
            processing_field = int(length / core_number)
        for i in range(core_number):
            p = multiprocessing.Process(target=direction, args=(array, level, i, processing_field))
            p.daemon = False
            jobs.append(p)
            p.start()
        for p in jobs:
            p.join()

    depth = int(log(length, 2))
    for level in range(1, depth + 1):
        parallelize(level, up_sum)
        sum = array[length - 1]

    array[length - 1] = 0
    core_number = 1
    for level in range(int(depth), 0, -1):
        parallelize(level, down_sum)
        array[length] = sum

    return array[:]