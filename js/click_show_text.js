var a_idx = 0;
jQuery(document).ready(function($) {
  $("body").click(function(e) {
    var a = new Array(
      "你是谁——", "要做什么！？", "为什么？", "——我是谁？",
      "是这样吗", "是哪样吗", "原来如此", "是这样啊", "不清楚欸",
      "没有吗", "不可以", "可以吗？", "不行！", "做不到啊……",
      "下雨了", "好冷", "好困", "好饿", "可以吧，", "好像是？", 
      "也许吧", "可能是吧", "大概是？", "不是吗", "不知道啊",
      "唔……", "啊，我想到了", "嗯？", "什么", "啧啧",
    );
    var $i = $("<span/>").text(a[a_idx]);
    a_idx = (a_idx + 1) % a.length;
    var x = e.pageX, y = e.pageY;
    $i.css({
      "z-index": 5,
      "top": y - 20,
      "left": x,
      "position": "absolute",
      "font-weight": "bold",
      "color": "#5DAFE6"
    });
    $("body").append($i);
    $i.animate({
      "top": y - 180,
      "opacity": 0
    },
		3000,
		function() { $i.remove(); });
  });
  setTimeout('delay()', 3000);
});

function delay() {
  $(".buryit").removeAttr("onclick");
}