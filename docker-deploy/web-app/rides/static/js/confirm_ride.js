async function confirmRide(rideId) {
    try {
        const confirmBtn = document.getElementById(`confirm-button-${rideId}`);
        console.log(confirmBtn)
        // return
        const spinnerBtn = document.getElementById(`spinner-button-${rideId}`);
        confirmBtn.classList.add("d-none");
        spinnerBtn.classList.remove("d-none");
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
        if (response) {
            spinnerBtn.classList.add("d-none");
        }

        console.log("Success:", response);
        location.reload();
    } catch (error) {
        console.log(error);
        location.reload();
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
        location.reload();
    }
}

