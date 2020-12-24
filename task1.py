####もとの行列を(81, 243)として、tucker分解####
#ただし残す特異値は1:3



import numpy as np
from scipy import linalg
import matplotlib.pyplot as plt
import main


get_np = np.load('../svd/three_eyes.npy')               


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
	#フロべニウスノルムの相対誤差
	norm = np.sqrt(np.sum(X * X))
	norm1 = np.sqrt(np.sum((X-Y) * (X-Y)))
	frob = norm1 / norm
	return [Y.reshape(3,3,3,3,3,3,3,3,3), rate, frob]

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

#make_plot()


#5回分の平均と標準偏差を算出しdatファイルを作成
def save_file():
	with open("task1.dat", "w") as f:
		for i in range(0, 81):
			#圧縮率
			x = tucker(get_np, i)[1]  
			#battle 
			y1 = []
			y2 = []
			y3 = []
			for _ in range(5):
				y1.append(main.battle(get_np, tucker(get_np, i)[0])[0])   #originalが勝つ割合
				y2.append(main.battle(get_np, tucker(get_np, i)[0])[1])   #svdが勝つ割合 
				y3.append(main.battle(get_np, tucker(get_np, i)[0])[2])   #引き分けの割合
			y1_m = np.mean(y1)
			y2_m = np.mean(y2)
			y3_m = np.mean(y3)
			y1_std = np.std(y1)
			y2_std = np.std(y2)
			y3_std = np.std(y3)
			#frobenius
			y4 = tucker(get_np, i)[2] 
			f.write("{} {} {} {} {} {} {} {}\n".format(x, y1_m, y2_m, y3_m, y4, y1_std, y2_std, y3_std))


save_file()




















