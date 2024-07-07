"""module docstring should be here"""

import nibabel as nib
import numpy as np
import tempfile
import tkinter as tk

from numpy.typing import ArrayLike
from skimage.morphology import skeletonize
from typing import Final, TypeAlias

TupleOf2Ints: TypeAlias = tuple[int, int]


def format_float_as_in_paper(x: float) -> str:
    return '{0:.2f}'.format(x).rstrip('.')


def ascii_to_binary_mask_2d(ascii_file_path: str) -> np.ndarray:
    """
    Converts an ASCII file representing a binary mask 2D to a binary 2D numpy array.

    Args:
        ascii_file_path (str): Path to the ASCII file.

    Returns:
        numpy.ndarray: A 2D binary mask where 0 represents background and 1 represents foreground.
    """

    with open(ascii_file_path, "r") as f:
        lines = f.readlines()

    # Determine dimensions of the image
    height: Final[int] = len(lines)
    width: Final[int] = max(len(line.strip()) for line in lines)

    # Create an empty numpy array
    mask = np.zeros((height, width), dtype=np.uint8)

    # Iterate through each line and character
    for y, line in enumerate(lines):
        for x, char in enumerate(line.strip()):
            # Set pixel to 1 if it's a non-whitespace character or '0'
            if char != ' ' and char != '0':
                mask[y, x] = 1

    return mask


def precision(mask1: np.ndarray, mask2: np.ndarray) -> float:
    intersection = np.logical_and(mask1, mask2)
    result = intersection.sum() / mask2.sum()
    return result


def recall(mask1: np.ndarray, mask2: np.ndarray) -> float:
    intersection = np.logical_and(mask1, mask2)
    result = intersection.sum() / mask1.sum()
    return result


def dice_coefficient_a(mask1: np.ndarray, mask2: np.ndarray) -> float:
    intersection: Final = np.logical_and(mask1, mask2)
    result: Final = (2.0 * intersection.sum()) / (mask1.sum() + mask2.sum())
    return result


def dice_coefficient_b(precision_value: float, recall_value: float) -> float:
    result: Final = 2 * (precision_value * recall_value) / (precision_value + recall_value)
    return result


def cl_score(v, s):
    """[this function computes the skeleton volume overlap]

    Args:
        v ([bool]): [image]
        s ([bool]): [skeleton]

    Returns:
        [float]: [computed skeleton volume intersection]
    """
    return np.sum(v*s)/np.sum(s)


def cl_dice(v_p, v_l) -> float:
    """[this function computes the clDice metric]

    Args:
        v_p ([bool]): [predicted image]
        v_l ([bool]): [ground truth image]

    Returns:
        [float]: [clDice metric]
    """
    len_v_p_shape: Final = len(v_p.shape)
    if len_v_p_shape != 2 and len_v_p_shape != 3:
        print(f'ERROR: Cannot compute the clDice when len(v_p.shape) = {len_v_p_shape} is not 2 or 3')
        return -666.

    t_prec: Final = cl_score(v_p, skeletonize(v_l))
    t_sens: Final = cl_score(v_l, skeletonize(v_p))
    return 2*t_prec*t_sens/(t_prec+t_sens)


class Masks2DWindow(object):
    shape: Final[TupleOf2Ints]
    cell_size: Final[int]

    def __new__(cls, mask_shape: TupleOf2Ints, cell_size: int) -> 'Masks2DWindow':
        for i in 0, 1:
            if mask_shape[i] <= 0:
                raise ValueError(f'Mask shape[{i}] = {mask_shape[i]} is out of range')
        if cell_size <= 0:
            raise ValueError(f'Cell size value {cell_size} is out of range')
        return object.__new__(cls)

    def __init__(self, mask_shape: TupleOf2Ints, cell_size: int) -> None:
        self.shape = mask_shape
        self.cell_size = cell_size

        res_x = self.shape[0]
        res_y = self.shape[1]

        # Create tkinter window
        self.root: Final = tk.Tk()
        self.root.title('2D Masks')

        # Create the frame(s)
        self.canvas: Final[tk.Canvas] = tk.Canvas(self.root, width=res_x*cell_size, height=res_y*cell_size,
                                                  background='gray')

        # Pack the frame(s)
        self.canvas.pack(side="right")

    def __str__(self) -> str:
        return f'Masks2DWindow(shape={self.shape}, cell_size={self.cell_size})'

    def spy(self, message: str) -> None:
        print(f'{message}: {self}')

    def paint_cell(self, i: int, j: int, color: str, cell_unpainted_inner_border) -> None:
        self.canvas.create_rectangle(
            # Experimentally we found out we need + 2 to paint ALL pixels
            i*self.cell_size + cell_unpainted_inner_border + 2,
            j*self.cell_size + cell_unpainted_inner_border + 2,
            i*self.cell_size + self.cell_size - cell_unpainted_inner_border + 2,
            j*self.cell_size + self.cell_size - cell_unpainted_inner_border + 2,
            fill=color, outline='')  # faster than canvas.create_oval

    def clean(self, cell_unpainted_inner_border: int) -> None:
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.paint_cell(j, i, 'white', cell_unpainted_inner_border)

    def paint_over(self, mask: np.ndarray, color: str, cell_unpainted_inner_border: int = 0) -> None:
        if mask.shape != self.shape:
            raise ValueError(f'Mask shape of input mask {mask.shape} should be equal to {self.shape}')
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                cell_color = color if mask[i][j] != 0 else 'white'
                self.paint_cell(j, i, cell_color, cell_unpainted_inner_border)

    def show(self) -> None:
        self.root.mainloop()


def replicate_reinke_2024_extended_data_fig_1_p2_2a(top_or_bottom: str, spy: bool) -> None:
    identity: Final = np.eye(4)  # Used to save NIFTI files (if the conditions to do so are met)
    temp_dir = tempfile.gettempdir()  # Used to save NIFTI files (if the conditions to do so are met)

    basename_file_mask_2d: Final[str] = 'binary-mask-2d-Extended-Data-Fig-1-P2-2a-' + top_or_bottom

    basename_file_mask_2d_reference: Final[str] = basename_file_mask_2d + '-Reference'
    filename_ascii_mask_2d_reference: Final[str] = 'data/Reinke-2024/' + basename_file_mask_2d_reference + ".txt"
    mask_2d_reference: Final = ascii_to_binary_mask_2d(filename_ascii_mask_2d_reference)
    if spy:
        print(f'mask_2d_reference =\n{mask_2d_reference}')
        mask_2d_nifti = nib.Nifti1Image(ArrayLike(mask_2d_reference), identity)  # Create NIfTI1 image object
        filename_nifti_mask_2d = temp_dir + "/" + basename_file_mask_2d_reference + ".nii.gz"
        nib.save(mask_2d_nifti, filename_nifti_mask_2d)  # Save the NIFTI objects to file

    cell_width: Final = 21

    for i in 1, 2:
        basename_file_mask_2d_prediction = basename_file_mask_2d + '-Prediction-' + str(i)
        filename_ascii_mask_2d_prediction = 'data/Reinke-2024/' + basename_file_mask_2d_prediction + ".txt"
        mask_2d_prediction = ascii_to_binary_mask_2d(filename_ascii_mask_2d_prediction)
        if spy:
            print(f'mask_2d_prediction #{i} =\n{mask_2d_prediction}')
            mask_2d_nifti = nib.Nifti1Image(ArrayLike(mask_2d_prediction), identity)  # Create NIfTI1 image object
            filename_nifti_mask_2d = temp_dir + "/" + basename_file_mask_2d_prediction + ".nii.gz"
            nib.save(mask_2d_nifti, filename_nifti_mask_2d)  # Save the NIFTI objects to file

        # Compute the Dice coefficient
        dice_a = dice_coefficient_a(mask_2d_reference, mask_2d_prediction)
        dice_b = dice_coefficient_b(
            precision(mask_2d_reference, mask_2d_prediction),
            recall(mask_2d_reference, mask_2d_prediction))

        print(f'Dice({filename_ascii_mask_2d_reference}, {filename_ascii_mask_2d_prediction}) = '
              f'{format_float_as_in_paper(dice_a)} or {format_float_as_in_paper(dice_b)}')

        masks_2d_window = Masks2DWindow(mask_2d_reference.shape, cell_width)
        # masks_2d_window.spy('Initial mask_2d_window')
        masks_2d_window.clean(cell_unpainted_inner_border=1)
        masks_2d_window.paint_over(mask_2d_reference, 'green', cell_unpainted_inner_border=1)
        masks_2d_window.paint_over(mask_2d_prediction, 'orange' if i == 1 else 'cyan', cell_unpainted_inner_border=3)
        masks_2d_window.show()


def replicate_reinke_2024_extended_data_fig_1_p2_2b(spy: bool) -> None:
    identity: Final = np.eye(4)  # Used to save NIFTI files (if the conditions to do so are met)
    temp_dir = tempfile.gettempdir()  # Used to save NIFTI files (if the conditions to do so are met)

    basename_file_mask_2d: Final[str] = 'binary-mask-2d-Extended-Data-Fig-1-P2-2b'

    basename_file_mask_2d_reference: Final[str] = basename_file_mask_2d + '-Reference'
    filename_ascii_mask_2d_reference: Final[str] = 'data/Reinke-2024/' + basename_file_mask_2d_reference + ".txt"
    mask_2d_reference: Final[np.ndarray] = ascii_to_binary_mask_2d(filename_ascii_mask_2d_reference)
    if spy:
        print(f'mask_2d_reference =\n{mask_2d_reference}')
        mask_2d_nifti = nib.Nifti1Image(ArrayLike(mask_2d_reference), identity)  # Create NIfTI1 image object
        filename_nifti_mask_2d = temp_dir + "/" + basename_file_mask_2d_reference + ".nii.gz"
        nib.save(mask_2d_nifti, filename_nifti_mask_2d)  # Save the NIFTI objects to file

    cell_width: Final = 21

    for i in 1, 2:
        basename_file_mask_2d_prediction = basename_file_mask_2d + '-Prediction-' + str(i)
        filename_ascii_mask_2d_prediction = 'data/Reinke-2024/' + basename_file_mask_2d_prediction + ".txt"
        mask_2d_prediction = ascii_to_binary_mask_2d(filename_ascii_mask_2d_prediction)
        if spy:
            print(f'mask_2d_prediction #{i} =\n{mask_2d_prediction}')
            mask_2d_nifti = nib.Nifti1Image(ArrayLike(mask_2d_prediction), identity)  # Create NIfTI1 image object
            filename_nifti_mask_2d = temp_dir + "/" + basename_file_mask_2d_prediction + ".nii.gz"
            nib.save(mask_2d_nifti, filename_nifti_mask_2d)  # Save the NIFTI objects to file

        # Compute the Dice coefficient
        dice_a = dice_coefficient_a(mask_2d_reference, mask_2d_prediction)
        dice_b = dice_coefficient_b(
            precision(mask_2d_reference, mask_2d_prediction),
            recall(mask_2d_reference, mask_2d_prediction))
        cl_dice_value = cl_dice(mask_2d_reference, mask_2d_prediction)
        print(f'Dice({filename_ascii_mask_2d_reference}, {filename_ascii_mask_2d_prediction}) = '
              f'{format_float_as_in_paper(dice_a)} or {format_float_as_in_paper(dice_b)}; '
              f'clDice = {format_float_as_in_paper(cl_dice_value)}')

        masks_2d_window = Masks2DWindow(mask_2d_reference.shape, cell_width)
        # masks_2d_window.spy('Initial mask_2d_window')
        masks_2d_window.clean(cell_unpainted_inner_border=1)
        masks_2d_window.paint_over(mask_2d_reference, 'green', cell_unpainted_inner_border=1)
        masks_2d_window.paint_over(mask_2d_prediction, 'orange' if i == 1 else 'cyan', cell_unpainted_inner_border=3)
        masks_2d_window.show()


def replicate_reinke_2024_extended_data_fig_1_p2_2() -> None:
    """
    Here we sort of replicate the very interesting stuff from this article:
    Reinke, A., Tizabi, M.D., Baumgartner, M. et al. Understanding metric-related pitfalls in image analysis validation.
    Nat Methods 21, 182–194 (2024). https://doi.org/10.1038/s41592-023-02150-0,
    concretely its Extended Data's Fig. 1's P2.2
    """
    spy = False  # True

    for top_or_bottom in 'top', 'bottom':
        replicate_reinke_2024_extended_data_fig_1_p2_2a(top_or_bottom, spy)
    replicate_reinke_2024_extended_data_fig_1_p2_2b(spy)


def compute_cl_dice_for_input_masks_using_paths(mask_1_path: str, mask_2_path) -> float:
    spy: Final = False  # True

    mask_1_nib = nib.load(mask_1_path)
    mask_1_data = mask_1_nib.get_fdata()  # type: ignore[attr-defined]
    mask_1_array = np.array(mask_1_data, dtype=np.int8)
    if spy:
        print(f'mask_1_array =\n{mask_1_array}')

    mask_2_nib = nib.load(mask_2_path)
    mask_2_data = mask_2_nib.get_fdata()  # type: ignore[attr-defined]
    mask_2_array = np.array(mask_2_data, dtype=np.int8)
    if spy:
        print(f'mask_2_array =\n{mask_2_array}')

    mask_1_array_shape: Final = mask_1_array.shape
    mask_2_array_shape: Final = mask_2_array.shape
    if mask_1_array_shape != mask_2_array_shape:
        print('ERROR: Cannot compute the clDice for masks with different shapes: '
              f'{mask_1_array_shape} != {mask_2_array_shape}')
        return -666.

    cl_dice_value: Final = cl_dice(mask_1_array, mask_2_array)
    return cl_dice_value


def replicate_reinke_2024_extended_data_fig_1_p2_2b_bottom_using_nifti_files() -> None:
    mask_1_path = 'data/Reinke-2024/binary-mask-2d-Extended-Data-Fig-1-P2-2b-Reference.nii.gz'
    for i in 1, 2:
        mask_2_path = 'data/Reinke-2024/binary-mask-2d-Extended-Data-Fig-1-P2-2b-Prediction-' + str(i) + '.nii.gz'
        cl_dice_value = compute_cl_dice_for_input_masks_using_paths(mask_1_path, mask_2_path)
        print(f'clDice({mask_1_path}, {mask_2_path}) = {format_float_as_in_paper(cl_dice_value)}')


def compute_cl_dice_for_input_masks_provided_by_the_user() -> None:
    # Ask the user if they want to compute the ClDice value from binary masks
    prompt = "Do you want to compute the clDice value from binary masks (.nii.gz files)? (yes/no): "
    answer = input(prompt).lower()

    # Check the user's answer and proceed accordingly
    if answer == 'yes' or answer == 'y':
        mask_1_path = input("Please, provide path of first mask: ")
        mask_2_path = input("Please, provide path of second mask: ")
        cl_dice_value = compute_cl_dice_for_input_masks_using_paths(mask_1_path, mask_2_path)
        print(f'clDice({mask_1_path}, {mask_2_path}) = {format_float_as_in_paper(cl_dice_value)}')


def main():
    replicate_reinke_2024_extended_data_fig_1_p2_2()
    replicate_reinke_2024_extended_data_fig_1_p2_2b_bottom_using_nifti_files()
    compute_cl_dice_for_input_masks_provided_by_the_user()


if __name__ == '__main__':
    main()