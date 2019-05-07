'module docstring should be here'

import logging
import numpy as np
import subprocess
from sphere import \
    Sphere, get_sphere, epsilon_distance, equal_in_practice, zero_in_practice
from timer import Timer

logging.basicConfig(format='%(asctime)s.%(msecs)d %(levelname)-8s %(filename)s:%(lineno)d %(funcName)s: %(message)s',
    datefmt='%m.%d.%Y %H:%M:%S',
    level=logging.DEBUG)

logger = logging.getLogger(__name__)

def play_with_numpy_random_numbers():
    np.random.seed(42)
    NUM_POINTS = 1
    points = np.random.rand(NUM_POINTS, 3)
    print("points = {}".format(points))

def average(*numbers):
    """Self-explanatory"""
    if not numbers:
        raise ValueError('numbers should not be empty')

    numbers = [float(number) for number in numbers]
    return sum(numbers) / float(len(numbers))

def get_sphere_given4Points(description, points):
    SPHERE = get_sphere(points)
    logger.info('Sphere given %s: %s', description, SPHERE)

def get_git_version():
    COMMAND = 'git --version'
    timer = Timer()
    RESULT = subprocess.call(COMMAND, shell=True)  # returns the exit code in unix
    logger.info('Command `%s` took %s and returned %d', COMMAND, timer.get_duration_string(), RESULT)

def download_file_using_curl(url, output_filename):
    COMMAND = 'curl ' + url + ' -o ' + output_filename
    timer = Timer()
    RESULT = subprocess.call(COMMAND, shell=True)  # returns the exit code in unix
    if RESULT == 0:
        logger.info('File `%s` has been downloaded in %s', output_filename, timer.get_duration_string())
    else:
        logger.error('Failed to download file `%s`', output_filename)

def decompress_7z_file(filename, output_directory):
    COMMAND = '7z x ' + filename + ' -o' + output_directory
    timer = Timer()
    RESULT = subprocess.call(COMMAND, shell=True)  # returns the exit code in unix
    logger.info('Command `%s` took %s and returned %d', COMMAND, timer.get_duration_string(), RESULT)

if __name__ == '__main__':

    play_with_numpy_random_numbers()

    ARRAY_OF_DESCRIPTION_AND_POINTS = [
        ('4 straight crosshair points from whatnot 42', [
            [-35.3025, 0.6357,   3.8584],
            [-35.0932, 1.3599, -43.2535],
            [ -9.054, -0.958,  -19.6768],
            [-62.0412, 5.9778, -19.7658]
        ]),
        ('4 rotated crosshair points from whatnot 42', [
            [-58.7767,  4.9348,    -3.7779],
            [-13.3565, -0.644701, -29.8066],
            [-16.4319, -0.999301,   1.6949],
            [-55.543,   4.7384,   -37.1852]
        ]),
        ('4 straight crosshair points from whatnot 46', [
            [-36.9284,  2.1009,  -1.0189],
            [-37.0922,  2.2078, -51.4502],
            [-10.4147, -0.1741, -26.0583],
            [-65.5153,  8.0756, -26.2123]
        ]),
        ('4 rotated crosshair points from whatnot 46', [
            [-56.2434, 5.6835, -8.3162],
            [-15.5323, 0.0641003, -37.5089],
            [-54.5831, 5.3886, -44.8675],
            [-18.2069, 0.2075, -3.8871]
        ])
    ]
    for description, points in ARRAY_OF_DESCRIPTION_AND_POINTS:
        get_sphere_given4Points(description, points)

    get_git_version()

    FILENAME_AND_URL_ARRAY = [
      ['data/_L.7z', 'https://uccbc8e1809ffe6c06563a47e1bb66.dl.dropboxusercontent.com/cd/0/get/AcqreqsqlnLf9OlXvIf54sAFQPhaV7Xoexyd_bJIe4fa3HBgaiVwMJ2uT0w5YZhZObLZZhFrCzbEdcoNGYQN9tXa-sB4liuyx5pA6zEH1nr8XTaSGBcSCQZuNcXVugLwypw/file#'],
      ['data/_M.7z', 'https://uc26a4adfaf1d3cdc9423283971b37.dl.dropboxusercontent.com/cd/0/get/AcqqVOiBNeEZzpeXi_6Fmp883j7ikUNiR6OaW0gpf-B7RHXAFl1jrmxZ4AlL5W7czzfonoegeBGJDOeMWUE7xzchzz6zWlFt-EksvSWTfNbU3ydePSl4BjM-I29RfrAd0ns/file#']
      #['data/_C54.xml', 'https://uc7b36b201202ac7cc04d68a05a966.dl.dropboxusercontent.com/cd/0/get/AclhxNHBCsS2_ilqbP43MbJnWUNyZmirnWtmSg3D5bM8pDq4WUk4H2sk_dMI0j63OU3q5HQyDAvxCdI3LrjlGms7Ui5B4zsSIJMoEyUmJB5F9SpRKIHYU3J1ZNSNgwl_eFg/file#'],
      #['data/_F.stl', 'https://uc9961f6bd3472cdc89cd193cf4f37.dl.dropboxusercontent.com/cd/0/get/AcmcZszabuV-PTcgdSLBXqurosEBnS7zHxU0Kj5cjLkNUbIIoigDcRQsMjYa3Ndr7xWHXljjLn0MANfe-AEntU6vSz2Q7yosMEDkb_g2svrOjEGk9ila4Vd8lQLr8KJdo7k/file#'],
      #['data/_L.stl', 'https://uc0a059daf35cb3466bfa34ee51666.dl.dropboxusercontent.com/cd/0/get/AcnlQBb60Hl8eGw5p-s99eCERh8m32TdJeU-RMh1JL_LbI7SNemva-Hp5zoxArCRBjwm_49fT6aClct0FAHXSyDFopXVy6K2__tFNrliWp-O9mRmmEkL-GDOHml1xAMYuLY/file#'],
      #['data/_R.stl', 'https://uc0dfa07f6b21b5c7d4102e78bb537.dl.dropboxusercontent.com/cd/0/get/AcnyAgA-ShRXNUP2rp8iCvrLd99DRThS_p1TWfgK1SDV0TRYlY6UdLHbN24WOsNv2TeJTjKAPTzkZdvJLITMy7I4TO5JEHhm8rLt7uv9ZKOvXqPfNloTB4WiVwHfzyuYYos/file#']
    ]
    for filename_and_url in FILENAME_AND_URL_ARRAY:
        filename, url = filename_and_url
        download_file_using_curl(url, filename)

        filename_extension = filename[-2:]
        if filename_extension == '7z':
            output_directory = filename[0:7]
            decompress_7z_file(filename, output_directory)
