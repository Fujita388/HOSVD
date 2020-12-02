# Using HOSVD(Higher-Order SVD) for data-approximation of Tic-Tac-Toe AI


## Summary
SVD does not take into account the multidimensionality of data. Compared with SVD, HOSVD is more useful for the approximation of higher-order data.


## task1.py  
1. もとの行列を(81, 243）のテンソルとして、HOSVD、圧縮

   ※ただし、残す特異値の数の比を1:3にする
   
2. 戦績、フロベニウスノルムと圧縮率の関係をプロット
           
       
## task2.py 
 1. もとの行列を(27, 27, 27）のテンソルとして、HOSVD、圧縮
 
 2. 戦績、フロベニウスノルムと圧縮率の関係をプロット
