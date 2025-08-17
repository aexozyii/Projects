<!-- starting on incremental game search website -->
<!-- changed idea from chatbot (no chatbot code so unable to produce) -->
<!-- planning start - -->
<!-- search function -->
<!-- redirect function -->
<!-- add game function -->

<h1>Documentation<br></h1>
<p>- Started planning<br></p>
<h3>Incremental website<br></h3>
<h6>Allows for browsing, searching & adding incremental games</h6><br>

<h1>**Functional and Non-functional requirements**</h1><br>
 **Requirement**                                                  | **Type**       |<br>
 ---------------------------------------------------------------- | -------------- |<br>
 Users can browse a catalog of incremental games.                 | Functional     |<br>
 Users can search games by name, tags, or genre.                  | Functional     |<br>
 Users can filter games (e.g., sci-fi, idle, prestige mechanics). | Functional     |<br>
 Display trending, new, and most-played games.                    | Functional     |<br>
 Users can play games directly in the browser.                    | Functional     |<br>
 Users can switch to fullscreen mode.                             | Functional     |<br>
 Save progress locally for guests (local storage).                | Functional     |<br>
 Save progress in the cloud for logged-in users.                  | Functional     |<br>
 Users can sign up, log in, and log out.                          | Functional     |<br>
 Profiles include saved games, favorites, play history.           | Functional     |<br>
 Users can rate and review games.                                 | Functional     |<br>
 Users can comment/discuss games.                                 | Functional     |<br>
 System can recommend games based on play history.                | Functional     |<br>
 Admins can add, edit, or remove games.                           | Functional     |<br>
 Admins can manage tags/genres.                                   | Functional     |<br>
 Admins can moderate user reviews and comments.                   | Functional     |<br>
 Admins have analytics dashboard (engagement, most played).       | Functional     |<br>
 Notifications for new games (optional).                          | Functional     |<br>
 Guest play supported without account.                            | Functional     |<br>
 Page load time under 3 seconds.                                  | Non-Functional |<br>
 Games load within 5 seconds on average.                          | Non-Functional |<br>
 System supports multiple concurrent users.                       | Non-Functional |<br>
 Auto-save game progress (local + cloud).                         | Non-Functional |<br>
 Backup and restore of database.                                  | Non-Functional |<br>
 Intuitive, simple interface with minimal clicks.                 | Non-Functional |<br>
 Encrypted connections via HTTPS.                                 | Non-Functional |<br>
 Passwords stored with hashing (e.g., bcrypt).                    | Non-Functional |<br>
 Protection against XSS, CSRF, SQL injection.                     | Non-Functional |<br>
 Content moderation for user input.                               | Non-Functional |<br>
 Modular codebase (easy to add new games).                        | Non-Functional |<br>
 Clear developer/admin documentation.                             | Non-Functional |<br>    
 Works on Chrome, Firefox, Safari, Edge.                          | Non-Functional |<br>
<br>


![first page prototype](Images/firstpage.jpg)

![game page prototype](Images/secondpage.jpg)

<br>Alternate Website Design<br>

<br>Continued on Figma prototype, adding different colours (black and white), typography, a signup/login page and search function. <br>

![loginpage](Images/loginpage.jpg)

 Designing Algorithms:<br>
 Created 2 Algorithms-
<br>
1. Login Page<br>
Test case - Valid login credentials<br>
Verify that the user can successfully log in with valid credentials.<br>
Preconditions: The user has created an account and has a valid username and password.<br>
Steps:
1. Open the login page.
2. Enter the valid username and password in the username field.
3. Click the login button.
Expected Result: The user is successfully logged in and redirected to the homepage.

![algorithm for Login Page](Images/loginalgorithm.jpg)<br>

2. Search Function<br>
Test Case- Search function<br>
Verify that the search bar returns relevant results for a valid search query.<br>
Preconditions: The search function is enabled and the search database includes relevant data.<br>
Steps:
1. Open the search bar.
2. Enter a valid search query (e.g. "incremental game").
3. Click the search button or press Enter.
Expected Result: The search results page displays a list of relevant incremental games, including titles, descriptions, and other relevant information.

![algorithm for Search Function](Images/searchalgorithm.jpg)<br>


