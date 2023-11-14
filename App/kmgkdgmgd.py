import datetime
h = "1995-12-26T14:50:17.170000Z"



ocurredTime  = h[:16] 
ocurredTime = datetime.datetime.strptime(ocurredTime , "%Y-%m-%dT%H:%M")
h = h[:16]
print(h)
print(5==5.000)
