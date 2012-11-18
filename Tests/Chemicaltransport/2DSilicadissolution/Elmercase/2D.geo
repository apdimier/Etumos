nx=71;
ny=71;
nx1=20;
nx2=3;
nx3=34;
ny1=34;
ny2=3;
L1=0.995;
L2=1.005;
L3=2;
H1=0.995;
H2=1.005;
H3=2;
Point (1) = {0, 0, 0, 0.1};
Point (2) = {L1, 0, 0, 0.1};
Point (3) = {L2, 0, 0, 0.1};
Point (4) = {L3, 0, 0, 0.1};
Point (5) = {L3, H1, 0, 0.1};
Point (6) = {L3, H2, 0, 0.1};
Point (7) = {L3, H3, 0, 0.1};
Point (8) = {L2, H3, 0, 0.1};
Point (9) = {L1, H3, 0, 0.1};
Point (10) = {0, H3, 0, 0.1};
Point (11) = {0, H2, 0, 0.1};
Point (12) = {0, H1, 0, 0.1};
Point (13) = {L1, H1, 0, 0.1};
Point (14) = {L2, H1, 0, 0.1};
Point (15) = {L2, H2, 0, 0.1};
Point (16) = {L1, H2, 0, 0.1};
Line (1) = {1, 2};Line (2) = {2, 3};Line (3) = {3, 4};
Line (4) = {4, 5};Line (5) = {5, 6};Line (6) = {6, 7};
Line (7) = {7, 8};Line (8) = {8, 9};Line (9) = {9, 10};
Line (10) = {10, 11};Line (11) = {11, 12};Line (12) = {12, 1};
Line (13) = {2, 13};
Line (14) = {3, 14};
Line (15) = {14, 15};

Line (16) = {13, 16};
Line (17) = {15, 8};
Line (18) = {16, 9};
Line (19) = {14, 5};
Line (20) = {13, 14};
Line (21) = {13, 12};
Line (22) = {15, 6};
Line (23) = {16, 11};
Line (24) = {15, 16};

Transfinite Line {1, 9, 21, 23} = nx1 Using Progression 1;
Transfinite Line {2, 8, 20, 24} = nx2 Using Progression 1;
Transfinite Line {3, 7, 19, 22} = nx3 Using Progression 1;
Transfinite Line {4, 12, 13, 14} = ny1 Using Progression 1;
Transfinite Line {5, 11, 15, 16} = ny2 Using Progression 1;
Transfinite Line {6, 10, 17, 18} = ny1 Using Progression 1;

Line Loop (22) = {1, 13, 21, 12};Ruled Surface (22) = {22};

Line Loop (23) = {-21, 16, 23, 11};Ruled Surface (23) = {23};

Line Loop (24) = {-23, 18, 9, 10};Ruled Surface (24) = {24};

Line Loop (25) = {2, 14, -20, -13};Ruled Surface (25) = {25};

Line Loop (26) = {20, 15, 24, -16};Ruled Surface (26) = {26};

Line Loop (27) = {-24, 17, 8, -18};Ruled Surface (27) = {27};

Line Loop (28) = {3, 4, -19, -14};Ruled Surface (28) = {28};

Line Loop (29) = {19, 5, -22, -15};Ruled Surface (29) = {29};

Line Loop (30) = {22, 6, 7, -17};Ruled Surface (30) = {30};

Transfinite Surface {22} = {1,2,13,12};
Transfinite Surface {23} = {12,13,16,11};
Transfinite Surface {24} = {11,16,9,10};

Transfinite Surface {25} = {2, 3, 14, 13};
Transfinite Surface {26} = {13, 14, 15, 16};
Transfinite Surface {27} = {16, 15, 8, 9};

Transfinite Surface {28} = {3, 4, 5, 14};
Transfinite Surface {29} = {14, 5, 6, 15};
Transfinite Surface {30} = {15, 6, 7, 8};

Recombine Surface {22, 23, 24, 25, 26, 27, 28, 29, 30};

Physical Line("inlet") = {4, 5, 6};
Physical Line("outlet") = {10, 11, 12};
Physical Line("symmetry") = {1, 2, 3, 7, 8, 9};
Physical Surface("domain1") = {26};
Physical Surface("domain") = {22, 23, 24, 25, 27, 28, 29, 30};
