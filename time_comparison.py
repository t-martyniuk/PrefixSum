from prefix_sum import parallel_prefix_sum, seq_prefix_sum
import multiprocessing
from time import time
from matplotlib import pyplot as plt

degrees = list(range(3,20))
time_seq = []
time_par = []

for ii in degrees:
    length = pow(2,ii)
    seq_list = [1]*length
    par_list = seq_list + [0]
    par_list = multiprocessing.Array('i', par_list)

    t = time()
    seq_list = seq_prefix_sum(seq_list)
    t_new = time() - t
    time_seq.append(t_new)

    t = time()
    par_list = parallel_prefix_sum(par_list)
    t_new = time() - t
    time_par.append(t_new)

plt.plot(degrees,time_seq)
plt.plot(degrees,time_par)
plt.legend(['seq','par'])
plt.show()