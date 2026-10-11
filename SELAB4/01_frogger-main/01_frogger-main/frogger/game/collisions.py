"""
collisions: frog-vs-vehicle collision detection.
"""

CELL_SIZE = 50


def check_collision(frog, vehicles):
    """
    Returns True if the frog is currently hit by any vehicle.
    """
    frog_rect = frog.get_rect(CELL_SIZE)
    for v in vehicles:
        if v.row == frog.row and frog_rect.colliderect(v.get_rect(CELL_SIZE)):
            return True
    return False

