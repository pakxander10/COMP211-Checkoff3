import ctypes
import time
import numpy as np
import os


lib_path = os.path.join(os.path.dirname(__file__), 'cstuff.so')
c_lib = ctypes.CDLL(lib_path)

c_lib.dot_product.argtypes = [
    ctypes.POINTER(ctypes.c_double), 
    ctypes.POINTER(ctypes.c_double), 
    ctypes.c_int
]
c_lib.dot_product.restype = ctypes.c_double

def python_dot_product(vec1, vec2):
    result = 0.0
    for i in range(len(vec1)):
        result += vec1[i] * vec2[i]
    return result

def c_dot_product(np_vec1, np_vec2):
    ptr1 = np_vec1.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    ptr2 = np_vec2.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    return c_lib.dot_product(ptr1, ptr2, len(np_vec1))

if __name__ == "__main__":
    N = 10_000_000
    print(f"Initializing vectors of length {N:,}...\n")

    #Basically this creates a list of size 10000000
    vec1 = [1.5] * N
    vec2 = [2.0] * N
    
    np_vec1 = np.array(vec1, dtype=np.float64)
    np_vec2 = np.array(vec2, dtype=np.float64)

    #Starts time tracker for Python code run
    start = time.time()
    res_py = python_dot_product(vec1, vec2)
    time_py = time.time() - start
    print(f"Pure Python: {time_py:.5f} seconds \t(Result: {res_py})")

    #Starts time tracker for C code run
    start = time.time()
    res_c = c_dot_product(np_vec1, np_vec2)
    time_c = time.time() - start
    print(f"C (ctypes):  {time_c:.5f} seconds \t(Result: {res_c})")

    #Starts time tracker for NumPy
    start = time.time()
    res_np = np.dot(np_vec1, np_vec2)
    time_np = time.time() - start
    print(f"NumPy:       {time_np:.5f} seconds \t(Result: {res_np})")