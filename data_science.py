from main_help_functions import *
# name_to_load = 'sea-2/map'
# name_to_load = 'building-2/map'
name_to_load = 'land-2/map'
file_name = "%s.results" % name_to_load

if os.path.isfile(file_name):
    with open(file_name, 'rb') as fileObject:
        # load the object from the file into var b
        results_for_map = pickle.load(fileObject)

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
    for heuristic_type in to_print[piv_type].keys():
        for piv_type2 in to_print.keys():
            for heuristic_type2 in to_print[piv_type].keys():
                print('(%s + %s) vs (%s + %s) -> %s' % (piv_type, heuristic_type,
                                                    piv_type2, heuristic_type2,
                                    stats.ttest_ind(to_print[piv_type][heuristic_type],
                                                    to_print[piv_type2][heuristic_type2])))
