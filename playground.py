'module docstring should be here'

import logging
import numpy as np
import subprocess
from sphere import \
    Sphere, get_sphere, epsilon_distance, equal_in_practice, zero_in_practice
from timer import Timer

logging.basicConfig(format='%(asctime)s.%(msecs)d %(levelname)-8s %(filename)s:L%(lineno)d %(funcName)s: %(message)s',
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
    logger.info('SPHERE_42 given 4 straight crosshair points: %s', SPHERE_42)

def get_sphere_given4RotatedCrosshairPoints_From_42():
    POINT_1 = np.array([-58.7767,  4.9348,    -3.7779], np.float_)
    POINT_2 = np.array([-13.3565, -0.644701, -29.8066], np.float_)
    POINT_3 = np.array([-16.4319, -0.999301,   1.6949], np.float_)
    POINT_4 = np.array([-55.543,   4.7384,   -37.1852], np.float_)
    POINTS = (POINT_1, POINT_2, POINT_3, POINT_4)
    SPHERE_42 = get_sphere(POINTS)
    logger.info('SPHERE_42 given 4 rotated crosshair points: %s', SPHERE_42)

def get_sphere_given4StraightCrosshairPoints_From_46():
    POINT_1 = np.array([-36.9284,  2.1009,  -1.0189], np.float_)
    POINT_2 = np.array([-37.0922,  2.2078, -51.4502], np.float_)
    POINT_3 = np.array([-10.4147, -0.1741, -26.0583], np.float_)
    POINT_4 = np.array([-65.5153,  8.0756, -26.2123], np.float_)
    POINTS = (POINT_1, POINT_2, POINT_3, POINT_4)
    SPHERE_46 = get_sphere(POINTS)
    logger.info('SPHERE_46 given 4 straight crosshair points: %s', SPHERE_46)

def get_sphere_given4RotatedCrosshairPoints_From_46():
    POINT_1 = np.array([-56.2434, 5.6835, -8.3162], np.float_)
    POINT_2 = np.array([-15.5323, 0.0641003, -37.5089], np.float_)
    POINT_3 = np.array([-54.5831, 5.3886, -44.8675], np.float_)
    POINT_4 = np.array([-18.2069, 0.2075, -3.8871], np.float_)
    POINTS = (POINT_1, POINT_2, POINT_3, POINT_4)
    SPHERE_46 = get_sphere(POINTS)
    logger.info('SPHERE_46 given 4 rotated crosshair points: %s', SPHERE_46)

def get_git_version():
    COMMAND = "git --version"
    timer = Timer()
    RESULT = subprocess.call(COMMAND, shell=True)  # returns the exit code in unix
    logger.info('Command \"%s\" took %s and returned %d', COMMAND, timer.get_duration_string(), RESULT)

def download_file_using_curl(url, output_filename):
    COMMAND = "curl " + url + " -o " + output_filename
    timer = Timer()
    RESULT = subprocess.call(COMMAND, shell=True)  # returns the exit code in unix
    if RESULT == 0:
        logger.info('File "%s" has been downloaded in %s', output_filename, timer.get_duration_string())
    else:
        logger.error('Failed to download file "%s"', output_filename)

if __name__ == '__main__':

    get_sphere_given4StraightCrosshairPoints_From_42()
    get_sphere_given4RotatedCrosshairPoints_From_42()

    get_sphere_given4StraightCrosshairPoints_From_46()
    get_sphere_given4RotatedCrosshairPoints_From_46()

    get_git_version()

    FILENAME_AND_URL_ARRAY = [
      # ['data/_L.7z', 'https://ucfc43a66550d50a72d5c6ad893966.dl.dropboxusercontent.com/cd/0/get/Acgtbdfxtq1Hv_TCylXob8zA8RNVbg9qJNZUkuBJ9GrD039rGB4SQ4vvTlDHCw_Wvzxivl1re-R_i-HM_dkKPzcpowNgxikC8ot3SkB2Y7_gSMYBVN8gxsCMzExKMUvxqvU/file#'],
      # ['data/_M.7z', 'https://ucfa13937452aeb2f165f01ea16937.dl.dropboxusercontent.com/cd/0/get/Aclm3eKtglwJbgFkBAX8u_8Lbf1ZkoqfgchqjzGEXju8LUjgHyIfRGKfKnpHg1opTaisrztJFu8Sda-S3He6zgthINXLc5dpwJUo8dqaCX1SE5dbpdQoMsffGxqe8hmsg_k/file?dl=1#'],
      ['data/_C54.xml', 'https://uc7b36b201202ac7cc04d68a05a966.dl.dropboxusercontent.com/cd/0/get/AclhxNHBCsS2_ilqbP43MbJnWUNyZmirnWtmSg3D5bM8pDq4WUk4H2sk_dMI0j63OU3q5HQyDAvxCdI3LrjlGms7Ui5B4zsSIJMoEyUmJB5F9SpRKIHYU3J1ZNSNgwl_eFg/file#'],
      ['data/_F.stl', 'https://uc9961f6bd3472cdc89cd193cf4f37.dl.dropboxusercontent.com/cd/0/get/AcmcZszabuV-PTcgdSLBXqurosEBnS7zHxU0Kj5cjLkNUbIIoigDcRQsMjYa3Ndr7xWHXljjLn0MANfe-AEntU6vSz2Q7yosMEDkb_g2svrOjEGk9ila4Vd8lQLr8KJdo7k/file#'],
      ['data/_L.stl', 'https://uc0a059daf35cb3466bfa34ee51666.dl.dropboxusercontent.com/cd/0/get/AcnlQBb60Hl8eGw5p-s99eCERh8m32TdJeU-RMh1JL_LbI7SNemva-Hp5zoxArCRBjwm_49fT6aClct0FAHXSyDFopXVy6K2__tFNrliWp-O9mRmmEkL-GDOHml1xAMYuLY/file#'],
      ['data/_R.stl', 'https://uc0dfa07f6b21b5c7d4102e78bb537.dl.dropboxusercontent.com/cd/0/get/AcnyAgA-ShRXNUP2rp8iCvrLd99DRThS_p1TWfgK1SDV0TRYlY6UdLHbN24WOsNv2TeJTjKAPTzkZdvJLITMy7I4TO5JEHhm8rLt7uv9ZKOvXqPfNloTB4WiVwHfzyuYYos/file#']
    ]
    for filename_and_url in FILENAME_AND_URL_ARRAY:
        filename, url = filename_and_url
        download_file_using_curl(url, filename)
        # decompress_7z_file
        # generate_sizes
  