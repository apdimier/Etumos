Point(1) = {-0.1, -0.1, 0, 1e+22};
Point(2) = {0.1, -0.1, 0, 1e+22};
Point(3) = {0.1, 0.1, 0, 1e+22};
Point(4) = {-0.1, 0.1, 0, 1e+22};
Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};
Line Loop(6) = {1, 2, 3, 4};
Plane Surface(8) = {6};
Transfinite Line {1, 2, 3, 4} = 11 Using Progression 1;
Transfinite Surface {8} = {1,2,3,4};
Recombine Surface {8};
Physical Line("AB") = {1};
Physical Line("BC") = {2};
Physical Line("CD") = {3};
Physical Line("DA") = {4};
Physical Surface("domain") = {8};
Show "*";

Show "*";

