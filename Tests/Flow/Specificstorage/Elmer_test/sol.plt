#
# study name: fresh water comparison to Duan results
#
set title "comparison of analytical solution: erfc\n with Elmer results"
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
f(x) = h0*erfc(x/(2*sqrt(k0*t)) )
set label 1 "Comparison of Elmer results to" at graph 0.35,0.7  
set label 4 "the analytical solution h0*erfc(x/(2*sqrt(k0*t/h0))" at graph 0.35,0.65  
set label 2 "K = 1.e-4" at graph 0.35,0.55
set label 3 "H0 = 1.23456" at graph 0.35,0.5 
plot 'result21' using 1:2 title 'Elmer' with points, f(x) title 'analytical' with lines
pause -1 "Hit return to continue"
set terminal png
set output 'Elmer_analytic_comparison_21.png'
#set terminal png
#set output 'co2solubility_1m.png'
replot

