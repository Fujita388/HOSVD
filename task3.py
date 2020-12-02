###svdとhosvdの比較(グラフを重ねる)###





import numpy as np
from scipy import linalg
import matplotlib.pyplot as plt
import main
import task2


get_np = np.load('study/svd/three_eyes.npy')


#もとの評価値の配列をsvdする            r:残す特異値の数   
def approx(original_np, r):
    #svd#
    X = original_np.reshape(81, 243)
    u, s, v = linalg.svd(X)                 
    ur = u[:, :r]
    sr = np.diag(np.sqrt(s[:r]))                 #sの平方根
    vr = v[:r, :]
    A = ur @ sr
    B = sr @ vr
    #データの復元#
    svd_np1 = np.array(A @ B)
    svd_np = svd_np1.reshape((3,3,3,3,3,3,3,3,3))     #もとの配列に復元
    rate = (A.size+B.size) / X.size
    return [svd_np, rate]


#(81, 243)の行列をsvd vs (27, 27, 27)のテンソルをhosvd  originalとhosvdの勝率を比較
def make_plot():             
    x1 = []
    x2 = []
    y1 = []                                  #svd
    y2 = []                                  #tucker                    
    for i in range(0, 82):
        y1.append(main.battle(get_np, approx(get_np, i)[0])[0])
        x1.append(approx(get_np, i)[1])
    for j in range(0, 28):
        y2.append(main.battle(get_np, task2.tucker(get_np, j)[0])[0])
        x2.append(task2.tucker(get_np, j)[1])
    plt.xlabel("compression ratio")
    plt.plot(x1, y1, color = 'red')
    plt.plot(x2, y2, color = 'blue')

    plt.show()


#make_plot()

#(81, 243)の行列をsvd vs (27, 27, 27)のテンソルをhosvd  originalとhosvdの勝率の"差"を比較
def make_plot1():             
    x1 = []
    x2 = []
    y1 = []                                  #svd
    y2 = []                                  #tucker                    
    for i in range(0, 82):
        y1.append(main.battle(get_np, approx(get_np, i)[0])[0] - main.battle(get_np, approx(get_np, i)[0])[1])
        x1.append(approx(get_np, i)[1])
    for j in range(0, 28):
        y2.append(main.battle(get_np, task2.tucker(get_np, j)[0])[0] - main.battle(get_np, task2.tucker(get_np, j)[0])[1])
        x2.append(task2.tucker(get_np, j)[1])
    plt.xlabel("compression ratio")
    plt.plot(x1, y1, color = 'red')
    plt.plot(x2, y2, color = 'blue')

    plt.show()


make_plot1()