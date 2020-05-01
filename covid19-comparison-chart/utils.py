# Fill with array
def fillWithArray(sheet, row, col, array):
    # Iter through cells and fill
    for _row in range(row, row + len(array)):
        sheet.cell(_row, col, int(array[_row - row]))

def adjustWidth(ws):
    dims = {}
    for row in ws.rows:
        for cell in row:
            if cell.value:
                dims[cell.column_letter] = max((dims.get(cell.column_letter, 0), len(str(cell.value))))    
    for col, value in dims.items():
        ws.column_dimensions[col].width = value + 1