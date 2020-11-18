####もとの行列を(27, 27, 27)のテンソルとして、tucker分解####



import numpy as np
from scipy import linalg


get_np = np.load('study/svd_study/three_eyes.npy')


#もとの行列を(27, 27, 27)のテンソルとして、tucker分解
def tucker(X, r):
    X = X.reshape(27, 27, 27)
    #右
    XR = X.reshape(729, 27) 
    _, _, v = linalg.svd(XR)                                              
    VRt = v[:r, :]                                    #vダガー
    VR = np.transpose(VRt)                             #v
    #真ん中
    XM = X.transpose(0, 2, 1)
    XM = XM.reshape(729, 27)
    _, _, v = linalg.svd(XM)                                              
    VMt = v[:r, :]                                    #vダガー
    VM = np.transpose(VMt)                             #v
    #左
    XL = X.transpose(2, 1, 0)
    XL = XL.reshape(729, 27)
    _, _, v = linalg.svd(XL)                                              
    VLt = v[:r, :]                                    #vダガー
    VL = np.transpose(VLt)                             #v
    #コアテンソル
    C2 = np.tensordot(X, VR, (2,0))               
    C1 = np.tensordot(C2, VM, (1,0)) 
    C = np.tensordot(C1, VL, (0,0))               
    #復元
    Y2 = np.tensordot(C, VRt, (2,0))  
    Y1 = np.tensordot(Y2, VMt, (1,0))
    Y = np.tensordot(Y1, VLt, (0,0))
    #圧縮率
    rate = (VRt.size + VMt.size + VLt.size + C.size) / X.size
    print(rate)

    #return [Y.reshape(3,3,3,3,3,3,3,3,3), rate]

tucker(get_np, 10)