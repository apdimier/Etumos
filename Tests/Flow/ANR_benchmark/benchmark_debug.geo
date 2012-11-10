factor = 1;

nx1=9*factor;
nx2=3*factor;
nx3=3*factor;
nx4=12*factor;
nx5=3*factor;
nx6=12*factor;
nx7=3*factor;
nx8=12*factor;
nx = nx1 + nx2 + nx3 + nx4 + nx5 + nx6 + nx7 + nx8;

ny1 = 6*factor;
ny2 = 6*factor;
ny3 = 3*factor;
ny4 = 9*factor;
ny5 = 12*factor;

ny = ny1 + ny2 + ny3 + ny4 + ny5;

L1=     75.;
L2=L1+  25.;
L3=L2+  25.;
L4=L3+ 100.;
L5=L4+  25.;
L6=L5+ 100.;
L7=L6+  25.;
L8=L7+ 100.;

H1=     50.;
H2=H1+  50.;
H3=H2+  25.;
H4=H3+  75.;
H5=H4+ 100.;

Point (1) = { 0, 0, 0, 0.1};
Point (2) = {L1, 0, 0, 0.1};
Point (3) = {L2, 0, 0, 0.1};
Point (4) = {L3, 0, 0, 0.1};
Point (5) = {L4, 0, 0, 0.1};
Point (6) = {L5, 0, 0, 0.1};
Point (7) = {L6, 0, 0, 0.1};
Point (8) = {L7, 0, 0, 0.1};
Point (9) = {L8, 0, 0, 0.1};

Point (11) = { 0, H1, 0, 0.1};
Point (12) = {L1, H1, 0, 0.1};
Point (13) = {L2, H1, 0, 0.1};
Point (14) = {L3, H1, 0, 0.1};
Point (15) = {L4, H1, 0, 0.1};
Point (16) = {L5, H1, 0, 0.1};
Point (17) = {L6, H1, 0, 0.1};
Point (18) = {L7, H1, 0, 0.1};
Point (19) = {L8, H1, 0, 0.1};

Point (21) = { 0, H2, 0, 0.1};
Point (22) = {L1, H2, 0, 0.1};
Point (23) = {L2, H2, 0, 0.1};
Point (24) = {L3, H2, 0, 0.1};
Point (25) = {L4, H2, 0, 0.1};
Point (26) = {L5, H2, 0, 0.1};
Point (27) = {L6, H2, 0, 0.1};
Point (28) = {L7, H2, 0, 0.1};
Point (29) = {L8, H2, 0, 0.1};

Point (31) = { 0, H3, 0, 0.1};
Point (32) = {L1, H3, 0, 0.1};
Point (33) = {L2, H3, 0, 0.1};
Point (34) = {L3, H3, 0, 0.1};
Point (35) = {L4, H3, 0, 0.1};
Point (36) = {L5, H3, 0, 0.1};
Point (37) = {L6, H3, 0, 0.1};
Point (38) = {L7, H3, 0, 0.1};
Point (39) = {L8, H3, 0, 0.1};

Point (41) = { 0, H4, 0, 0.1};
Point (42) = {L1, H4, 0, 0.1};
Point (43) = {L2, H4, 0, 0.1};
Point (44) = {L3, H4, 0, 0.1};
Point (45) = {L4, H4, 0, 0.1};
Point (46) = {L5, H4, 0, 0.1};
Point (47) = {L6, H4, 0, 0.1};
Point (48) = {L7, H4, 0, 0.1};
Point (49) = {L8, H4, 0, 0.1};

Point (51) = { 0, H5, 0, 0.1};
Point (52) = {L1, H5, 0, 0.1};
Point (53) = {L2, H5, 0, 0.1};
Point (54) = {L3, H5, 0, 0.1};
Point (55) = {L4, H5, 0, 0.1};
Point (56) = {L5, H5, 0, 0.1};
Point (57) = {L6, H5, 0, 0.1};
Point (58) = {L7, H5, 0, 0.1};
Point (59) = {L8, H5, 0, 0.1};


Line (71) = { 1, 2};
Line (72) = { 2, 3};
Line (73) = { 3, 4};
Line (74) = { 4, 5};
Line (75) = { 5, 6};
Line (76) = { 6, 7};
Line (77) = { 7, 8};
Line (78) = { 8, 9};


Line (81) = {11,12};
Line (82) = {12,13};
Line (83) = {13,14};
Line (84) = {14,15};
Line (85) = {15,16};
Line (86) = {16,17};
Line (87) = {17,18};
Line (88) = {18,19};

Line (91) = {21,22};
Line (92) = {22,23};
Line (93) = {23,24};
Line (94) = {24,25};
Line (95) = {25,26};
Line (96) = {26,27};
Line (97) = {27,28};
Line (98) = {28,29};

Line (101) = {31,32};
Line (102) = {32,33};
Line (103) = {33,34};
Line (104) = {34,35};
Line (105) = {35,36};
Line (106) = {36,37};
Line (107) = {37,38};
Line (108) = {38,39};

Line (111) = {41,42};
Line (112) = {42,43};
Line (113) = {43,44};
Line (114) = {44,45};
Line (115) = {45,46};
Line (116) = {46,47};
Line (117) = {47,48};
Line (118) = {48,49};

Line (121) = {51,52};
Line (122) = {52,53};
Line (123) = {53,54};
Line (124) = {54,55};
Line (125) = {55,56};
Line (126) = {56,57};
Line (127) = {57,58};
Line (128) = {58,59};

Line (131) = { 1,11};
Line (132) = {11,21};
Line (133) = {21,31};
Line (134) = {31,41};
Line (135) = {41,51};

Line (141) = { 2,12};
Line (142) = {12,22};
Line (143) = {22,32};
Line (144) = {32,42};
Line (145) = {42,52};

Line (151) = { 3,13};
Line (152) = {13,23};
Line (153) = {23,33};
Line (154) = {33,43};
Line (155) = {43,53};

Line (161) = { 4,14};
Line (162) = {14,24};
Line (163) = {24,34};
Line (164) = {34,44};
Line (165) = {44,54};

Line (171) = { 5,15};
Line (172) = {15,25};
Line (173) = {25,35};
Line (174) = {35,45};
Line (175) = {45,55};

Line (181) = { 6,16};
Line (182) = {16,26};
Line (183) = {26,36};
Line (184) = {36,46};
Line (185) = {46,56};

Line (191) = { 7,17};
Line (192) = {17,27};
Line (193) = {27,37};
Line (194) = {37,47};
Line (195) = {47,57};

Line (201) = { 8,18};
Line (202) = {18,28};
Line (203) = {28,38};
Line (204) = {38,48};
Line (205) = {48,58};

Line (211) = { 9,19};
Line (212) = {19,29};
Line (213) = {29,39};
Line (214) = {39,49};
Line (215) = {49,59};

Transfinite Line {71, 81, 91, 101, 111, 121} = nx1 Using Progression 1;
Transfinite Line {72, 82, 92, 102, 112, 122} = nx2 Using Progression 1;
Transfinite Line {73, 83, 93, 103, 113, 123} = nx3 Using Progression 1;
Transfinite Line {74, 84, 94, 104, 114, 124} = nx4 Using Progression 1;
Transfinite Line {75, 85, 95, 105, 115, 125} = nx5 Using Progression 1;
Transfinite Line {76, 86, 96, 106, 116, 126} = nx6 Using Progression 1;
Transfinite Line {77, 87, 97, 107, 117, 127} = nx7 Using Progression 1;
Transfinite Line {78, 88, 98, 108, 118, 128} = nx8 Using Progression 1;

Transfinite Line {131, 141, 151, 161, 171, 181, 191, 201, 211} = ny1 Using Progression 1;
Transfinite Line {132, 142, 152, 162, 172, 182, 192, 202, 212} = ny2 Using Progression 1;
Transfinite Line {133, 143, 153, 163, 173, 183, 193, 203, 213} = ny3 Using Progression 1;
Transfinite Line {134, 144, 154, 164, 174, 184, 194, 204, 214} = ny4 Using Progression 1;
Transfinite Line {135, 145, 155, 165, 175, 185, 195, 205, 215} = ny5 Using Progression 1;

Line Loop (221) = { 71,141, -81,-131};
Line Loop (231) = { 81,142, -91,-132};
Line Loop (241) = { 91,143,-101,-133};
Line Loop (251) = {101,144,-111,-134};
Line Loop (261) = {111,145,-121,-135};

Line Loop (222) = { 72,151, -82,-141};
Line Loop (232) = { 82,152, -92,-142};
Line Loop (242) = { 92,153,-102,-143};
Line Loop (252) = {102,154,-112,-144};
Line Loop (262) = {112,155,-122,-145};

Line Loop (223) = { 73,161, -83,-151};
Line Loop (233) = { 83,162, -93,-152};
Line Loop (243) = { 93,163,-103,-153};
Line Loop (253) = {103,164,-113,-154};
Line Loop (263) = {113,165,-123,-155};

Line Loop (224) = { 74,171, -84,-161};
Line Loop (234) = { 84,172, -94,-162};
Line Loop (244) = { 94,173,-104,-163};
Line Loop (254) = {104,174,-114,-164};
Line Loop (264) = {114,175,-124,-165};

Line Loop (225) = { 75,181, -85,-171};
Line Loop (235) = { 85,182, -95,-172};
Line Loop (245) = { 95,183,-105,-173};
Line Loop (255) = {105,184,-115,-174};
Line Loop (265) = {115,185,-125,-175};

Line Loop (226) = { 76,191, -86,-181};
Line Loop (236) = { 86,192, -96,-182};
Line Loop (246) = { 96,193,-106,-183};
Line Loop (256) = {106,194,-116,-184};
Line Loop (266) = {116,195,-126,-185};

Line Loop (227) = { 77,201, -87,-191};
Line Loop (237) = { 87,202, -97,-192};
Line Loop (247) = { 97,203,-107,-193};
Line Loop (257) = {107,204,-117,-194};
Line Loop (267) = {117,205,-127,-195};

Line Loop (228) = { 78,211, -88,-201};
Line Loop (238) = { 88,212, -98,-202};
Line Loop (248) = { 98,213,-108,-203};
Line Loop (258) = {108,214,-118,-204};
Line Loop (268) = {118,215,-128,-205};
//------------------------------------
Ruled Surface (221) = {221};Ruled Surface (231) = {231};Ruled Surface (241) = {241};Ruled Surface (251) = {251};Ruled Surface (261) = {261};
Ruled Surface (222) = {222};Ruled Surface (232) = {232};Ruled Surface (242) = {242};Ruled Surface (252) = {252};Ruled Surface (262) = {262};
Ruled Surface (223) = {223};Ruled Surface (233) = {233};Ruled Surface (243) = {243};Ruled Surface (253) = {253};Ruled Surface (263) = {263};
Ruled Surface (224) = {224};Ruled Surface (234) = {234};Ruled Surface (244) = {244};Ruled Surface (254) = {254};Ruled Surface (264) = {264};
Ruled Surface (225) = {225};Ruled Surface (235) = {235};Ruled Surface (245) = {245};Ruled Surface (255) = {255};Ruled Surface (265) = {265};
Ruled Surface (226) = {226};Ruled Surface (236) = {236};Ruled Surface (246) = {246};Ruled Surface (256) = {256};Ruled Surface (266) = {266};
Ruled Surface (227) = {227};Ruled Surface (237) = {237};Ruled Surface (247) = {247};Ruled Surface (257) = {257};Ruled Surface (267) = {267};
Ruled Surface (228) = {228};Ruled Surface (238) = {238};Ruled Surface (248) = {248};Ruled Surface (258) = {258};Ruled Surface (268) = {268};
//------------------------------------
Transfinite Surface {221} = { 1, 2,12,11};
Transfinite Surface {231} = {11,12,22,21};
Transfinite Surface {241} = {21,22,32,31};
Transfinite Surface {251} = {31,32,42,41};
Transfinite Surface {261} = {41,42,52,51};

Transfinite Surface {222} = { 2, 3,13,12};
Transfinite Surface {232} = {12,13,23,22};
Transfinite Surface {242} = {22,23,33,32};
Transfinite Surface {252} = {32,33,43,42};
Transfinite Surface {262} = {42,43,53,52};

Transfinite Surface {223} = { 3, 4,14,13};
Transfinite Surface {233} = {13,14,24,23};
Transfinite Surface {243} = {23,24,34,33};
Transfinite Surface {253} = {33,34,44,43};
Transfinite Surface {263} = {43,44,54,53};

Transfinite Surface {224} = { 4, 5,15,14};
Transfinite Surface {234} = {14,15,25,24};
Transfinite Surface {244} = {24,25,35,34};
Transfinite Surface {254} = {34,35,45,44};
Transfinite Surface {264} = {44,45,55,54};

Transfinite Surface {225} = { 5, 6,16,15};
Transfinite Surface {235} = {15,16,26,25};
Transfinite Surface {245} = {25,26,36,35};
Transfinite Surface {255} = {35,36,46,45};
Transfinite Surface {265} = {45,46,56,55};

Transfinite Surface {226} = { 6, 7,17,16};
Transfinite Surface {236} = {16,17,27,26};
Transfinite Surface {246} = {26,27,37,36};
Transfinite Surface {256} = {36,37,47,46};
Transfinite Surface {266} = {46,47,57,56};

Transfinite Surface {227} = { 7, 8,18,17};
Transfinite Surface {237} = {17,18,28,27};
Transfinite Surface {247} = {27,28,38,37};
Transfinite Surface {257} = {37,38,48,47};
Transfinite Surface {267} = {47,48,58,57};

Transfinite Surface {228} = { 8, 9,19,18};
Transfinite Surface {238} = {18,19,29,28};
Transfinite Surface {248} = {28,29,39,38};
Transfinite Surface {258} = {38,39,49,48};
Transfinite Surface {268} = {48,49,59,58};

Recombine Surface {221,231,241,251,261,222,232,242,252,262,223,233,243,253,263,224,234,244,254,264,225,235,245,255,265,226,236,246,256,266,227,237,247,257,267,228,238,248,258,268};

Physical Line("inlet1") = {131,132};
Physical Line("inlet2") = {126};
Physical Line("outlet") = {2111, 212, 213, 214, 215};

Physical Surface("rock")        = {223, 233, 243, 253,    245, 255, 265,    237, 247, 257, 267};
Physical Surface("co2")         = {252, 262, 263, 254, 264};
Physical Surface("water")       = {221, 231, 241, 251, 261,    222, 232, 242,    224, 234, 244,    225, 235,    226, 236, 246, 256, 266,    227,     228, 238, 248, 258, 268};

