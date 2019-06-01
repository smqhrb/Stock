Attribute VB_Name = "loadAccount"
Public Sub click_get_stockbase()
Dim args As String
Dim pathBase As String: pathBase = Workbooks("AcountWork.xlsm").Path & "\Account\"
Dim workPath As String: workPath = Workbooks("AcountWork.xlsm").Path

Dim pythonPath As String: pythonPath = """" & workPath & "\downAcountData.py"""

Dim csvFileName As String

args = "stock"

retVal = CallPythonMethod(workPath, pythonPath, args)
'retVal = 0
If retVal <> 0 Then
   MsgBox "error"
   Exit Sub
End If
'sheet code is exist,no create new
'IsExit (args)
csvFileName = pathBase & "StockClass.csv"
Dim stock_list As String: stock_list = "StockClass"
'sheet name :args
'csvFileName :data store filename
'stocklist : filename without appendix

Call WriteSheetXlsx(args, csvFileName, stock_list, "$A$1")
'get maximum row in the sheet(args)
max_row = Worksheets(args).Cells(Rows.Count, "A").End(xlUp).row
'If (Worksheets("OperUI").CheckBoxes.Count <= 1) Then
'
    'Worksheets("OperUI").CheckBoxes.Delete
    For i = 2 To max_row
        code = Worksheets(args).Cells(i, "A")
        If (code = "") Then
            Exit For
            
        End If
        code = Format$(code, "000000")
        Worksheets("OperUI").Cells(i, "C") = code
        Worksheets("OperUI").Cells(i, "D") = Worksheets(args).Cells(i, "B")
        Worksheets("OperUI").Cells(i, "E") = Worksheets(args).Cells(i, "C")
'
'        ret = Worksheets("OperUI").CheckBoxes.Add(Cells(i, "B").Left, Cells(i, "B").Top, 24, 16.5).Select
'
'        With Selection
'         .Value = xlOn
'         .LinkedCell = "$B" & i
'         .Display3DShading = True
'
'         .name = "CheckBox" & i
'         .Caption = "CheckBox" & i
'         .Text = ""
'        End With

    
    Next
'End If
End Sub



'Public Sub SelectAllCheckBox()
'RowCount = Worksheets("OperUI").CheckBoxes.Count
'If True = Worksheets("OperUI").CheckBoxes(i).Value Then
'For i = 2 To RowCount
'   Worksheets("OperUI").CheckBoxes(i).Value = True
'Next
'Else
'    For i = 2 To RowCount
'       Worksheets("OperUI").CheckBoxes(i).Value = False
'    Next
'End If


'End Sub


Public Sub click_get_data()
Dim code As String
Dim name As String
Dim i As Integer
  lastRow = Worksheets("OperUI").Cells(Rows.Count, "C").End(xlUp).row
  For i = 2 To lastRow
    code = Worksheets("OperUI").Cells(i, "C").Value
    
    name = Worksheets("OperUI").Cells(i, "D").Value
    
    Dim tm
    tm = Now()
    Call importAcount(code, name, i, 1)
    Worksheets("operui").Cells(i, "B") = Format$(Now() - tm, "hh:mm:ss")
    Application.DisplayAlerts = False
    Worksheets(code).Delete
    Application.DisplayAlerts = True
  Next
End Sub
Public Sub importAcount(code As String, name As String, row As Integer, isLoad As Integer)
Dim args As String
Dim pathBase As String: pathBase = Workbooks("AcountWork.xlsm").Path & "\Account\"
Dim workPath As String: workPath = Workbooks("AcountWork.xlsm").Path

Dim pythonPath As String: pythonPath = """" & workPath & "\downAcountData.py"""

Dim csvFileName As String
'sheet code is exist,no create new
IsExit (code)
name = RemoveSpaceInStr(name)
args = code & " " & name
If (isLoad = 1) Then
    retVal = CallPythonMethod(workPath, pythonPath, args)
    'retVal = 0
    If retVal <> 0 Then
       'MsgBox "error"
       Exit Sub
    End If
End If

'clear sheet code contents
Worksheets(code).UsedRange.ClearContents

Dim zcfzb_columns As Integer

zcfzb_columns = 120
Dim lrb_columns As Integer
lrb_columns = 50
Dim llb_columns As Integer
llb_columns = 104

typeQ = "year"
Dim year_zcfzb As String
year_zcfzb = code & "(" & name & "_" & typeQ & "_zcfzb)"
'year_zcfzb = code & "(" & name & "_" & typeQ & "_zcfzb).xlsx"
Dim year_lrb As String
year_lrb = code & "(" & name & "_" & typeQ & "_lrb)"
Dim year_llb As String
year_llb = code & "(" & name & "_" & typeQ & "_llb)"

csvFileName = pathBase & year_zcfzb & ".csv" '000651(格力电器_year_zcfzb).csv
'Call WriteSheet(code, csvFileName, 0, 0)
Call WriteSheetXlsx(code, csvFileName, year_zcfzb, "$A$1")

csvFileName = pathBase & year_lrb & ".csv"
Call WriteSheetXlsx(code, csvFileName, year_lrb, "$DG$1")
'Call WriteSheet(code, csvFileName, 0, zcfzb_columns)

csvFileName = pathBase & year_llb & ".csv"
Call WriteSheetXlsx(code, csvFileName, year_llb, "$FB$1")
'Call WriteSheet(code, csvFileName, 0, zcfzb_columns + lrb_columns)

Dim offLine As Integer

offLine = zcfzb_columns + lrb_columns + llb_columns
typeQ = "quarter"
Dim quarter_zcfzb As String
quarter_zcfzb = code & "(" & name & "_" & typeQ & "_zcfzb)"
Dim quarter_lrb As String
quarter_lrb = code & "(" & name & "_" & typeQ & "_lrb)"
Dim quarter_llb As String
quarter_llb = code & "(" & name & "_" & typeQ & "_llb)"

csvFileName = pathBase & quarter_zcfzb & ".csv"
Call WriteSheetXlsx(code, csvFileName, quarter_zcfzb, "$IO$1")

'Call WriteSheet(code, csvFileName, 0, offLine)

csvFileName = pathBase & quarter_lrb & ".csv"
Call WriteSheetXlsx(code, csvFileName, quarter_lrb, "$MU$1")

'Call WriteSheet(code, csvFileName, 0, offLine + zcfzb_columns)

csvFileName = pathBase & quarter_llb & ".csv"
Call WriteSheetXlsx(code, csvFileName, quarter_llb, "$OP$1")
'Call WriteSheet(code, csvFileName, 0, offLine + zcfzb_columns + lrb_columns)
'
'
For i = 6 To 180
    Worksheets("operui").Cells(row, i) = ""
Next

''3月母公司股东权益   3月少数股东权益 3月应收账款 3月其他应收账款 3月存货 3月可供出售金融资产 3月长期股权投资 3月固定资产 3月商誉 3月无性资产 3月短期借款 3月长期借款 3月应付债券 净资产收益率    销售毛利率  存货的减少  经营性应收项目的减少    经营性应收项目的增加    流动资产/流动负债   折旧与摊销
'zcfzb_mgsgdqy_col = 106 'DB 3月母公司股东权益
zcfzb_mgsgdqy_col = "MP"
lastRow = Worksheets(code).Cells(Rows.Count, zcfzb_mgsgdqy_col).End(xlUp).row
Worksheets("operui").Cells(row, "F") = Worksheets(code).Cells(lastRow, zcfzb_mgsgdqy_col).Value
'zcfzb_ssguqy_col = zcfzb_mgsgdqy_col + 1 'DC 3月少数股东权益
Dim zcfzb_ssguqy_col As String: zcfzb_ssguqy_col = "MQ"
Call SetCellValuesLastRow(code, zcfzb_ssguqy_col, row, "G")

'zcfzb_yszk = 8 ' H 3月应收账款
Dim zcfzb_yszk_col As String: zcfzb_yszk_col = "IV"
Call SetCellValuesLastRow(code, zcfzb_yszk_col, row, "H")

'zcfzb_qtyszk = 14 'O 3月其他应收账款

Dim zcfzb_qtyszk_col As String: zcfzb_qtyszk_col = "JC"
Call SetCellValuesLastRow(code, zcfzb_qtyszk_col, row, "I")
'zcfzb_ch = 21 'U 3月存货
Dim zcfzb_ch_col As String: zcfzb_ch_col = "JI"
Call SetCellValuesLastRow(code, zcfzb_ch_col, row, "J")
'zcfzb_kgcsjrzc = 28 'AB 3月可供出售金融资产
Dim zcfzb_kgcsjrzc_col As String: zcfzb_kgcsjrzc_col = "JP"
Call SetCellValuesLastRow(code, zcfzb_kgcsjrzc_col, row, "K")
'zcfzb_cqgqtz = zcfzb_kgcsjrzc + 3 'AE 3月长期股权投资
Dim zcfzb_cqgqtz_col As String: zcfzb_cqgqtz_col = "JS"
Call SetCellValuesLastRow(code, zcfzb_cqgqtz_col, row, "L")
'zcfzb_gdzc = 38 'AL 3月固定资产
Dim zcfzb_gdzc_col As String: zcfzb_gdzc_col = "JZ"
Call SetCellValuesLastRow(code, zcfzb_gdzc_col, row, "M")
'zcfzb_sy = "AU" '3月商誉
Dim zcfzb_sy_col As String: zcfzb_sy_col = "AU"
Call SetCellValuesLastRow(code, zcfzb_sy_col, row, "N")
'zcfzb_wxzc = "AS" '3月无形资产
Dim zcfzb_wxzc_col As String: zcfzb_wxzc_col = "KG"
Call SetCellValuesLastRow(code, zcfzb_wxzc_col, row, "O")
'zcfzb_dqjk = "BB" '3月短期借款
Dim zcfzb_dqjk_col As String: zcfzb_dqjk_col = "KP"
Call SetCellValuesLastRow(code, zcfzb_dqjk_col, row, "P")
'zcfzb_cqjk = "CH" '3月长期借款
Dim zcfzb_cqjk_col As String: zcfzb_cqjk_col = "LV"
Call SetCellValuesLastRow(code, zcfzb_cqjk_col, row, "Q")
'zcfzb_yfzq = "CI" '3月应付债券
Dim zcfzb_yfzq_col As String: zcfzb_yfzq_col = "LW"
Call SetCellValuesLastRow(code, zcfzb_yfzq_col, row, "R")
'2018-1990


lastRow = Worksheets(code).Cells(Rows.Count, "EU").End(xlUp).row
minRow = 2
If (lastRow - minRow > 29) Then
    minRow = minRow + (lastRow - minRow - 29)
End If
For i = lastRow To minRow Step -1
    'lrb_jzcsyl = lrb_jlr / zcfzb_syzqy '净资产收益率
    lrb_jlr = Worksheets(code).Cells(i, "EU").Value
    zcfzb_syzqy = Worksheets(code).Cells(i, "DD").Value
    If (zcfzb_syzqy > 0) Then
        'U 21
        cellpos = Replace("U" & Str(row), " ", "")
        Set Rng = Worksheets("operui").Range(cellpos)
        'Worksheets("operui").Cells(row, 21 + i - 2) = lrb_jlr / zcfzb_syzqy
        Rng.Cells(1, lastRow - i + 1) = lrb_jlr / zcfzb_syzqy
    End If
    '销售毛利率 =(营业收入 -营业成本)/营业收入
    lrb_yysr = Worksheets(code).Cells(i, "DI").Value
    lrb_yycb = Worksheets(code).Cells(i, "DP").Value
    If (lrb_yycb > 0) Then
        cellpos = Replace("AX" & Str(row), " ", "")
        Set Rng = Worksheets("operui").Range(cellpos)
        Rng.Cells(1, lastRow - i + 1) = (lrb_yysr - lrb_yycb) / lrb_yycb
    End If
    '存货的减少
    xjllb_chjx = Worksheets(code).Cells(i, "HY").Value
    cellpos = Replace("CA" & Str(row), " ", "")
    Set Rng = Worksheets("operui").Range(cellpos)
    Rng.Cells(1, lastRow - i + 1) = xjllb_chjx
    '经营性应收项目的减少
    xjllb_jyxysxmjs = Worksheets(code).Cells(i, "HZ").Value
    cellpos = Replace("DD" & Str(row), " ", "")
    Set Rng = Worksheets("operui").Range(cellpos)
    Rng.Cells(1, lastRow - i + 1) = xjllb_jyxysxmjs
    '经营性应收项目的增加
    xjllb_jyxysxmzj = Worksheets(code).Cells(i, "IA").Value
    cellpos = Replace("EG" & Str(row), " ", "")
    Set Rng = Worksheets("operui").Range(cellpos)
    Rng.Cells(1, lastRow - i + 1) = xjllb_jyxysxmzj
    '流动资产/流动负债
    zcfzb_ldzc = Worksheets(code).Cells(i, "Z").Value
    zcfzb_ldfz = Worksheets(code).Cells(i, "CG").Value
    If (zcfzb_ldfz <> 0) Then
        cellpos = Replace("FJ" & Str(row), " ", "")
        Set Rng = Worksheets("operui").Range(cellpos)
        Rng.Cells(1, lastRow - i + 1) = zcfzb_ldzc / zcfzb_ldfz
    End If
    '折旧与摊销 没有
Next
''销售毛利率 =营业收入 -营业成本/营业收入

'xjllb_chjs = "BX" '存货的减少
'xjllb_jyxysxmjs = "BY" ' 经营性应收项目的减少
'xjllb_jyxysxmzj = "BZ" '经营性应收项目的增加
''流动资产/流动负债
''折旧与摊销 没有
'



End Sub
Public Function SetCellValuesLastRow(srcSheetName As String, col As String, destinRow As Integer, destinCol As String)
'col = "MP"
lastRow = Worksheets(srcSheetName).Cells(Rows.Count, col).End(xlUp).row
Worksheets("operui").Cells(destinRow, destinCol) = Worksheets(srcSheetName).Cells(lastRow, col).Value
End Function
Public Function WriteSheet(sheetName As String, csvFilePos As String, startRow As Integer, startCol As Integer)
'Read file 'csvFilePos' ,Write to sheetName



CSVFileNumber = FreeFile
'Open csvFilePos For Input As #CSVFileNumber
Open csvFilePos For Binary As #CSVFileNumber
content = Input(LOF(CSVFileNumber), CSVFileNumber)
'content = StrConv(content, vbNarrow)
rowText = Split(content, vbNewLine)
For rowIter = 1 To UBound(rowText)
    If rowText(rowIter) <> "" Then
        colText = Empty
        colText = Split(rowText(rowIter), ",")
        For colIter = 0 To UBound(colText)
            Worksheets(sheetName).Cells(rowIter + 1, colIter + 1 + startCol).Value = colText(colIter)
        Next colIter
    End If
Next rowIter
WriteSheet = UBound(rowText)
End Function

Public Function WriteSheetXlsx(sheetName As String, csvFilePos As String, fileName As String, rangPos As String) ', startRow As Integer, startCol As Integer)
'Read file 'csvFilePos' ,Write to sheetName

IsExit (sheetName)
On Error GoTo Err_Handle
    With Worksheets(sheetName).QueryTables.Add(Connection:= _
        "TEXT;" & csvFilePos _
        , Destination:=Worksheets(sheetName).Range(rangPos))
        .name = fileName
        .FieldNames = True
        .RowNumbers = False
        .FillAdjacentFormulas = False
        .PreserveFormatting = True
        .RefreshOnFileOpen = False
        .RefreshStyle = xlInsertDeleteCells
        .SavePassword = False
        .SaveData = True
        .AdjustColumnWidth = True
        .RefreshPeriod = 0
        .TextFilePromptOnRefresh = False
        .TextFilePlatform = 65001
        .TextFileStartRow = 1
        .TextFileParseType = xlDelimited
        .TextFileTextQualifier = xlTextQualifierDoubleQuote
        .TextFileConsecutiveDelimiter = False
        .TextFileTabDelimiter = True
        .TextFileSemicolonDelimiter = False
        .TextFileCommaDelimiter = True
        .TextFileSpaceDelimiter = False
    '        .TextFileColumnDataTypes = Array(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, _
    '        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 _
    '        , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
        .TextFileTrailingMinusNumbers = True
        .Refresh BackgroundQuery:=False
    End With
    Return
Err_Handle:
    If Erl > 0 Then
    Worksheets(sheetName).Cells(1, 1) = Erl
    End If
    
    
End Function
Public Function CallPythonMethod(workPath As String, filePath As String, argsCmd As String)
'filePath is python file
'workPath is data path
'parameter argsCmd
Dim shellObj As Object
Set shellObj = VBA.CreateObject("WSCript.Shell")
Dim waitOnReturn As Boolean: waitOnReturn = True
Dim windowStyle As Integer: windowStyle = 2
Dim cmdPath As String

args = filePath & " " & workPath & " " & argsCmd
CallPythonMethod = shellObj.Run("%comspec% /c " & args, windowStyle, waitOnReturn)
End Function
Sub IsExit(code)
'判断code的sheet是否存在
Dim d, sh As Worksheet, s$
Dim sX As Worksheet

    Set d = CreateObject("Scripting.Dictionary")
    For Each sh In Worksheets
       d(sh.name) = ""
    Next
   If d.exists(code) Then

       
    Else
        Sheets.Add after:=Sheets(Sheets.Count) '添加sheet
        ActiveSheet.name = code
        Set sX = ActiveSheet
        Worksheets("OperUI").Activate '#
    End If
    Set d = Nothing
 
End Sub
Private Function RemoveSpaceInStr(paraString As String)
Dim a As String, b As String
a = paraString
For i = 1 To Len(a)
    If Mid(a, i, 1) <> " " And Mid(a, i, 1) <> "*" Then
        b = b & Mid(a, i, 1)
    End If
Next i
RemoveSpaceInStr = b
End Function
