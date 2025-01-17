import py.utils as ut


def get_wins(totals_list):
    return len([row for row in totals_list
                if row['score'] == ut.get_max_score(row['options']['variantName'])])


def get_losses(totals_list):
    return len([row for row in totals_list
                if row['score'] != ut.get_max_score(row['options']['variantName'])])


def get_totals(stat_list):
    results = {}
    # total - count
    total = len(stat_list)
    total_wins = get_wins(stat_list)
    total_losses = get_losses(stat_list)
    results['total_c'] = [total_wins, total_losses, total]
    # total - %
    results['total_p'] = [ut.p(total_wins, total), ut.p(total_losses, total), ut.p(total_wins, total_losses)]
    # 2p - count
    list_2p = get_list_2p(stat_list)
    total = len(list_2p)
    total_wins = get_wins(list_2p)
    total_losses = get_losses(list_2p)
    results['total_2p_c'] = [total_wins, total_losses, total]
    # 2p - %
    results['total_2p_p'] = [ut.p(total_wins, total), ut.p(total_losses, total), ut.p(total_wins, total_losses)]
    # 3p - count
    list_3p = get_list_3p(stat_list)
    total = len(list_3p)
    total_wins = get_wins(list_3p)
    total_losses = get_losses(list_3p)
    results['total_3p_c'] = [total_wins, total_losses, total]
    # 3p - %
    results['total_3p_p'] = [ut.p(total_wins, total), ut.p(total_losses, total), ut.p(total_wins, total_losses)]
    return results


def get_list_2p(stat_list):
    return [row for row in stat_list if row['options']['numPlayers'] == 2]


def get_list_3p(stat_list):
    return [row for row in stat_list if row['options']['numPlayers'] != 2]


def get_variant_types():
    with open(f'resources/variant_types.txt', 'r') as f:
        variants = {}
        for line in f.readlines():
            line = line.rstrip().split('\t')
            (key, val) = line[0], line[2]
            variants[key] = val
    return variants


def group_stats_by_eff(stats):
    variants = get_variant_types()
    list_easy = [row for row in stats if variants[row['options']['variantName']] == 'easy']
    list_null = [row for row in stats if variants[row['options']['variantName']] == 'null']
    list_sd = [row for row in stats if variants[row['options']['variantName']] == 'sd']
    list_dd = [row for row in stats if variants[row['options']['variantName']] == 'dd']
    return ut.clear_speedruns(stats), ut.clear_speedruns(list_easy), ut.clear_speedruns(list_null), ut.clear_speedruns(list_sd), ut.clear_speedruns(list_dd)


def get_all_stats(items, s_id):
    stats, list_easy, list_null, list_sd, list_dd = group_stats_by_eff(items)
    if s_id == 'bga':
        stats, list_easy, list_null, list_sd, list_dd = \
            ut.filter_bga(stats), \
            ut.filter_bga(list_easy), \
            ut.filter_bga(list_null), \
            ut.filter_bga(list_sd), \
            ut.filter_bga(list_dd)
    totals = get_totals(stats)
    totals_easy = get_totals(list_easy)
    totals_null = get_totals(list_null)
    totals_sd = get_totals(list_sd)
    totals_dd = get_totals(list_dd)
    return {
        'Totals': totals,
        'Easy': totals_easy,
        'Null': totals_null,
        'Single dark': totals_sd,
        'Double dark': totals_dd
    }


def get_games_by_month(stats):
    stats = get_list_3p(stats)
    months = {}
    for game in stats:
        d_game = game['datetimeFinished'][:7]
        if d_game in months:
            months[d_game] += 1
        else:
            months[d_game] = 1
    return dict(sorted(months.items()))
