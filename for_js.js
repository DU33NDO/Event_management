let eventAPI = "http://localhost:5000/events";
const box_for_fetch = document.querySelector(".box_for_all_fetched_blocks");
const all_types_of_event = document.querySelector(".categories_for_events");

const selected_type_all = document.querySelector("#each_event_category_all");
const selected_type_entertainment = document.querySelector(
  "#each_event_category_entertainment"
);
const selected_type_art = document.querySelector("#each_event_category_art");
const selected_type_education = document.querySelector(
  "#each_event_category_study"
);

const button_next = document.querySelector(".next_values");
function mainFetch() {
  fetch(eventAPI)
    .then((response) => response.json())
    .then((answer) => {
      console.log(answer);
      answer.forEach((element) => {
        const outside_box_event = document.createElement("div");
        const left_part_of_event = document.createElement("div");
        const right_part_of_event = document.createElement("div");
        const poster_image = document.createElement("img");
        const inner_text_of_right_part = document.createElement("div");
        const event_name_in_event_listing = document.createElement("p");
        const box_for_details = document.createElement("div");
        const block_outer_info_date = document.createElement("div");
        const mini_info_date = document.createElement("p");
        const block_outer_info_time = document.createElement("div");
        const mini_info_time = document.createElement("p");
        const block_outer_info_address = document.createElement("div");
        const mini_info_address = document.createElement("p");
        const description_of_event_listing = document.createElement("p");
        const last_row_for_listing = document.createElement("div");
        const button_to_book_in_listing = document.createElement("button");
        const price_for_ticket = document.createElement("p");
        const fa_icon_calendar = document.createElement("i");
        const fa_icon_clock = document.createElement("i");
        const fa_icon_location = document.createElement("i");
        const fa_icon_calendar_to_buy = document.createElement("i");

        outside_box_event.classList.add("outside_box_event");
        left_part_of_event.classList.add("left_part_of_event");
        right_part_of_event.classList.add("right_part_of_event");
        inner_text_of_right_part.classList.add("inner_text_of_right_part");
        poster_image.classList.add("event_photo_for_listing");
        event_name_in_event_listing.classList.add(
          "event_name_in_event_listing"
        );
        box_for_details.classList.add("box_for_details");
        block_outer_info_date.classList.add("block_outer_info");
        mini_info_date.classList.add("mini_info");
        block_outer_info_time.classList.add("block_outer_info");
        mini_info_time.classList.add("mini_info");
        block_outer_info_address.classList.add("block_outer_info");
        mini_info_address.classList.add("mini_info");
        description_of_event_listing.classList.add(
          "description_of_event_listing"
        );
        last_row_for_listing.classList.add("last_row_for_listing");
        button_to_book_in_listing.classList.add("button_to_book_in_listing");
        price_for_ticket.classList.add("price_for_ticket");
        fa_icon_calendar.classList.add("fa-solid", "fa-calendar-days");
        fa_icon_clock.classList.add("fa-regular", "fa-clock");
        fa_icon_location.classList.add("fa-solid", "fa-location-dot");
        fa_icon_calendar_to_buy.classList.add("fa-regular", "fa-calendar");

        const startDate = new Date(element.date_of_event_start);
        const endDate = new Date(element.date_of_event_end);

        const options = { year: "numeric", month: "long", day: "numeric" };
        const startDateFormatted = startDate.toLocaleDateString(
          "ru-RU",
          options
        );

        const endDateFormatted = endDate.toLocaleDateString("ru-RU", options);

        const duration = endDate - startDate;
        const durationHours = Math.floor(duration / (1000 * 60 * 60));
        const durationDays = Math.floor(duration / (1000 * 60 * 60 * 24));
        if (durationDays === 0) {
          mini_info_time.textContent = `Длительность: ${durationHours} часов`;
        } else {
          mini_info_time.textContent = `Длительность: ${durationDays} дней`;
        }

        button_to_book_in_listing.textContent = "Забронировать";
        poster_image.src = element.poster_url;
        event_name_in_event_listing.textContent = element.name;
        mini_info_date.textContent = `Начало: ${startDateFormatted} - Конец: ${endDateFormatted}`;
        mini_info_address.textContent = element.address;
        description_of_event_listing.textContent =
          element.description.substring(0, 100) + "...";
        price_for_ticket.textContent = `${element.price_for_ticket} тенге`;

        outside_box_event.onclick = function () {
          redirectToEventDetails(element.event_id);
        };
        box_for_fetch.appendChild(outside_box_event);

        outside_box_event.appendChild(left_part_of_event);
        left_part_of_event.appendChild(poster_image);
        outside_box_event.appendChild(right_part_of_event);
        right_part_of_event.appendChild(inner_text_of_right_part);
        inner_text_of_right_part.appendChild(event_name_in_event_listing);
        inner_text_of_right_part.appendChild(box_for_details);

        box_for_details.appendChild(block_outer_info_date);
        block_outer_info_date.appendChild(mini_info_date);
        block_outer_info_date.appendChild(fa_icon_calendar);

        box_for_details.appendChild(block_outer_info_time);
        block_outer_info_time.appendChild(mini_info_time);
        block_outer_info_time.appendChild(fa_icon_clock);

        box_for_details.appendChild(block_outer_info_address);
        block_outer_info_address.appendChild(mini_info_address);
        block_outer_info_address.appendChild(fa_icon_location);

        inner_text_of_right_part.appendChild(description_of_event_listing);
        inner_text_of_right_part.appendChild(last_row_for_listing);
        last_row_for_listing.appendChild(button_to_book_in_listing);
        last_row_for_listing.appendChild(fa_icon_calendar_to_buy);
        last_row_for_listing.appendChild(price_for_ticket);
      });
    });
}

function redirectToEventDetails(eventId) {
  window.location.href = `event_details.html?event_id=${eventId}`;
}

selected_type_all.addEventListener("click", function () {
  eventAPI = "http://localhost:5000/events";
  box_for_fetch.innerHTML = "";
  mainFetch();
});

selected_type_entertainment.addEventListener("click", function () {
  eventAPI = "http://localhost:5000/events/entertainment";
  box_for_fetch.innerHTML = "";
  mainFetch();
});

selected_type_art.addEventListener("click", function () {
  eventAPI = "http://localhost:5000/events/art";
  box_for_fetch.innerHTML = "";
  mainFetch();
});

selected_type_education.addEventListener("click", function () {
  eventAPI = "http://localhost:5000/events/education";
  box_for_fetch.innerHTML = "";
  mainFetch();
});
window.onload = mainFetch;

button_next.addEventListener("click", function () {});
