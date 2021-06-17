import datetime as dt

hours = [(dt.time(i).strftime('%I%p')) for i in range(5, 24)]  # List of hours in 12-hour format
off_peak_hours = [(dt.time(i).strftime('%I%p')) for i in range(9, 16)]  # List of off peak hours

for i in range(19, 24):  # add rest of peak hours
    off_peak_hours.append((dt.time(i).strftime('%I%p')))
