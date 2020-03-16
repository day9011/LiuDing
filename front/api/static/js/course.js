function make_date(arr) {
    var date = "";
    arr.forEach(function(str) {
        console.log(str);
        if (Number(str) === 1) {
            if (!date) { 
                date += "星期一";
            } else {
                date += " 星期一";
            }
        }
        if (Number(str) === 2) {
            if (!date) { 
                date += "星期二";
            } else {
                date += " 星期二";
            }
        }
        if (Number(str) === 3) {
            if (!date) { 
                date += "星期三";
            } else {
                date += " 星期三";
            }
        }
        if (Number(str) === 4) {
            if (!date) { 
                date += "星期四";
            } else {
                date += " 星期四";
            }
        }
        if (Number(str) === 5) {
            if (!date) { 
                date += "星期五";
            } else {
                date += " 星期五";
            }
        }
        if (Number(str) === 6) {
            if (!date) { 
                date += "星期六";
            } else {
                date += " 星期六";
            }
        }
        if (Number(str) === 7) {
            if (!date) { 
                date += "星期日";
            } else {
                date += " 星期日";
            }
        }
    })
    return date;
}

function load_courses() {
    $.ajax({
        url: "/course/query",
        type: "HTTP",
        method: "GET",
        contentType: false,
        cache: false,
        processData: false,
        success: function(req) {
            var ret = JSON.parse(req);
            console.log(ret);
            if (Boolean(ret['status']) === true) {
                var table = $("#course_table");
                ret['courses'].forEach(function(subject) {
                    var td1 = "<td>" + String(subject['subject']) + "</td>";
                    var td2 = "<td>" + String(subject['grade']) + "</td>";
                    if (Number(subject['term']) === 0) {
                        var term = "上学期";
                    }
                    else {
                        var term = "下学期";
                    }
                    var td3 = "<td>" + term + "</td>";
                    var date = make_date(subject['date']);
                    date += ':' + subject['time'];
                    console.log(date);
                    var td4 = "<td>" + date + "</td>";
                    var td5 = "<td>" + String(subject['fee']) + "</td>";
                    var tr = "<tr>" + td1 + td2 + td3 + td4 + td5 + "</tr>";
                    table.append(tr);
                })
            }
            else {
                alert(req);
            }
        },
        error: function(){
            alert('Recognize failed');
        }
    })
}

$(function() {
    load_courses();
    M.AutoInit();
    M.updateTextFields();
});

