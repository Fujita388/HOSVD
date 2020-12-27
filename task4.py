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


#SVD vs HOSVD(datファイル作成)
def iteration():
	with open("task4.dat", "w") as f:
		f.write("{} {} {} {}\n".format(cmpr(0,0,0)[0], cmpr(0,0,0)[1], cmpr(0,0,0)[2], cmpr(0,0,0)[3]))
		f.write("{} {} {} {}\n".format(cmpr(0.08,5,2)[0], cmpr(0.08,5,2)[1], cmpr(0.08,5,2)[2], cmpr(0.08,5,2)[3]))
		f.write("{} {} {} {}\n".format(cmpr(0.13,8,12)[0], cmpr(0.13,8,12)[1], cmpr(0.13,8,12)[2], cmpr(0.13,8,12)[3]))
		f.write("{} {} {} {}\n".format(cmpr(0.20,12,14)[0], cmpr(0.20,12,14)[1], cmpr(0.20,12,14)[2], cmpr(0.20,12,14)[3]))
		f.write("{} {} {} {}\n".format(cmpr(0.31,19,17)[0], cmpr(0.31,19,17)[1], cmpr(0.31,19,17)[2], cmpr(0.31,19,17)[3]))
		f.write("{} {} {} {}\n".format(cmpr(0.43,26,19)[0], cmpr(0.43,26,19)[1], cmpr(0.43,26,19)[2], cmpr(0.43,26,19)[3]))
		f.write("{} {} {} {}\n".format(cmpr(0.80,49,24)[0], cmpr(0.80,49,24)[1], cmpr(0.80,49,24)[2], cmpr(0.80,49,24)[3]))
		f.write("{} {} {} {}\n".format(cmpr(1,61,26)[0], cmpr(1,61,26)[1], cmpr(1,61,26)[2], cmpr(1,61,26)[3]))



#iteration()


#5回分の標準偏差を算出しdatファイルを作成
def std_calc():
	with open("task4.dat", "w") as f:
		x1 = []   #hosvd
		x2 = []   #svd
		x3 = []   #引き分け
		for _ in range(5):
			x1.append(cmpr(0,0,0)[1])
			x2.append(cmpr(0,0,0)[2])
			x3.append(cmpr(0,0,0)[3])
		ans1 = np.std(x1)
		ans2 = np.std(x2)
		ans3 = np.std(x3)
		f.write("{} {} {}\n".format(ans1, ans2, ans3))


std_calc()


#追記用
def std_calc1():
	with open("task4_std.dat", "a") as f:
		x1 = []   #hosvd
		x2 = []   #svd
		x3 = []   #引き分け
		for _ in range(5):
			x1.append(cmpr(1,61,26)[1])
			x2.append(cmpr(1,61,26)[2])
			x3.append(cmpr(1,61,26)[3])
		ans1 = np.std(x1)
		ans2 = np.std(x2)
		ans3 = np.std(x3)
		f.write("{} {} {}\n".format(ans1, ans2, ans3))

#std_calc1()




