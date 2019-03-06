'module docstring should be here'

import logging
import numpy as np
import subprocess
from sphere import \
    Sphere, get_sphere, epsilon_distance, equal_in_practice, zero_in_practice
from timer import Timer

logging.basicConfig(format='%(asctime)s.%(msecs)d %(levelname)-8s %(filename)s:L%(lineno)d %(message)s',
    datefmt='%m.%d.%Y %H:%M:%S',
    level=logging.DEBUG)

logger = logging.getLogger(__name__)

def average(*numbers):
    """Self-explanatory"""
    if not numbers:
        raise ValueError('numbers should not be empty')

    numbers = [float(number) for number in numbers]
    return sum(numbers) / float(len(numbers))

def get_sphere_given4StraightCrosshairPoints_From_42():
    POINT_1 = np.array([-35.3025, 0.6357,   3.8584], np.float_)
    POINT_2 = np.array([-35.0932, 1.3599, -43.2535], np.float_)
    POINT_3 = np.array([ -9.054, -0.958,  -19.6768], np.float_)
    POINT_4 = np.array([-62.0412, 5.9778, -19.7658], np.float_)
    POINTS = (POINT_1, POINT_2, POINT_3, POINT_4)
    SPHERE_42 = get_sphere(POINTS)
    logger.info('SPHERE_42 given 4 straight crosshair points: ' + SPHERE_42.__str__())

def get_sphere_given4RotatedCrosshairPoints_From_42():
    POINT_1 = np.array([-58.7767,  4.9348,    -3.7779], np.float_)
    POINT_2 = np.array([-13.3565, -0.644701, -29.8066], np.float_)
    POINT_3 = np.array([-16.4319, -0.999301,   1.6949], np.float_)
    POINT_4 = np.array([-55.543,   4.7384,   -37.1852], np.float_)
    POINTS = (POINT_1, POINT_2, POINT_3, POINT_4)
    SPHERE_42 = get_sphere(POINTS)
    logger.info('SPHERE_42 given 4 rotated crosshair points: ' + SPHERE_42.__str__())

def get_sphere_given4StraightCrosshairPoints_From_46():
    POINT_1 = np.array([-36.9284,  2.1009,  -1.0189], np.float_)
    POINT_2 = np.array([-37.0922,  2.2078, -51.4502], np.float_)
    POINT_3 = np.array([-10.4147, -0.1741, -26.0583], np.float_)
    POINT_4 = np.array([-65.5153,  8.0756, -26.2123], np.float_)
    POINTS = (POINT_1, POINT_2, POINT_3, POINT_4)
    SPHERE_46 = get_sphere(POINTS)
    logger.info('SPHERE_46 given 4 straight crosshair points: ' + SPHERE_46.__str__())

def get_sphere_given4RotatedCrosshairPoints_From_46():
    POINT_1 = np.array([-56.2434, 5.6835, -8.3162], np.float_)
    POINT_2 = np.array([-15.5323, 0.0641003, -37.5089], np.float_)
    POINT_3 = np.array([-54.5831, 5.3886, -44.8675], np.float_)
    POINT_4 = np.array([-18.2069, 0.2075, -3.8871], np.float_)
    POINTS = (POINT_1, POINT_2, POINT_3, POINT_4)
    SPHERE_46 = get_sphere(POINTS)
    logger.info('SPHERE_46 given 4 rotated crosshair points: ' + SPHERE_46.__str__())

def download_file_using_curl(url, output_filename):
    COMMAND = "curl " + url + " -o " + output_filename
    timer = Timer()
    RESULT = subprocess.call(COMMAND, shell=True)  # returns the exit code in unix
    if RESULT == 0:
        logger.info('File ' + output_filename + ' downloaded in ' + timer.get_duration_string())
    else:
        logger.error('Failed to download file ' + output_filename)

if __name__ == '__main__':

    get_sphere_given4StraightCrosshairPoints_From_42()
    get_sphere_given4RotatedCrosshairPoints_From_42()

    get_sphere_given4StraightCrosshairPoints_From_46()
    get_sphere_given4RotatedCrosshairPoints_From_46()

    command = "git --version"
    timer = Timer()
    RESULT = subprocess.call(command, shell=True)  # returns the exit code in unix
    logger.info('Command \"' + command + '\" returned ' + str(RESULT) + ' and took ' + timer.get_duration_string())

    download_file_using_curl("https://ucfc6643a66550d50a72d5c6ad8939.dl.dropboxusercontent.com/cd/0/get/Acgtbdfxtq1Hv_TCylXob8zA8RNVbg9qJNZUkuBJ9GrD039rGB4SQ4vvTlDHCw_Wvzxivl1re-R_i-HM_dkKPzcpowNgxikC8ot3SkB2Y7_gSMYBVN8gxsCMzExKMUvxqvU/file#", "_L.7z")
    # download_file_using_curl("https://uc664893b3b0452d68ea9a97c6d215.dl.dropboxusercontent.com/cd/0/get/AcizWDT7iMqgf95wFZmzRDSNI8abCb1scDvPIXmwT2blSDWJPRB1reUF-C46fXplNvTR3rB2s4VYbYM4tVzF_-4B9DAJV4gJYynGKFvmD_dyjIM-2H4oIHuWmCy-1mkhomk/file#", "_M.7z")
  