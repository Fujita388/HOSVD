####もとの行列を(81, 243)として、tucker分解####



import numpy as np
from scipy import linalg


original_np = np.load('study/svd_study/three_eyes.npy')
original_np2 = original_np.reshape(81, 243)        #もとの行列をreshape
u, s, v = linalg.svd(original_np2)                


#右側をsvd
r = 30                                             #残す特異値の数   
ur = u[:, :r]                                      #u
sr = np.diag(s[:r])                                #s
vr_t = v[:r, :]                                    #vダガー
vr = np.transpose(vr_t)                            #v
L = ur @ sr
print(f"L: {L.shape}")           
print(f"vr_t: {vr_t.shape}")


#左側をsvd
r2 = 10                                             #残す特異値の数   
ur2 = u[:, :r2]                                      #u
ur_t2 = np.transpose(ur2)                            #uダガー
sr2 = np.diag(s[:r2])                                #s
vr_t2 = v[:r2, :]                                    #vダガー
L2 = sr2 @ vr_t2
print(f"ur2: {ur2.shape}")
print(f"L2: {L2.shape}")  


#復元
core_np = ur_t2 @ original_np2 @ vr                 #コアテンソル
recover_np = ur2 @ ur_t2 @ original_np2 @ vr @ vr_t
print(f"core_np: {core_np.shape}") 
print(f"recover_np: {recover_np.shape}")  


#圧縮率
print((ur2.size + core_np.size + vr_t.size) / original_np2.size) 