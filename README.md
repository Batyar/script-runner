# script-runner
This is small control panel for quick script running and file browsing

###Install:
  * cd script-runner
  * mkdir env
  * virtualenv env
  * source env/bin/activate
  * pip install -r requirements.txt 

######Set a mysql host into app.config['SQLALCHEMY_DATABASE_URI'] variable in models.py after that create new user:

  * python create_user.py username password role

######This command will create credentials adm/pass

  * python app.py
  
######Navigate in browser http://0.0.0.0:5000/login

###Logo:
![alt text][logo]

[logo]: https://github.com/Batyar/script-runner/blob/master/static/example.jpg "Example"
