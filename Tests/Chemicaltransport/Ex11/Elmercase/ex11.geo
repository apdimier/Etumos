nx = 41;
ny = 1;
L = 0.08;
H = 0.01;
Point(1) = {0.0,0.0,0,0.1};
Point(2) = {L,0.0,0,0.1};
Line(3) = {1,2};
Transfinite Line {3} = nx Using Progression 1;
Physical Point("inlet") = {1};
Physical Line("domain") = {3};