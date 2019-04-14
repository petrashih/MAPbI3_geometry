#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 15:33:16 2019

This is used to convert .xyz file into direct coordinate, and create a POSCAR
input   .xyz file
        lattice parameters
        POSCAR first seven lines
output  POSCAR

@author: petrashih
"""
FileXYZ = 'Chosen_structure_4069.xyz'
FileDir = 'POSCAR_4069'
import numpy as np
## input the lattice parameters
a = [12.6140, 0, 0]
b = [0, 12.6140, 0]
c = [0, 0, 12.6140]

## construct the matrix used after
lattice_M = np.block([a, b, c])

lattice_M_inv = np.linalg.inv(lattice_M)
#D = np.matmul(lattice_M, lattice_M_inv)

## load structure .xyz
with open(FileXYZ) as f:
    lines = f.readlines()
    
NAtoms = len(lines) - 2
Structure = []
for i, l in enumerate(lines):
    if i >= 2:
        i, x, y, z = l.split()
        r = float(x), float(y), float(z)
        Structure.append([*r])


## transform cartesian coordinate to direct coordinate
direct_coor = []
for i, R in enumerate(Structure):
    direct_vec = lattice_M_inv.dot(np.array([R]).T)
    direct_coor.append(direct_vec.T.tolist()[-1])
    
## save the output structure in direct coordinate
with open(FileDir, 'w') as f:
    f.write("C_N_H_Pb_I\n")
    f.write("1.0\n")
    f.write("       {}\t{}\t{}\n".format(*a))
    f.write("       {}\t{}\t{}\n".format(*b))
    f.write("       {}\t{}\t{}\n".format(*c))
    f.write("    C    N    H   Pb    I\n")
    f.write("    8    8   48    8   24\n")
    f.write("Direct\n")
    for r in direct_coor:
        f.write("{}\t{}\t{}\n".format(*r))
f.close()


