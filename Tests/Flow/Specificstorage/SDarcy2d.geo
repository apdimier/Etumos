Point(1) = {0.0,  0.0, 0, 1e+22};
Point(2) = {1.0,  0.0, 0, 1e+22};
Point(3) = {1.0,  0.1, 0, 1e+22};
Point(4) = {0.0,  0.1, 0, 1e+22};
Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};
Line Loop(6) = {1, 2, 3, 4};
Plane Surface(8) = {6};
Transfinite Line {1,-3} = 21 Using Progression 1.1;
Transfinite Line {2, 4} =  3 Using Progression 1;
Transfinite Surface {8} = {1,2,3,4};
Recombine Surface {8};
Physical Line("AB") = {4};
Physical Surface("domain") = {8};
Show "*";

Show "*";

