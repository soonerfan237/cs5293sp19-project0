# cs5293sp19-project0
Alexander Sullivan-Wilson

You can run the code with the following command:
pipenv run python project0/main.py --arrests http://normanpd.normanok.gov/content/daily-activity

arrest_time is hard-coded to be the first column in each row.  
case_number is hard-coded to be the second column in each row.
Officer is hard-coded to be the final column in each row.
arrestee_birthday is parsed by using regex to search for a date field that comes after the arrest_time in the row.
arrestee_address is everything in between the arrestee_birthday and the status.
Parsing arrest_location, offense, and arrestee was more complicated because they can all be variable line lengths and there is inconsistent formatting that can be picked up by regex.  The pattern I used to identify these is that when a line ends with a space character, it means that the contents of that item continue on the next line.  I used this method to detect if arrestee_name and arrest_location were multiple lines.
Parsing assumes that arrestee_name is never more than 2 lines in length.  
It also assumes that arrest_location is never more than 2 lines in length.When parsing status it will assume 1 line in length unless it is a status containing the string "Citation" in which case it will parse 2 lines for status.
