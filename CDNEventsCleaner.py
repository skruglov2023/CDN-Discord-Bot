# first get all lines from file
with open('/home/pi/Desktop/scripts/CDN-Discord-Bot/CDNEvents.txt', 'r') as f:
    lines = f.readlines()

# remove spaces
lines=[line.replace('Timestamp,Moderator/Coach\'s Name,What is your team/club name,What is the time/date of this event,What is the location for this event?,"Would you like us to film, photograph, create a video?",Email Address', '') for line in lines]
lines = [line.replace(',,,,,,\n', '') for line in lines]
lines=[line.replace(',', '	') for line in lines]

# finally, write lines in the file
with open('/home/pi/Desktop/scripts/CDN-Discord-Bot/CDNEvents.txt', 'w') as f:
    f.writelines(lines)
