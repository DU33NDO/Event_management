const urlParams = new URLSearchParams(window.location.search);
const eventId = urlParams.get("event_id");

fetch(`http://localhost:5000/events/${eventId}`)
  .then((response) => response.json())
  .then((eventData) => {
    updateEventDetails(eventData);
    CountDownTimer(eventData.date_of_event_start, 'days_timer', 'hours_timer', 'min_timer', 'sec_timer', 'title_for_countdown');
  })
  .catch((error) => console.error("Ошибка загрузки event:", error));

function updateEventDetails(eventData) {
  const placeForPoster = document.querySelector(".poster_photo");
  const placeForPrice = document.querySelector(".price_for_ticket");
  const placeForDate = document.querySelector(".date_of_event");
  const placeForTime = document.querySelector(".time_for_event");
  const placeForTitle = document.querySelector(".title_event_fetch");
  const placeForDescription = document.querySelector(".description_for_event");
  const placeForPriceBox = document.querySelector(".ticket_price_fetch");
  const placeForDateBox = document.querySelector(".date_event_fetch");
  const placeForAddress = document.querySelector(".location_fetch");

  placeForPoster.src = eventData.poster_url;
  placeForPrice.textContent = eventData.price_for_ticket + ' тенге';
  placeForDateBox.textContent = formatDate(eventData.date_of_event_start);
  placeForTitle.textContent = eventData.name;
  placeForTime.textContent = formatTime(eventData.date_of_event_start, eventData.date_of_event_end);
  placeForDescription.textContent = eventData.description;
  placeForPriceBox.textContent = eventData.price_for_ticket + ' тенге';
  placeForDateBox.textContent = formatDate(eventData.date_of_event_start)+ ' - ' + formatDate(eventData.date_of_event_end);
  placeForAddress.textContent = eventData.address;

}
function formatDate(dateString) {
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  const date = new Date(dateString);
  return date.toLocaleDateString('ru-RU', options);
}

function formatTime(startString, endString) {
  const startDate = new Date(startString);
  const endDate = new Date(endString);

  const startHours = startDate.getHours().toString().padStart(2, '0');
  const startMinutes = startDate.getMinutes().toString().padStart(2, '0');
  const endHours = endDate.getHours().toString().padStart(2, '0');
  const endMinutes = endDate.getMinutes().toString().padStart(2, '0');

  return `${startHours}:${startMinutes} - ${endHours}:${endMinutes}`;
}
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
