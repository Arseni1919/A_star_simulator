from pure_functions import *


class Heuristic:
    def __init__(self):
        self.data = {}
        self.type = ''

    def create_data(self, piv_heuristic, cells, pivots, cell_hight_without_padding, heuristic_name_to_load):
        load_heuristic(heuristic_name_to_load, self, piv_heuristic, cells, pivots, cell_hight_without_padding)

    def get_data(self):
        return self.data

    def calc_dif(self, a, b, pivots):
        max_value = 0
        for pivot in pivots:
            h_x = abs(self.data[pivot.get_ord_number()][a.get_ord_number()] -
                      self.data[pivot.get_ord_number()][b.get_ord_number()])
            max_value = max(max_value, h_x)
            # hx(a, b) = | d(a, x) - d(b,x) |
        return max_value

    def calc_can(self, a, b, pivots):
        pivot_a, dist_a = min(self.data[a.get_ord_number()].items(), key=lambda x: x[1])
        pivot_b, dist_b = min(self.data[b.get_ord_number()].items(), key=lambda x: x[1])
        pivot_dist = self.data[pivot_a][pivot_b]
        dist = max(pivot_dist - dist_a - dist_b, get_distance(a, b))
        return dist
        # hx,y(a, b) = | d(x,y) - d(a,x)- d(b,y) |

    def calc_bor(self, a, b, pivots):
        pass

    def calc_per(self, a, b):
        return self.data[a.get_ord_number()][b.get_ord_number()]

    def calc(self, a, b, pivots):
        if self.type == '' or not self.data:
            return 0
        if self.type == 'dif':
            return self.calc_dif(a, b, pivots)
        if self.type == 'can':
            return self.calc_can(a, b, pivots)
        if self.type == 'bor':
            return self.calc_bor(a, b, pivots)
        if self.type == 'per':
            return self.calc_per(a, b)
