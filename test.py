from openpyxl import Workbook, worksheet
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import get_column_letter

from conditional_formating import custom_conditional_formatting

wb = Workbook()
ws = wb.active

ws["B2"].value = '1ahit'
ws["C2"].value = '1ahit'
ws["B3"].value = '1ahit'
ws["C3"].value = '1bhit'

custom_conditional_formatting(ws, "C2:C3", type='group')

ws["E1"].value = 6
ws["E2"].value = 10
ws["D1"].value = 0
ws["D2"].value = 1
ws["D3"].value = 2
ws["D4"].value = 3
ws["D5"].value = 4
ws["D6"].value = 5
ws["D7"].value = 6
ws["D8"].value = 7
ws["D9"].value = 8
ws["D10"].value = 9
ws["D11"].value = 10

custom_conditional_formatting(ws, "D1:D11", type='points', start='$E$1', end='$E$2')

wb.save("test.xlsx")
