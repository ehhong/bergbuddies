# bergbuddies

# Description:

Something Harvard really prides itself on is how at the start of the year, you can sit down with anyone in Annenberg, strike up a conversation, and make a new friend. However, we couldn't help but notice that a few months later, this spirit of spontaneous interaction has waned, and there's an unspoken rule that this is no longer common practice.
We created this application to revive the spirit of friendship and combat loneliness in the dining halls, because sometimes people want company and aren't sure how to make other people aware of it.
Berg buddies is an application that allows freshmen in Annenberg (Harvard's freshmen dining hall) to identify other freshmen to eat with. The application does this by allowing users to "check in" to a specific table at Annenberg when they arrive.

# Installing:

Berg buddies is a Flask web application. To run the application, download the application files, open the application folder, and run the command "Flask run" into your terminal or IDE.
If the application is already running on a server, simply enter the URL in your web browser.

# ~ Functions ~

## Home:
The home page of the application displays a graphic visualizaiton of the table setup in Annenberg. Each table has an ID (ex. "A1") that corresponds to its ID in Annenberg. If user(s) are currently checked into a table, the table will turn red and display the number of users at that table.

## Table Buddies:
Users can see which users are at each table by clicking on them (if they're occupied). The application will then display the relevant table ID and a list of users' names at that table. The table also displays users' meal completion progress bars. The progress bars show an estimate for how far someone is into their meal, giving the user an idea of how much longer that person will still be there.

## List View:
The list view page displays a list of all users currently checked into Annenberg. The table shows users' names, table IDs, check in times, and average eating times.

## Random Buddy:
Aiming to help with indecision, the random buddy page displays a randomly selected user from the users currently checked into Annenberg. The random buddy's name, table ID, and check in time are displayed. A new random buddy can be displayed by clicking "find me another!" or reloading the page.

## Register:
To fully use Berg buddies, users need to create an account. The register page takes in a user's name, username, and password to register a new account. A user may not have the same username as another user.

## Login (account required):
The login page allows a user to login into their account by entering their username and password.

## Check in (account required):
The check in page prompts the user for a table ID (the table ID they're sitting at) and allows them to be seen by other Berg buddies users. The user will then be considered as present in Annenberg at that particular table.

## Check out (account required):
The check out function checks out a user from Annenberg. The user will no longer be recognized as present in Annenberg.

## Logout (account required):
The logout link logs a user out and returns them to the home page.