function createXhr(){
    var xhr = null;
    if(window.XMLHttpRequest){
        xhr = new XMLHttpRequest();
    }else{
        xhr = new ActiveXObject("Microsoft.XMLHTTP");
    }
    return xhr;
};


function showbook(books) {
    console.log(books.length);
    b_type = $("#book_type").val()
    $.each(books, function (i, obj) {
        var html = '';
        html += "<a href=\"" + obj.url + '\"><img src=\"' + "../static/images/" + b_type + '/' + obj.img_name + "\"> </a>";
        show_img = ".show_img:eq(" + i + ")";
        $(show_img).html(html);    //  图片和网址
        show_info = ".show_info:eq(" + i + ")";
        ul_html = "";
        ul_html += "<li>" + obj.r_name;
        if (obj.t_name) {
            ul_html += ":" + obj.t_name
        };
        ul_html += "</li><li>" + obj.info + "</li><li>评分:" + obj.score + "</li><li><span>" + obj.nums + "</span>人评价</li>";
        ul_html += "<li>&lt;描述&gt;<label>" + obj.ds + "</label></li>";
        $(show_info).html(ul_html);  //信息
        if (i > 29) {
            return;
        }
    });
    if(books.length<30){
        for(var i = books.length-1;i<30;i++){
            var info_html = "#info:eq("+ i +")";
            $(info_html).html("");
        };
    }
};




$(function (){
    $('.show_img img').css({"title":"点击了解详情"});
    var arr = ['小说', '外国文学', '文学', '随笔', '中国文学', '经典', '日本文学', '散文',
        '村上春树', '诗歌', '童话', '儿童文学', '古典文学', '名著', '王小波', '杂文', '余华',
        '张爱玲', '当代文学', '钱钟书', '外国名著', '鲁迅', '诗词', '茨威格', '米兰·昆德拉',
        '杜拉斯', '港台'];
        var html = '';
    $.each(arr,function(i,obj){
        html +=  "<option value=" + obj +">" + obj + "</option>";
        });
    $("#book_type").html(html);
// ---------------------------------------
    $("#variety").change(function(){
    if($("#variety").val()=="流行"){
        var arr = ['漫画', '推理', '绘本', '青春', '东野圭吾', '科幻', '悬疑', '言情', '奇幻', '武侠',
        '日本漫画', '推理小说', '韩寒', '耽美', '亦舒', '网络小说', '三毛', '安妮宝贝',
        '阿加莎·克里斯蒂', '科幻小说', '金庸', '穿越', '郭敬明', '轻小说', '青春文学', '魔幻',
        '几米', '幾米', '张小娴', 'J.K.罗琳', '古龙', '高木直子', '沧月', '校园', '落落', '张悦然']
    }else if($("#variety").val()=="文化"){
        var arr = ['历史', '心理学', '哲学', '传记', '文化', '社会学', '艺术', '社会', '设计', '政治', '建筑',
        '宗教', '电影', '政治学', '数学', '中国历史', '回忆录', '思想', '国学', '人物传记', '人文',
        '音乐', '艺术史', '绘画', '戏剧', '西方哲学', '二战', '军事', '佛教', '近代史', '考古', '自由主义', '美术']
    }else if($("#variety").val()=="生活"){
        var arr = ['爱情', '旅行', '成长', '生活', '心理', '励志', '女性', '摄影', '教育', '职场', '美食', '游记', '灵修',
        '健康', '情感', '两性', '人际关系', '手工', '养生', '家居', '自助游']
    }else if($("#variety").val()=="经管"){
        var arr = ['经济学', '管理', '经济', '商业', '金融', '投资', '营销', '理财', '创业', '广告',
        '股票', '企业史', '策划']
    }else if($("#variety").val()=="科技"){
        var arr = ['科普', '互联网', '编程', '科学', '交互设计', '用户体验', '算法', '科技', 'web', 'UE', '交互',
        '通信', 'UCD', '神经网络', '程序']
    }else{
        var arr = ['小说', '外国文学', '文学', '随笔', '中国文学', '经典', '日本文学', '散文',
        '村上春树', '诗歌', '童话', '儿童文学', '古典文学', '名著', '王小波', '杂文', '余华',
        '张爱玲', '当代文学', '钱钟书', '外国名著', '鲁迅', '诗词', '茨威格', '米兰·昆德拉',
        '杜拉斯', '港台']
    }
    var html = '';
    $.each(arr,function(i,obj){
        html +=  "<option value=" + obj +">" + obj + "</option>";
    });
    $("#book_type").html(html);

    b_type = $("#book_type").val();  //
    var params = {'book_type': b_type};
    $.post('/book', params, function (books) {
        showbook(books);
        $("div .book_N").text(1);
        $('.bar>span>a:first').css({"color":"#fa00aa",});
        $('.bar>span>a:eq(1)').css({"color":"blue",});
        $('.bar>span>a:eq(2)').css({"color":"blue",});
    }, "json");

    });

// ---------------------------

    $('.bar>span>a:eq(0)').css({"color":"#fa00aa",});    //综合排序
    $('.bar>span>a:first').click(function(){                //综合排序
        $('.bar>span>a:first').css({"color":"#fa00aa",});
        $('.bar>span>a:eq(1)').css({"color":"blue",});
        $('.bar>span>a:eq(2)').css({"color":"blue",});
        b_type = $("#book_type").val();
        var params = {'book_type': b_type};
        $.post('/book', params, function (books) {
            showbook(books);
            $("div .book_N").text(1);
        }, "json");
    });
    $('.bar>span>a:eq(1)').click(function(){                //评分排序
        $('.bar>span>a:eq(1)').css({"color":"#fa00aa",});
        $('.bar>span>a:eq(0)').css({"color":"blue",});
        $('.bar>span>a:eq(2)').css({"color":"blue",});
        b_type = $("#book_type").val();
        $("[name='book_T']").val('S')
        $.get('/book_TN?T=S&b_type='+b_type, function (books) {
            showbook(books);
            $("div .book_N").text(1);
        }, "json");
    });
    $('.bar>span>a:last').click(function(){            //评论人数排序
        $('.bar>span>a:last').css({"color":"#fa00aa",});
        $('.bar>span>a:eq(0)').css({"color":"blue",});
        $('.bar>span>a:eq(1)').css({"color":"blue",});
        b_type = $("#book_type").val();
        $("[name='book_T']").val('C')
        $.get('/book_TN?T=C&b_type='+b_type, function (books) {
            showbook(books);
            $("div .book_N").text(1);
        }, "json");
    });
// ---------------------------
    $("#book_type").change(function () {
        b_type = $(this).val();
        var params = {'book_type': b_type};
        $.post('/book', params, function (books) {
            showbook(books);
            $("div .book_N").text(1);
        }, "json");
    });

    $("#previous").click(function () {
        var b_type = $("#book_type").val();
        var book_N = $("div .book_N").text();
        if(book_N==1){
            return;
        };
        var st = $(".book_T").val();
        book_N = Number(book_N)-1
        var params = {'book_type': b_type,'pape':'previous','book_N':book_N,'st':st};
        $.post('/book_TN', params, function (books) {
            showbook(books);
            $("div .book_N").text(book_N);
    }, "json");
    });

    $("#nextpapg").click(function () {
        var b_type = $("#book_type").val();
        var book_N = $(".book_N").text();
        var st = $(".book_T").val();
        book_N = Number(book_N)+1
        var params = {'book_type':b_type,'pape':'nextpapg','book_N':book_N,'st':st};
        $.post('/book_TN',params,function (books){
            showbook(books);
            $(".book_N").text(book_N);
            if(!books){
                return;
            };
        }, "json")
    });




    // console.log($("[name='book_T']").val()) //类型type
    // $("[name='book_N']").val()  //页数pagination
    //$obj.append($new)


    // $("#book_type").change(function () {
    //      b_type = $(this).val();
    //      var params = {'book_type':b_type};
    //      $.post('/',params,function(books){
    //          $.each(books,function (i,obj) {
    //              var html = '';
    //              html += "<a href=\"" + obj.url + '\"><img src=\"' + "../static/images/"+b_type+'/' + obj.img_name+ "\"> </a>";
    //              show_img = ".show_img:eq(" + i + ")";
    //              $(show_img).html(html);    //  图片和网址
    //              show_info = ".show_info:eq(" + i + ")";
    //              ul_html = "";
    //              ul_html += "<li>" + obj.r_name;
    //              if(obj.t_name){
    //                  ul_html += ":" + obj.t_name
    //              };
    //              ul_html += "</li><li>" + obj.info +"</li><li>评分:" +obj.score+ "</li><li><span>"+obj.nums+"</span>人评价</li>";
    //              ul_html += "<li>&lt;描述&gt;<label>" + obj.ds+"</label></li>";
    //              console.log(ul_html);
    //              $(show_info).html(ul_html);
    //              if(i>29){
    //                  return;
    //              }
    //          });
    //      },"json");
    // });


});



