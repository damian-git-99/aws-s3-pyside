# Layer 2 - Depends on constants
from constants import PI, GRAVITY

def circle_area(r):
    return PI * r * r

def falling_time(h):
    return (2 * h / GRAVITY) ** 0.5
