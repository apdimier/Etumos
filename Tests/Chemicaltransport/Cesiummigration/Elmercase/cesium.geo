nx=101;
ny=2;
nx1=101;
ny1=2;
L1=0.001*nx1;
H1=0.001*ny1;
Point (1) = {0, 0, 0, 1.e+22};
Point (2) = {L1, 0, 0, 1.e+22};
Point (3) = {L1, H1, 0, 1.e+22};
Point (4) = {0, H1, 0, 1.e+22};
Line (1) = {1, 2};
Line (2) = {2, 3};
Line (3) = {3, 4};
Line (4) = {4, 1};
Line Loop (8) = {1, 2, 3, 4};
Transfinite Line {1, 3} = nx1 Using Progression 1;
Transfinite Line {2, 4} = ny1 Using Progression 1;

Ruled Surface (8) = {8};
Transfinite Surface {8} = {1,2,3,4};
Recombine Surface {8};

Physical Line("inlet") = {4};
Physical Line("outlet") = {2};
Physical Surface("domain") = {8};
Recombine Surface {8};

