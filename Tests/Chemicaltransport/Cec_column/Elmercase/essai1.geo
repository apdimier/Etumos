Point(1) = {0, 0, 0, 1e+22};
Point(2) = {0.04, 0, 0, 1e+22};
Point(3) = {0.04, 0.01, 0, 1e+22};
Point(4) = {0, 0.01, 0, 1e+22};
Point(5) = {0, 0.01, 0, 1e+22};
Point(6) = {0, 0.01, 0, 1e+22};
Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};
Line Loop(6) = {1, 2, 3, 4};
Plane Surface(6) = {6};
