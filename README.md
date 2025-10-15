<!-- starting on incremental game search website -->
<!-- changed idea from chatbot (no chatbot code so unable to produce) -->
<!-- planning start - -->
<!-- search function -->
<!-- redirect function -->
<!-- add game function -->

<h1>Documentation<br></h1>

<h3>Incremental website<br></h3>
<h6>Allows for browsing, searching & adding incremental games</h6><br>
Similarly to websites like Galaxy.click and Steam, I aim for my website to display the following:<br>

- Search and filter games by genre, platform, and release date.<br>

- Compare availability across different online stores and platforms.<br>

- Read and share community reviews, ratings, and recommendations.<br>

- Save and track favorite games for quick access.<br>

<h1><b>Week 1: Functional and Non-functional requirements</b></h1><br>
<pre><b>Requirement</b>                                                       | <b>Type</b>           |<br>
 ---------------------------------------------------------------- | -------------- |<br>
 Users can browse a catalog of incremental games.                 | Functional     |<br>
 Users can search games by name, tags, or genre.                  | Functional     |<br>
 Users can filter games (e.g., sci-fi, idle, prestige mechanics). | Functional     |<br>
 Display trending, new, and most-played games.                    | Functional     |<br>
 Users can play games directly in the browser.                    | Functional     |<br>
 Users can switch to fullscreen mode.                             | Functional     |<br>
 Save progress locally for guests (local storage).                | Functional     |<br>
 Save progress in database for logged-in users.                   | Functional     |<br>
 Users can sign up, log in, and log out.                          | Functional     |<br>
 Profiles include saved games, favorites, play history.           | Functional     |<br>
 Users can rate and review games.                                 | Functional     |<br>
 Users can comment/discuss games.                                 | Functional     |<br>
 System can recommend games based on play history.                | Functional     |<br>
 Notifications for new games (optional).                          | Functional     |<br>
 Guest play supported without account.                            | Functional     |<br>
 Page load time under 3 seconds.                                  | Non-Functional |<br>
 Games load within 5 seconds on average.                          | Non-Functional |<br>
 System supports multiple concurrent users.                       | Non-Functional |<br>
 Auto-save game progress (local + cloud).                         | Non-Functional |<br>
 Backup and restore of database.                                  | Non-Functional |<br>
 Intuitive, simple interface with minimal clicks.                 | Non-Functional |<br>
 Passwords stored with hashing (e.g., bcrypt).                    | Non-Functional |<br>
<br></pre>
<h1><b>Week 2: Website Design</b></h1><br>

![first page prototype](static/Images/firstpage.webp)

![game page prototype](static/Images/secondpage.webp)

<h1><b>Week 3: Alternate Website Design</b></h1><br>

<br>Continued on Figma prototype, adding different colours (black and white), typography, a signup/login page and search function. <br>

![loginpage](static/Images/loginpage.webp)

<h1><b>Week 4: Website Algorithms</b></h1><br>

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

![algorithm for Login Page](static/Images/loginalgorithm.webp)<br>

2. Search Function<br>
Test Case- Search function<br>
Verify that the search bar returns relevant results for a valid search query.<br>
Preconditions: The search function is enabled and the search database includes relevant data.<br>
Steps:
1. Open the search bar.
2. Enter a valid search query (e.g. "incremental game").
3. Click the search button or press Enter.
Expected Result: The search results page displays a list of relevant incremental games, including titles, descriptions, and other relevant information.

![algorithm for Search Function](static/Images/searchalgorithm.webp)<br>

<h1><b>Week 5 & 6: SQL Setup</b></h1><br>
<h3>Queries</h3><br>
1. Logininformation to gameinformation<br>
   dblogin username > game history (game name), last login > game visit date<br>
2. Favourites table > Login Data<br>
   Use login data to add favourites to user data, displaying favourites in specific area.<br>
3. Genres table > gameinformation<br>
   Display game genre (with link to other games of game genre) under game information.<br>
4. Reviews table > gameinformation<br>
   Display review data for specific game underneath gameinformation<br>
5. Sessions table > Login Data<br>
   Sessions table ensures the user can stay logged in if they close or refresh the browser using their ip address.<br>
6. Gamelinks table > Stores
   Allows user to click on link to be redirect to a store where user can view or buy game (if game is paid).

![sql queries](static/Images/sqlqueries.webp)<br>
^shows all links between each table^

<h1><b>Week 7 & 8: Website styling/development</b></h1><br>
<h3>Creating CSS & Html Files</h3><br>
Followed through the provided template and creates a styles.css file to put provided styles in. Changed the code around a tiny bit to fit my planned Figma colour scheme.

![css code](static/Images/csscode.webp)<br>

Created a Home, Signup & login page. These all successfully link to their respective table databases.\

![home page](static/Images/homepage.webp)<br>
^image of homepage^
![signup page](static/Images/signuppage.webp)<br>
^image of signup page^
![web login page](static/Images/webloginpage.webp)<br>
^image of login page^

<h1><b>Week 9 & 10: Adding Interactivity</b></h1><br>
Multiple different interactive features have been added to the webapp, such as game thumbnails, an about & explore section, a profile section with recently visited and favourited games, a search bar to search for games and a tag based filter for games.

![newer home](static/Images/newerhome.webp)<br>
^the revised home page with all added features^
![profile page](static/Images/profilepage.webp)<br>
^profiles page with most recently visited and favourite games^
<h1><b>Holidays:</b></h1><br>
Added a Comments section for users to write reviews on the games. 

![comments section](static/Images/commentssection.webp)<br>


<h1>How to run webapp:</h1><br>
Open VSCode and open Terminal with Ctrl + `<br>
Run the following command: <br>
python3 main.py<br>
The website should now be running on 127.0.0.1:5000