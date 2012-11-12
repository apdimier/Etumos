nx = 101;
ny = 2;
L = 0.04;
H = 0.01;
Point(1) = {0.0,0.0,0,0.1};
Point(2) = {L,0.0,0,0.1};
Point(3) = {L,H,0,0.1};
Point(4) = {0,H,0,0.1};
Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};
Line Loop(5) = {1,2,3,4};
Plane Surface(6) = {5};
Transfinite Line {1,3} = nx Using Progression 1;
Transfinite Line {2,4} = ny Using Progression 1;
Transfinite Surface {6} = {1,2,3,4};
Recombine Surface {6};
Physical Line("inlet") = {4};
Physical Line("outlet") = {2};
Physical Surface("domain") = {6};

