const innerBox = document.querySelector(".inner_box_for_purchase");
const urlParams = new URLSearchParams(window.location.search);
const eventId = urlParams.get("event_id");
function getTicketById(event_id) {
  fetch(`http://localhost:5000/purchase/${event_id}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
  })
    .then((response) => {
      return response.json();
    })
    .then((answer) => {
      if (answer.length === 0) {
        const soldOutMessage = document.createElement("div");
        soldOutMessage.classList.add('sold_out_message')
        soldOutMessage.textContent = "Все билеты проданы";
        innerBox.appendChild(soldOutMessage);
      } else {
        answer.forEach((element) => {
          console.log(answer);
          const blockForTicket = document.createElement("div");

          blockForTicket.classList.add("block_for_ticket");
          blockForTicket.textContent = element.ticket_id;
          if (element.is_purchased === false) {
            blockForTicket.style.backgroundColor = "gray";
          } else {
            blockForTicket.style.backgroundColor = "red";
          }
          innerBox.appendChild(blockForTicket);
          blockForTicket.addEventListener("click", () => {
            checkLoggedIn().then((response) => {
              if (!response.logged_in) {
                alert(
                  "Вы не авторизованы. Пожалуйста, войдите, чтобы купить билет."
                );
              } else {
                const confirmPurchase = confirm(
                  "Вы уверены, что хотите купить этот билет?"
                );
                if (confirmPurchase) {
                  blockForTicket.style.backgroundColor = "green";
                }
              }
            });
          });
        });
      }
    });
}

function checkLoggedIn() {
  return fetch("http://localhost:5000/is_logged_in", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
  }).then((response) => response.json());
}

window.onload = getTicketById(eventId);
