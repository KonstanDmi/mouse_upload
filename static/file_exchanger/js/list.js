clearTimeout()
// Fancybox Configuration
$('[data-fancybox="gallery"]').fancybox({
  buttons: [
//    "slideShow",
//    "zoom",
    "fullScreen",
//    "share",
    "close"
  ],
  loop: false,
  protect: true
});

function preventLongPressContextMenu(el){
    el.ontouchstart = ignoreEvent_;
    el.ontouchmove = ignoreEvent_;
    el.ontouchend = ignoreEvent_;
    el.ontouchcancel = ignoreEvent_;
}

function getTimeRemaining(endtime) {
  var t = Date.parse(endtime) - Date.now();
  var seconds = Math.floor((t / 1000) % 60);
  var minutes = Math.floor((t / 1000 / 60) % 60);
  var hours = Math.floor((t / (1000 * 60 * 60)) % 24);
  var days = Math.floor(t / (1000 * 60 * 60 * 24));
  return {
    'total': t,
    'days': days,
    'hours': hours,
    'minutes': minutes,
    'seconds': seconds
  };
}

function initializeCountdown(id, endtime) {
  var daysSpan = $('#'+id+' .days');
  var hoursSpan = $('#'+id+' .hours');
  var minutesSpan = $('#'+id+' .minutes');
  var secondsSpan = $('#'+id+' .seconds');

  function updateClock() {
    var t = getTimeRemaining(endtime);

    daysSpan.html(t.days);
    hoursSpan.html(('0' + t.hours).slice(-2));
    minutesSpan.html(('0' + t.minutes).slice(-2));
    secondsSpan.html(('0' + t.seconds).slice(-2));

    if (t.total <= 0) {
      clearInterval(timeinterval);
    }
  }

  updateClock();
  var timeinterval = setInterval(updateClock, 1000);
}
// count down timer:

var deadline = new Date($('#count-down').attr('datetime'));
initializeCountdown('countdown', deadline);