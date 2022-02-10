from openpyxl import Workbook, worksheet
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import get_column_letter

wb = Workbook()
ws = wb.active

ws["A1"].value = '=_xlfn.IFS(SUMPRODUCT(--ISNUMBER(FIND({"n","-"},B1 & C1)))>0,5,B1>=5,1)'

wb.save("test.xlsx")
