const rideShareRequestForm = document.getElementById("ride-share-request-form");
const ride_id = document.getElementById("ride_id");
const earliest_arrive_date = document.getElementById("earliest_arrive_date");
const latest_arrive_date = document.getElementById("latest_arrive_date");
const required_passengers_num = document.getElementById(
  "required_passengers_num"
);
// var toastNotice = document.getElementById("toast_notice"); //select id of toast
const share_request_submit_button = document.getElementById(
  "share-request-submit-button"
);

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie("csrftoken");
// console.log(csrftoken);

share_request_submit_button.addEventListener("click", (e) => {
  e.preventDefault();
  // const formData = new FormData(rideShareRequestForm);
  const formData = new FormData();
  formData.append("ride_id", ride_id.value);

  formData.append("earliest_arrive_date", earliest_arrive_date.value);
  formData.append("latest_arrive_date", latest_arrive_date.value);
  formData.append("required_passengers_num", required_passengers_num.value);

  MakeShareRequest(formData);
});

async function MakeShareRequest(formData) {
  try {
    const response = await (
      await fetch("/create_shared_request/", {
        headers: {
          // "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        method: "POST",
        mode: "same-origin",
        body: formData,
      })
    ).json();
    // console.log('asd')
    // console.log(response);

    // if (response.ok) {
    console.log("Success:", response);
    // let bsAlert = new bootstrap.Toast(toastNotice); //inizialize it
    // bsAlert.show(); //show it
    // } else {
    //   console.log("Error:", response);
    //   // createToast("invalid input, please try again. ");
    // }
    location.reload();
  } catch (error) {
    console.log(error);
  }
}

function setRideId(rideId) {
  document.getElementById("ride_id").value = rideId;
}

// function createToast(alert) {
//   //   const newToast = document.createElement("div");
//   //   newToast.innerHTML = ` <div role="alert" aria-live="assertive" aria-atomic="true" class="toast" data-bs-autohide="false">
//   //   <div class="toast-header">
//   //     <img src="..." class="rounded me-2" alt="...">
//   //     <strong class="me-auto">Ride App</strong>
//   //     <small>11 mins ago</small>
//   //     <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
//   //   </div>
//   //   <div class="toast-body">
//   //    ${alert}
//   //   </div>
//   // </div>`;
//   //   toastNotice.appendChild(newToast);
//   // console.log(true)
//   const newToast = document.querySelectorAll(".toast");
//   let bsAlert = new bootstrap.Toast(newToast); //inizialize it
//   console.log(bsAlert)
//   bsAlert.show(); //show it
//   // console.log(false)
// }
