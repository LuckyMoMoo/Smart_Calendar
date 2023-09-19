#!/usr/bin/env python3

"""
    SENG_265
    Assignment #2
    Pengfei Li
    V00831098
"""

import sys
import argparse
import datetime


def month(dt_obj):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']
    return months[dt_obj.month - 1]


def weekday(dt_obj):
    weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    return weekdays[dt_obj.weekday()]


def time(tm_obj):
    h = tm_obj.hour if (tm_obj.hour <= 12) else tm_obj.hour - 12
    h = 12 if h == 0 else h
    m = tm_obj.minute
    t = 'AM' if (tm_obj.hour < 12) else 'PM'
    return '{0: >2}:{1:0>2} {2}'.format(h, m, t)


def one_week(dtm_obj):
    seven_days = datetime.timedelta(days=7)
    return dtm_obj + seven_days


def dtm_ical_to_obj(dtm_ical):
    (y, mo, d, h, mi, s) = (dtm_ical[0:4], dtm_ical[4:6], dtm_ical[6:8],
                            dtm_ical[9:11], dtm_ical[11:13], dtm_ical[13:])
    return datetime.datetime(int(y), int(mo), int(d), int(h), int(mi), int(s))


def time_obj(dt_cmd):
    i = [pos for (pos, ch) in enumerate(dt_cmd) if ch == '/']
    (y, mo, d) = (dt_cmd[:i[0]], dt_cmd[(i[0] + 1):i[1]], dt_cmd[(i[1] + 1):])
    return datetime.date(int(y), int(mo), int(d))


def read_file(filename):

    try:
        myfile = open(filename, 'r')
        lines = [line.strip() for line in myfile]

        lines.remove('BEGIN:VCALENDAR')
        lines.remove('END:VCALENDAR')

        if 'VERSION:A' in lines:
            lines.remove('VERSION:A')
        if '' in lines:
            lines.remove('')

        categories = ('\n'.join(lines)).split('END:VEVENT')

        if '' in categories:
            categories.remove('')

        categories = [cat.split('\n') for cat in categories]
        categories = [[line for line in cat if ((line != '') and (
            line != 'BEGIN:VEVENT'))] for cat in categories]
        myfile.close()
        return categories

    except FileNotFoundError:
        print("Error: Cannot find the target file")
        exit()
    except PermissionError:
        print("Error: No permission to access the file")
        exit()


def store_events(categories):

    events = {}
    for cat in categories:
        dtm_ical_start = cat[0][8:]
        dtm_ical_end = cat[1][6:]

        if cat[2][:32] == 'RRULE:FREQ=WEEKLY;WKST=MO;UNTIL=':
            dtm_ical_until = cat[2][32:47]
        elif cat[2][:24] == 'RRULE:FREQ=WEEKLY;UNTIL=':
            dtm_ical_until = cat[2][24:39]
        else:
            dtm_ical_until = cat[1][6:]

        summary = cat[-1][8:]
        location = cat[-2][9:]

        dtm_obj_start = dtm_ical_to_obj(dtm_ical_start)
        dtm_obj_end = dtm_ical_to_obj(dtm_ical_end)
        dtm_obj_until = dtm_ical_to_obj(dtm_ical_until)

        while dtm_obj_end <= dtm_obj_until:
            date = dtm_obj_start.date()
            if date not in events:

                events[date] = []
            events[date].append((dtm_obj_start.time(),
                                 dtm_obj_end.time(), summary, location))
            dtm_obj_start = one_week(dtm_obj_start)
            dtm_obj_end = one_week(dtm_obj_end)

    for date in events:
        events[date].sort(key=lambda tup: [tup[0], tup[2]])
    return events


def print_events(events, start, end):

    range_start = time_obj(start)
    range_end = time_obj(end)

    keys = list(events.keys())
    keys.sort()
    keys = [key for key in keys if (key >= range_start and key <= range_end)]

    try:

        key = keys[0]
        dt_str = '{0} {1:0>2}, {2} ({3})'.format(month(key), key.day,
                                                 key.year, weekday(key))
        print(dt_str)
        print('-' * len(dt_str))
        for event in events[key]:
            print('{0} to {1}: {2} {{{{{3}}}}}'.format(time(event[0]),
                                                       time(event[1]), event[2], event[3]))

        for key in keys[1:]:
            print()
            dt_str = '{0} {1:0>2}, {2} ({3})'.format(month(key),
                                                     key.day, key.year, weekday(key))
            print(dt_str)
            print('-' * len(dt_str))
            for event in events[key]:
                print('{0} to {1}: {2} {{{{{3}}}}}'.format(time(event[0]),
                                                           time(event[1]), event[2], event[3]))
    except IndexError:
        exit()


def main():

    if len(sys.argv) != 4:
        print(
            "usage:", sys.argv[0], "./process_cal2.py --start=yyyy/m/d --end=yyyy/m/d --file=<file name>")
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, help='file to be processed')
    parser.add_argument('--start', type=str, help='start of date range')
    parser.add_argument('--end', type=str, help='end of data range')

    args = parser.parse_args()

    if not args.file:
        print("Need --file=<ics filename>")

    if not args.start:
        print("Need --start=yyyy/mm/dd")

    if not args.end:
        print("Need --end=yyyy/mm/dd")

    cal_1 = read_file(args.file)
    events = store_events(cal_1)
    print_events(events, args.start, args.end)


if __name__ == "__main__":
    main()
