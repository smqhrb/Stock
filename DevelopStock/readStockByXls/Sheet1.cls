VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "Sheet1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Private Sub Worksheet_Change(ByVal Target As Range)
   Dim url As String
   Dim row As Integer
   Dim code As String
   
    If Target.Column = 1 Then
        row = Target.row
    
        If row < 2 Then
            Exit Sub
        End If
        code = Sheet1.Cells(row, 1).Value
        If code <> "" Then
                'url = "http://hq.sinajs.cn/list=sh" & code
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
    Set d = CreateObject("Scripting.Dictionary")
    For j = 2 To Sheets.Count
        code1 = Sheets(j).Name
        flag = False
        For i = 3 To Sheet1.UsedRange.Rows.Count
            code = Sheet1.Cells(i, 1)
            If code1 = code Then
              flag = True
              Exit For
            End If
            
        Next
        If flag = False Then
            d.Add code1, 1
        End If
    Next
    For Each x In d.keys
     code = x
     Application.DisplayAlerts = False
     Sheets(code).Delete
    Next



End Sub

Private Sub Worksheet_SelectionChange(ByVal Target As Range)
 Call GetSheet(Target.row, Target.Column)
 
 
End Sub

