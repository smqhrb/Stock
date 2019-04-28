Attribute VB_Name = "baseCall"
Public TimerEnabled As Boolean
Private Declare Function SetTimer Lib "user32.dll" (ByVal hwnd As Long, ByVal nIDEvent As Long, _
ByVal uElapse As Long, ByVal lpTimerFunc As Long) As Long
Private Declare Function KillTimer Lib "user32.dll" (ByVal hwnd As Long, ByVal nIDEvent As Long) As Long
Public lngTimerID As Long
Public recordUpdate As Object
'Private Declare Sub Sleep Lib "kernel32" (ByVal dwMilliseconds As Long)
Public Declare Sub Sleep Lib "kernel32" (ByVal dwMilliseconds As Long)

'Sub DownHistData()
'        For j = 2 To 5000
'          code = Sheet1.Cells(j, 1)
'          If code = "" Then
'             Return
'          End If
'          col = (j - 1) * 3
'          Call getHistPrice(Sheet2, code, col)
'        Next
'End Sub



Sub getHistPrice(sheet As Worksheet, code, col)
Dim html, i, j, tr, td, YearOld
Set html = CreateObject("htmlfile")
With CreateObject("msxml2.xmlhttp")
    .Open "GET", "http://quotes.money.163.com/trade/lsjysj_" & code & ".html", False
    .send
    html.body.innerhtml = .responsetext
    'Cells(1, 1) = .responsetext
    'sheet.Cells(1, col) = code
    i = 0
    For Each tr In html.All.tags("table")(3).Rows
        i = i + 1
        
        'For Each td In tr.Cells
        '    j = j + 1
        '    Cells(i, j) = td.innerText
        'Next
        sheet.Cells(i, col) = tr.Cells(0).innerText
       ' Cells(i, 2) = tr.Cells(1).innerText
        sheet.Cells(i, col + 1) = tr.Cells(2).innerText '最高价
        sheet.Cells(i, col + 2) = tr.Cells(3).innerText '最低价
        sheet.Cells(i, col + 3) = tr.Cells(4).innerText '收盘价
    Next
    If i > 30 Then
       Exit Sub
    End If
 End With
    'http://quotes.money.163.com/trade/lsjysj_000001.html?year=2019&season=1
    Sleep 3000
   jd = Now()
    season = DatePart("q", jd)
    If season <= 1 Then
       YearOld = Year(Now()) - 1
       season = 4
    Else
       YearOld = Year(Now())
       season = season - 1
    End If
  Set html = CreateObject("htmlfile")
  With CreateObject("msxml2.xmlhttp")
    .Open "GET", "http://quotes.money.163.com/trade/lsjysj_" & code & ".html?year=" & YearOld & "&" & "season=" & season, False
    .send
    html.body.innerhtml = .responsetext
    j = 0
    For Each tr In html.All.tags("table")(3).Rows
        
        If j = 0 Then
            j = j + 1
            
            GoTo line
        End If
        i = i + 1
        'For Each td In tr.Cells
        '    j = j + 1
        '    Cells(i, j) = td.innerText
        'Next
        sheet.Cells(i, col) = tr.Cells(0).innerText
       ' Cells(i, 2) = tr.Cells(1).innerText
        sheet.Cells(i, col + 1) = tr.Cells(2).innerText '最高价
        sheet.Cells(i, col + 2) = tr.Cells(3).innerText '最低价
        sheet.Cells(i, col + 3) = tr.Cells(4).innerText '收盘价
line:
        If i > 30 Then
          Exit For
        End If
    Next
End With

End Sub


Sub isExit(code)
Dim d, sh As Worksheet, s$
Dim sX As Worksheet

    Set d = CreateObject("Scripting.Dictionary")
    For Each sh In Worksheets
       d(sh.Name) = ""
    Next
   If d.exists(code) Then
       'If (Weekday(today(), 2) >= 6) Then '周六日
         If recordUpdate Is Nothing Then
           Set recordUpdate = CreateObject("Scripting.Dictionary")
        End If
        Set sX = Sheets(code)
        If recordUpdate(code) = 0 Then
            Call getHistPrice(sX, code, 1)
            recordUpdate(code) = 1
        End If
       'Else
        
       'End If
       
    Else
        Sheets.Add after:=Sheets(Sheets.Count)
        ActiveSheet.Name = code
        Set sX = ActiveSheet
        sX.Visible = False
        If recordUpdate Is Nothing Then
           Set recordUpdate = CreateObject("Scripting.Dictionary")
        End If
        If recordUpdate.exists(code) Then
            recordUpdate(code) = 1
        Else
            recordUpdate.Add code, 1
        End If
        Call getHistPrice(sX, code, 1)
    End If
    Set d = Nothing
End Sub
Sub addHistDataToForm(code)
'ColumnHeaders.Add , , "第" & i & "列", .Width / 8, lvwColumnCenter '从第2, lvwColumnCenter
   
   HistDataView.ListViewHist.ListItems.Clear
HistDataView.ListViewHist.ColumnHeaders.Add , , "日期", 50, lvwColumnLeft
HistDataView.ListViewHist.ColumnHeaders.Add , , "最低价", 50, lvwColumnRight
HistDataView.ListViewHist.ColumnHeaders.Add , , "最高价", 50, lvwColumnRight
HistDataView.ListViewHist.ColumnHeaders.Add , , "极限", 60, lvwColumnRight
HistDataView.ListViewHist.ColumnHeaders.Add , , "最高比", 60, lvwColumnRight
HistDataView.ListViewHist.ColumnHeaders.Add , , "高涨", 60, lvwColumnRight
HistDataView.ListViewHist.ColumnHeaders.Add , , "最低比", 60, lvwColumnRight
HistDataView.ListViewHist.ColumnHeaders.Add , , "低涨", 60, lvwColumnRight

HistDataView.ListViewHist.ColumnHeaders.Add , , "收限", 60, lvwColumnRight
HistDataView.ListViewHist.ColumnHeaders.Add , , "振幅", 60, lvwColumnRight
'HistDataView.ListViewHist.ColumnHeaders.Add , , "差距", 60
HistDataView.ListViewHist.View = lvwReport
HistDataView.ListViewHist.FullRowSelect = True
HistDataView.ListViewHist.Gridlines = True
    With Sheets(code)
    
        For i = 2 To .Cells(Rows.Count, 1).End(xlUp).row
            If i < 32 Then
             Set itm = HistDataView.ListViewHist.ListItems.Add()
                priceMax = .Cells(i, 2) '最高价
                priceMaxLast = .Cells(i + 1, 2) '最高价
                priceMin = .Cells(i, 3) '最低价
                priceMinLast = .Cells(i + 1, 3) '最低价
                priceCloseLost = .Cells(i + 1, 4) '
                priceClose = .Cells(i, 4) '
                itm.Text = .Cells(i, 1) '日期
                'itm.SubItems(1) = .Cells(i, 2) '收盘价
                'format$("10.23","0.00%") '返回值 1023.00%
'                itm.SubItems(3) = Application.Round(100 * (priceMax - priceMinLast) / priceMinLast, 2) '极值
'                itm.SubItems(4) = Application.Round(100 * (priceMax - priceMaxLast) / priceMaxLast, 2) '最高价比较
'                itm.SubItems(5) = Application.Round(100 * (priceMin - priceMinLast) / priceMinLast, 2) '最低价比较
'                itm.SubItems(6) = Application.Round(100 * (priceMin - priceCloseLost) / priceCloseLost, 2) '差距

                itm.SubItems(1) = Format$(priceMin, "0.00")
                itm.SubItems(2) = Format$(priceMax, "0.00")
                itm.SubItems(3) = Format$((priceMax - priceMinLast) / priceMinLast, "0.0%") '极限
                itm.SubItems(4) = Format$((priceMax - priceMaxLast) / priceMaxLast, "0.0%") '最高比
                itm.SubItems(5) = Format$((priceMax - priceCloseLost) / priceCloseLost, "0.0%") '高涨
                itm.SubItems(6) = Format$((priceMin - priceMinLast) / priceMinLast, "0.0%") '最低比
                itm.SubItems(7) = Format$((priceMin - priceCloseLost) / priceCloseLost, "0.0%") '低涨
                itm.SubItems(8) = Format$((priceClose - priceMinLast) / priceMinLast, "0.0%") '收限
                itm.SubItems(9) = Format$((priceMax - priceMin) / priceCloseLost, "0.0%") '振幅
            End If
        Next i
    End With
End Sub
Sub GetSheet(row, col)
Dim flag As Boolean
Dim sX As Object
Dim code As String
On Error Resume Next
   ' row = Target.row
   ' col = Target.Column
    'With ActiveWorkbook
        If col = 2 Then
            If row > 2 Then
               code = Sheet1.Cells(row, 1)
               If Len(code) <> 6 Then
                    Return
               End If
               cnt = Sheets.Count
               For i = 2 To cnt
                    
                   Set sX = Sheets(i)
                   
                   If code = sX.Name Then
                      flag = True
                      Exit For
                   End If
               Next
               If flag = True Then
                   Call getHistPrice(sX, code, 1)
               Else
                  
                   
                   If code = "" Then
                   Else
                        Sheets.Add after:=Sheets(Sheets.Count)
                        ActiveSheet.Name = code
                        ActiveSheet.Visible = False
                        Set sX = ActiveSheet
                        Call getHistPrice(sX, code, 1)
                   End If
               End If
               If code = "" Then
               Else
                addHistDataToForm (code)
               End If
               If code = "" Then
               Else
                 HistDataView.Caption = "(" & Sheet1.Cells(row, 1) & ")" & Sheet1.Cells(row, 2)
                 HistDataView.Show vbModal
               End If
            End If
            '
        End If
    'End With
    
End Sub
Public Function FillOneRow(url As String, r As Integer, code As String) As Integer
    Dim price3, price20 As Integer
    Dim Zs As Double
    Dim sX As Worksheet
    
  '  Dim cuDate As String
  '  cuDate = Date
    With CreateObject("msxml2.xmlhttp")
        .Open "GET", url, False
        .send
        sp = Split(.responsetext, "~")
        If UBound(sp) > 3 Then
            FillOneRow = 1
         
           Zs = sp(4) '昨收
           Sheet1.Cells(r, 2).Value = sp(1) '名称
           Sheet1.Cells(r, 3).Value = sp(33) '最高价
           Sheet1.Cells(r, 4).Value = sp(3) '当前价格
           Sheet1.Cells(r, 5).Value = sp(34) '最低价
           jj = Split(sp(35), "/")
           Sheet1.Cells(r, 6).Value = jj(0) '均价
           'sp(5) 开盘
           If (sp(4) > 0) Then
            Sheet1.Cells(r, 7).Value = Format$((sp(33) - sp(4)) / sp(4), "0.0%") '最高%
            Sheet1.Cells(r, 8).Value = Format$((sp(34) - sp(4)) / sp(4), "0.0%") '最低%
            Sheet1.Cells(r, 11).Value = Format$((sp(5) - sp(4)) / sp(4), "0.0%") '开盘%
           End If
           Sheet1.Cells(r, 9).Value = sp(32) '涨幅%
           Sheet1.Cells(r, 10).Value = sp(43) '振幅%
           Sheet1.Cells(r, 12).Value = sp(38) '换手%
           Sheet1.Cells(r, 13).Value = sp(10) '买量
           Sheet1.Cells(r, 14).Value = sp(20) '卖量
           Sheet1.Cells(r, 15).Value = sp(10) '封单量
           '''
           isExit (code)
           Set sX = Sheets(code)

          price3 = sX.Cells(1 + 3, 4)
          price20 = sX.Cells(1 + 20, 4)
            price_zd = sX.Cells(1 + 1, 3)
            price_zg = sX.Cells(1 + 1, 2)
            price_sp = sX.Cells(1 + 1, 4)
           If price3 > 0 Then
                Sheet1.Cells(r, 16).Value = Format$((sp(3) - price3) / price3, "0.00%") '3日涨幅
           End If
           If price20 > 0 Then
                Sheet1.Cells(r, 17).Value = Format$((sp(3) - price20) / price20, "0.00%")  '20日涨幅
           End If
           If price_zd > 0 Then
                Sheet1.Cells(r, 18).Value = Format$((sp(33) - price_zd) / price_zd, "0.0%") '极限
                Sheet1.Cells(r, 20).Value = Format$((sp(34) - price_zd) / price_zd, "0.0%") '最低比
           End If
           If price_zg > 0 Then
                Sheet1.Cells(r, 19).Value = Format$((sp(33) - price_zg) / price_zg, "0.0%") '最高比
           End If
            If price_sp > 0 Then
                Sheet1.Cells(r, 21).Value = Format$((sp(3) - price_zd) / price_zd, "0.0%") '收限
           
           End If
           ''''
           Dim zhangDie As Double
           zhangDie = sp(32)
           
               If zhangDie > 0 Then
                  '上涨使用红色
                   For i = 2 To 22
                    Sheet1.Cells(r, i).Font.Color = vbRed
    '                Sheet1.Cells(r, 3).Font.Color = vbRed
                   Next
                Else
                   For i = 2 To 22
                    '下跌使用绿色
                    Sheet1.Cells(r, i).Font.Color = &H228B22
                    'Sheet1.Cells(r, 3).Font.Color = &H228B22
                   Next
               End If
           
        Else
            FillOneRow = 0
        End If
    End With
End Function
Sub GetStockHistoryData(sheet As Worksheet, code As String)
'
'http://quotes.money.163.com/trade/lsjysj_000651.html#01b07
'
    sheet.UsedRange.ClearContents
    sheet.Name = code
    With sheet.QueryTables.Add(Connection:= _
        "URL;http://quotes.money.163.com/trade/lsjysj_" & code & ".html#01b07", Destination _
        :=Sheet3.Range("$A$1"))
        .Name = "lsjysj_" & code & ".html#01b07_1"
        .FieldNames = True
        .RowNumbers = False
        .FillAdjacentFormulas = False
        .PreserveFormatting = True
        .RefreshOnFileOpen = False
        .BackgroundQuery = True
        .RefreshStyle = xlInsertDeleteCells
        .SavePassword = False
        .SaveData = True
        .AdjustColumnWidth = True
        .RefreshPeriod = 0
        .WebSelectionType = xlSpecifiedTables
        .WebFormatting = xlWebFormattingNone
        .WebTables = "4"
        .WebPreFormattedTextToColumns = True
        .WebConsecutiveDelimitersAsOne = True
        .WebSingleBlockTextImport = False
        .WebDisableDateRecognition = False
        .WebDisableRedirections = False
        .Refresh BackgroundQuery:=False
    End With
End Sub


Sub GetData()
    Dim succeeded As Integer
    Dim url As String
    Dim row As Integer
    Dim code As String
    On Error Resume Next
    [E1] = "正在更新"
    [E1].Font.Color = vbRed
    For row = 3 To Range("A1").CurrentRegion.Rows.Count '从第二行开始
        code = Cells(row, 1).Value
        If code <> "" Then
            'url = "http://hq.sinajs.cn/list=sh" & code
            If Len(code) = 6 Then
                If code > 600000 Then
                    url = "http://qt.gtimg.cn/q=sh" & code '沪市
                    succeeded = FillOneRow(url, row, code)
                
                Else
                    url = "http://qt.gtimg.cn/q=sz" & code '深市
                    succeeded = FillOneRow(url, row, code)
                End If
                
                If succeeded = 0 Then
                    MsgBox ("获取失败")
                End If
            End If
        End If
    Next
    [E1] = ""
    'Call GetStockHistoryData(Sheet3, "000651")
End Sub

Sub StartTimer(lDuration As Long)
' 如果定时器不存在，则设置定时器，定时器触发的时间为IDuration，定时器触发后执行OnTime
If lngTimerID = 0 Then
 lngTimerID = SetTimer(0&, 0&, lDuration, AddressOf GetData)
 ' 否则停止定时器，并设置一个新的定时器
Else
  Call StopTimer
  lngTimerID = SetTimer(0&, 0&, lDuration, AddressOf GetData)
End If
End Sub
Sub period()
'ss = Application.Round(12.5678, 2)
If recordUpdate Is Nothing Then

    Set recordUpdate = CreateObject("Scripting.Dictionary")
    For i = 1 To Sheets.Count
        code = Sheets(i).Name
        recordUpdate.Add code, 0
    Next
End If
If [D1] = True Then
    tim = [C1]
    StartTimer (tim * 1000)
Else
    StopTimer
End If

End Sub
Sub StopTimer()
   KillTimer 0&, lngTimerID
End Sub
'Sub checkUpdate()
'Dim d, sh As Worksheet, s$
'Dim sX As Worksheet
'code = "config"
' Set d = CreateObject("Scripting.Dictionary")
' For Each sh In Worksheets
'    d(sh.Name) = ""
' Next
'If d.exists(code) Then
'    Set sX = Sheets(code)
'
' Else
'     Sheets.Add after:=Sheets(Sheets.Count)
'     ActiveSheet.Name = code
'     Set sX = ActiveSheet
'     sX.Visible = False
'
' End If
' Set d = Nothing
'
'End Sub


