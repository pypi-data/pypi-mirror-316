def evenorodd(x):
    """Checks if the number provided is even or odd."""
    if x % 2 == 0:
        return True
    elif x % 2 == 1:
        return False
    else:
        return None
print(evenorodd(10))