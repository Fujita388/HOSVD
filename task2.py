####もとの行列を(27, 27, 27)のテンソルとして、tucker分解####



import numpy as np
from scipy import linalg
import matplotlib.pyplot as plt
import main


get_np = np.load('study/svd_study/three_eyes.npy')


#もとの行列を(27, 27, 27)のテンソルとして、tucker分解
def tucker(X, r):  #特異値を全て残す
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
    C1 = C1.transpose(0, 2, 1)                      #tensordotの計算によるテンソルの順番を調整
    C = np.tensordot(C1, VL, (0,0))  
    C = C.transpose(2, 0, 1)         
    #復元
    Y2 = np.tensordot(C, VRt, (2,0))  
    Y1 = np.tensordot(Y2, VMt, (1,0))
    Y1 = Y1.transpose(0, 2, 1)
    Y = np.tensordot(Y1, VLt, (0,0))
    Y = Y.transpose(2, 0, 1)  
    #圧縮率
    rate = (VRt.size + VMt.size + VLt.size + C.size) / X.size
    return [Y.reshape(3,3,3,3,3,3,3,3,3), rate]

#tucker(get_np, 27)


def make_plot():             
    x = []
    #battle#
    y1 = []                                  #originalが勝つ割合
    y2 = []                                  #svdが勝つ割合
    y3 = []                                  #引き分けの割合
    #frobenius#
    y4 = []
    X = get_np.reshape(27, 27, 27)       
    norm = np.sqrt(np.sum(X * X))                      
    for i in range(0, 28):
        #battle#
        y1.append(main.battle(get_np, tucker(get_np, i)[0])[0])
        y2.append(main.battle(get_np, tucker(get_np, i)[0])[1])
        y3.append(main.battle(get_np, tucker(get_np, i)[0])[2])
        #frobenius#
        Y = tucker(get_np, i)[0].reshape(27, 27, 27)
        rate = tucker(get_np, i)[1]
        norm1 = np.sqrt(np.sum((X-Y) * (X-Y)))    
        x.append(rate)
        y4.append(norm1 / norm)
    #battle#
    plt.xlabel("compression ratio")
    plt.plot(x, y1, color = 'red')
    plt.plot(x, y2, color = 'blue')
    plt.plot(x, y3, color = 'green')
    #frobenius#
    plt.plot(x, y4, color = 'black')

    plt.show()


make_plot()