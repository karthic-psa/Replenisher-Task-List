# Replenisher Task List #

A rudimentary “full-stack” app that allows management of template tasks by experienced group, and assignment of these templates as recurring tasks to individuals.  The app should allow for tracking of progress, notes and feedback.  

## About the Project: ##

Today’s Replenishment manager is required to complete a variety of tasks, working with many people to insure optimal product movement through the supply chain.  
The goal of this challenge to create an application which allows individuals to create independent tasks to be added to their personalized task list.  This service is used by the user to create tasks.  In addition, it also exposed as that other tasks can be created on behalf of the user.
Keeping in mind on how to drive future enhancements.


## Dependencies for Project: ##

1. Python 2.7
2. Django 1.11+
3. Bootstrap - already provided through CDN in project file (however you can install it or modify as you need.)
4. jQuery - already provided through CDN in project file
5. SQLite3 - as the database (already preinstalled with the project on django)

## Instructions on how to install and run the project: ##

1. Make sure Python 2 (version 2.7) is installed; in Command Prompt or PowerShell, type ```python --version  (else install Python and ensure the Python path is updated in Environment Variables)
	- To install Python - (Windows)
		1. Download from https://www.python.org/downloads/
		2. Be sure to check you're downloading the right python version for your system (64bit vs 32bit) 
		3. Open Python Installer - Customize as per requirements and change install Location and use: `C:\Python27
		4. Click ```Install```
		5. Update the Python path in Environment Variables of the system
		6. Verify installation - in Command Prompt or PowerShell, type ```python --v`` or ```python -version```
	- If Python is installed correctly, we use pip to install other components and packages
2. Make sure you have django installed (else install django 1.11.X)
	- To install django - (Windows)
		1. Open Command Prompt or PowerShell (Run as adminstrator)
		2. Type ```pip install django==1.11.3```
			*NOTE: django==1.11.3 is for version 1.11.3. If you need a different version, replace those numbers accordingly. Such as django==1.8.7 or django==1.10.7 or django==1.11.2. This is true for any python package.
	- It is highly recommended that you install and run django on a **Virtual Environmen**t; to do this open Command Prompt or PowerShell
		1. Type ```pip install virtualenv```
		2. Navigate to your project directory and make virtualenv parent directory 
			- ```mkdir 'homedirname'```
			- ```cd 'homedirname'```
		3. Create virtualenv by typing ```virtualenv .``` or ```virtualenv yourenvname```
		4. Go to your virtual environment directory ```cd yourenvname```
		5. Activate your environment:
			- ```cd \path\to\your\virtualen\env\ ```
 			- ```cd ~\dirname\homedirname```
 			- ```.\Scripts\activate```
		6. To Reactivate and Deactivate Virtualenv
			- ```cd ~\dirname\homedirname # or your virtualenv's path```
			- ```.\Scripts\activate```
			-```(homedirname) > deactivate```
			- ```.\Scripts\activate```
			- ```(homedirname) >```
		7. Now install django or any Python Package as mention in the above point
3. Now clone or download the github repo to the correct directory
4. Go ```cd``` to the cloned or downloaded project directory where you will see a manage.py file
5. Now we need to create and migrate the database Models
	- In the cmd type and run ```python manage.py migrate tasklistapp```
	- Then run ```python manage.py makemigration tasklistapp```
	- Next, ```python manage.py sqlmigrate tasklistapp 0001```
	- Finally, run ```python manage.py migrate```
6. We need to create a Superuser (Administrator) for the django admin panel who can control all aspects of the app and authentication/authorization
	- Type ```python manage.py createsuperuser```
	- Enter the appropriate details - (username and password to login to the admin panel)
7. To get our localhost running, django provides us with a simple server to test and run apps
	- Type ```python manage.py runserver```
	- This should start running our ```http://localhost:8000``` at http://127.0.0.1:8000 - (Defaults to port 8000)
8. Now, visit http://127.0.0.1:8000/admin and login to access your database models, groups and users
9. Create necessary groups and users as per requirements - auth for people who can access and use our app
	- Ensure normal users only have ```Active``` permissions check, not admin or superuser status
10. **Start** using the app by just visitng the localhost or ```http://127.0.0.1:8000/```
	- Auth for different users vary
11. Still adding a lot of features and ironing out a few small bugs - ** The App works properly for the provided features **



## The following are the API (JSON) endpoints: ##

1. http://127.0.0.1:8000/api/ (at /api)

2. http://127.0.0.1:8000/api/users/

3. http://127.0.0.1:8000/api/groups/

4. http://127.0.0.1:8000/api/tasks/

5. http://127.0.0.1:8000/api/taskslist/

** Still adding more API (JSON) endpoints which filters results according to specific requests. ** Basic endpoints work.

