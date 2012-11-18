Point(1) = {0, 0, 0, 1e+22};
Point(2) = {0.30, 0, 0, 1e+22};
Point(3) = {0.30, 0.01, 0, 1e+22};
Point(4) = {0, 0.01, 0, 1e+22};
Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};
Line Loop(6) = {1, 2, 3, 4};
Plane Surface(6) = {6};
Transfinite Line {1,3} = 151 Using Progression 1;
Transfinite Line {2,4} = 2 Using Progression 1;
Transfinite Surface {6} = {1,2,3,4};
Recombine Surface {6};
Physical Line("inlet") = {4};
Physical Surface("domain") = {6};
