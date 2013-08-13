nx=201;
Point(1) = {0.0, 0, 0, 1e+22};
Point(2) = {0.43, 0, 0, 1e+22};
Line(3) = {1, 2};
//Transfinite Line {1} = nx Using Progression 1.02;
Transfinite Line {3} = nx Using Progression 1.02;
Physical Point("inlet") = {1};
Physical Line("domain") = {3};
