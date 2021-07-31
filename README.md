# Genskill_Project-Anonymous_Voting_Sytsem

This is a web application that allows the user to create polls and participate in polls anonymously (Works best on Chrome)

* Users can register to the database and login to the site
* They can create a poll and shedule the deadline. The creators can view the poll info in runtime
* Users can participate in polls through links or through their home screen

To configure install the python packages listed in the requirements.txt and make sure you have postgresql in your system

Run the commands in a unix shell in the following order to run the application

* export FLASK_APP=voting
* flask initdb : (This has to be run only once to setup the database)
* flask run : to run the application

The site is deployed at https://anonymousvoting.herokuapp.com/
