import os

# Fill with array
def fillWithArray(sheet, row, col, array):
    # Iter through cells and fill
    for _row in range(row, row + len(array)):
        sheet.cell(_row, col, round(float(array[_row - row]), 2))


def adjustWidth(ws):
    dims = {}
    for row in ws.rows:
        for cell in row:
            if cell.value:
                dims[cell.column_letter] = max((dims.get(cell.column_letter, 0), len(str(cell.value))))    
    for col, value in dims.items():
        ws.column_dimensions[col].width = value + 2


def getAbsolutePath(path):
    script_dir = os.path.dirname(__file__)
    rel_path = path
    abs_file_path = os.path.join(script_dir, rel_path)
    return abs_file_path

