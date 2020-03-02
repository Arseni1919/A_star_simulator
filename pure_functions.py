from CONSTANTS import *


def get_distance(a, b):
    a1, a2 = a.get_pos()
    b1, b2 = b.get_pos()
    cell_size = a.get_cell_size()
    x = abs((a1 - b1) / (cell_size + PADDING))
    y = abs((a2 - b2) / (cell_size + PADDING))
    # return int((x + y) * (cell_size + PADDING))
    return int(math.sqrt((a1 - b1) ** 2 + (a2 - b2) ** 2))


def get_closest_pivot(a, pivots):
    curr_list = []
    for b in pivots:
        dist = get_distance(a, b)
        curr_list.append((b.get_ord_number(), dist))
    return min(curr_list, key=lambda x: x[1])


def get_closet(dict):
    return min(dict.items(), key=lambda x: x[1])


def get_start_and_end(cells):
    start_node, end_node = 0, 0
    for cell in cells:
        if cell.get_goal() == 0:
            start_node = cell
        if cell.get_goal() == 1:
            end_node = cell
    return start_node, end_node


def choose_least_f_from(curr_open):
    f_values_list = []
    for node in curr_open:
        f_values_list.append(node.f)
    val = curr_open[np.argmin(f_values_list)]
    return val  # !!!!!!!!!!!!!!!!!!


def has_wall_neightbour(q, cells, cell_hight_without_padding):
    # successors = []
    q_x, q_y = q.get_pos()
    aside = cell_hight_without_padding + PADDING

    for cell in cells:
        cell_x, cell_y = cell.get_pos()
        neighbour = False

        if q_x == cell_x and q_y == cell_y + aside:
            neighbour = True
        if q_x == cell_x and q_y == cell_y - aside:
            neighbour = True
        if q_x == cell_x + aside and q_y == cell_y:
            neighbour = True
        if q_x == cell_x - aside and q_y == cell_y:
            neighbour = True

        if q_x == cell_x + aside and q_y == cell_y + aside:
            neighbour = True
        if q_x == cell_x + aside and q_y == cell_y - aside:
            neighbour = True
        if q_x == cell_x - aside and q_y == cell_y + aside:
            neighbour = True
        if q_x == cell_x - aside and q_y == cell_y - aside:
            neighbour = True

        if neighbour:
            if cell.occupied:
                return True
    return False


def generate_successors(q, cells, cell_hight_without_padding):
    successors = []
    q_x, q_y = q.get_pos()
    aside = cell_hight_without_padding + PADDING

    for cell in cells:
        cell_x, cell_y = cell.get_pos()
        neighbour = False

        if q_x == cell_x and q_y == cell_y + aside:
            neighbour = True
        if q_x == cell_x and q_y == cell_y - aside:
            neighbour = True
        if q_x == cell_x + aside and q_y == cell_y:
            neighbour = True
        if q_x == cell_x - aside and q_y == cell_y:
            neighbour = True

        if q_x == cell_x + aside and q_y == cell_y + aside:
            neighbour = True
        if q_x == cell_x + aside and q_y == cell_y - aside:
            neighbour = True
        if q_x == cell_x - aside and q_y == cell_y + aside:
            neighbour = True
        if q_x == cell_x - aside and q_y == cell_y - aside:
            neighbour = True

        if neighbour:
            if not cell.occupied:
                successors.append(cell)

    return successors


def run_a_star(cells, pivots, heuristic, cell_hight_without_padding):
    start_node, end_node = get_start_and_end(cells)
    curr_open = [start_node]
    curr_closed = []

    while len(curr_open) != 0:
        # print('curr_open', len(curr_open))
        q = choose_least_f_from(curr_open)
        curr_open.remove(q)
        # curr_closed.append(q)
        successors = generate_successors(q, cells, cell_hight_without_padding)

        for successor in successors:
            if successor is end_node:
                successor.set_father(q)
                return curr_closed, curr_open
            g = q.g + get_distance(q, successor)
            h = heuristic.calc(successor, end_node, pivots)
            f = g + h
            if successor in curr_open:
                if successor.f <= f:
                    continue
                else:
                    curr_open.remove(successor)
            if successor in curr_closed:
                if successor.f <= f:
                    continue
                else:
                    curr_closed.remove(successor)
            successor.g = g
            successor.f = f
            successor.set_father(q)
            curr_open.append(successor)

        curr_closed.append(q)
    return curr_closed, curr_open


def dif_BFS(cells, pivots, heuristic, cell_hight_without_padding):
    for pivot in pivots:
        renew_cells(cells)
        heuristic.data[pivot.get_ord_number()] = {}
        heuristic.data[pivot.get_ord_number()][pivot.get_ord_number()] = 0
        curr_open = [pivot]
        curr_closed = []

        while len(curr_open) != 0:
            # print('curr_open', len(curr_open))
            q = choose_least_f_from(curr_open)
            curr_open.remove(q)
            # curr_closed.append(q)
            successors = generate_successors(q, cells, cell_hight_without_padding)

            for successor in successors:
                g = q.g + get_distance(q, successor)
                f = g
                if successor in curr_open:
                    if successor.f <= f:
                        continue
                    else:
                        curr_open.remove(successor)
                if successor in curr_closed:
                    if successor.f <= f:
                        continue
                    else:
                        curr_closed.remove(successor)
                successor.g = g
                successor.f = f
                curr_open.append(successor)
                heuristic.data[pivot.get_ord_number()][successor.get_ord_number()] = f

            curr_closed.append(q)
    renew_cells(cells)


def renew_cells(cells):
    for cell in cells:
        cell.g = 0
        cell.f = 0


def can_BFS(cells, pivots, heuristic, cell_hight_without_padding):
    data = {}
    dif_BFS(cells, pivots, heuristic, cell_hight_without_padding)
    for pivot1 in pivots:
        data[pivot1.get_ord_number()] = {}
        for pivot2 in pivots:
            data[pivot1.get_ord_number()][pivot2.get_ord_number()] = heuristic.data[pivot1.get_ord_number()][pivot2.get_ord_number()]
    for cell in cells:
        if not cell.occupied:
            if cell not in pivots:
                data[cell.get_ord_number()] = {}
                curr_list = []
                for pivot in pivots:
                    curr_list.append((pivot.get_ord_number(),
                                      heuristic.data[pivot.get_ord_number()][cell.get_ord_number()]))
                min_piv, min_val = min(curr_list, key=lambda x: x[1])
                data[cell.get_ord_number()][min_piv] = min_val
    heuristic.data = data


def dif_PER(cells, heuristic, cell_hight_without_padding):
    for pivot in cells:
        renew_cells(cells)
        heuristic.data[pivot.get_ord_number()] = {}
        heuristic.data[pivot.get_ord_number()][pivot.get_ord_number()] = 0
        curr_open = [pivot]
        curr_closed = []

        while len(curr_open) != 0:
            # print('curr_open', len(curr_open))
            q = choose_least_f_from(curr_open)
            curr_open.remove(q)
            # curr_closed.append(q)
            successors = generate_successors(q, cells, cell_hight_without_padding)

            for successor in successors:
                g = q.g + get_distance(q, successor)
                f = g
                if successor in curr_open:
                    if successor.f <= f:
                        continue
                    else:
                        curr_open.remove(successor)
                if successor in curr_closed:
                    if successor.f <= f:
                        continue
                    else:
                        curr_closed.remove(successor)
                successor.g = g
                successor.f = f
                curr_open.append(successor)
                heuristic.data[pivot.get_ord_number()][successor.get_ord_number()] = f

            curr_closed.append(q)
    renew_cells(cells)


def load_heuristic(name, heuristic, piv_heuristic, cells, pivots, cell_hight_without_padding):
    heuristic.type = piv_heuristic
    if os.path.isfile(name):
        with open(name, 'rb') as fileObject:
            # load the object from the file into var b
            data = pickle.load(fileObject)
            heuristic.data = data
    else:
        if piv_heuristic == 'dif':
            dif_BFS(cells, pivots, heuristic, cell_hight_without_padding)
        if piv_heuristic == 'can':
            can_BFS(cells, pivots, heuristic, cell_hight_without_padding)
        if piv_heuristic == 'per':
            dif_PER(cells, heuristic, cell_hight_without_padding)

        with open(name, 'wb') as fileObject:
            pickle.dump(heuristic.data, fileObject)
