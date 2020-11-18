####もとの行列を(81, 243)として、tucker分解####



import numpy as np
from scipy import linalg
import matplotlib.pyplot as plt
import battle_record1 as bt1


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
    print(rate) 

    return [Y.reshape(3,3,3,3,3,3,3,3,3), rate]

#tucker(get_np, 10)

#戦績とフロベニウスノルムをプロット
def make_plot():              
    #battle#
    x = []
    y1 = []                                  #originalが勝つ割合
    y2 = []                                  #svdが勝つ割合
    y3 = []                                  #引き分けの割合
    #frobenius#
    # y4 = []
    # original_np = get_np.reshape(81,243)     #もとの行列をreshape    
    # X = original_np.copy()        
    # u, s, v = linalg.svd(X)                              #svd
    # norm = np.sqrt(np.sum(X * X))                        #sのフロベニウスノルム

    for r in range(0, 28):
        x.append(tucker(get_np, r)[1])                        #残した特異値の割合                       
        #battle#
        y1.append(bt1.battle(get_np, tucker(get_np, r)[0])[0])
        y2.append(bt1.battle(get_np, tucker(get_np, r)[0])[1])
        y3.append(bt1.battle(get_np, tucker(get_np, r)[0])[2])
        #frobenius#  
        # ur = u[:, :r]
        # sr = np.diag(np.sqrt(s[:r]))                #sの平方根
        # vr = v[:r, :]
        # A = ur @ sr
        # B = sr @ vr
        # Y = A @ B                                   #近似した行列
        # norm1 = np.sqrt(np.sum((X-Y) * (X-Y)))     #フロベニウスノルム
        # y4.append(norm1 / norm)
    plt.xlabel("left singular value ratio")
    ######plt.ylabel("ratio")
    #battle#
    plt.plot(x, y1, color = 'red')
    plt.plot(x, y2, color = 'blue')
    plt.plot(x, y3, color = 'green')
    #frobenius#
    # plt.plot(x, y4, color = 'black')

    plt.show()

make_plot()