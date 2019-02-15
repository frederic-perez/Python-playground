"""
Run the tests by executing, for all test classes:

  $ python -m unittest -v test_input_output
"""

import numpy as np
import unittest
from input_output import save_as_ply

class Test_save_as_ply(unittest.TestCase):

    def test_GivenNoParameters_When_save_as_play_ThenExceptionIsRaised(self):
        self.assertRaises(TypeError, save_as_ply)

    def test_GivenAnNonexistentInputFile_When_save_as_play_ThenExceptionIsRaised(self):
        NONEXISTENT_FILE_IN_XYX = 'data/this-file-does-not-exist'
        FILENAME_OUT_PLY = "data/out.ply"
        self.assertRaises(IOError, save_as_ply, NONEXISTENT_FILE_IN_XYX, FILENAME_OUT_PLY)

    def test_GivenAnEmptyInputFile_When_save_as_play_ThenExceptionIsRaised(self):
        EMPTY_FILE_IN_XYX = 'data/empty-file'
        FILENAME_OUT_PLY = "data/out.ply"
        self.assertRaises(ValueError, save_as_ply, EMPTY_FILE_IN_XYX, FILENAME_OUT_PLY)

    def test_GivenAFaultyInputFile_When_save_as_play_ThenExceptionIsRaised(self):
        FAULTY_FILE_IN_XYX = 'data/points-in--faulty.xyz'
        FILENAME_OUT_PLY = "data/out.ply"
        self.assertRaises(ValueError, save_as_ply, FAULTY_FILE_IN_XYX, FILENAME_OUT_PLY)

if __name__ == '__main__':
    unittest.main()
