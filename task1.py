####もとの行列を(81, 243)として、tucker分解####



import numpy as np
from scipy import linalg
import matplotlib.pyplot as plt


get_np = np.load('study/svd_study/three_eyes.npy')               


#もとの評価値の配列(81, 243)をtucker分解する        
def tucker(X, r):
    X = X.reshape(81, 243)
    u, _, v = linalg.svd(X)
    #左側  
    U = u[:, :r]                                      #u
    Ut = np.transpose(U)                               #uダガー                             
    #右側 
    r2 = 3 * r                                      
    Vt = v[:r2, :]                                    #vダガー
    V = np.transpose(Vt)                             #v
    #コアテンソル
    C = Ut @ X @ V     
    #復元            
    Y = U @ C @ Vt
    #圧縮率
    rate = (U.size + C.size + Vt.size) / X.size
    #print(rate) 

    return [Y.reshape(3,3,3,3,3,3,3,3,3), rate]

#tucker(get_np, 10)

