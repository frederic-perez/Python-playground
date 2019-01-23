'module docstring should be here'

def average(*numbers):
    """Self-explanatory"""
    numbers = [float(number) for number in numbers]
    return sum(numbers) / float(len(numbers))
