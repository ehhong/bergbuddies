# bergbuddies design

Berg buddies is a Flask web application. It is developed using the model-view-controller pattern.
Berg buddies consists of:

- Models
    - bergbuddies.db
- Views
    - static/
        - images/
            - bergbuddies_hor.png (Berg buddies logo with text on the side)
            - bergbuddies_text_vert.png (Berg buddies logo with text below)
        - styles.css
    - templates/
        - apology.html (displays error messages)
        - checkin.html (takes in user's table ID through a dropdown select form. uses a for loop in Jinja to list table columns 1-17)
        - home.html (displays home page)
        - layout.html (establishes the application's general layout (navigation bar, logo). links html pages to the Bootstrap library and styles.css)
        - login.html (takes in user's username and password through a form)
        - random.html (displays random buddy in a html table)
        - register.html (takes in user's name, username, and password through a form)
        - table.html (displays all checked in users in a html table)
        - tablebuddies.html (displays all checked in users at a particular table in a html table. uses the html progress bar element to display meal completion progress)
- Controllers
    - application.py
    - helpers.py

# bergbuddies.db

The database of Berg buddies is organized into three tables: users, berg, and tables.
The users table is a list of all Berg buddies users. Each user has 4 corresponding fields: userID (integer, not null, primary key), username (text), hash (hashed form of user's password, text), name (text), eatingTime (real), totalEatingTime (real), and numMeals (integer).
The berg table is a list of all users currently checked into Berg buddies. The table has 4 fields: userID (integer), tableID (text), checkInTime (datetime), and checkOutTime (datetime). UserID is a foreign key linking users to berg.
The tables table is a list of tables and how many people are currently at them. The table has 2 fields: tableID (text) and count (integer).

# home.html

Home.html creates the graphic visualization of Annenberg through SVG elements. Because the tables are essentially a 3 x 17 matrix, the tables are displayed using nested Jinja for loops, with one ranging from 0 to 3 and the other from 0 to 17.
The table ID is printed onto each table by setting the indices of each for loop as a component of the table ID. The index ranging from 0 to 3 corresponds to a variable assigned to table rows "A", "B", and "C", and the index ranging from corresponds to table columns 1 through 18. These two values are then concatenated and assigned to a Jinja variable "tableID", which is printed on each table as a SVG text element.
To change the display of the table depending on if it users are checked into it or not, the html page receives a list of table objects, each with a tableID and count greater than 0 (the table is occupied). If the table ID of the table being printed is the same as one of the table IDs in the occupied table list, a red SVG rectangle of the same size will be printed on top of the previous one and a SVG text element will display the count (the number of users at that table) and a ":-)".
The red SVG rectangle and the count text are html links that redirect to the table buddies page. Using Jinja, the link takes in the corresponding table ID (xlink:href="/tablebuddies?tableID={{ tableID }}).

# helpers.py

Helpers.py defines the apology function and the login required function.
The apology function takes in an error message, escapes special characters in the error message, and renders the apology template (apology.html), passing in the message and html error code.
The login required function creates a login_required decorator that makes certain app routes and functions accessible only if a user is logged in. If a user is not logged in and tries to access them, the decorator will redirect to the login page.

# application.py

Application.py sets up the Flask application, configures session to use a filesystem to manage users' login info, and uses the CS50 to use the SQLite database bergbuddies.db.
From there, the file is organized into functions corresponding to an application route.

##Home:
The home function corresponds to the "/" route of the application, or the first visible page. The home function passes in a list of occupied tables to the template home.html. To do this, it selects all objects from the tables table, traverses through them, and appends tables with a count greater than 1 to a list named "occTables".

##Register:
The register function corresponds to the "/register" route of the application. If the route is reached using a "GET" method, the function renders the register.html page.
If the route is reached using a "POST" method, the function checks that all fields are filled (name, username, password), generates the hashed form of the password using a hash function, and inserts a new user into the users table with those values. If the username is the same as another username, the database insert request will return as none because the username field is set as an index and must have unique values. If the request returns as none, the apology function is called, displaying an error message.
If the user is successfully added to the database, the user is logged in by storing the user's ID in session and setting session's logged in variable to true. The application then redirects to the home page.

##Login:
The login function corresponds to the "/login" route of the application. If the route is reached using a "GET" method, the function renders the login.html page.
If the route is reached using a "POST" method, the function checks that a username and password were entered and queries for users in the database with the same username. If the username exists, the inputted password is hashed and checked with the stored hash value. The user is then logged in by storing the userID in session and setting the logged_in variable to true. The function then redirects to the home page.

##Logout:
The logout function clears all session values and redirects to the home page.

##Check in:
The login function corresponds to the "/checkin" route of the application. If the route is reached using a "GET" method, the function renders the checkin.html page, where the user can input a table ID.
If the route is reached using a "POST" method, the function checks that a table ID has been selected, finds the current time using the python datetime library, and adds the user with a corresponding table ID and check in time to the berg table. Because userIDs are indexed in berg and must be unique, if the insert request returns as none, the user is already checked in and an error message is returned.
If the user is successfully checked in, the count of the user's table will be increased by one in the tables table. If the table does not exist in the tables table, it will be inserted. The function will then redirect to the home page.

##Check out:
### michele pls finish stuff about meal time
The user's table count is decreased by one in the tables table, and the user is removed from the berg table. The function then redirects to the home page.

##Meal Stage:
### michele pls describe this one too

##Table View:
Table view selects all entries in the berg table and passes the list of all users in berg to the table.html template as it is rendered.

##Table Buddies:
Table buddies takes in a table ID and gets a list of users at the given table and their meal stage values through the mealstage function. The list of users is then sorted by increasing meal completion percentage using a selection sort. The function then renders the tablebuddies.html template, passing through the sorted list of users and their meal stages.

## Random Buddy:
Random buddy selects all entries in the berg table. It then finds a random integer between 0 and the number of users checked into berg (length of all berg entries list minus 1) and saves the user at the random index. The random user is then passed into the rendering random.html template.