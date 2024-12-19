# from stensor import Tensor, Sin, Cos
import sys, os
stensor_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.append(stensor_dir)
print("sys.path: ",sys.path)
import numpy as np
import cupy as cp
import time
import torch
from stensor.ops import functional as F
from stensor import Tensor, Config
# print("=======start test =====")

# print("=======shape: (64, 1024, 1024)=========")
# from stensor import Tensor, matmul, Config
# Config.device = "gpu"
# Config.recomputer = False
# for i in range(100):
#     # Forward:
#     # float64: 3390MiB, 3390MiB
#     # float32: 1854MiB, 2622MiB
#     # float16: 1982MiB, 2110
    
#     # Forward + Backward:
#     # float64: 4414MiB
#     # float32: 2366MiB
#     # float16: 2238MiB

#     # Forward:
#     # float64: 3390MiB
#     # float32: 2622MiB
#     # float16: 2110MiB
#     x_0 = np.random.rand(64, 1024, 1024).astype(np.float64)   
#     x_1 = np.random.rand(64, 1024, 1024).astype(np.float64)
#     x0 = Tensor(x_0).to_gpu().astype(cp.float16)  #float32: 256MB
#     x1 = Tensor(x_1).to_gpu().astype(cp.float16)
#     time0 = time.time()
#     y = matmul(x0, x1)
#     #print(y.shape)
#     time1 = time.time()
#     #y.backward()
#     #print(x0.grad.shape,  x1.grad.shape)
#     time2 = time.time()
#     print(f"y:{y.shape}, forward : {time1-time0}, backward : {time2-time1}") #0.00059s
    
# for i in range(100):    
#     x_0 = np.random.rand(64, 1024, 1024).astype(np.float64)   
#     x_1 = np.random.rand(64, 1024, 1024).astype(np.float64)
#     x0 = cp.asarray(x_0).astype(cp.float16)  #float32: 256MB
#     x1 = cp.asarray(x_0).astype(cp.float16)
#     time0 = time.time()
#     y = cp.matmul(x0, x1)
#     print(y.shape)
#     time1 = time.time()
#     print(time1-time0)  #0.00036s

# device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
# for i in range(100):    
#     x_0 = np.random.rand(64, 1024, 1024).astype(np.float64)   
#     x_1 = np.random.rand(64, 1024, 1024).astype(np.float64)
#     x0 = torch.tensor(x_0, dtype=torch.float16).to(device) 
#     x1 = torch.tensor(x_1, dtype=torch.float16).to(device)
#     time0 = time.time()
#     y = torch.matmul(x0, x1)
#     print(y.shape)
#     time1 = time.time()
#     print(time1-time0)  #0.00024s

Config.device = "gpu"
x_0 = np.random.rand(64, 1024, 1024).astype(np.float64)   
x_1 = np.random.rand(64, 1024, 1024).astype(np.float64)
x0 = cp.asarray(x_0).astype(cp.float16)  #float32: 256MB
x1 = cp.asarray(x_1).astype(cp.float16)
tensor_x0 = Tensor(x0)
tensor_x1 = Tensor(x1)

y = cp.matmul(x0, x1)
time0 = time.time()
for i in range(100):
    time00 = time.time()    
    y = cp.matmul(x0, x1)
    time01 = time.time()
    print("step cupy:", time01-time00)
    #print(y.shape)
time1 = time.time()
print("cupy: ",(time1-time0))

y = F.matmul(tensor_x0, tensor_x1)
time2 = time.time()
for i in range(100):
    time02 = time.time()    
    y = F.matmul(tensor_x0, tensor_x1)
    time03 = time.time() 
    print("step stensor:", time03-time02)  
    #print(y.shape)
time3 = time.time()
print("stensor: ",(time3-time2))