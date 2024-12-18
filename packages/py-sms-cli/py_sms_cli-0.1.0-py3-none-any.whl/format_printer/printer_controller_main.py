import prettytable as pt

def printer_main_list(data):
    data_list = data["data"]["data"]
    if len(data_list) == 0:
        raise Exception("No data")
    tb = pt.PrettyTable()
    tb.field_names = data_list[0].keys()
    for d in data_list:
        tb.add_row(d.values())
    return tb