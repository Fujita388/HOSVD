####SVDした関数とHOSVDした関数を戦わせる####



import numpy as np
from scipy import linalg
import matplotlib.pyplot as plt
import main


get_np = np.load('../svd/three_eyes.npy') 


#もとの行列を(27, 27, 27)のテンソルとして、HOSVD
def hosvd(X, r):  
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
    return [Y.reshape((3,3,3,3,3,3,3,3,3)), rate]


#もとの評価値を(81, 243)の行列としてSVD            r:残す特異値の数   
def svd(X, r):
    #svd#
    X = X.reshape(81, 243)
    u, s, v = linalg.svd(X)                 
    ur = u[:, :r]
    sr = np.diag(np.sqrt(s[:r]))                 #sの平方根
    vr = v[:r, :]
    A = ur @ sr
    B = sr @ vr
    #データの復元#
    svd = np.array(A @ B)
    rate = (A.size+B.size) / X.size
    return [svd.reshape((3,3,3,3,3,3,3,3,3)), rate]


#SVD vs HOSVD(同じ圧縮率で対戦)
def cmpr(rate, num_svd, num_hosvd):  #圧縮率、svd特異値数、hosvd特異値数
	y1 = main.battle(hosvd(get_np, num_hosvd)[0], svd(get_np, num_svd)[0])[0]  #hosvdの勝率
	y2 = main.battle(hosvd(get_np, num_hosvd)[0], svd(get_np, num_svd)[0])[1]  #svdの勝利
	y3 = main.battle(hosvd(get_np, num_hosvd)[0], svd(get_np, num_svd)[0])[2]  #引き分け
	return [rate, y1, y2, y3]


#SVD vs HOSVD
#5回分の平均と標準偏差を算出しdatファイルを作成
def std_calc():
	rate = [0.0, 0.08, 0.13, 0.20, 0.31, 0.43, 0.80, 1.0]
	num_svd = [0, 5, 8, 12, 19, 26, 49, 61]
	num_hosvd = [0, 2, 12, 14, 17, 19, 24, 26]
	with open("task4.dat", "w") as f:
		for i, j, k in zip(rate, num_svd, num_hosvd):
			x = cmpr(i, j, k)[0]   #圧縮率
			y1 = []   #hosvd
			y2 = []   #svd
			y3 = []   #引き分け
			for _ in range(5):
				y1.append(cmpr(i, j, k)[1])
				y2.append(cmpr(i, j, k)[2])
				y3.append(cmpr(i, j, k)[3])
			y1_m = np.mean(y1)
			y2_m = np.mean(y2)
			y3_m = np.mean(y3)
			y1_std = np.std(y1)
			y2_std = np.std(y2)
			y3_std = np.std(y3)
			f.write("{} {} {} {} {} {} {}\n".format(x, y1_m, y2_m, y3_m, y1_std, y2_std, y3_std))


std_calc()





