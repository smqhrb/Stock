Attribute VB_Name = "loadAccount"

Public Sub click_get_stockbase()
'获取股票代码
Dim args As String
Dim pathBase As String: pathBase = Workbooks("AcountWorkThx.xlsm").Path & "\Account\"
Dim workPath As String: workPath = Workbooks("AcountWorkThx.xlsm").Path

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
max_row = Worksheets(args).Cells(Rows.count, "A").End(xlUp).row
'max_row = 3 'test

    For i = 2 To max_row
        code = Worksheets(args).Cells(i, "A")
        If (code = "") Then
            Exit For
            
        End If
        code = Format$(code, "000000")
        Worksheets("OperUI").Cells(i + 1, "C") = code
        Worksheets("OperUI").Cells(i + 1, "D") = Worksheets(args).Cells(i, "B")
        Worksheets("OperUI").Cells(i + 1, "E") = Worksheets(args).Cells(i, "C")
'
   
    Next

End Sub
Public Function WalkFolder(str As String) As String
    Dim MyFile As String
    Dim s As String
    Dim count As Integer
    Dim pathBase As String: pathBase = Workbooks("AcountWorkThx.xlsm").Path & "\Account\"
    MyFile = Dir(pathBase & "*.csv")
    WalkFolder = ""

    Do While MyFile <> ""
        MyFile = Dir
        If MyFile = "" Then
            Exit Do
        End If
        If (str = Mid(MyFile, 1, 6)) Then
            pos = InStr(MyFile, "_")
            WalkFolder = Mid(MyFile, 8, pos - 8)
            Exit Do
        End If
    Loop
    
End Function
Public Sub click_get_data()
'get data from www
Dim code As String
Dim name As String
Dim i As Integer
  lastRow = Worksheets("OperUI").Cells(Rows.count, "C").End(xlUp).row
  'lastRow = 4 'test
  For i = 3 To lastRow
    code = Worksheets("OperUI").Cells(i, "C").Value
    
    name = Worksheets("OperUI").Cells(i, "D").Value
    
    Dim tm
    tm = Now()
    Call importAcount(code, name, i, 1, 1)
    Worksheets("operui").Cells(i, "B") = Format$(Now() - tm, "hh:mm:ss")
'    Application.DisplayAlerts = False
'    Worksheets(code).Delete
'    Application.DisplayAlerts = True
  Next
End Sub
Public Sub click_get_local_data()
'load data from path '/Account'
Dim code As String
Dim name As String
Dim i As Integer
  lastRow = Worksheets("OperUI").Cells(Rows.count, "C").End(xlUp).row
  'lastRow = 11 'test
  For i = 3 To lastRow
    code = Worksheets("OperUI").Cells(i, "C").Value
    
    name = Worksheets("OperUI").Cells(i, "D").Value
    
    Dim tm
    tm = Now()
    Call importAcount(code, name, i, 0, 1)
    Worksheets("operui").Cells(i, "B") = Format$(Now() - tm, "hh:mm:ss")
'    Application.DisplayAlerts = False
'    Worksheets(code).Delete
'    Application.DisplayAlerts = True
  Next
End Sub
Public Sub importAcount(code As String, name As String, row As Integer, isLoad As Integer, isDeleteSheet As Integer)
Dim args As String
Dim pathBase As String: pathBase = Workbooks("AcountWorkThx.xlsm").Path & "\Account\"
Dim workPath As String: workPath = Workbooks("AcountWorkThx.xlsm").Path

Dim pythonPath As String: pythonPath = """" & workPath & "\downAcountData.py"""

Dim csvFileName As String
'sheet code is exist,no create new
'IsExit (code)
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
'Worksheets(code).UsedRange.ClearContents
maxcoulmn = Worksheets("OperUI").Cells(2, Columns.count).End(xlToLeft).Column
'load quarter report at first


typeQ = "quarter"
'color set
color_0 = RGB(230, 184, 183)
color_1 = RGB(216, 228, 188)
color_use = color_0
Dim quarter_all As String
quarter_all = code & "(" & name & "_" & typeQ & "_all)"
csvFileName = pathBase & quarter_all & ".csv"
Dim code_sheet_name As String
code_sheet_name = quarter_all
IsExit (code_sheet_name)
Worksheets(code_sheet_name).UsedRange.ClearContents
Call WriteSheetXlsx(code_sheet_name, csvFileName, quarter_all, "$A$1")
'get column's name until split
startCol = 6 'first col of quarter data
startYCol = 17 'first col of year data
'code sheet maximum row
lastRow = Worksheets(code_sheet_name).Cells(Rows.count, 1).End(xlUp).row

'
lastRowCol = ""
colIndex = 2
color_switch = 0
cell_update = 0 '
For colIterQ = startCol To maxcoulmn
    operui_colName = Worksheets("operui").Cells(2, colIterQ)
    'Worksheets("operui").Cells(row, colIterQ) = ""
    If operui_colName = "split" Then
        startYCol = colIterQ + 1
        Exit For
    End If
    cell_update = 0
    If operui_colName <> "" Then
        
        If lastRowCol <> operui_colName Then
            lastRowCol = operui_colName
            colIndex = 2
            
            If color_switch = 0 Then
              color_use = color_0
              color_switch = color_switch + 1
            Else
                color_switch = 0
                color_use = color_1
            End If
                
            
            
        Else
            
        End If
        If (Worksheets("operui").Cells(row, colIterQ).Interior.Color <> color_use) Then
            Worksheets("operui").Cells(row, colIterQ).Interior.Color = color_use
        End If
        If (Worksheets("operui").Cells(2, colIterQ).Interior.Color <> color_use) Then
            Worksheets("operui").Cells(2, colIterQ).Interior.Color = color_use
        End If
        If Worksheets("operui").Cells(1, colIterQ).Interior.Color <> color_use Then
            Worksheets("operui").Cells(1, colIterQ).Interior.Color = color_use
        End If

        For codeRowIter = 1 To lastRow
            code_colName = Worksheets(code_sheet_name).Cells(codeRowIter, 1)

            If (InStr(operui_colName, code_colName)) Then
                Worksheets("operui").Cells(row, colIterQ) = Worksheets(code_sheet_name).Cells(codeRowIter, colIndex)
                cell_update = 1
                If Worksheets("operui").Cells(1, colIterQ) = "" Then
                    Worksheets("operui").Cells(1, colIterQ) = Worksheets(code_sheet_name).Cells(2, colIndex)

                End If
                colIndex = colIndex + 1
                Exit For
            End If
            
        Next
        If (cell_update = 0) Then
            Worksheets("operui").Cells(row, colIterQ) = ""
        End If

        
    Else
        If lastRowCol <> "" Then
            '
            If (Worksheets("operui").Cells(row, colIterQ).Interior.Color <> color_use) Then
                Worksheets("operui").Cells(row, colIterQ).Interior.Color = color_use
            End If
            If (Worksheets("operui").Cells(2, colIterQ).Interior.Color <> color_use) Then
                Worksheets("operui").Cells(2, colIterQ).Interior.Color = color_use
            End If
            If Worksheets("operui").Cells(1, colIterQ).Interior.Color <> color_use Then
                Worksheets("operui").Cells(1, colIterQ).Interior.Color = color_use
            End If
            
            For codeRowIter = 1 To lastRow
                code_colName = Worksheets(code_sheet_name).Cells(codeRowIter, 1)
                If (InStr(lastRowCol, code_colName)) Then
                    Worksheets("operui").Cells(row, colIterQ) = Worksheets(code_sheet_name).Cells(codeRowIter, colIndex)
                    cell_update = 1

                    If Worksheets("operui").Cells(1, colIterQ) = "" Then
                        Worksheets("operui").Cells(1, colIterQ) = Worksheets(code_sheet_name).Cells(2, colIndex)
                    End If
                    colIndex = colIndex + 1
         
                    Exit For
                End If
                
            Next
            If (cell_update = 0) Then
                Worksheets("operui").Cells(row, colIterQ) = ""
            End If
            
        End If
        
    End If
Next
'

'For colIter = startCol To maxcoulmn
'    Worksheets("operui").Cells(row, colIter) = ""
'    operui_colName = Worksheets("operui").Cells(2, colIter)
'    If operui_colName = "split" Then
'        startYCol = colIter + 1
'        Exit For
'    Else
'
'        For codeRowIter = 1 To lastRow
'            code_colName = Worksheets(code_sheet_name).Cells(codeRowIter, 1)
'            If (InStr(operui_colName, code_colName)) Then
'                Worksheets("operui").Cells(row, colIter) = Worksheets(code_sheet_name).Cells(codeRowIter, 2)
'                If Worksheets("operui").Cells(1, colIter) = "" Then
'                    Worksheets("operui").Cells(1, colIter) = Worksheets(code_sheet_name).Cells(2, 2)
'                End If
'                Exit For
'            End If
'
'        Next
'    End If
'Next
If isDeleteSheet = 1 Then
    Application.DisplayAlerts = False
    Worksheets(code_sheet_name).Delete
    Application.DisplayAlerts = True
End If

'year report
'color set
color_0 = RGB(163, 223, 192)
color_1 = RGB(163, 160, 224)
color_use = color_0
typeQ = "year"
Dim year_all As String
year_all = code & "(" & name & "_" & typeQ & "_all)"
csvFileName = pathBase & year_all & ".csv"
'Call WriteSheet(code, csvFileName, 0, 0)
code_sheet_name = year_all
IsExit (code_sheet_name)
Worksheets(code_sheet_name).UsedRange.ClearContents
Call WriteSheetXlsx(code_sheet_name, csvFileName, year_all, "$A$1")
'get column's name until split
startCol = 6 'first col of quarter
lastRow = Worksheets(code_sheet_name).Cells(Rows.count, 1).End(xlUp).row
lastRowCol = ""
colIndex = 2
color_switch = 0
cell_update = 0 '
For colIter = startYCol To maxcoulmn
    operui_colName = Worksheets("operui").Cells(2, colIter)
    'Worksheets("operui").Cells(row, colIter) = ""
    cell_update = 0
    If operui_colName <> "" Then
        
        If lastRowCol <> operui_colName Then
            lastRowCol = operui_colName
            colIndex = 2
            
            If color_switch = 0 Then
              color_use = color_0
              color_switch = color_switch + 1
            Else
                color_switch = 0
                color_use = color_1
            End If
                
            
            
        Else
            
        End If
        If (Worksheets("operui").Cells(row, colIter).Interior.Color <> color_use) Then
            Worksheets("operui").Cells(row, colIter).Interior.Color = color_use
        End If
        If (Worksheets("operui").Cells(2, colIter).Interior.Color <> color_use) Then
            Worksheets("operui").Cells(2, colIter).Interior.Color = color_use
        End If
        If Worksheets("operui").Cells(1, colIter).Interior.Color <> color_use Then
            Worksheets("operui").Cells(1, colIter).Interior.Color = color_use
        End If

        For codeRowIter = 1 To lastRow
            code_colName = Worksheets(code_sheet_name).Cells(codeRowIter, 1)

            If (InStr(operui_colName, code_colName)) Then
                Worksheets("operui").Cells(row, colIter) = Worksheets(code_sheet_name).Cells(codeRowIter, colIndex)
                cell_update = 1
'                Worksheets("operui").Cells(row, colIter).Interior.Color = color_use
'                Worksheets("operui").Cells(2, colIter).Interior.Color = color_use
                If Worksheets("operui").Cells(1, colIter) = "" Then
                    Worksheets("operui").Cells(1, colIter) = Worksheets(code_sheet_name).Cells(2, colIndex)
'                    Worksheets("operui").Cells(1, colIter).Interior.Color = color_use
                End If
                colIndex = colIndex + 1
                Exit For
            End If
            
        Next
        If (cell_update = 0) Then
            Worksheets("operui").Cells(row, colIter) = ""
        End If

        
    Else
        If lastRowCol <> "" Then
            '
            If (Worksheets("operui").Cells(row, colIter).Interior.Color <> color_use) Then
                Worksheets("operui").Cells(row, colIter).Interior.Color = color_use
            End If
            If (Worksheets("operui").Cells(2, colIter).Interior.Color <> color_use) Then
                Worksheets("operui").Cells(2, colIter).Interior.Color = color_use
            End If
            If Worksheets("operui").Cells(1, colIter).Interior.Color <> color_use Then
                Worksheets("operui").Cells(1, colIter).Interior.Color = color_use
            End If
            
            For codeRowIter = 1 To lastRow
                code_colName = Worksheets(code_sheet_name).Cells(codeRowIter, 1)
'                Worksheets("operui").Cells(row, colIter).Interior.Color = color_use
'                Worksheets("operui").Cells(2, colIter).Interior.Color = color_use
'                Worksheets("operui").Cells(1, colIter).Interior.Color = color_use
                If (InStr(lastRowCol, code_colName)) Then
                    Worksheets("operui").Cells(row, colIter) = Worksheets(code_sheet_name).Cells(codeRowIter, colIndex)
                    cell_update = 1
'                    Worksheets("operui").Cells(row, colIter).Interior.Color = color_use
'                    Worksheets("operui").Cells(2, colIter).Interior.Color = color_use
                    If Worksheets("operui").Cells(1, colIter) = "" Then
                        Worksheets("operui").Cells(1, colIter) = Worksheets(code_sheet_name).Cells(2, colIndex)
'                        Worksheets("operui").Cells(1, colIter).Interior.Color = color_use
                    End If
                    colIndex = colIndex + 1
         
                    Exit For
                End If
                
            Next
            If (cell_update = 0) Then
                Worksheets("operui").Cells(row, colIter) = ""
            End If
            
        End If
        
    End If
    
Next
If isDeleteSheet = 1 Then
    Application.DisplayAlerts = False
    Worksheets(code_sheet_name).Delete
    Application.DisplayAlerts = True
End If

'
'Next

End Sub
Public Function SetCellValuesLastRow(srcSheetName As String, col As String, destinRow As Integer, destinCol As String)
'col = "MP"
lastRow = Worksheets(srcSheetName).Cells(Rows.count, col).End(xlUp).row
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
        Sheets.Add after:=Sheets(Sheets.count) '添加sheet
        ActiveSheet.name = code
        Set sX = ActiveSheet
        Worksheets("OperUI").Activate '#
    End If
    Set d = Nothing
 
End Sub
Public Function GetIndustryInSheet(code) As String
'判断code的sheet是否存在
stock_sheet_name = "stock"
Dim d, sh As Worksheet, s$
Dim sX As Worksheet
    industry = ""
    Set d = CreateObject("Scripting.Dictionary")
    For Each sh In Worksheets
       d(sh.name) = ""
    Next
   If d.exists(stock_sheet_name) Then
        lastRow = Worksheets(stock_sheet_name).Cells(Rows.count, 1).End(xlUp).row
        For RowIndex = 2 To lastRow
            curCode = Worksheets(stock_sheet_name).Cells(RowIndex, 1)
            curCode = Format$(curCode, "000000")
            If code = curCode Then
               industry = Worksheets(stock_sheet_name).Cells(RowIndex, 3)
               Exit For
               
            End If
        Next
       
    Else

    End If
    Set d = Nothing
    GetIndustryInSheet = industry
End Function
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
