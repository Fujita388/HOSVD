set term pdf
set out "task4_axis.pdf"
set xlabel "圧縮率" font "Arial,15"
set ylabel "勝率" font "Arial,15"
set xrange [-0.1:1.1]
set yrange [0:0.5]
set key right center font "Arial,10"
set key font "Arial,14"
p "task4.dat" u 1:2:5 pt 6 ps 0.3 lt rgb 'red' w yerrorlines t "{/Times:Italic:Bold f}_{HOSVD}の勝率",\
 "task4.dat" u 1:3:6 pt 2 ps 0.3 lt rgb 'blue' w yerrorlines t "{/Times:Italic:Bold f}_{SVD}の勝率",\
