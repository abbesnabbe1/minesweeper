#INIT
field_width = 0
field_height = 0
rows = 0
cols = 0

def init_logic(field_width_in, field_height_in, rows_in, cols_in):
    global field_width, field_height, rows, cols
    field_width = field_width_in
    field_height = field_height_in
    rows = rows_in
    cols = cols_in

def get_box_tuple(x, y):
    global field_width, field_height
    return x//field_width, y//field_height