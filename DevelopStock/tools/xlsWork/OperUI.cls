VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "OperUI"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Private Sub Worksheet_Change(ByVal Target As Range)
  If Target.Column = 3 Then
    row = Target.row
    If (row > 1) Then
        Dim code As String
        code = Worksheets("OperUI").Cells(row, "C").Value
        cName = WalkFolder(code)
        Worksheets("OperUI").Cells(row, "D") = cName
        industry = GetIndustryInSheet(code)
        Worksheets("OperUI").Cells(row, "E") = industry
    End If
   
  End If
End Sub

Private Sub Worksheet_SelectionChange(ByVal Target As Range)
'     If Target.Column = 3 Then
'        Dim row As Integer
'
'        row = Target.row
'        If (row > 1) Then
'            Dim code As String
'            Dim name As String
'            code = Worksheets("OperUI").Cells(row, "C").Value
'            name = Worksheets("OperUI").Cells(row, "D").Value
'            Msg = code & "(" & name & ")   是否重新下载？"
'            Style = vbYesNo + vbDefaultButton2
'            Title = "提示"
'            Help = ""
'            Ctxt = 1000
'            Response = MsgBox(Msg, Style, Title, Help, Ctxt)
'            If Response = vbYes Then    ' 用户按下“是”
'                Dim tm
'                tm = Now()
'                Call importAcount(code, name, row, 1)
'                Worksheets("operui").Cells(row, "B") = Format$(Now() - tm, "hh:mm:ss")
'
'            Else    ' 用户按下“否”
'                 Call importAcount(code, name, row, 0)
'            End If
'
'            Worksheets(code).Activate
'        End If
'    End If
End Sub
