var testArray = [
  {
    RRYID: "039",
    ggbf: "22.0440",
    sbgl: "0",
    bzgl: "0",
    yxgl: "-0.20",
    aqgl: "-0.10"
  },
  {
    RRYID: "586",
    ggbf: "33.2670",
    sbgl: "0",
    bzgl: "0",
    yxgl: "-1.50",
    aqgl: "-0.20"
  },
  {
    RRYID: "429",
    ggbf: "10.7290",
    sbgl: "0",
    bzgl: "0",
    yxgl: "-0.20",
    aqgl: "0"
  }
];
var headArray = [];

function appendTable() {
  for (var i in testArray[0]) {
    headArray[headArray.length] = i;
  }
  for (var tableNo = 0; tableNo < testArray.length; tableNo++) {
    var table = document.createElement("table");
    var thead = document.createElement("tr");
    for (var count = 0; count < headArray.length; count++) {
      var td = document.createElement("td");
      td.innerHTML = headArray[count];
      td.id ="count"
      thead.appendChild(td)
    }
    table.appendChild(thead);
    var tbody = document.createElement("tr");
    for (var headCount = 0; headCount < headArray.length; headCount++) {
      var cell = document.createElement("td");
      cell.innerHTML = testArray[tableNo][headArray[headCount]];
      cell.id ="cell"
      tbody.appendChild(cell);
    }
    table.appendChild(tbody);
    document.body.appendChild(table);
  }
}
//dynamic create table
var data = [{
  name: "传智播客",
  url: "http://www.itcast.cn",
  type: "IT最强培训机构"
},{
  name: "黑马程序员",
  url: "http://www.itheima.com",
  type: "大学生IT培训机构"
},{
  name: "传智前端学院",
  url: "http://web.itcast.cn",
  type: "前端的黄埔军校"
}];

$(function(){
  //第一种：动态创建表格的方式，使用拼接html的方式 （推荐）
  // var html = "";
  // for( var i = 0; i < data.length; i++ ) {
  //     html += "<tr>";
  //     html +=     "<td>" + data[i].name + "</td>"
  //     html +=     "<td>" + data[i].url + "</td>"
  //     html +=     "<td>" + data[i].type + "</td>"
  //     html += "</tr>";
  // }
  // $("#J_TbData").html(html);

  //第二种： 动态创建表格的方式，使用动态创建dom对象的方式
  //清空所有的子节点
  $("#J_TbData").empty();

  //自杀
  // $("#J_TbData").remove();

  for( var i = 0; i < data.length; i++ ) {
      //动态创建一个tr行标签,并且转换成jQuery对象
      var $trTemp = $("<tr></tr>");

      //往行里面追加 td单元格
      $trTemp.append("<td>"+ data[i].name +"</td>");
      $trTemp.append("<td>"+ data[i].url +"</td>");
      $trTemp.append("<td>"+ data[i].type +"</td>");
      // $("#J_TbData").append($trTemp);
      $trTemp.appendTo("#J_TbData");
  }
});
