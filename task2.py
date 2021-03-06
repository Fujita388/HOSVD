####もとの行列を(27, 27, 27)のテンソルとして、tucker分解####



import numpy as np
from scipy import linalg
import matplotlib.pyplot as plt
import main


get_np = np.load('../svd/three_eyes.npy')


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
	#フロべニウスノルムの相対誤差
	norm = np.sqrt(np.sum(X * X))
	norm1 = np.sqrt(np.sum((X-Y) * (X-Y)))    
	frob = norm1 / norm  
	return [Y.reshape((3,3,3,3,3,3,3,3,3)), rate, frob]

#tucker(get_np, 27)



#matplotlibで図を作成
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
        Y = tucker(get_np, i)[0].reshape((27, 27, 27))
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
	with open("task2.dat", "w") as f:
		for i in range(0, 28):
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


































