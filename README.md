# Smart_Calendar
A smart calendar that can take input dates and output corresponding events.
You are to write a python program that inputs lines of data from a calendar file provided, accepts options and
arguments from the command line, and then outputs to the console events from the calendar file into a
more readable form. To get started, the teaching team has provided a skeleton version of process_cal.c,
plus another different C program with a few functions that may be helpful for your implementation. For
example, on the SENG server at UVic (seng265.seng.uvic.ca) there is one such ics file contained in the
/seng265work/A1 subdirectory (named one.ics) which is an extract from the schedule of a fictional UVic

student named Diana Devps:
BEGIN:VCALENDAR
BEGIN:VEVENT
DTSTART:20210214T180000
DTEND:20210214T210000
LOCATION:Burger King
SUMMARY:Romantic dinner with Chris
END:VEVENT
END:VCALENDAR
