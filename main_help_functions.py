from Cell import *
from Title import *
from Heuristic import *


def create_field(cells, all_sprites, grid_size):
    ord_number = 1
    curr_hight = SCREEN_HEIGHT - PADDING
    cell_hight_with_padding = math.floor(curr_hight / grid_size)
    cell_hight_without_padding = cell_hight_with_padding - PADDING
    for h in range(grid_size):
        for w in range(grid_size):
            surf_center = (
                h * cell_hight_with_padding + PADDING + cell_hight_without_padding / 2,
                w * cell_hight_with_padding + PADDING + cell_hight_without_padding / 2
            )
            cell = Cell(cell_hight_without_padding, surf_center, ord_number)
            cells.add(cell)
            all_sprites.add(cell)
            ord_number += 1
    return cell_hight_without_padding


def update_cell(cells):
    mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
    for cell in cells:
        cell_pos_x, cell_pos_y = cell.get_pos()
        cell_size = cell.get_cell_size()
        if cell_pos_x - cell_size / 2 < mouse_pos_x < cell_pos_x + cell_size / 2:
            if cell_pos_y - cell_size / 2 < mouse_pos_y < cell_pos_y + cell_size / 2:
                if not cell.on:
                    cell.set_if_occupied()
                    cell.on = True
            else:
                cell.on = False
        else:
            cell.on = False


def create_titles(titles, all_sprites, mode):
    title = ''
    if mode == 1:
        title = 'SAVE MAP'
    if mode == 2:
        title = 'SAVE PIVOTS'
    if mode == 3:
        title = PREPARE_AND_RUN_TITLE
        # Button for saving map
    button_hight = SCREEN_WIDTH - SCREEN_HEIGHT - 2 * PADDING
    # (SCREEN_WIDTH + button_hight/2, button_hight/2)
    button = Title(
        button_hight,
        (SCREEN_HEIGHT + button_hight / 2, PADDING + button_hight / 2),
        title,
        mode
    )
    titles.add(button)
    all_sprites.add(button)
    if mode == 3:
        reset_button = Title(button_hight,
                             (SCREEN_HEIGHT + button_hight / 2, PADDING * 2 + button_hight*1.5),
                             RESET_TITLE,
                             mode)
        titles.add(reset_button)
        all_sprites.add(reset_button)


def update_cells(cells):
    pushed, _, _ = pygame.mouse.get_pressed()
    if pushed == 1:
        update_cell(cells)


def create_pivot(cells):
    mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
    for cell in cells:
        cell_pos_x, cell_pos_y = cell.get_pos()
        cell_size = cell.get_cell_size()
        if cell_pos_x - cell_size / 2 < mouse_pos_x < cell_pos_x + cell_size / 2:
            if cell_pos_y - cell_size / 2 < mouse_pos_y < cell_pos_y + cell_size / 2:
                cell.create_pivot()
                return


def create_pivots_according_to_dist(piv_dist, NUM_OF_PIVOTS, cells, cell_hight_without_padding, max_dist):
    if piv_dist == '':
        return
    if piv_dist == 'RAN':
        RAN_dist(cells, NUM_OF_PIVOTS)
    if piv_dist == 'DCB':
        DCB_dist(cells, NUM_OF_PIVOTS, cell_hight_without_padding, max_dist)
    if piv_dist == 'ATB':
        ATB_dist(cells, NUM_OF_PIVOTS, cell_hight_without_padding)


def RAN_dist(cells, NUM_OF_PIVOTS):
    not_occupied_cells = []
    for cell in cells:
        if not cell.occupied:
            not_occupied_cells.append(cell)
    for _ in range(NUM_OF_PIVOTS):
        cell = random.choice(not_occupied_cells)
        cell.create_pivot()
        not_occupied_cells.remove(cell)


def neighbours_up_to(dist, q, cells, cell_hight_without_padding):
    neighbours = []
    q_x, q_y = q.get_pos()
    aside = dist * (cell_hight_without_padding + PADDING)

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
                neighbours.append(cell)

    return neighbours


def DCB_dist(cells, NUM_OF_PIVOTS, cell_hight_without_padding, max_dist):

    occupied_cells = []
    not_occupied_cells = {}
    for cell in cells:
        if cell.occupied:
            occupied_cells.append(cell)
        else:
            not_occupied_cells[cell] = 0

    for occ_cell in occupied_cells:
        for dist in range(max_dist):
            neighbours = neighbours_up_to(dist + 1, occ_cell, cells, cell_hight_without_padding)
            weight = max_dist - dist
            for neighbour in neighbours:
                not_occupied_cells[neighbour] = not_occupied_cells[neighbour] + weight

    sum_of_weights = sum(not_occupied_cells.values())
    p = []
    cells_to_pick = []
    for cell, weight in not_occupied_cells.items():
        cells_to_pick.append(cell)
        p.append(weight/sum_of_weights)

    to_pivots = np.random.choice(cells_to_pick, NUM_OF_PIVOTS, replace=False, p=p)
    for cell in to_pivots:
        cell.create_pivot()


def ATB_dist(cells, NUM_OF_PIVOTS, cell_hight_without_padding):
    list_of_cells_of_interest = []
    for cell in cells:
        if not cell.occupied:
            if has_wall_neightbour(cell, cells, cell_hight_without_padding):
                list_of_cells_of_interest.append(cell)

    for _ in range(NUM_OF_PIVOTS):
        cell = random.choice(list_of_cells_of_interest)
        cell.create_pivot()
        list_of_cells_of_interest.remove(cell)

def create_goals(cells):
    kind_of_cell = 0
    for cell in cells:
        if cell.get_goal() != -1:
            kind_of_cell = 1
            break
    mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
    for cell in cells:
        cell_pos_x, cell_pos_y = cell.get_pos()
        cell_size = cell.get_cell_size()
        if cell_pos_x - cell_size / 2 < mouse_pos_x < cell_pos_x + cell_size / 2:
            if cell_pos_y - cell_size / 2 < mouse_pos_y < cell_pos_y + cell_size / 2:
                if cell.get_goal() != -1:
                    cell.set_goal(-1)
                else:
                    cell.set_goal(kind_of_cell)


def upload_map(name, cells, grid_size):
    if name == '':
        return
    file_name = '%s.map' % name
    with open(file_name, 'rb') as fileObject:
        # load the object from the file into var b
        curr_dict = pickle.load(fileObject)

        if len(curr_dict.keys()) != grid_size ** 2:
            print('[ERROR]: grid_size is have to be - %s' % math.sqrt(len(curr_dict.keys())))
            raise ValueError()

        for cell in cells:
            cell.set_occupied(curr_dict[cell.get_ord_number()])


def upload_pivots(name, cells, pivots, grid_size):
    if name == '':
        return
    file_name = '%s.piv' % name
    with open(file_name, 'rb') as fileObject:
        # load the object from the file into var b
        curr_dict = pickle.load(fileObject)

        if len(curr_dict.keys()) != grid_size ** 2:
            print('[ERROR]')
            raise ValueError()

        for cell in cells:
            if curr_dict[cell.get_ord_number()]:
                cell.create_pivot()
                pivots.add(cell)


def update_title_up(titles):
    for title in titles:
        title.push(False)


def button_func(titles, cells, pivots, name, name_to_load, piv_name, piv_dist_to_load, piv_heuristic,
                cell_hight_without_padding, piv_dist):
    mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
    for title in titles:
        title_pos_x, title_pos_y = title.get_pos()
        title_size = title.get_cell_size()
        if title_pos_x - title_size / 2 < mouse_pos_x < title_pos_x + title_size / 2:
            if title_pos_y - title_size / 2 < mouse_pos_y < title_pos_y + title_size / 2:
                title.push(True)
                mode = title.get_mode()
                if mode == 1:
                    first_stage(cells, name)
                if mode == 2:
                    second_stage(cells, name_to_load, piv_name, piv_dist)
                if mode == 3:
                    if title.title == PREPARE_AND_RUN_TITLE:
                        third_stage(cells, pivots,
                                    name_to_load, piv_name, piv_dist_to_load, piv_heuristic,
                                    cell_hight_without_padding)
                    if title.title == RESET_TITLE:
                        reset_cells(cells)


def reset_cells(cells):
    for cell in cells:
        cell.reset()


def reset_cells_without_resetting_goal(cells):
    for cell in cells:
        cell.reset_without_resetting_goal()


def first_stage(cells, name):
    # timestr = time.strftime("%d.%m.%Y-%H:%M:%S")
    dict_to_save = {}
    for cell in cells:
        dict_to_save[cell.get_ord_number()] = cell.occupied
    file_name = "%s.map" % name
    # open the file for writing
    with open(file_name, 'wb') as fileObject:
        pickle.dump(dict_to_save, fileObject)


def second_stage(cells, name, piv_name, piv_dist):
    dict_to_save = {}
    for cell in cells:
        dict_to_save[cell.get_ord_number()] = cell.get_if_pivot()
    file_name = "%s-%s-%s.piv" % (name, piv_name, piv_dist)
    # open the file for writing
    with open(file_name, 'wb') as fileObject:
        pickle.dump(dict_to_save, fileObject)


def third_stage(cells, pivots,
                name_to_load, piv_name, piv_dist_to_load, piv_heuristic,
                cell_hight_without_padding):
    # print([i.get_ord_number() for i in pivots.sprites()])
    heuristic = Heuristic()
    heuristic_name_to_load = '%s-%s-%s.%s' % (name_to_load, piv_name, piv_dist_to_load, piv_heuristic)
    heuristic.create_data(piv_heuristic, cells, pivots, cell_hight_without_padding, heuristic_name_to_load)
    curr_closed, curr_open = run_a_star(cells, pivots, heuristic, cell_hight_without_padding)
    return paint_closed_nodes(curr_closed, curr_open, cells, pivots)
    # pprint(heuristic.get_data())


def paint_closed_nodes(curr_closed, curr_open, cells, pivots):
    for node in curr_closed:
        node.set_closed()
    for node in curr_open:
        node.set_open()
    for node in curr_closed:
        node.set_goal_color()
    for node in pivots:
        node.set_pivot_color()
    path_length = paint_path(cells)
    indicator = (path_length/(len(curr_closed) + len(curr_open)))*100
    print('OPEN: %s, CLOSED: %s' % (len(curr_open), len(curr_closed)))
    print('[INDICATOR]: %s' % indicator)
    return indicator


def paint_path(cells):
    path_length = 0
    start_node, end_node = get_start_and_end(cells)
    father = end_node.get_father()
    path_length += 1
    # while father.get_ord_number() != start_node.get_ord_number():
    while father is not None:
        path_length += 1
        father.set_path_sign_color()
        father = father.get_father()
        # print(father.get_ord_number())
    return path_length


def create_start_and_end_goals(cells, cell_hight_without_padding):
    list_of_free_cells = []
    for cell in cells:
        if not cell.occupied:
            if not cell.pivot:
                list_of_free_cells.append(cell)

    # create start
    start = random.choice(list_of_free_cells)
    start.set_goal(0)
    list_of_free_cells.remove(start)

    neighbours = neighbours_up_to(1, start, cells, cell_hight_without_padding)
    neighbours.append(start)
    there_is_not = True
    goal = random.choice(list_of_free_cells)
    while there_is_not:
        there_is_not = False
        if goal in neighbours:
            there_is_not = True
            goal = random.choice(list_of_free_cells)
    goal.set_goal(1)


def save_and_print_results(results_for_map, name_to_load):
    file_name = "%s.results" % name_to_load
    # open the file for writing
    with open(file_name, 'wb') as fileObject:
        pickle.dump(results_for_map, fileObject)

    # results_for_map['RAN', 'DCB', 'ATB'][1,..., 10][range(30)]['dif', 'can'] = indicator
    # results_for_map[piv_type][piv_num][prob_num][heuristic_type] = indicator
    to_print = {}
    for piv_type in results_for_map.keys():
        to_print[piv_type] = {'dif': [], 'can': []}
        for piv_num in results_for_map[piv_type].keys():
            for prob_num in results_for_map[piv_type][piv_num].keys():
                for heuristic_type, indicator in results_for_map[piv_type][piv_num][prob_num].items():
                    to_print[piv_type][heuristic_type].append(indicator)

    for piv_type in to_print.keys():
        for heuristic_type, list_of_indicators in to_print[piv_type].items():
            print('%s: %s -> %s' % (piv_type, heuristic_type, np.mean(list_of_indicators)))



