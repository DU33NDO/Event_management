const BtnSend = document.querySelector(
  ".login__outer_box__inner_box__inputs__btn"
);

BtnSend.addEventListener("click", function () {
  const login = document.querySelector("#login").value;
  const password = document.querySelector("#password").value;

  if (login && password) {
    const user = {
      login: login,
      password: password,
    };

    fetch("http://localhost:5000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(user),
      credentials: "include",
    })
      .then((response) => response.json())
      .then((answer) => {
        if (answer.message !== "Вы вошли в аккаунт!") {
          alert(`Ошибка: ${answer.message}`);
        } else {
          alert(answer.message);
          window.location.href = "./index.html";
        }
      });
  } else {
    alert("Введите логин и пароль");
  }
});
