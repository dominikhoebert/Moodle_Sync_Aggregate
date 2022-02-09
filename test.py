from openpyxl import Workbook, worksheet
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import get_column_letter

wb = Workbook()
ws = wb.active

ws["A1"].value = '=SUMPRODUCT(--EXACT(B1:C1,"ü"))

wb.save("test.xlsx")
