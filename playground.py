'module docstring should be here'

def average(*numbers):
    """Self-explanatory"""
    if not numbers:
        raise ValueError('numbers should not be empty')

    numbers = [float(number) for number in numbers]
    return sum(numbers) / float(len(numbers))
