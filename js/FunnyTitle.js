let OriginTitle = document.title;
let title_timer;
document.addEventListener('visibilitychange', function () {
  if (document.hidden) {
    // $('[rel="icon"]').attr('href', "/img/favicon.ico");
    document.title = 'ヽ(●-`Д´-)ノ你丑你就走！';
    clearTimeout(title_timer);
  }
  else {
    // $('[rel="icon"]').attr('href', "/img/favicon.ico");
    document.title = 'ヾ(Ő∀Ő3)ノ你帅就回来！' + OriginTitle;
    title_timer = setTimeout(function () {
      document.title = OriginTitle;
    }, 1500);
  }
});