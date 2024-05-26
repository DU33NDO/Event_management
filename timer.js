const urlParams = new URLSearchParams(window.location.search);
const eventId = urlParams.get("event_id");

fetch(`http://localhost:5000/events/${eventId}`)
  .then((response) => response.json())
  .then((eventData) => {

  })

    function CountDownTimer(dt, id_days, id_hours, id_min, id_sec, id_title)
    {
        var end = new Date(dt);

        var _second = 1000;
        var _minute = _second * 60;
        var _hour = _minute * 60;
        var _day = _hour * 24;
        var timer;

        function showRemaining() {
            var now = new Date();
            var distance = end - now;
            if (distance < 0) {

                clearInterval(timer);
                document.getElementById(id_title).innerHTML = 'Уже прошел!';

                return;
            }
            var days = Math.floor(distance / _day);
            var hours = Math.floor((distance % _day) / _hour);
            var minutes = Math.floor((distance % _hour) / _minute);
            var seconds = Math.floor((distance % _minute) / _second);

            document.getElementById(id_days).innerHTML = '';
            document.getElementById(id_hours).innerHTML = '';
            document.getElementById(id_min).innerHTML = '';
            document.getElementById(id_sec).innerHTML = '';

            document.getElementById(id_days).innerHTML = days;
            document.getElementById(id_hours).innerHTML += hours;
            document.getElementById(id_min).innerHTML += minutes;
            document.getElementById(id_sec).innerHTML += seconds;
        }

        timer = setInterval(showRemaining, 1000);
    }
