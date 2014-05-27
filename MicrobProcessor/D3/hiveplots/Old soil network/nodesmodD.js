var nodes = [
  {axis: 2, pos: 0.02, mod: 4, ind: 7},
  {axis: 2, pos: 0.03, mod: 4, ind: 7},
  {axis: 4, pos: 0.04, mod: 4, ind: 7},
  {axis: 2, pos: 0.04, mod: 4, ind: 7},
  {axis: 2, pos: 0.05, mod: 4, ind: 0},
  {axis: 2, pos: 0.06, mod: 4, ind: 0},
  {axis: 2, pos: 0.06, mod: 4, ind: 7},
  {axis: 4, pos: 0.07, mod: 4, ind: 1},
  {axis: 4, pos: 0.07, mod: 4, ind: 7},
  {axis: 2, pos: 0.07, mod: 4, ind: 0},
  {axis: 4, pos: 0.07, mod: 4, ind: 7},
  {axis: 0, pos: 0.07, mod: 4, ind: 0},
  {axis: 4, pos: 0.07, mod: 4, ind: 7},
  {axis: 2, pos: 0.07, mod: 4, ind: 0},
  {axis: 2, pos: 0.08, mod: 4, ind: 1},
  {axis: 2, pos: 0.08, mod: 4, ind: 1},
  {axis: 0, pos: 0.08, mod: 4, ind: 1},
  {axis: 2, pos: 0.08, mod: 4, ind: 7},
  {axis: 0, pos: 0.08, mod: 4, ind: 0},
  {axis: 2, pos: 0.09, mod: 4, ind: 0},
  {axis: 2, pos: 0.09, mod: 4, ind: 0},
  {axis: 4, pos: 0.1, mod: 4, ind: 0},
  {axis: 2, pos: 0.1, mod: 4, ind: 0},
  {axis: 2, pos: 0.1, mod: 4, ind: 7},
  {axis: 4, pos: 0.1, mod: 4, ind: 7},
  {axis: 4, pos: 0.11, mod: 4, ind: 7},
  {axis: 0, pos: 0.11, mod: 4, ind: 7},
  {axis: 4, pos: 0.11, mod: 4, ind: 0},
  {axis: 0, pos: 0.11, mod: 4, ind: 0},
  {axis: 2, pos: 0.12, mod: 4, ind: 0},
  {axis: 2, pos: 0.12, mod: 4, ind: 0},
  {axis: 2, pos: 0.12, mod: 4, ind: 7},
  {axis: 2, pos: 0.12, mod: 4, ind: 0},
  {axis: 2, pos: 0.12, mod: 4, ind: 7},
  {axis: 4, pos: 0.12, mod: 4, ind: 0},
  {axis: 4, pos: 0.12, mod: 4, ind: 0},
  {axis: 4, pos: 0.12, mod: 4, ind: 7},
  {axis: 2, pos: 0.13, mod: 4, ind: 7},
  {axis: 2, pos: 0.13, mod: 4, ind: 0},
  {axis: 0, pos: 0.13, mod: 4, ind: 0},
  {axis: 4, pos: 0.13, mod: 4, ind: 0},
  {axis: 2, pos: 0.13, mod: 4, ind: 0},
  {axis: 0, pos: 0.13, mod: 4, ind: 0},
  {axis: 4, pos: 0.14, mod: 4, ind: 7},
  {axis: 2, pos: 0.14, mod: 4, ind: 0},
  {axis: 4, pos: 0.14, mod: 4, ind: 0},
  {axis: 4, pos: 0.15, mod: 4, ind: 0},
  {axis: 4, pos: 0.15, mod: 4, ind: 0},
  {axis: 2, pos: 0.15, mod: 4, ind: 0},
  {axis: 2, pos: 0.15, mod: 4, ind: 0},
  {axis: 4, pos: 0.15, mod: 4, ind: 0},
  {axis: 2, pos: 0.15, mod: 4, ind: 0},
  {axis: 4, pos: 0.16, mod: 4, ind: 0},
  {axis: 2, pos: 0.16, mod: 4, ind: 0},
  {axis: 2, pos: 0.16, mod: 4, ind: 0},
  {axis: 2, pos: 0.16, mod: 4, ind: 0},
  {axis: 2, pos: 0.17, mod: 4, ind: 0},
  {axis: 2, pos: 0.17, mod: 4, ind: 0},
  {axis: 4, pos: 0.17, mod: 4, ind: 0},
  {axis: 4, pos: 0.17, mod: 4, ind: 0},
  {axis: 2, pos: 0.18, mod: 4, ind: 7},
  {axis: 2, pos: 0.18, mod: 4, ind: 0},
  {axis: 2, pos: 0.18, mod: 4, ind: 0},
  {axis: 2, pos: 0.18, mod: 4, ind: 7},
  {axis: 2, pos: 0.19, mod: 4, ind: 0},
  {axis: 2, pos: 0.19, mod: 4, ind: 0},
  {axis: 0, pos: 0.2, mod: 4, ind: 0},
  {axis: 2, pos: 0.2, mod: 4, ind: 0},
  {axis: 2, pos: 0.2, mod: 4, ind: 0},
  {axis: 2, pos: 0.21, mod: 4, ind: 0},
  {axis: 2, pos: 0.21, mod: 4, ind: 0},
  {axis: 0, pos: 0.21, mod: 4, ind: 0},
  {axis: 0, pos: 0.21, mod: 4, ind: 0},
  {axis: 4, pos: 0.21, mod: 4, ind: 0},
  {axis: 2, pos: 0.22, mod: 4, ind: 0},
  {axis: 4, pos: 0.23, mod: 4, ind: 0},
  {axis: 0, pos: 0.23, mod: 4, ind: 0},
  {axis: 4, pos: 0.23, mod: 4, ind: 0},
  {axis: 0, pos: 0.24, mod: 4, ind: 0},
  {axis: 2, pos: 0.24, mod: 4, ind: 0},
  {axis: 0, pos: 0.25, mod: 4, ind: 0},
  {axis: 0, pos: 0.25, mod: 4, ind: 0},
  {axis: 2, pos: 0.26, mod: 4, ind: 0},
  {axis: 4, pos: 0.27, mod: 4, ind: 0},
  {axis: 0, pos: 0.28, mod: 4, ind: 0},
  {axis: 2, pos: 0.28, mod: 4, ind: 0},
  {axis: 2, pos: 0.29, mod: 4, ind: 0},
  {axis: 2, pos: 0.35, mod: 4, ind: 0},
  {axis: 0, pos: 0.37, mod: 4, ind: 0},
  {axis: 2, pos: 0.38, mod: 4, ind: 0},
  {axis: 2, pos: 0.38, mod: 4, ind: 6},
  {axis: 2, pos: 0.38, mod: 4, ind: 6},
  {axis: 0, pos: 0.4, mod: 4, ind: 0},
  {axis: 2, pos: 0.4, mod: 4, ind: 0},
  {axis: 0, pos: 0.41, mod: 4, ind: 0},
  {axis: 2, pos: 0.42, mod: 4, ind: 0},
  {axis: 2, pos: 0.42, mod: 4, ind: 0},
  {axis: 2, pos: 0.42, mod: 4, ind: 0},
  {axis: 2, pos: 0.42, mod: 4, ind: 6},
  {axis: 0, pos: 0.42, mod: 4, ind: 0},
  {axis: 2, pos: 0.43, mod: 4, ind: 6},
  {axis: 2, pos: 0.44, mod: 4, ind: 6},
  {axis: 2, pos: 0.44, mod: 4, ind: 0},
  {axis: 2, pos: 0.45, mod: 4, ind: 0},
  {axis: 2, pos: 0.46, mod: 4, ind: 6},
  {axis: 0, pos: 0.46, mod: 4, ind: 6},
  {axis: 0, pos: 0.46, mod: 4, ind: 6},
  {axis: 4, pos: 0.46, mod: 4, ind: 0},
  {axis: 2, pos: 0.47, mod: 4, ind: 0},
  {axis: 2, pos: 0.47, mod: 4, ind: 0},
  {axis: 0, pos: 0.47, mod: 4, ind: 0},
  {axis: 2, pos: 0.47, mod: 4, ind: 0},
  {axis: 2, pos: 0.47, mod: 4, ind: 0},
  {axis: 2, pos: 0.48, mod: 4, ind: 6},
  {axis: 0, pos: 0.48, mod: 4, ind: 0},
  {axis: 0, pos: 0.48, mod: 4, ind: 6},
  {axis: 2, pos: 0.48, mod: 4, ind: 6},
  {axis: 2, pos: 0.49, mod: 4, ind: 6},
  {axis: 2, pos: 0.49, mod: 4, ind: 6},
  {axis: 0, pos: 0.49, mod: 4, ind: 0},
  {axis: 2, pos: 0.49, mod: 4, ind: 6},
  {axis: 2, pos: 0.5, mod: 4, ind: 6},
  {axis: 2, pos: 0.5, mod: 4, ind: 6},
  {axis: 0, pos: 0.5, mod: 4, ind: 6},
  {axis: 0, pos: 0.5, mod: 4, ind: 0},
  {axis: 2, pos: 0.5, mod: 4, ind: 0},
  {axis: 2, pos: 0.5, mod: 4, ind: 0},
  {axis: 2, pos: 0.51, mod: 4, ind: 6},
  {axis: 2, pos: 0.51, mod: 4, ind: 6},
  {axis: 2, pos: 0.51, mod: 4, ind: 6},
  {axis: 0, pos: 0.51, mod: 4, ind: 0},
  {axis: 0, pos: 0.51, mod: 4, ind: 6},
  {axis: 2, pos: 0.52, mod: 4, ind: 0},
  {axis: 0, pos: 0.52, mod: 4, ind: 0},
  {axis: 2, pos: 0.52, mod: 4, ind: 0},
  {axis: 2, pos: 0.52, mod: 4, ind: 6},
  {axis: 0, pos: 0.52, mod: 4, ind: 0},
  {axis: 2, pos: 0.52, mod: 4, ind: 6},
  {axis: 2, pos: 0.52, mod: 4, ind: 6},
  {axis: 0, pos: 0.53, mod: 4, ind: 6},
  {axis: 2, pos: 0.53, mod: 4, ind: 6},
  {axis: 2, pos: 0.53, mod: 4, ind: 6},
  {axis: 2, pos: 0.53, mod: 4, ind: 0},
  {axis: 2, pos: 0.53, mod: 4, ind: 6},
  {axis: 2, pos: 0.53, mod: 4, ind: 0},
  {axis: 2, pos: 0.53, mod: 4, ind: 6},
  {axis: 2, pos: 0.53, mod: 4, ind: 6},
  {axis: 2, pos: 0.53, mod: 4, ind: 6},
  {axis: 2, pos: 0.54, mod: 4, ind: 0},
  {axis: 2, pos: 0.54, mod: 4, ind: 6},
  {axis: 2, pos: 0.54, mod: 4, ind: 6},
  {axis: 0, pos: 0.54, mod: 4, ind: 6},
  {axis: 2, pos: 0.54, mod: 4, ind: 0},
  {axis: 2, pos: 0.54, mod: 4, ind: 6},
  {axis: 2, pos: 0.54, mod: 4, ind: 6},
  {axis: 2, pos: 0.55, mod: 4, ind: 6},
  {axis: 2, pos: 0.55, mod: 4, ind: 6},
  {axis: 4, pos: 0.55, mod: 4, ind: 6},
  {axis: 2, pos: 0.55, mod: 4, ind: 0},
  {axis: 2, pos: 0.55, mod: 4, ind: 0},
  {axis: 2, pos: 0.55, mod: 4, ind: 6},
  {axis: 2, pos: 0.55, mod: 4, ind: 6},
  {axis: 2, pos: 0.55, mod: 4, ind: 6},
  {axis: 0, pos: 0.56, mod: 4, ind: 0},
  {axis: 2, pos: 0.56, mod: 4, ind: 0},
  {axis: 4, pos: 0.56, mod: 4, ind: 6},
  {axis: 0, pos: 0.56, mod: 4, ind: 6},
  {axis: 2, pos: 0.56, mod: 4, ind: 0},
  {axis: 2, pos: 0.57, mod: 4, ind: 0},
  {axis: 2, pos: 0.57, mod: 4, ind: 6},
  {axis: 2, pos: 0.57, mod: 4, ind: 6},
  {axis: 2, pos: 0.57, mod: 4, ind: 6},
  {axis: 0, pos: 0.57, mod: 4, ind: 0},
  {axis: 2, pos: 0.57, mod: 4, ind: 6},
  {axis: 2, pos: 0.57, mod: 4, ind: 0},
  {axis: 2, pos: 0.57, mod: 4, ind: 0},
  {axis: 2, pos: 0.57, mod: 4, ind: 6},
  {axis: 2, pos: 0.58, mod: 4, ind: 0},
  {axis: 2, pos: 0.58, mod: 4, ind: 6},
  {axis: 2, pos: 0.58, mod: 4, ind: 6},
  {axis: 4, pos: 0.58, mod: 4, ind: 6},
  {axis: 4, pos: 0.58, mod: 4, ind: 6},
  {axis: 2, pos: 0.59, mod: 4, ind: 6},
  {axis: 2, pos: 0.59, mod: 4, ind: 6},
  {axis: 2, pos: 0.59, mod: 4, ind: 0},
  {axis: 2, pos: 0.59, mod: 4, ind: 0},
  {axis: 2, pos: 0.59, mod: 4, ind: 0},
  {axis: 4, pos: 0.59, mod: 4, ind: 6},
  {axis: 4, pos: 0.59, mod: 4, ind: 0},
  {axis: 2, pos: 0.6, mod: 4, ind: 6},
  {axis: 2, pos: 0.6, mod: 4, ind: 6},
  {axis: 0, pos: 0.6, mod: 4, ind: 0},
  {axis: 2, pos: 0.6, mod: 4, ind: 0},
  {axis: 4, pos: 0.6, mod: 4, ind: 6},
  {axis: 2, pos: 0.6, mod: 4, ind: 6},
  {axis: 2, pos: 0.6, mod: 4, ind: 0},
  {axis: 0, pos: 0.6, mod: 4, ind: 0},
  {axis: 4, pos: 0.6, mod: 4, ind: 0},
  {axis: 0, pos: 0.6, mod: 4, ind: 0},
  {axis: 2, pos: 0.61, mod: 4, ind: 0},
  {axis: 2, pos: 0.61, mod: 4, ind: 0},
  {axis: 2, pos: 0.61, mod: 4, ind: 6},
  {axis: 2, pos: 0.61, mod: 4, ind: 0},
  {axis: 4, pos: 0.61, mod: 4, ind: 6},
  {axis: 4, pos: 0.62, mod: 4, ind: 0},
  {axis: 2, pos: 0.62, mod: 4, ind: 6},
  {axis: 4, pos: 0.62, mod: 4, ind: 6},
  {axis: 4, pos: 0.62, mod: 4, ind: 0},
  {axis: 2, pos: 0.62, mod: 4, ind: 0},
  {axis: 4, pos: 0.62, mod: 4, ind: 6},
  {axis: 0, pos: 0.62, mod: 4, ind: 0},
  {axis: 4, pos: 0.62, mod: 4, ind: 6},
  {axis: 2, pos: 0.62, mod: 4, ind: 0},
  {axis: 2, pos: 0.62, mod: 4, ind: 6},
  {axis: 2, pos: 0.62, mod: 4, ind: 0},
  {axis: 2, pos: 0.62, mod: 4, ind: 6},
  {axis: 4, pos: 0.63, mod: 4, ind: 6},
  {axis: 0, pos: 0.63, mod: 4, ind: 0},
  {axis: 0, pos: 0.63, mod: 4, ind: 0},
  {axis: 2, pos: 0.63, mod: 4, ind: 6},
  {axis: 2, pos: 0.63, mod: 4, ind: 0},
  {axis: 2, pos: 0.63, mod: 4, ind: 0},
  {axis: 0, pos: 0.63, mod: 4, ind: 0},
  {axis: 2, pos: 0.64, mod: 4, ind: 0},
  {axis: 4, pos: 0.64, mod: 4, ind: 6},
  {axis: 0, pos: 0.64, mod: 4, ind: 6},
  {axis: 0, pos: 0.64, mod: 4, ind: 0},
  {axis: 4, pos: 0.64, mod: 4, ind: 6},
  {axis: 4, pos: 0.64, mod: 4, ind: 0},
  {axis: 2, pos: 0.64, mod: 4, ind: 0},
  {axis: 4, pos: 0.64, mod: 4, ind: 6},
  {axis: 2, pos: 0.64, mod: 4, ind: 6},
  {axis: 4, pos: 0.65, mod: 4, ind: 6},
  {axis: 2, pos: 0.65, mod: 4, ind: 6},
  {axis: 4, pos: 0.65, mod: 4, ind: 0},
  {axis: 0, pos: 0.65, mod: 4, ind: 0},
  {axis: 4, pos: 0.66, mod: 4, ind: 6},
  {axis: 4, pos: 0.66, mod: 4, ind: 6},
  {axis: 0, pos: 0.66, mod: 4, ind: 0},
  {axis: 2, pos: 0.66, mod: 4, ind: 0},
  {axis: 2, pos: 0.67, mod: 4, ind: 0},
  {axis: 2, pos: 0.67, mod: 4, ind: 0},
  {axis: 2, pos: 0.67, mod: 4, ind: 6},
  {axis: 2, pos: 0.67, mod: 4, ind: 6},
  {axis: 2, pos: 0.67, mod: 4, ind: 0},
  {axis: 0, pos: 0.67, mod: 4, ind: 0},
  {axis: 2, pos: 0.67, mod: 4, ind: 0},
  {axis: 2, pos: 0.68, mod: 4, ind: 0},
  {axis: 2, pos: 0.68, mod: 4, ind: 0},
  {axis: 2, pos: 0.68, mod: 4, ind: 6},
  {axis: 2, pos: 0.68, mod: 4, ind: 0},
  {axis: 0, pos: 0.68, mod: 4, ind: 0},
  {axis: 2, pos: 0.68, mod: 4, ind: 6},
  {axis: 4, pos: 0.69, mod: 4, ind: 6},
  {axis: 2, pos: 0.69, mod: 4, ind: 0},
  {axis: 2, pos: 0.69, mod: 4, ind: 0},
  {axis: 2, pos: 0.69, mod: 4, ind: 6},
  {axis: 0, pos: 0.69, mod: 4, ind: 0},
  {axis: 2, pos: 0.69, mod: 4, ind: 0},
  {axis: 2, pos: 0.69, mod: 4, ind: 6},
  {axis: 2, pos: 0.7, mod: 4, ind: 6},
  {axis: 2, pos: 0.7, mod: 4, ind: 6},
  {axis: 2, pos: 0.7, mod: 4, ind: 0},
  {axis: 2, pos: 0.7, mod: 4, ind: 6},
  {axis: 2, pos: 0.7, mod: 4, ind: 0},
  {axis: 4, pos: 0.7, mod: 4, ind: 6},
  {axis: 2, pos: 0.7, mod: 4, ind: 6},
  {axis: 2, pos: 0.71, mod: 4, ind: 6},
  {axis: 2, pos: 0.71, mod: 4, ind: 6},
  {axis: 2, pos: 0.71, mod: 4, ind: 6},
  {axis: 2, pos: 0.71, mod: 4, ind: 6},
  {axis: 4, pos: 0.71, mod: 4, ind: 0},
  {axis: 2, pos: 0.71, mod: 4, ind: 0},
  {axis: 2, pos: 0.71, mod: 4, ind: 6},
  {axis: 2, pos: 0.71, mod: 4, ind: 0},
  {axis: 4, pos: 0.71, mod: 4, ind: 6},
  {axis: 4, pos: 0.72, mod: 4, ind: 6},
  {axis: 2, pos: 0.72, mod: 4, ind: 6},
  {axis: 0, pos: 0.72, mod: 4, ind: 0},
  {axis: 2, pos: 0.72, mod: 4, ind: 0},
  {axis: 4, pos: 0.72, mod: 4, ind: 0},
  {axis: 2, pos: 0.73, mod: 4, ind: 6},
  {axis: 4, pos: 0.73, mod: 4, ind: 6},
  {axis: 4, pos: 0.73, mod: 4, ind: 6},
  {axis: 4, pos: 0.73, mod: 4, ind: 6},
  {axis: 2, pos: 0.73, mod: 4, ind: 0},
  {axis: 2, pos: 0.73, mod: 4, ind: 0},
  {axis: 4, pos: 0.74, mod: 4, ind: 6},
  {axis: 2, pos: 0.74, mod: 4, ind: 6},
  {axis: 2, pos: 0.74, mod: 4, ind: 5},
  {axis: 2, pos: 0.74, mod: 4, ind: 0},
  {axis: 2, pos: 0.74, mod: 4, ind: 0},
  {axis: 2, pos: 0.75, mod: 4, ind: 0},
  {axis: 0, pos: 0.75, mod: 4, ind: 0},
  {axis: 2, pos: 0.75, mod: 4, ind: 0},
  {axis: 4, pos: 0.75, mod: 4, ind: 6},
  {axis: 2, pos: 0.75, mod: 4, ind: 0},
  {axis: 2, pos: 0.76, mod: 4, ind: 0},
  {axis: 4, pos: 0.76, mod: 4, ind: 6},
  {axis: 2, pos: 0.76, mod: 4, ind: 6},
  {axis: 4, pos: 0.76, mod: 4, ind: 5},
  {axis: 4, pos: 0.76, mod: 4, ind: 6},
  {axis: 4, pos: 0.76, mod: 4, ind: 6},
  {axis: 4, pos: 0.76, mod: 4, ind: 6},
  {axis: 0, pos: 0.76, mod: 4, ind: 0},
  {axis: 2, pos: 0.76, mod: 4, ind: 0},
  {axis: 2, pos: 0.76, mod: 4, ind: 0},
  {axis: 2, pos: 0.77, mod: 4, ind: 0},
  {axis: 2, pos: 0.77, mod: 4, ind: 6},
  {axis: 2, pos: 0.77, mod: 4, ind: 5},
  {axis: 4, pos: 0.77, mod: 4, ind: 6},
  {axis: 4, pos: 0.78, mod: 4, ind: 6},
  {axis: 2, pos: 0.78, mod: 4, ind: 0},
  {axis: 2, pos: 0.78, mod: 4, ind: 6},
  {axis: 2, pos: 0.78, mod: 4, ind: 0},
  {axis: 2, pos: 0.78, mod: 4, ind: 6},
  {axis: 4, pos: 0.78, mod: 4, ind: 6},
  {axis: 4, pos: 0.78, mod: 4, ind: 6},
  {axis: 4, pos: 0.78, mod: 4, ind: 6},
  {axis: 2, pos: 0.79, mod: 4, ind: 0},
  {axis: 2, pos: 0.79, mod: 4, ind: 0},
  {axis: 0, pos: 0.79, mod: 4, ind: 5},
  {axis: 2, pos: 0.79, mod: 4, ind: 6},
  {axis: 4, pos: 0.79, mod: 4, ind: 5},
  {axis: 2, pos: 0.79, mod: 4, ind: 0},
  {axis: 0, pos: 0.79, mod: 4, ind: 0},
  {axis: 2, pos: 0.8, mod: 4, ind: 0},
  {axis: 4, pos: 0.8, mod: 4, ind: 6},
  {axis: 4, pos: 0.8, mod: 4, ind: 6},
  {axis: 2, pos: 0.8, mod: 4, ind: 6},
  {axis: 4, pos: 0.81, mod: 4, ind: 6},
  {axis: 4, pos: 0.81, mod: 4, ind: 6},
  {axis: 2, pos: 0.81, mod: 4, ind: 5},
  {axis: 4, pos: 0.81, mod: 4, ind: 5},
  {axis: 0, pos: 0.81, mod: 4, ind: 5},
  {axis: 2, pos: 0.81, mod: 4, ind: 0},
  {axis: 2, pos: 0.81, mod: 4, ind: 5},
  {axis: 0, pos: 0.81, mod: 4, ind: 0},
  {axis: 2, pos: 0.82, mod: 4, ind: 5},
  {axis: 4, pos: 0.82, mod: 4, ind: 6},
  {axis: 0, pos: 0.82, mod: 4, ind: 0},
  {axis: 2, pos: 0.82, mod: 4, ind: 5},
  {axis: 2, pos: 0.82, mod: 4, ind: 0},
  {axis: 2, pos: 0.82, mod: 4, ind: 5},
  {axis: 2, pos: 0.83, mod: 4, ind: 5},
  {axis: 2, pos: 0.83, mod: 4, ind: 0},
  {axis: 2, pos: 0.84, mod: 4, ind: 5},
  {axis: 0, pos: 0.84, mod: 4, ind: 0},
  {axis: 2, pos: 0.84, mod: 4, ind: 6},
  {axis: 2, pos: 0.85, mod: 4, ind: 5},
  {axis: 2, pos: 0.85, mod: 4, ind: 0},
  {axis: 2, pos: 0.85, mod: 4, ind: 0},
  {axis: 2, pos: 0.85, mod: 4, ind: 5},
  {axis: 4, pos: 0.85, mod: 4, ind: 6},
  {axis: 4, pos: 0.85, mod: 4, ind: 5},
  {axis: 2, pos: 0.85, mod: 4, ind: 5},
  {axis: 0, pos: 0.85, mod: 4, ind: 0},
  {axis: 0, pos: 0.86, mod: 4, ind: 5},
  {axis: 2, pos: 0.86, mod: 4, ind: 5},
  {axis: 4, pos: 0.86, mod: 4, ind: 6},
  {axis: 2, pos: 0.86, mod: 4, ind: 5},
  {axis: 4, pos: 0.86, mod: 4, ind: 6},
  {axis: 2, pos: 0.86, mod: 4, ind: 5},
  {axis: 4, pos: 0.86, mod: 4, ind: 5},
  {axis: 2, pos: 0.87, mod: 4, ind: 5},
  {axis: 4, pos: 0.87, mod: 4, ind: 5},
  {axis: 4, pos: 0.87, mod: 4, ind: 5},
  {axis: 4, pos: 0.87, mod: 4, ind: 5},
  {axis: 4, pos: 0.88, mod: 4, ind: 5},
  {axis: 2, pos: 0.88, mod: 4, ind: 5},
  {axis: 2, pos: 0.89, mod: 4, ind: 5},
  {axis: 2, pos: 0.89, mod: 4, ind: 6},
  {axis: 4, pos: 0.89, mod: 4, ind: 6},
  {axis: 2, pos: 0.89, mod: 4, ind: 5},
  {axis: 4, pos: 0.9, mod: 4, ind: 5},
  {axis: 2, pos: 0.9, mod: 4, ind: 5},
  {axis: 2, pos: 0.9, mod: 4, ind: 5},
  {axis: 2, pos: 0.9, mod: 4, ind: 5},
  {axis: 2, pos: 0.91, mod: 4, ind: 5},
  {axis: 2, pos: 0.92, mod: 4, ind: 5},
  {axis: 4, pos: 0.93, mod: 4, ind: 5},
  {axis: 2, pos: 0.93, mod: 4, ind: 5},
  {axis: 4, pos: 0.93, mod: 4, ind: 5},
  {axis: 0, pos: 0.93, mod: 4, ind: 5},
  {axis: 4, pos: 0.93, mod: 4, ind: 5},
  {axis: 2, pos: 0.94, mod: 4, ind: 5},
  {axis: 2, pos: 0.94, mod: 4, ind: 5},
  {axis: 4, pos: 0.94, mod: 4, ind: 5},
  {axis: 4, pos: 0.94, mod: 4, ind: 5},
  {axis: 4, pos: 0.94, mod: 4, ind: 5},
  {axis: 2, pos: 0.95, mod: 4, ind: 5},
  {axis: 2, pos: 0.95, mod: 4, ind: 5},
  {axis: 4, pos: 0.95, mod: 4, ind: 5},
  {axis: 4, pos: 0.95, mod: 4, ind: 5},
  {axis: 2, pos: 0.96, mod: 4, ind: 5},
  {axis: 2, pos: 0.96, mod: 4, ind: 5},
  {axis: 4, pos: 0.96, mod: 4, ind: 5},
  {axis: 2, pos: 0.96, mod: 4, ind: 5},
  {axis: 4, pos: 0.97, mod: 4, ind: 5},
  {axis: 4, pos: 0.97, mod: 4, ind: 5},
  {axis: 4, pos: 0.97, mod: 4, ind: 5},
  {axis: 4, pos: 0.97, mod: 4, ind: 5},
  {axis: 2, pos: 0.98, mod: 4, ind: 5},
  {axis: 2, pos: 0.98, mod: 4, ind: 5},
  {axis: 4, pos: 0.98, mod: 4, ind: 5},
  {axis: 4, pos: 0.99, mod: 4, ind: 5},
  {axis: 2, pos: 1.0, mod: 4, ind: 5},
  {axis: 3, pos: 0.02, mod: 4, ind: 7},
  {axis: 3, pos: 0.03, mod: 4, ind: 7},
  {axis: 5, pos: 0.04, mod: 4, ind: 7},
  {axis: 3, pos: 0.04, mod: 4, ind: 7},
  {axis: 3, pos: 0.05, mod: 4, ind: 0},
  {axis: 3, pos: 0.06, mod: 4, ind: 0},
  {axis: 3, pos: 0.06, mod: 4, ind: 7},
  {axis: 5, pos: 0.07, mod: 4, ind: 1},
  {axis: 5, pos: 0.07, mod: 4, ind: 7},
  {axis: 3, pos: 0.07, mod: 4, ind: 0},
  {axis: 5, pos: 0.07, mod: 4, ind: 7},
  {axis: 1, pos: 0.07, mod: 4, ind: 0},
  {axis: 5, pos: 0.07, mod: 4, ind: 7},
  {axis: 3, pos: 0.07, mod: 4, ind: 0},
  {axis: 3, pos: 0.08, mod: 4, ind: 1},
  {axis: 3, pos: 0.08, mod: 4, ind: 1},
  {axis: 1, pos: 0.08, mod: 4, ind: 1},
  {axis: 3, pos: 0.08, mod: 4, ind: 7},
  {axis: 1, pos: 0.08, mod: 4, ind: 0},
  {axis: 3, pos: 0.09, mod: 4, ind: 0},
  {axis: 3, pos: 0.09, mod: 4, ind: 0},
  {axis: 5, pos: 0.1, mod: 4, ind: 0},
  {axis: 3, pos: 0.1, mod: 4, ind: 0},
  {axis: 3, pos: 0.1, mod: 4, ind: 7},
  {axis: 5, pos: 0.1, mod: 4, ind: 7},
  {axis: 5, pos: 0.11, mod: 4, ind: 7},
  {axis: 1, pos: 0.11, mod: 4, ind: 7},
  {axis: 5, pos: 0.11, mod: 4, ind: 0},
  {axis: 1, pos: 0.11, mod: 4, ind: 0},
  {axis: 3, pos: 0.12, mod: 4, ind: 0},
  {axis: 3, pos: 0.12, mod: 4, ind: 0},
  {axis: 3, pos: 0.12, mod: 4, ind: 7},
  {axis: 3, pos: 0.12, mod: 4, ind: 0},
  {axis: 3, pos: 0.12, mod: 4, ind: 7},
  {axis: 5, pos: 0.12, mod: 4, ind: 0},
  {axis: 5, pos: 0.12, mod: 4, ind: 0},
  {axis: 5, pos: 0.12, mod: 4, ind: 7},
  {axis: 3, pos: 0.13, mod: 4, ind: 7},
  {axis: 3, pos: 0.13, mod: 4, ind: 0},
  {axis: 1, pos: 0.13, mod: 4, ind: 0},
  {axis: 5, pos: 0.13, mod: 4, ind: 0},
  {axis: 3, pos: 0.13, mod: 4, ind: 0},
  {axis: 1, pos: 0.13, mod: 4, ind: 0},
  {axis: 5, pos: 0.14, mod: 4, ind: 7},
  {axis: 3, pos: 0.14, mod: 4, ind: 0},
  {axis: 5, pos: 0.14, mod: 4, ind: 0},
  {axis: 5, pos: 0.15, mod: 4, ind: 0},
  {axis: 5, pos: 0.15, mod: 4, ind: 0},
  {axis: 3, pos: 0.15, mod: 4, ind: 0},
  {axis: 3, pos: 0.15, mod: 4, ind: 0},
  {axis: 5, pos: 0.15, mod: 4, ind: 0},
  {axis: 3, pos: 0.15, mod: 4, ind: 0},
  {axis: 5, pos: 0.16, mod: 4, ind: 0},
  {axis: 3, pos: 0.16, mod: 4, ind: 0},
  {axis: 3, pos: 0.16, mod: 4, ind: 0},
  {axis: 3, pos: 0.16, mod: 4, ind: 0},
  {axis: 3, pos: 0.17, mod: 4, ind: 0},
  {axis: 3, pos: 0.17, mod: 4, ind: 0},
  {axis: 5, pos: 0.17, mod: 4, ind: 0},
  {axis: 5, pos: 0.17, mod: 4, ind: 0},
  {axis: 3, pos: 0.18, mod: 4, ind: 7},
  {axis: 3, pos: 0.18, mod: 4, ind: 0},
  {axis: 3, pos: 0.18, mod: 4, ind: 0},
  {axis: 3, pos: 0.18, mod: 4, ind: 7},
  {axis: 3, pos: 0.19, mod: 4, ind: 0},
  {axis: 3, pos: 0.19, mod: 4, ind: 0},
  {axis: 1, pos: 0.2, mod: 4, ind: 0},
  {axis: 3, pos: 0.2, mod: 4, ind: 0},
  {axis: 3, pos: 0.2, mod: 4, ind: 0},
  {axis: 3, pos: 0.21, mod: 4, ind: 0},
  {axis: 3, pos: 0.21, mod: 4, ind: 0},
  {axis: 1, pos: 0.21, mod: 4, ind: 0},
  {axis: 1, pos: 0.21, mod: 4, ind: 0},
  {axis: 5, pos: 0.21, mod: 4, ind: 0},
  {axis: 3, pos: 0.22, mod: 4, ind: 0},
  {axis: 5, pos: 0.23, mod: 4, ind: 0},
  {axis: 1, pos: 0.23, mod: 4, ind: 0},
  {axis: 5, pos: 0.23, mod: 4, ind: 0},
  {axis: 1, pos: 0.24, mod: 4, ind: 0},
  {axis: 3, pos: 0.24, mod: 4, ind: 0},
  {axis: 1, pos: 0.25, mod: 4, ind: 0},
  {axis: 1, pos: 0.25, mod: 4, ind: 0},
  {axis: 3, pos: 0.26, mod: 4, ind: 0},
  {axis: 5, pos: 0.27, mod: 4, ind: 0},
  {axis: 1, pos: 0.28, mod: 4, ind: 0},
  {axis: 3, pos: 0.28, mod: 4, ind: 0},
  {axis: 3, pos: 0.29, mod: 4, ind: 0},
  {axis: 3, pos: 0.35, mod: 4, ind: 0},
  {axis: 1, pos: 0.37, mod: 4, ind: 0},
  {axis: 3, pos: 0.38, mod: 4, ind: 0},
  {axis: 3, pos: 0.38, mod: 4, ind: 6},
  {axis: 3, pos: 0.38, mod: 4, ind: 6},
  {axis: 1, pos: 0.4, mod: 4, ind: 0},
  {axis: 3, pos: 0.4, mod: 4, ind: 0},
  {axis: 1, pos: 0.41, mod: 4, ind: 0},
  {axis: 3, pos: 0.42, mod: 4, ind: 0},
  {axis: 3, pos: 0.42, mod: 4, ind: 0},
  {axis: 3, pos: 0.42, mod: 4, ind: 0},
  {axis: 3, pos: 0.42, mod: 4, ind: 6},
  {axis: 1, pos: 0.42, mod: 4, ind: 0},
  {axis: 3, pos: 0.43, mod: 4, ind: 6},
  {axis: 3, pos: 0.44, mod: 4, ind: 6},
  {axis: 3, pos: 0.44, mod: 4, ind: 0},
  {axis: 3, pos: 0.45, mod: 4, ind: 0},
  {axis: 3, pos: 0.46, mod: 4, ind: 6},
  {axis: 1, pos: 0.46, mod: 4, ind: 6},
  {axis: 1, pos: 0.46, mod: 4, ind: 6},
  {axis: 5, pos: 0.46, mod: 4, ind: 0},
  {axis: 3, pos: 0.47, mod: 4, ind: 0},
  {axis: 3, pos: 0.47, mod: 4, ind: 0},
  {axis: 1, pos: 0.47, mod: 4, ind: 0},
  {axis: 3, pos: 0.47, mod: 4, ind: 0},
  {axis: 3, pos: 0.47, mod: 4, ind: 0},
  {axis: 3, pos: 0.48, mod: 4, ind: 6},
  {axis: 1, pos: 0.48, mod: 4, ind: 0},
  {axis: 1, pos: 0.48, mod: 4, ind: 6},
  {axis: 3, pos: 0.48, mod: 4, ind: 6},
  {axis: 3, pos: 0.49, mod: 4, ind: 6},
  {axis: 3, pos: 0.49, mod: 4, ind: 6},
  {axis: 1, pos: 0.49, mod: 4, ind: 0},
  {axis: 3, pos: 0.49, mod: 4, ind: 6},
  {axis: 3, pos: 0.5, mod: 4, ind: 6},
  {axis: 3, pos: 0.5, mod: 4, ind: 6},
  {axis: 1, pos: 0.5, mod: 4, ind: 6},
  {axis: 1, pos: 0.5, mod: 4, ind: 0},
  {axis: 3, pos: 0.5, mod: 4, ind: 0},
  {axis: 3, pos: 0.5, mod: 4, ind: 0},
  {axis: 3, pos: 0.51, mod: 4, ind: 6},
  {axis: 3, pos: 0.51, mod: 4, ind: 6},
  {axis: 3, pos: 0.51, mod: 4, ind: 6},
  {axis: 1, pos: 0.51, mod: 4, ind: 0},
  {axis: 1, pos: 0.51, mod: 4, ind: 6},
  {axis: 3, pos: 0.52, mod: 4, ind: 0},
  {axis: 1, pos: 0.52, mod: 4, ind: 0},
  {axis: 3, pos: 0.52, mod: 4, ind: 0},
  {axis: 3, pos: 0.52, mod: 4, ind: 6},
  {axis: 1, pos: 0.52, mod: 4, ind: 0},
  {axis: 3, pos: 0.52, mod: 4, ind: 6},
  {axis: 3, pos: 0.52, mod: 4, ind: 6},
  {axis: 1, pos: 0.53, mod: 4, ind: 6},
  {axis: 3, pos: 0.53, mod: 4, ind: 6},
  {axis: 3, pos: 0.53, mod: 4, ind: 6},
  {axis: 3, pos: 0.53, mod: 4, ind: 0},
  {axis: 3, pos: 0.53, mod: 4, ind: 6},
  {axis: 3, pos: 0.53, mod: 4, ind: 0},
  {axis: 3, pos: 0.53, mod: 4, ind: 6},
  {axis: 3, pos: 0.53, mod: 4, ind: 6},
  {axis: 3, pos: 0.53, mod: 4, ind: 6},
  {axis: 3, pos: 0.54, mod: 4, ind: 0},
  {axis: 3, pos: 0.54, mod: 4, ind: 6},
  {axis: 3, pos: 0.54, mod: 4, ind: 6},
  {axis: 1, pos: 0.54, mod: 4, ind: 6},
  {axis: 3, pos: 0.54, mod: 4, ind: 0},
  {axis: 3, pos: 0.54, mod: 4, ind: 6},
  {axis: 3, pos: 0.54, mod: 4, ind: 6},
  {axis: 3, pos: 0.55, mod: 4, ind: 6},
  {axis: 3, pos: 0.55, mod: 4, ind: 6},
  {axis: 5, pos: 0.55, mod: 4, ind: 6},
  {axis: 3, pos: 0.55, mod: 4, ind: 0},
  {axis: 3, pos: 0.55, mod: 4, ind: 0},
  {axis: 3, pos: 0.55, mod: 4, ind: 6},
  {axis: 3, pos: 0.55, mod: 4, ind: 6},
  {axis: 3, pos: 0.55, mod: 4, ind: 6},
  {axis: 1, pos: 0.56, mod: 4, ind: 0},
  {axis: 3, pos: 0.56, mod: 4, ind: 0},
  {axis: 5, pos: 0.56, mod: 4, ind: 6},
  {axis: 1, pos: 0.56, mod: 4, ind: 6},
  {axis: 3, pos: 0.56, mod: 4, ind: 0},
  {axis: 3, pos: 0.57, mod: 4, ind: 0},
  {axis: 3, pos: 0.57, mod: 4, ind: 6},
  {axis: 3, pos: 0.57, mod: 4, ind: 6},
  {axis: 3, pos: 0.57, mod: 4, ind: 6},
  {axis: 1, pos: 0.57, mod: 4, ind: 0},
  {axis: 3, pos: 0.57, mod: 4, ind: 6},
  {axis: 3, pos: 0.57, mod: 4, ind: 0},
  {axis: 3, pos: 0.57, mod: 4, ind: 0},
  {axis: 3, pos: 0.57, mod: 4, ind: 6},
  {axis: 3, pos: 0.58, mod: 4, ind: 0},
  {axis: 3, pos: 0.58, mod: 4, ind: 6},
  {axis: 3, pos: 0.58, mod: 4, ind: 6},
  {axis: 5, pos: 0.58, mod: 4, ind: 6},
  {axis: 5, pos: 0.58, mod: 4, ind: 6},
  {axis: 3, pos: 0.59, mod: 4, ind: 6},
  {axis: 3, pos: 0.59, mod: 4, ind: 6},
  {axis: 3, pos: 0.59, mod: 4, ind: 0},
  {axis: 3, pos: 0.59, mod: 4, ind: 0},
  {axis: 3, pos: 0.59, mod: 4, ind: 0},
  {axis: 5, pos: 0.59, mod: 4, ind: 6},
  {axis: 5, pos: 0.59, mod: 4, ind: 0},
  {axis: 3, pos: 0.6, mod: 4, ind: 6},
  {axis: 3, pos: 0.6, mod: 4, ind: 6},
  {axis: 1, pos: 0.6, mod: 4, ind: 0},
  {axis: 3, pos: 0.6, mod: 4, ind: 0},
  {axis: 5, pos: 0.6, mod: 4, ind: 6},
  {axis: 3, pos: 0.6, mod: 4, ind: 6},
  {axis: 3, pos: 0.6, mod: 4, ind: 0},
  {axis: 1, pos: 0.6, mod: 4, ind: 0},
  {axis: 5, pos: 0.6, mod: 4, ind: 0},
  {axis: 1, pos: 0.6, mod: 4, ind: 0},
  {axis: 3, pos: 0.61, mod: 4, ind: 0},
  {axis: 3, pos: 0.61, mod: 4, ind: 0},
  {axis: 3, pos: 0.61, mod: 4, ind: 6},
  {axis: 3, pos: 0.61, mod: 4, ind: 0},
  {axis: 5, pos: 0.61, mod: 4, ind: 6},
  {axis: 5, pos: 0.62, mod: 4, ind: 0},
  {axis: 3, pos: 0.62, mod: 4, ind: 6},
  {axis: 5, pos: 0.62, mod: 4, ind: 6},
  {axis: 5, pos: 0.62, mod: 4, ind: 0},
  {axis: 3, pos: 0.62, mod: 4, ind: 0},
  {axis: 5, pos: 0.62, mod: 4, ind: 6},
  {axis: 1, pos: 0.62, mod: 4, ind: 0},
  {axis: 5, pos: 0.62, mod: 4, ind: 6},
  {axis: 3, pos: 0.62, mod: 4, ind: 0},
  {axis: 3, pos: 0.62, mod: 4, ind: 6},
  {axis: 3, pos: 0.62, mod: 4, ind: 0},
  {axis: 3, pos: 0.62, mod: 4, ind: 6},
  {axis: 5, pos: 0.63, mod: 4, ind: 6},
  {axis: 1, pos: 0.63, mod: 4, ind: 0},
  {axis: 1, pos: 0.63, mod: 4, ind: 0},
  {axis: 3, pos: 0.63, mod: 4, ind: 6},
  {axis: 3, pos: 0.63, mod: 4, ind: 0},
  {axis: 3, pos: 0.63, mod: 4, ind: 0},
  {axis: 1, pos: 0.63, mod: 4, ind: 0},
  {axis: 3, pos: 0.64, mod: 4, ind: 0},
  {axis: 5, pos: 0.64, mod: 4, ind: 6},
  {axis: 1, pos: 0.64, mod: 4, ind: 6},
  {axis: 1, pos: 0.64, mod: 4, ind: 0},
  {axis: 5, pos: 0.64, mod: 4, ind: 6},
  {axis: 5, pos: 0.64, mod: 4, ind: 0},
  {axis: 3, pos: 0.64, mod: 4, ind: 0},
  {axis: 5, pos: 0.64, mod: 4, ind: 6},
  {axis: 3, pos: 0.64, mod: 4, ind: 6},
  {axis: 5, pos: 0.65, mod: 4, ind: 6},
  {axis: 3, pos: 0.65, mod: 4, ind: 6},
  {axis: 5, pos: 0.65, mod: 4, ind: 0},
  {axis: 1, pos: 0.65, mod: 4, ind: 0},
  {axis: 5, pos: 0.66, mod: 4, ind: 6},
  {axis: 5, pos: 0.66, mod: 4, ind: 6},
  {axis: 1, pos: 0.66, mod: 4, ind: 0},
  {axis: 3, pos: 0.66, mod: 4, ind: 0},
  {axis: 3, pos: 0.67, mod: 4, ind: 0},
  {axis: 3, pos: 0.67, mod: 4, ind: 0},
  {axis: 3, pos: 0.67, mod: 4, ind: 6},
  {axis: 3, pos: 0.67, mod: 4, ind: 6},
  {axis: 3, pos: 0.67, mod: 4, ind: 0},
  {axis: 1, pos: 0.67, mod: 4, ind: 0},
  {axis: 3, pos: 0.67, mod: 4, ind: 0},
  {axis: 3, pos: 0.68, mod: 4, ind: 0},
  {axis: 3, pos: 0.68, mod: 4, ind: 0},
  {axis: 3, pos: 0.68, mod: 4, ind: 6},
  {axis: 3, pos: 0.68, mod: 4, ind: 0},
  {axis: 1, pos: 0.68, mod: 4, ind: 0},
  {axis: 3, pos: 0.68, mod: 4, ind: 6},
  {axis: 5, pos: 0.69, mod: 4, ind: 6},
  {axis: 3, pos: 0.69, mod: 4, ind: 0},
  {axis: 3, pos: 0.69, mod: 4, ind: 0},
  {axis: 3, pos: 0.69, mod: 4, ind: 6},
  {axis: 1, pos: 0.69, mod: 4, ind: 0},
  {axis: 3, pos: 0.69, mod: 4, ind: 0},
  {axis: 3, pos: 0.69, mod: 4, ind: 6},
  {axis: 3, pos: 0.7, mod: 4, ind: 6},
  {axis: 3, pos: 0.7, mod: 4, ind: 6},
  {axis: 3, pos: 0.7, mod: 4, ind: 0},
  {axis: 3, pos: 0.7, mod: 4, ind: 6},
  {axis: 3, pos: 0.7, mod: 4, ind: 0},
  {axis: 5, pos: 0.7, mod: 4, ind: 6},
  {axis: 3, pos: 0.7, mod: 4, ind: 6},
  {axis: 3, pos: 0.71, mod: 4, ind: 6},
  {axis: 3, pos: 0.71, mod: 4, ind: 6},
  {axis: 3, pos: 0.71, mod: 4, ind: 6},
  {axis: 3, pos: 0.71, mod: 4, ind: 6},
  {axis: 5, pos: 0.71, mod: 4, ind: 0},
  {axis: 3, pos: 0.71, mod: 4, ind: 0},
  {axis: 3, pos: 0.71, mod: 4, ind: 6},
  {axis: 3, pos: 0.71, mod: 4, ind: 0},
  {axis: 5, pos: 0.71, mod: 4, ind: 6},
  {axis: 5, pos: 0.72, mod: 4, ind: 6},
  {axis: 3, pos: 0.72, mod: 4, ind: 6},
  {axis: 1, pos: 0.72, mod: 4, ind: 0},
  {axis: 3, pos: 0.72, mod: 4, ind: 0},
  {axis: 5, pos: 0.72, mod: 4, ind: 0},
  {axis: 3, pos: 0.73, mod: 4, ind: 6},
  {axis: 5, pos: 0.73, mod: 4, ind: 6},
  {axis: 5, pos: 0.73, mod: 4, ind: 6},
  {axis: 5, pos: 0.73, mod: 4, ind: 6},
  {axis: 3, pos: 0.73, mod: 4, ind: 0},
  {axis: 3, pos: 0.73, mod: 4, ind: 0},
  {axis: 5, pos: 0.74, mod: 4, ind: 6},
  {axis: 3, pos: 0.74, mod: 4, ind: 6},
  {axis: 3, pos: 0.74, mod: 4, ind: 5},
  {axis: 3, pos: 0.74, mod: 4, ind: 0},
  {axis: 3, pos: 0.74, mod: 4, ind: 0},
  {axis: 3, pos: 0.75, mod: 4, ind: 0},
  {axis: 1, pos: 0.75, mod: 4, ind: 0},
  {axis: 3, pos: 0.75, mod: 4, ind: 0},
  {axis: 5, pos: 0.75, mod: 4, ind: 6},
  {axis: 3, pos: 0.75, mod: 4, ind: 0},
  {axis: 3, pos: 0.76, mod: 4, ind: 0},
  {axis: 5, pos: 0.76, mod: 4, ind: 6},
  {axis: 3, pos: 0.76, mod: 4, ind: 6},
  {axis: 5, pos: 0.76, mod: 4, ind: 5},
  {axis: 5, pos: 0.76, mod: 4, ind: 6},
  {axis: 5, pos: 0.76, mod: 4, ind: 6},
  {axis: 5, pos: 0.76, mod: 4, ind: 6},
  {axis: 1, pos: 0.76, mod: 4, ind: 0},
  {axis: 3, pos: 0.76, mod: 4, ind: 0},
  {axis: 3, pos: 0.76, mod: 4, ind: 0},
  {axis: 3, pos: 0.77, mod: 4, ind: 0},
  {axis: 3, pos: 0.77, mod: 4, ind: 6},
  {axis: 3, pos: 0.77, mod: 4, ind: 5},
  {axis: 5, pos: 0.77, mod: 4, ind: 6},
  {axis: 5, pos: 0.78, mod: 4, ind: 6},
  {axis: 3, pos: 0.78, mod: 4, ind: 0},
  {axis: 3, pos: 0.78, mod: 4, ind: 6},
  {axis: 3, pos: 0.78, mod: 4, ind: 0},
  {axis: 3, pos: 0.78, mod: 4, ind: 6},
  {axis: 5, pos: 0.78, mod: 4, ind: 6},
  {axis: 5, pos: 0.78, mod: 4, ind: 6},
  {axis: 5, pos: 0.78, mod: 4, ind: 6},
  {axis: 3, pos: 0.79, mod: 4, ind: 0},
  {axis: 3, pos: 0.79, mod: 4, ind: 0},
  {axis: 1, pos: 0.79, mod: 4, ind: 5},
  {axis: 3, pos: 0.79, mod: 4, ind: 6},
  {axis: 5, pos: 0.79, mod: 4, ind: 5},
  {axis: 3, pos: 0.79, mod: 4, ind: 0},
  {axis: 1, pos: 0.79, mod: 4, ind: 0},
  {axis: 3, pos: 0.8, mod: 4, ind: 0},
  {axis: 5, pos: 0.8, mod: 4, ind: 6},
  {axis: 5, pos: 0.8, mod: 4, ind: 6},
  {axis: 3, pos: 0.8, mod: 4, ind: 6},
  {axis: 5, pos: 0.81, mod: 4, ind: 6},
  {axis: 5, pos: 0.81, mod: 4, ind: 6},
  {axis: 3, pos: 0.81, mod: 4, ind: 5},
  {axis: 5, pos: 0.81, mod: 4, ind: 5},
  {axis: 1, pos: 0.81, mod: 4, ind: 5},
  {axis: 3, pos: 0.81, mod: 4, ind: 0},
  {axis: 3, pos: 0.81, mod: 4, ind: 5},
  {axis: 1, pos: 0.81, mod: 4, ind: 0},
  {axis: 3, pos: 0.82, mod: 4, ind: 5},
  {axis: 5, pos: 0.82, mod: 4, ind: 6},
  {axis: 1, pos: 0.82, mod: 4, ind: 0},
  {axis: 3, pos: 0.82, mod: 4, ind: 5},
  {axis: 3, pos: 0.82, mod: 4, ind: 0},
  {axis: 3, pos: 0.82, mod: 4, ind: 5},
  {axis: 3, pos: 0.83, mod: 4, ind: 5},
  {axis: 3, pos: 0.83, mod: 4, ind: 0},
  {axis: 3, pos: 0.84, mod: 4, ind: 5},
  {axis: 1, pos: 0.84, mod: 4, ind: 0},
  {axis: 3, pos: 0.84, mod: 4, ind: 6},
  {axis: 3, pos: 0.85, mod: 4, ind: 5},
  {axis: 3, pos: 0.85, mod: 4, ind: 0},
  {axis: 3, pos: 0.85, mod: 4, ind: 0},
  {axis: 3, pos: 0.85, mod: 4, ind: 5},
  {axis: 5, pos: 0.85, mod: 4, ind: 6},
  {axis: 5, pos: 0.85, mod: 4, ind: 5},
  {axis: 3, pos: 0.85, mod: 4, ind: 5},
  {axis: 1, pos: 0.85, mod: 4, ind: 0},
  {axis: 1, pos: 0.86, mod: 4, ind: 5},
  {axis: 3, pos: 0.86, mod: 4, ind: 5},
  {axis: 5, pos: 0.86, mod: 4, ind: 6},
  {axis: 3, pos: 0.86, mod: 4, ind: 5},
  {axis: 5, pos: 0.86, mod: 4, ind: 6},
  {axis: 3, pos: 0.86, mod: 4, ind: 5},
  {axis: 5, pos: 0.86, mod: 4, ind: 5},
  {axis: 3, pos: 0.87, mod: 4, ind: 5},
  {axis: 5, pos: 0.87, mod: 4, ind: 5},
  {axis: 5, pos: 0.87, mod: 4, ind: 5},
  {axis: 5, pos: 0.87, mod: 4, ind: 5},
  {axis: 5, pos: 0.88, mod: 4, ind: 5},
  {axis: 3, pos: 0.88, mod: 4, ind: 5},
  {axis: 3, pos: 0.89, mod: 4, ind: 5},
  {axis: 3, pos: 0.89, mod: 4, ind: 6},
  {axis: 5, pos: 0.89, mod: 4, ind: 6},
  {axis: 3, pos: 0.89, mod: 4, ind: 5},
  {axis: 5, pos: 0.9, mod: 4, ind: 5},
  {axis: 3, pos: 0.9, mod: 4, ind: 5},
  {axis: 3, pos: 0.9, mod: 4, ind: 5},
  {axis: 3, pos: 0.9, mod: 4, ind: 5},
  {axis: 3, pos: 0.91, mod: 4, ind: 5},
  {axis: 3, pos: 0.92, mod: 4, ind: 5},
  {axis: 5, pos: 0.93, mod: 4, ind: 5},
  {axis: 3, pos: 0.93, mod: 4, ind: 5},
  {axis: 5, pos: 0.93, mod: 4, ind: 5},
  {axis: 1, pos: 0.93, mod: 4, ind: 5},
  {axis: 5, pos: 0.93, mod: 4, ind: 5},
  {axis: 3, pos: 0.94, mod: 4, ind: 5},
  {axis: 3, pos: 0.94, mod: 4, ind: 5},
  {axis: 5, pos: 0.94, mod: 4, ind: 5},
  {axis: 5, pos: 0.94, mod: 4, ind: 5},
  {axis: 5, pos: 0.94, mod: 4, ind: 5},
  {axis: 3, pos: 0.95, mod: 4, ind: 5},
  {axis: 3, pos: 0.95, mod: 4, ind: 5},
  {axis: 5, pos: 0.95, mod: 4, ind: 5},
  {axis: 5, pos: 0.95, mod: 4, ind: 5},
  {axis: 3, pos: 0.96, mod: 4, ind: 5},
  {axis: 3, pos: 0.96, mod: 4, ind: 5},
  {axis: 5, pos: 0.96, mod: 4, ind: 5},
  {axis: 3, pos: 0.96, mod: 4, ind: 5},
  {axis: 5, pos: 0.97, mod: 4, ind: 5},
  {axis: 5, pos: 0.97, mod: 4, ind: 5},
  {axis: 5, pos: 0.97, mod: 4, ind: 5},
  {axis: 5, pos: 0.97, mod: 4, ind: 5},
  {axis: 3, pos: 0.98, mod: 4, ind: 5},
  {axis: 3, pos: 0.98, mod: 4, ind: 5},
  {axis: 5, pos: 0.98, mod: 4, ind: 5},
  {axis: 5, pos: 0.99, mod: 4, ind: 5},
  {axis: 3, pos: 1.0, mod: 4, ind: 5},
  {axis: 2, pos: 0.5, mod: 4, ind: 4},
  {axis: 3, pos: 0.48, mod: 4, ind: 4},
  {axis: 3, pos: 0.61, mod: 4, ind: 4},
  {axis: 2, pos: 0.61, mod: 4, ind: 4},
  {axis: 2, pos: 0.48, mod: 4, ind: 4},
  {axis: 3, pos: 0.5, mod: 4, ind: 4},
];