import datetime;

# ct stores current time
ct = datetime.datetime.now()
print(f"{ct.year}{str(ct.month).zfill(2)}{str(ct.day).zfill(2)}")