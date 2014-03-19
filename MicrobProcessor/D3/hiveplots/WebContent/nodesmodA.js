var nodes = [
  {axis: 4, pos: 0.01, mod: 1, ind: 1},
  {axis: 2, pos: 0.01, mod: 1, ind: 1},
  {axis: 4, pos: 0.03, mod: 1, ind: 1},
  {axis: 2, pos: 0.03, mod: 1, ind: 1},
  {axis: 4, pos: 0.04, mod: 1, ind: 1},
  {axis: 4, pos: 0.04, mod: 1, ind: 1},
  {axis: 2, pos: 0.04, mod: 1, ind: 0},
  {axis: 4, pos: 0.04, mod: 1, ind: 1},
  {axis: 2, pos: 0.04, mod: 1, ind: 0},
  {axis: 4, pos: 0.05, mod: 1, ind: 1},
  {axis: 2, pos: 0.05, mod: 1, ind: 0},
  {axis: 4, pos: 0.06, mod: 1, ind: 1},
  {axis: 2, pos: 0.06, mod: 1, ind: 1},
  {axis: 4, pos: 0.07, mod: 1, ind: 1},
  {axis: 4, pos: 0.07, mod: 1, ind: 1},
  {axis: 2, pos: 0.07, mod: 1, ind: 1},
  {axis: 2, pos: 0.07, mod: 1, ind: 0},
  {axis: 0, pos: 0.07, mod: 1, ind: 1},
  {axis: 2, pos: 0.08, mod: 1, ind: 1},
  {axis: 2, pos: 0.08, mod: 1, ind: 1},
  {axis: 2, pos: 0.08, mod: 1, ind: 1},
  {axis: 4, pos: 0.08, mod: 1, ind: 1},
  {axis: 2, pos: 0.08, mod: 1, ind: 1},
  {axis: 2, pos: 0.08, mod: 1, ind: 1},
  {axis: 2, pos: 0.08, mod: 1, ind: 1},
  {axis: 2, pos: 0.08, mod: 1, ind: 0},
  {axis: 0, pos: 0.09, mod: 1, ind: 1},
  {axis: 2, pos: 0.09, mod: 1, ind: 1},
  {axis: 2, pos: 0.09, mod: 1, ind: 0},
  {axis: 2, pos: 0.09, mod: 1, ind: 1},
  {axis: 2, pos: 0.09, mod: 1, ind: 1},
  {axis: 4, pos: 0.09, mod: 1, ind: 1},
  {axis: 2, pos: 0.09, mod: 1, ind: 0},
  {axis: 4, pos: 0.09, mod: 1, ind: 1},
  {axis: 2, pos: 0.1, mod: 1, ind: 0},
  {axis: 2, pos: 0.1, mod: 1, ind: 1},
  {axis: 4, pos: 0.1, mod: 1, ind: 0},
  {axis: 4, pos: 0.1, mod: 1, ind: 1},
  {axis: 2, pos: 0.1, mod: 1, ind: 1},
  {axis: 2, pos: 0.11, mod: 1, ind: 0},
  {axis: 0, pos: 0.11, mod: 1, ind: 0},
  {axis: 2, pos: 0.11, mod: 1, ind: 1},
  {axis: 2, pos: 0.11, mod: 1, ind: 1},
  {axis: 2, pos: 0.11, mod: 1, ind: 0},
  {axis: 2, pos: 0.11, mod: 1, ind: 1},
  {axis: 2, pos: 0.11, mod: 1, ind: 1},
  {axis: 2, pos: 0.12, mod: 1, ind: 1},
  {axis: 2, pos: 0.12, mod: 1, ind: 0},
  {axis: 4, pos: 0.12, mod: 1, ind: 1},
  {axis: 4, pos: 0.12, mod: 1, ind: 1},
  {axis: 4, pos: 0.12, mod: 1, ind: 1},
  {axis: 2, pos: 0.12, mod: 1, ind: 1},
  {axis: 2, pos: 0.13, mod: 1, ind: 0},
  {axis: 2, pos: 0.13, mod: 1, ind: 1},
  {axis: 2, pos: 0.13, mod: 1, ind: 1},
  {axis: 2, pos: 0.14, mod: 1, ind: 1},
  {axis: 2, pos: 0.14, mod: 1, ind: 1},
  {axis: 4, pos: 0.14, mod: 1, ind: 1},
  {axis: 2, pos: 0.14, mod: 1, ind: 0},
  {axis: 2, pos: 0.15, mod: 1, ind: 1},
  {axis: 4, pos: 0.16, mod: 1, ind: 0},
  {axis: 0, pos: 0.16, mod: 1, ind: 1},
  {axis: 2, pos: 0.16, mod: 1, ind: 1},
  {axis: 2, pos: 0.16, mod: 1, ind: 1},
  {axis: 0, pos: 0.16, mod: 1, ind: 0},
  {axis: 2, pos: 0.16, mod: 1, ind: 1},
  {axis: 2, pos: 0.16, mod: 1, ind: 0},
  {axis: 2, pos: 0.17, mod: 1, ind: 0},
  {axis: 0, pos: 0.17, mod: 1, ind: 0},
  {axis: 2, pos: 0.17, mod: 1, ind: 1},
  {axis: 2, pos: 0.19, mod: 1, ind: 1},
  {axis: 2, pos: 0.2, mod: 1, ind: 1},
  {axis: 2, pos: 0.2, mod: 1, ind: 1},
  {axis: 2, pos: 0.21, mod: 1, ind: 1},
  {axis: 2, pos: 0.21, mod: 1, ind: 0},
  {axis: 2, pos: 0.21, mod: 1, ind: 0},
  {axis: 2, pos: 0.21, mod: 1, ind: 1},
  {axis: 2, pos: 0.22, mod: 1, ind: 0},
  {axis: 2, pos: 0.22, mod: 1, ind: 0},
  {axis: 2, pos: 0.22, mod: 1, ind: 1},
  {axis: 2, pos: 0.22, mod: 1, ind: 1},
  {axis: 2, pos: 0.22, mod: 1, ind: 0},
  {axis: 2, pos: 0.23, mod: 1, ind: 0},
  {axis: 2, pos: 0.23, mod: 1, ind: 1},
  {axis: 0, pos: 0.24, mod: 1, ind: 1},
  {axis: 4, pos: 0.24, mod: 1, ind: 0},
  {axis: 2, pos: 0.25, mod: 1, ind: 0},
  {axis: 2, pos: 0.25, mod: 1, ind: 1},
  {axis: 2, pos: 0.25, mod: 1, ind: 1},
  {axis: 2, pos: 0.26, mod: 1, ind: 0},
  {axis: 2, pos: 0.26, mod: 1, ind: 1},
  {axis: 0, pos: 0.26, mod: 1, ind: 0},
  {axis: 2, pos: 0.27, mod: 1, ind: 0},
  {axis: 2, pos: 0.27, mod: 1, ind: 0},
  {axis: 2, pos: 0.27, mod: 1, ind: 0},
  {axis: 4, pos: 0.27, mod: 1, ind: 0},
  {axis: 0, pos: 0.27, mod: 1, ind: 0},
  {axis: 0, pos: 0.27, mod: 1, ind: 0},
  {axis: 4, pos: 0.28, mod: 1, ind: 1},
  {axis: 2, pos: 0.28, mod: 1, ind: 0},
  {axis: 2, pos: 0.29, mod: 1, ind: 0},
  {axis: 2, pos: 0.29, mod: 1, ind: 0},
  {axis: 2, pos: 0.29, mod: 1, ind: 0},
  {axis: 2, pos: 0.32, mod: 1, ind: 0},
  {axis: 2, pos: 0.34, mod: 1, ind: 0},
  {axis: 2, pos: 0.35, mod: 1, ind: 0},
  {axis: 2, pos: 0.37, mod: 1, ind: 0},
  {axis: 2, pos: 0.37, mod: 1, ind: 1},
  {axis: 0, pos: 0.37, mod: 1, ind: 0},
  {axis: 2, pos: 0.37, mod: 1, ind: 0},
  {axis: 2, pos: 0.38, mod: 1, ind: 0},
  {axis: 2, pos: 0.4, mod: 1, ind: 0},
  {axis: 2, pos: 0.46, mod: 1, ind: 0},
  {axis: 0, pos: 0.46, mod: 1, ind: 0},
  {axis: 2, pos: 0.47, mod: 1, ind: 1},
  {axis: 0, pos: 0.51, mod: 1, ind: 0},
  {axis: 0, pos: 0.51, mod: 1, ind: 0},
  {axis: 2, pos: 0.84, mod: 1, ind: 0},
  {axis: 2, pos: 0.89, mod: 1, ind: 0},
  {axis: 2, pos: 1.0, mod: 1, ind: 0},
  {axis: 5, pos: 0.01, mod: 1, ind: 1},
  {axis: 3, pos: 0.01, mod: 1, ind: 1},
  {axis: 5, pos: 0.03, mod: 1, ind: 1},
  {axis: 3, pos: 0.03, mod: 1, ind: 1},
  {axis: 5, pos: 0.04, mod: 1, ind: 1},
  {axis: 5, pos: 0.04, mod: 1, ind: 1},
  {axis: 3, pos: 0.04, mod: 1, ind: 0},
  {axis: 5, pos: 0.04, mod: 1, ind: 1},
  {axis: 3, pos: 0.04, mod: 1, ind: 0},
  {axis: 5, pos: 0.05, mod: 1, ind: 1},
  {axis: 3, pos: 0.05, mod: 1, ind: 0},
  {axis: 5, pos: 0.06, mod: 1, ind: 1},
  {axis: 3, pos: 0.06, mod: 1, ind: 1},
  {axis: 5, pos: 0.07, mod: 1, ind: 1},
  {axis: 5, pos: 0.07, mod: 1, ind: 1},
  {axis: 3, pos: 0.07, mod: 1, ind: 1},
  {axis: 3, pos: 0.07, mod: 1, ind: 0},
  {axis: 1, pos: 0.07, mod: 1, ind: 1},
  {axis: 3, pos: 0.08, mod: 1, ind: 1},
  {axis: 3, pos: 0.08, mod: 1, ind: 1},
  {axis: 3, pos: 0.08, mod: 1, ind: 1},
  {axis: 5, pos: 0.08, mod: 1, ind: 1},
  {axis: 3, pos: 0.08, mod: 1, ind: 1},
  {axis: 3, pos: 0.08, mod: 1, ind: 1},
  {axis: 3, pos: 0.08, mod: 1, ind: 1},
  {axis: 3, pos: 0.08, mod: 1, ind: 0},
  {axis: 1, pos: 0.09, mod: 1, ind: 1},
  {axis: 3, pos: 0.09, mod: 1, ind: 1},
  {axis: 3, pos: 0.09, mod: 1, ind: 0},
  {axis: 3, pos: 0.09, mod: 1, ind: 1},
  {axis: 3, pos: 0.09, mod: 1, ind: 1},
  {axis: 5, pos: 0.09, mod: 1, ind: 1},
  {axis: 3, pos: 0.09, mod: 1, ind: 0},
  {axis: 5, pos: 0.09, mod: 1, ind: 1},
  {axis: 3, pos: 0.1, mod: 1, ind: 0},
  {axis: 3, pos: 0.1, mod: 1, ind: 1},
  {axis: 5, pos: 0.1, mod: 1, ind: 0},
  {axis: 5, pos: 0.1, mod: 1, ind: 1},
  {axis: 3, pos: 0.1, mod: 1, ind: 1},
  {axis: 3, pos: 0.11, mod: 1, ind: 0},
  {axis: 1, pos: 0.11, mod: 1, ind: 0},
  {axis: 3, pos: 0.11, mod: 1, ind: 1},
  {axis: 3, pos: 0.11, mod: 1, ind: 1},
  {axis: 3, pos: 0.11, mod: 1, ind: 0},
  {axis: 3, pos: 0.11, mod: 1, ind: 1},
  {axis: 3, pos: 0.11, mod: 1, ind: 1},
  {axis: 3, pos: 0.12, mod: 1, ind: 1},
  {axis: 3, pos: 0.12, mod: 1, ind: 0},
  {axis: 5, pos: 0.12, mod: 1, ind: 1},
  {axis: 5, pos: 0.12, mod: 1, ind: 1},
  {axis: 5, pos: 0.12, mod: 1, ind: 1},
  {axis: 3, pos: 0.12, mod: 1, ind: 1},
  {axis: 3, pos: 0.13, mod: 1, ind: 0},
  {axis: 3, pos: 0.13, mod: 1, ind: 1},
  {axis: 3, pos: 0.13, mod: 1, ind: 1},
  {axis: 3, pos: 0.14, mod: 1, ind: 1},
  {axis: 3, pos: 0.14, mod: 1, ind: 1},
  {axis: 5, pos: 0.14, mod: 1, ind: 1},
  {axis: 3, pos: 0.14, mod: 1, ind: 0},
  {axis: 3, pos: 0.15, mod: 1, ind: 1},
  {axis: 5, pos: 0.16, mod: 1, ind: 0},
  {axis: 1, pos: 0.16, mod: 1, ind: 1},
  {axis: 3, pos: 0.16, mod: 1, ind: 1},
  {axis: 3, pos: 0.16, mod: 1, ind: 1},
  {axis: 1, pos: 0.16, mod: 1, ind: 0},
  {axis: 3, pos: 0.16, mod: 1, ind: 1},
  {axis: 3, pos: 0.16, mod: 1, ind: 0},
  {axis: 3, pos: 0.17, mod: 1, ind: 0},
  {axis: 1, pos: 0.17, mod: 1, ind: 0},
  {axis: 3, pos: 0.17, mod: 1, ind: 1},
  {axis: 3, pos: 0.19, mod: 1, ind: 1},
  {axis: 3, pos: 0.2, mod: 1, ind: 1},
  {axis: 3, pos: 0.2, mod: 1, ind: 1},
  {axis: 3, pos: 0.21, mod: 1, ind: 1},
  {axis: 3, pos: 0.21, mod: 1, ind: 0},
  {axis: 3, pos: 0.21, mod: 1, ind: 0},
  {axis: 3, pos: 0.21, mod: 1, ind: 1},
  {axis: 3, pos: 0.22, mod: 1, ind: 0},
  {axis: 3, pos: 0.22, mod: 1, ind: 0},
  {axis: 3, pos: 0.22, mod: 1, ind: 1},
  {axis: 3, pos: 0.22, mod: 1, ind: 1},
  {axis: 3, pos: 0.22, mod: 1, ind: 0},
  {axis: 3, pos: 0.23, mod: 1, ind: 0},
  {axis: 3, pos: 0.23, mod: 1, ind: 1},
  {axis: 1, pos: 0.24, mod: 1, ind: 1},
  {axis: 5, pos: 0.24, mod: 1, ind: 0},
  {axis: 3, pos: 0.25, mod: 1, ind: 0},
  {axis: 3, pos: 0.25, mod: 1, ind: 1},
  {axis: 3, pos: 0.25, mod: 1, ind: 1},
  {axis: 3, pos: 0.26, mod: 1, ind: 0},
  {axis: 3, pos: 0.26, mod: 1, ind: 1},
  {axis: 1, pos: 0.26, mod: 1, ind: 0},
  {axis: 3, pos: 0.27, mod: 1, ind: 0},
  {axis: 3, pos: 0.27, mod: 1, ind: 0},
  {axis: 3, pos: 0.27, mod: 1, ind: 0},
  {axis: 5, pos: 0.27, mod: 1, ind: 0},
  {axis: 1, pos: 0.27, mod: 1, ind: 0},
  {axis: 1, pos: 0.27, mod: 1, ind: 0},
  {axis: 5, pos: 0.28, mod: 1, ind: 1},
  {axis: 3, pos: 0.28, mod: 1, ind: 0},
  {axis: 3, pos: 0.29, mod: 1, ind: 0},
  {axis: 3, pos: 0.29, mod: 1, ind: 0},
  {axis: 3, pos: 0.29, mod: 1, ind: 0},
  {axis: 3, pos: 0.32, mod: 1, ind: 0},
  {axis: 3, pos: 0.34, mod: 1, ind: 0},
  {axis: 3, pos: 0.35, mod: 1, ind: 0},
  {axis: 3, pos: 0.37, mod: 1, ind: 0},
  {axis: 3, pos: 0.37, mod: 1, ind: 1},
  {axis: 1, pos: 0.37, mod: 1, ind: 0},
  {axis: 3, pos: 0.37, mod: 1, ind: 0},
  {axis: 3, pos: 0.38, mod: 1, ind: 0},
  {axis: 3, pos: 0.4, mod: 1, ind: 0},
  {axis: 3, pos: 0.46, mod: 1, ind: 0},
  {axis: 1, pos: 0.46, mod: 1, ind: 0},
  {axis: 3, pos: 0.47, mod: 1, ind: 1},
  {axis: 1, pos: 0.51, mod: 1, ind: 0},
  {axis: 1, pos: 0.51, mod: 1, ind: 0},
  {axis: 3, pos: 0.84, mod: 1, ind: 0},
  {axis: 3, pos: 0.89, mod: 1, ind: 0},
  {axis: 3, pos: 1.0, mod: 1, ind: 0},
];