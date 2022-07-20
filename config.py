# 
HOST = ""
PORT = 53011
ENCODING = "UTF-8"

CHECK_SERVER_HOST = "vragi-vezde.to.digital"
CHECK_SERVER_PORT = 51624

PROTOCOL = "РКСОК/1.0"
SEPARATOR = "\r\n\r\n"

file_name = "phonebook.txt"

command_verbs = ("ОТДОВАЙ", "УДОЛИ", "ЗОПИШИ", "МОЖНА")
not_understand_response = "НИПОНЯЛ"
may_i = "АМОЖНА?"
you_can = "МОЖНА"
cannot = "НИЛЬЗЯ"
NO_DATA = "НИНАШОЛ"
SUCCESS = "НОРМАЛДЫКС"

class Commands():
    get = "ОТДОВАЙ"
    insert = "ЗОПИШИ"
    delete = "УДОЛИ"
