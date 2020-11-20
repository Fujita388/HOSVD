####もとの行列を(81, 243)として、tucker分解####



import numpy as np
from scipy import linalg
import matplotlib.pyplot as plt
import main


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
    return [Y.reshape(3,3,3,3,3,3,3,3,3), rate]

#tucker(get_np, 81)



#戦績、フロベニウスノルムの相対誤差と圧縮率のグラフをプロット
def make_plot():             
    x = []
    #battle#
    y1 = []                                  #originalが勝つ割合
    y2 = []                                  #svdが勝つ割合
    y3 = []                                  #引き分けの割合
    #frobenius#
    y4 = []
    X = get_np.reshape(81, 243)       
    norm = np.sqrt(np.sum(X * X))                      
    for i in range(0, 28):
        #battle#
        y1.append(main.battle(get_np, tucker(get_np, i)[0])[0])
        y2.append(main.battle(get_np, tucker(get_np, i)[0])[1])
        y3.append(main.battle(get_np, tucker(get_np, i)[0])[2])
        #frobenius#
        Y = tucker(get_np, i)[0].reshape(81, 243)
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



