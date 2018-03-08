import multiprocessing
#[2, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 7, 8, 8, 9]

def mergesort(lst):
    if len(lst) == 1:
        return lst
    else:
        m = int(len(lst)/2)
        l = mergesort(lst[:m])
        r = mergesort(lst[m:])
        #return seq_merge(l,r,lst)
        return par_merge(l,r,lst)

def seq_merge(l,r,lst):
    i = 0
    j = 0
    k = 0
    while i < len(l) and j < len(r):
        if l[i] < r[j]:
            lst[k] = l[i]
            i += 1
        else:
            lst[k] = r[j]
            j += 1
        k += 1

    while i < len(l):
        lst[k] = l[i]
        i += 1
        k += 1

    while j < len(r):
        lst[k] = r[j]
        j += 1
        k += 1
    return lst

def par_merge(l,r,lst):

    for i in range(len(l)):
        lst[i + par_bin_search(l[i],r)] = l[i]
    for i in range(len(r)):
        lst[i + par_bin_search(r[i],l)] = r[i]

    return lst

def par_bin_search(el, arr):
    max_cores = multiprocessing.cpu_count()
    jobs = []
    processing_field = len(arr) // (max_cores + 1)
    bin_array = [0]*max_cores
    idx_array = [0]*(max_cores+2)
    idx_array[0] = 0
    idx_array[-1] = len(arr)

    def comparison(el, core, num_per_core):
        right = arr[(core + 1) * num_per_core - 1]
        idx_array[core+1] = right
        if el >= right:
            bin_array[core] = 0
        else:
            bin_array[core] = 1

    for i in range(max_cores):
        p = multiprocessing.Process(target=comparison, args=(el, i, processing_field))
        p.daemon = False
        jobs.append(p)
        p.start()
    for p in jobs:
        p.join()
    if bin_array[0] == 1:
        par_bin_search(el, arr[:idx_array[0]+1])
    elif bin_array[-1] == 0:
        par_bin_search(el, arr[idx_array[-1]:])
    else:
        idx = 0
        while (idx < max_cores) and (bin_array[idx] == 0):
            idx += 1
        if idx_array[idx - 1] + 1 < idx_array[idx]:
            par_bin_search(el, arr[idx_array[idx-1]:idx_array[idx]+1])
        else:
            return idx_array[idx-1]


print(mergesort([3,4,9,8,7,2,4,6,5,6,5,8,4,3,4,5]))

