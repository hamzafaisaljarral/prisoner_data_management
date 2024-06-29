var jwt = localStorage.getItem("jwt");
if (jwt != null) {
  window.location.href = "./prisoner";
}

function login() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const xhttp = new XMLHttpRequest();
  xhttp.open("POST", "http://127.0.0.1:5000/api/login");
  xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhttp.send(
    JSON.stringify({
      username: username,
      password: password,
    })
  );
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4) {
      if (this.status == 200) {
        const response = JSON.parse(this.responseText);
        localStorage.setItem("accessToken", response["access_token"]);
        localStorage.setItem("refreshToken", response["refresh_token"]);
        Swal.fire({
          text: response["username"],
          icon: "success",
          confirmButtonText: "OK",
        }).then((result) => {
          if (result.isConfirmed) {
            window.location.href = "./prisoner";
          }
        });
      } else {
        Swal.fire({
          text: "Login failed. Please check your credentials.",
          icon: "error",
          confirmButtonText: "OK",
        });
      }
    }
  };
  return false;
}
