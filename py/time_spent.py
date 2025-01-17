import csv
from datetime import datetime
from itertools import groupby
import py.utils as ut


def save(data):
    with open(f'../output/times/times_spent.tsv', 'w', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
        w.writerow(['Player', 'Days', 'Hours', 'Per game (in min)', 'Per day (in h, incl. 0)', 'Per day (in h, excl. 0)'])
        for k, v in data.items():
            w.writerow([k, v[0]['days'], v[0]['hours'], v[1], v[2], v[3]])


def group_stats(data):
    groups = groupby(data, lambda row: row['datetimeFinished'][:10])
    keys = []
    for k, v in groups:
        keys.append(k)
    return len(keys)


users = ut.open_file('../input/list_of_players_notes.txt')
times = {}
# {'Valetta6789': [time, num_games, num_days_since_joined]}
# time in sec
# time / num_games (in min)
# time / num_days_since_joined (in h)
for u in users:
    print(u)
    stats = ut.clear_speedruns(ut.open_stats(u))
    days_2 = group_stats(stats)
    date = stats[len(stats) - 1]['datetimeStarted']
    try:
        d_joined = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        d_joined = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
    days_1 = (datetime.now() - d_joined).days
    times[u] = [0, len(stats), days_1, days_2]
    for s in stats:
        try:
            d_start = datetime.strptime(s['datetimeStarted'], '%Y-%m-%dT%H:%M:%S.%fZ')
            d_finish = datetime.strptime(s['datetimeFinished'], '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            d_start = datetime.strptime(s['datetimeStarted'], '%Y-%m-%dT%H:%M:%SZ')
            d_finish = datetime.strptime(s['datetimeFinished'], '%Y-%m-%dT%H:%M:%SZ')
        diff = d_finish - d_start
        times[u][0] += diff.total_seconds()
    # per game
    times[u][1] = times[u][0] / times[u][1] / 60
    # per day
    times[u][2] = times[u][0] / times[u][2] / 3600
    # per day excl. days with 0 games
    times[u][3] = times[u][0] / times[u][3] / 3600
times = {k: [ut.convert_sec_to_day(v[0]), round(v[1], 1), round(v[2], 1), round(v[3], 1)] for k, v in sorted(times.items(), key=lambda i: -i[1][0])}
save(times)
