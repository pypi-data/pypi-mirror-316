import pytest
import glob
import numpy as np
from axonemalyze.segment_axonemes import *
from axonemalyze.estimate_circularity import *

def test_distance():
    # test distances for kicks
    assert 1 == distance([0,0,0], [1,0,0])
    assert 1 == distance([0,0,0], [0,1,0])
    assert 1 == distance([0,0,0], [0,0,1])

def test_angle():
    # test angles for kicks
    assert np.isclose(np.pi/2, angle_between_points(np.array([1,0,0]), np.array([0,0,0]), np.array([0,1,0])))
    assert np.isclose(np.pi/2, angle_between_points(np.array([1,0,0]), np.array([0,0,0]), np.array([0,0,1])))
    assert np.isclose(np.pi, angle_between_points(np.array([1,0,0]), np.array([0,0,0]), np.array([-1,0,0])))

def test_load():
    # test loading
    xyz = load_coordinates('tests/test_coords/rec_DNAI1_9_1_PtsAdded.coords')
    array = np.array([[803.2, 93., 126.94],
     [795.48,  92.73, 129.02],
     [787.76,  92.46, 131.09],
     [780.04,  92.18, 133.17],
     [772.31,  91.91, 135.24]])
    assert np.all(array == xyz.values[:5,:])

def test_segment():
    # test clustering
    tomo_files = sorted(glob.glob('tests/test_coords/*coords'))
    assert [{0, 1, 2, 3, 4}, {5}, {6, 7, 8, 9, 11, 12, 13, 14, 15}, {10, 16, 17, 18, 19, 20, 21, 22, 23}] == segment(tomo_files, 'DNAI1_9', 'tests/test_coords/segmented/')
