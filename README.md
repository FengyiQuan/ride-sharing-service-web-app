# Ride-App

Ride Sharing Service

## Danger log

- 01/26 The schema of the tables might be not enough to deal with a more real situation.

- 01/28 Password is hashed and handle by Django authentication system, which handles user accounts, groups, permissions
  and cookie-based user sessions. Session is used to store login user information to avoid request user sensitive
  information every time to prevent middle attack. Further password validation can perform in order to have better
  password strength, such as password strength checking, throttling of login attempts, authentication against
  third-parties (OAuth, for example).

- 01/28 The driver can be in the same car as customers, or in another word, it means that the driver can also find open
  rides created by themselves.

- 01/28 The user can edit their rides' details by the fields we allowed them to edit. In this way, it can prevent some
  unexpected errors.

- 01/29 Filter and pagination are implemented to reduce the workload of the server to handle to many tuples in the
  request and not show on the page properly.

- 02/01 All API implementations ensure that authentication is checked prior to processing any requests. This is done to
  verify the identity of the user or client making the API call and ensure that they have the necessary permissions to
  access the requested resources.

- 02/03 To prevent multiple driver confirm the same request at the same time, atomic state update is done by checking
  the request state is set to the specific state. Otherwise, state change will fail.

- 02/04 When designing URLs for API endpoint, it is important to minimize the exposure of sensitive information in the
  URL string, such as username, destination. This information should instead be placed in the body section of the API
  request. Exposing sensitive information in the URL can pose security risks as it can be easily intercepted or seen in
  logs, cache, and history. All sensitive information place in the body section, it is encrypted and protected from
  unauthorized access.

- 02/05 The memory for our app is limited, which means that it is possible that our app would fail if it is out of
  memory.

- 02/05 All front end design have some sort of indication that user's permission. For example, when submit confirm
  request, webpage will show spinner to indicate that request is processing and prevent multiple form submit.

- 02/05 Back-end also prevent concurrent driver confirmation, by checking if a ride is confirmed by some driver. Thus,
  prevent ride is confirmed by multiple driver.

- 02/05 Editing ride information needed to make sure that new information not complicated with other riders. If
  conflicted, an error message will pop up and prevent updating.

- 02/07 The GitHub repo have some sensitive information leaking problems, but for easily testing for graders the raw
  sensitive information is in the public repo.

- 02/07 TODO Users can post rides arbitrarily. For example, the ride of the request ride can be earlier thanbe the
  current time; the requested passenger number can be larger than the maximum number of passengers that their requested
  vehicle can hold; A driver can confirm a ride which is earlier than the current time, etc. These kind od rides make
  nonsense.

## UserRole

### Ride Owner

- When a user requests a ride, he/she becomes the owner of that ride. Requesting
  a ride should involve specifying a destination address, a required arrival (date & me), the
  number of total passengers from the owner’s party, and optionally, a vehicle type and any other
  special requests. A request will also indicate whether this ride can be shared or not – a shared
  ride can be joined by other users (ride sharers). A ride owner would be able to modify a ride
  request up unl it is confirmed (a ride becomes confirmed once a driver accepts the ride and is
  in route). A ride is open from the me it is requested unl that point. A ride owner can also
  view ride status unl the ride is complete (a ride becomes closed once a driver finishes the ride
  and marks it as complete).

### Ride Driver

- A user can register as a driver, and in doing so will provide their name along with
  their vehicle information. The vehicle information includes the type, license plate number,
  maximum number of passengers, and optionally any other special vehicle information. To simplify, a
  driver can only have 1 vehicle. A driver can search for open ride requests based on the ride
  request attributes. A driver can claim and start a ride service, thus confirming it. A driver can
  also complete rides that they service aer reaching the destination to indicate that the ride is
  finished.

### Ride Sharer

- A user can search for open ride requests by specifying a destination, arrival
  window (the user’s earliest and latest acceptable arrival date & me) and number of passengers
  in their party. The user can then become a ride sharer, by joining that ride. A ride sharer can
  also view the ride status, similarly to a ride owner. Finally, a ride sharer can edit their ride status
  as long as the ride is open.

## Functionality supported

- **Create Account** – A user should be able to create an account if they do not have one.
- **Login/Logout** – A user with an account should be able to login and logout.
- **Driver Registration** – A logged-in user should be able to register as a driver and enter their
  personal and vehicle info. They should also be able to access and edit their info.
- **Ride Selection** – If a logged-in user is part of multiple rides, she should be able to select which
  ride she wants to perform actions on. If a logged in user belongs to only one ride, you MAY
  display your ride-selection mechanism with the one ride, or you MAY omit it (not show it). Note
  this should allow selection of any open or confirmed rides for that user (but not complete rides).
- **Ride Requesting** – A logged-in user should be able to request a ride. Requesting a ride should
  allow the owner to specify the destination address, a required arrival date / me, the number of
  total passengers from their party, a vehicle type (optionally), whether the ride may be shared by
  other users or not, and any other special requests.
- **Ride Request Editing (Owner)** – A ride owner should be able to edit the specific requested
  attributes of the ride as long as the ride is not confirmed.
- Ride Status Viewing (Owner / Sharer) – A ride owner or sharer should be able to view the
  status of their non-complete rides. For open ride requests, this should show the current ride
  details (from the original request + any updates due to sharers joining the ride). For confirmed
  ride requests, the driver and vehicle details should also be shown.
- **Ride Status Viewing (Driver)** – A ride driver should be able to view the status of their confirmed
  rides, which should show the information for the owner and each sharer of the ride, including
  the number of passengers in each party. A driver should also be able to edit a ride to mark it as
  complete.
- **Ride Searching (Driver)** – A driver should be able to search for open ride requests. Only requests
  which fit within the driver’s vehicle capacity and match the vehicle type and special request info
  (if either of those were specified in the ride request) should be shown. A driver can claim and
  start a ride service, thus confirming it. Once closed, the ride owner and each sharer should be
  notified by email that the ride has been confirmed (hence no further changes are allowed).
- **Ride Searching (Sharer)** – A user should be able to search for open ride requests by specifying a
  destination, arrival window (the user’s earliest and latest acceptable arrival me) and number
  of passengers in their party. A sharer should be able to join a selected ride, if any exist in the
  resulting list of pending rides.
