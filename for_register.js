const BtnSend = document.querySelector(
  ".register__outer_box__inner_box__inputs__register_btn"
);
BtnSend.addEventListener("click", function () {
  const username = document.querySelector("#username").value;
  const login = document.querySelector("#login").value;
  const password = document.querySelector("#password").value;
  const r_password = document.querySelector("#r_password").value;

  if (password.length > 8 && r_password.length > 8) {
    if (password === r_password && login && username) {
      const newUser = {
        username: username,
        login: login,
        password: password,
      };

      fetch("http://localhost:5000/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newUser),
      })
        .then((response) => response.json())
        .then((answer) => {
          if (answer.message !== "Регистрация прошла успешно!") {
            alert(`Ошибка: ${answer.message}`);
          } else {
            alert(answer.message);
            window.location.href = "./login.html";
          }
        });
    } else {
      alert("ошибка: пароли не совпадают");
    }
  } else {
    alert("Пароль минумум 8 символов(");
  }
});
