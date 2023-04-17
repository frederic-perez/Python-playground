"""
Run the tests by executing, for all test classes:

  $ python -m unittest -v test_input_output.py
  or
  $ python test_input_output.py
"""

import unittest
from input_output import save_as_ply


class Test_save_as_ply(unittest.TestCase):

    def test_GivenNoParameters_When_save_as_play_ThenExceptionIsRaised(self):
        self.assertRaises(TypeError, save_as_ply)

    def test_GivenAnNonexistentInputFile_When_save_as_play_ThenExceptionIsRaised(self):
        nonexistent_file_in_xyx = 'data/this-file-does-not-exist'
        filename_out_ply = "data/out.ply"
        self.assertRaises(IOError, save_as_ply, nonexistent_file_in_xyx, filename_out_ply)

    def test_GivenAnEmptyInputFile_When_save_as_play_ThenExceptionIsRaised(self):
        empty_file_in_xyx = 'data/empty-file'
        filename_out_ply = "data/out.ply"
        self.assertRaises(ValueError, save_as_ply, empty_file_in_xyx, filename_out_ply)

    def test_GivenAFaultyInputFile_When_save_as_play_ThenExceptionIsRaised(self):
        faulty_file_in_xyx = 'data/points-in--faulty.xyz'
        filename_out_ply = "data/out.ply"
        self.assertRaises(ValueError, save_as_ply, faulty_file_in_xyx, filename_out_ply)


if __name__ == '__main__':
    unittest.main()
