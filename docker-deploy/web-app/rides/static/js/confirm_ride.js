async function confirmRide(rideId) {
  try {
    const response = await (
      await fetch(`/driver/confirmed_ride/${rideId}`, {
        headers: {
          // "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        method: "POST",
        mode: "same-origin",
      })
    ).json();

    console.log("Success:", response);
       location.reload();
  } catch (error) {
    console.log(error);
  }
}
async function completeRide(rideId) {
  try {
    const response = await (
      await fetch(`/driver/complete_ride/${rideId}`, {
        headers: {
          // "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        method: "POST",
        mode: "same-origin",
      })
    ).json();

    console.log("Success:", response);
       location.reload();
  } catch (error) {
    console.log(error);
  }
}

