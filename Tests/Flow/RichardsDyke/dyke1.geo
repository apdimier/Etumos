Point( 1) = { 0.0,  0.0, 0, 1e+22};
Point(11) = {15.0,  0.0, 0, 1e+22};
Point(12) = {24.0,  0.0, 0, 1e+22};
Point(13) = {28.0,  0.0, 0, 1e+22};
Point(14) = {37.0,  0.0, 0, 1e+22};
Point(15) = {22.5,  8.5, 0, 1e+22};
Point(16) = {22.5,  0.0, 0, 1e+22};
Point( 2) = {52.0,  0.0, 0, 1e+22};
Point( 3) = {52.0,  6.0, 0, 1e+22};
Point( 4) = {37.0,  6.0, 0, 1e+22};
Point( 5) = {28.0,  9.0, 0, 1e+22};
Point( 6) = {24.0,  9.0, 0, 1e+22};
Point( 7) = {15.0,  6.0, 0, 1e+22};
Point( 8) = { 0.0,  6.0, 0, 1e+22};
Line( 1) = { 1,11};
Line( 2) = {11,16};
Line( 3) = {12,13};
Line( 4) = {13,14};
Line( 5) = {14, 2};
Line( 6) = { 2, 3};
Line( 7) = { 3, 4};
Line( 8) = { 4, 5};
Line( 9) = { 5, 6};
Line(10) = { 15, 7};
Line(11) = { 7, 8};
Line(12) = { 8, 1};

Line(13) = {11, 7};
Line(14) = {12, 6};
Line(15) = {14, 4};
Line(16) = { 5,13};
Line(17) = { 6, 15};
Line(18) = {16,12};
Line(19) = {16,15};
Transfinite Line {1,11}    = 16 Using Progression 1;
Transfinite Line {12,13}  =  7 Using Progression 1;
Transfinite Line {2,10}  =    10 Using Progression 1;
Transfinite Line {14}  =    7 Using Progression 1;
Line Loop(1) = {1, 13, 11, 12};
Plane Surface(1) = {1};

Transfinite Line {5,-7}    = 16 Using Progression 1.1;
Transfinite Line {6,-15}  =  7 Using Progression 1;
Line Loop(2) = {5, 6, 7,-15};
Plane Surface(2) = {2};

Transfinite Line {3, 9}     = 10 Using Progression 1;
Transfinite Line {19, 14,-16}  =  7 Using Progression 1;
Line Loop(3) = {3,-16, 9,-14};
Plane Surface(3) = {3};

Transfinite Line {2}    = 15 Using Progression 1;
Transfinite Line {10}   = 15 Using Progression 1;
Transfinite Line {17, 18}   = 4 Using Progression 1;
Transfinite Line {14,-13}  =  7 Using Progression 1;
Line Loop(4) = {2, 19, 10, -13};
Plane Surface(4) = {4};


Transfinite Line {4,8}    = 18 Using Progression 1;
Line Loop(5) = {4, 15, 8,16};
Plane Surface(5) = {5};


Line Loop(6) = {18, 14, 17, -19};
Plane Surface(6) = {6};

Transfinite Surface {1};
Recombine Surface {1};

Transfinite Surface {2};
Recombine Surface {2};

Transfinite Surface {3};
Recombine Surface {3};

Transfinite Surface {4};
Recombine Surface {4};

Transfinite Surface {5};
Recombine Surface {5};

Transfinite Surface {6};
Recombine Surface {6};
Show "*";

/*Physical Line("bottom") = {1, 2, 18, 3, 4, 5};
Physical Line("LeftWall") = {12};
Physical Line("RightWall") = {6};
Physical Line("WetRight") = {7};
Physical Line("WetLeft") = {11, 10};
Physical Line("DryDike") = {7, 9, 8};
*/
//Physical Line("bottom") = {1, 2, 18, 3, 4, 5};
Physical Surface("dyke") = {1, 4, 3, 5, 2, 6};
Physical Line("LeftWall") = {12};
Physical Line("RightWall") = {6};
//Physical Line("Top") = {7,8,9,10,11,17};
Show "*";
