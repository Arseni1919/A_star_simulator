# ----------------------------------------------------------------------- #
# ----------------------- SEARCH COURSE PROJECT ------------------------- #
# ----------------------------------------------------------------------- #

# Import and initialize
from main_help_functions import *

# ------------------------------------------------------- #
# -------------------- INPUT SETTING -------------------- #
# ------------------------------------------------------- #

grid_size = 40
mode = 3
curr_map = ''
curr_pivots = ''
curr_alg = ''
name_to_load = 'sea-2/map'
name_to_save = 'building-2/map'
piv_name = '10'
piv_dist_to_load = 'ATB'

# '' / dif / can / bor / per
piv_heuristic = ''
# piv_heuristic = 'dif'
# piv_heuristic = 'can'
# piv_heuristic = 'per'

NUM_OF_PIVOTS = 5
# 'RAN', 'DCB', 'ATB'
# piv_dist = ''
# piv_dist, max_DCB_dist = 'RAN', None
# piv_dist, max_DCB_dist = 'DCB', 3
piv_dist, max_DCB_dist = 'ATB', None

need_to_render = True
# ------------------------------------------------------- #

pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Heuristic: %s' % piv_heuristic)

# Instantiate
all_sprites = pygame.sprite.Group()
pivots = pygame.sprite.Group()
cells = pygame.sprite.Group()
titles = pygame.sprite.Group()

cell_hight_without_padding = create_field(cells, all_sprites, grid_size)
create_titles(titles, all_sprites, mode)
upload_map(name_to_load, cells, grid_size)
if mode == 2:
    create_pivots_according_to_dist(piv_dist, NUM_OF_PIVOTS, cells, cell_hight_without_padding, max_DCB_dist)
if mode == 3:
    if piv_dist_to_load != '':
        name = '%s-%s-%s' % (name_to_load, piv_name, piv_dist_to_load)
    else:
        name = '%s-%s' % (name_to_load, piv_name)
    upload_pivots(name, cells, pivots, grid_size)

if need_to_render:
    # Run until the user asks to quit
    while need_to_render:

        # Did the user click the window close button?
        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == K_ESCAPE:
                    need_to_render = False

            # Did the user click the window close button? If so, stop the loop.
            if event.type == QUIT:
                need_to_render = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                button_func(titles, cells, pivots, name_to_save, name_to_load,
                            piv_name, piv_dist_to_load, piv_heuristic,
                            cell_hight_without_padding, piv_dist)
                if mode == 2:
                    create_pivot(cells)
                if mode == 3:
                    create_goals(cells)

            if event.type == pygame.MOUSEBUTTONUP:
                update_title_up(titles)

        # Get the set of keys pressed and check for user input
        pressed_keys = pygame.key.get_pressed()

        if mode == 1:
            update_cells(cells)
        # Update the player sprite based on user keypresses
        # player.update(pressed_keys)

        # Fill the screen with black
        screen.fill((2, 189, 164))

        # Draw the player on the screen
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Flip the display
        pygame.display.flip()

else:
    results_for_map = {}
    for piv_type in ['DCB', 'ATB', 'RAN']:
        print('# ------------------------------------------------------------- #')
        print('# ----------------- [STARTS]: pivot set - %s ----------------- #' % piv_type)
        print('# ------------------------------------------------------------- #')
        results_for_map[piv_type] = {}

        # pass

        for piv_num in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            print('# -------- [STARTS]: set number - %s -------- #' % piv_num)
            results_for_map[piv_type][piv_num] = {}

            # new field

            # Instantiate
            all_sprites = pygame.sprite.Group()
            pivots = pygame.sprite.Group()
            cells = pygame.sprite.Group()
            titles = pygame.sprite.Group()

            cell_hight_without_padding = create_field(cells, all_sprites, grid_size)
            create_titles(titles, all_sprites, mode)
            upload_map(name_to_load, cells, grid_size)

            name = '%s-%s-%s' % (name_to_load, piv_num, piv_type)
            upload_pivots(name, cells, pivots, grid_size)

            for prob_num in range(15):
                print('# --- [STARTS]: problem -  %s --- #' % prob_num)
                results_for_map[piv_type][piv_num][prob_num] = {}

                # Create Start-End
                reset_cells(cells)
                create_start_and_end_goals(cells, cell_hight_without_padding)

                for heuristic_type in ['dif', 'can']:
                    # for heuristic_type in ['dif']:
                    # print('%s,%s,%s,%s' % (heuristic_type, piv_type, piv_num, prob_num))
                    # heuristic_name_to_load = '%s-%s-%s.%s' % (name_to_load, piv_name, piv_dist_to_load, piv_heuristic)
                    indicator = third_stage(cells, pivots,
                                            name_to_load, piv_num, piv_type, heuristic_type,
                                            cell_hight_without_padding)

                    results_for_map[piv_type][piv_num][prob_num][heuristic_type] = indicator
                    # results_for_map[piv_type][piv_num][prob_num]['can'] = 0

                    # Fill the screen with black
                    screen.fill((2, 189, 164))

                    # Draw the player on the screen
                    for entity in all_sprites:
                        screen.blit(entity.surf, entity.rect)

                    # Flip the display
                    pygame.display.flip()

                    # RESET
                    reset_cells_without_resetting_goal(cells)

    save_and_print_results(results_for_map, name_to_load)

# Done! Time to quit.
pygame.quit()
