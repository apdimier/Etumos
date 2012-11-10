#
# study name: fresh water comparison to Duan results
#
set title "analytic solution: erfc\n"
#
# Article: 	Carslaw / Jeager
#                Conduction of heat in solids
#
#set label 1 "Sim. date 22.11.2010" at graph 0.9,-0.1 center
set xlabel " space"
set ylabel " charge"
show label
set autoscale
set grid
k0=1.0000000000e-04
h0=1.123456e+00
t = 40.0
plot [0:0.5] h0*erfc(x/(2*sqrt(k0*t)) )with points
pause -1 "Hit return to continue"
#set terminal png
#set output 'temperature.png'
#set terminal png
#set output 'co2solubility_1m.png'
#replot

