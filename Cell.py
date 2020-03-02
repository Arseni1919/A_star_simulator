# Import the pygame module
from CONSTANTS import *


# Define the cell object by extending pygame.sprite.Sprite
# Use an image for a better-looking sprite
class Cell(pygame.sprite.Sprite):
    def __init__(self, cell_size=None, surf_center=None, ord_number=None):
        super(Cell, self).__init__()
        self.cell_size = cell_size
        self.surf = pygame.Surface((cell_size, cell_size))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=surf_center
        )
        self.on = False
        self.occupied = False
        self.ord_number = ord_number
        self.pivot = False
        self.goal = -1
        self.g = 0
        self.f = 0
        self.closed = False
        self.father = None
        self.FONT_SIZE = int(cell_size * 0.45)
        # Number of Robot
        font = pygame.font.SysFont("comicsansms", self.FONT_SIZE)
        text = font.render("%s" % self.ord_number, True, (225, 0, 0))
        wt, ht = text.get_size()
        self.surf.blit(text, (cell_size - wt, 0))

    def get_pos(self):
        return self.rect.center

    def get_cell_size(self):
        return self.cell_size

    def get_ord_number(self):
        return self.ord_number

    def get_if_pivot(self):
        return self.pivot

    def get_goal(self):
        return self.goal

    def set_father(self, father):
        self.father = father

    def get_father(self):
        return self.father

    def render_number(self):
        # Number of Robot
        font = pygame.font.SysFont("comicsansms", self.FONT_SIZE)
        text = font.render("%s" % self.ord_number, True, (225, 0, 0))
        wt, ht = text.get_size()
        self.surf.blit(text, (self.cell_size - wt, 0))

    def set_occupied(self, occupied):
        self.occupied = occupied
        self.set_occupied_color()

    def set_occupied_color(self):
        if self.occupied:
            self.surf.fill(OCCUPIED_COLOR)
        else:
            self.surf.fill(NOT_OCCUPIED_COLOR)
        self.render_number()

    def set_closed(self):
        self.closed = True
        self.surf.fill(CLOSED_COLOR)
        self.render_number()

    def set_open(self):
        self.closed = True
        self.surf.fill(OPEN_COLOR)
        self.render_number()

    def set_goal_color(self):
        if self.goal == 0:
            self.surf.fill(STRART_COLOR)
        if self.goal == 1:
            self.surf.fill(END_COLOR)
        self.render_number()

    def set_path_sign_color(self):
        pygame.draw.circle(self.surf,
                           PATH_COLOR,
                           (int(self.cell_size/2), int(self.cell_size/2)),
                           int(self.cell_size/4))

    def set_pivot_color(self):
        if self.pivot:
            if self.closed:
                self.surf.fill(PIVOT_CLOSED_COLOR)
            else:
                self.surf.fill(PIVOT_COLOR)
            self.render_number()

    def set_if_occupied(self):
        self.occupied = not self.occupied
        if self.occupied:
            self.surf.fill(OCCUPIED_COLOR)
        else:
            self.surf.fill(NOT_OCCUPIED_COLOR)
        self.render_number()

    def set_goal(self, goal):
        if self.occupied or self.pivot:
            return
        if goal == -1:
            self.surf.fill(NOT_OCCUPIED_COLOR)
        elif goal == 0:
            self.surf.fill(STRART_COLOR)
        elif goal == 1:
            self.surf.fill(END_COLOR)
        else:
            print('ERROR')
            raise ValueError()
        self.goal = goal
        self.render_number()

    def create_pivot(self):
        if not self.occupied:
            self.pivot = not self.pivot
            if self.pivot:
                self.surf.fill(PIVOT_COLOR)
            else:
                self.surf.fill(NOT_OCCUPIED_COLOR)
            self.render_number()

    def reset(self):
        self.g = 0
        self.f = 0
        self.closed = False
        self.father = None
        self.set_goal(-1)
        self.set_occupied_color()
        self.set_pivot_color()

    def reset_without_resetting_goal(self):
        self.g = 0
        self.f = 0
        self.closed = False
        self.father = None
        self.set_occupied_color()
        self.set_pivot_color()

