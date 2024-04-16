# validator

Install Python Virtualenv

$ sudo apt-get update

$ sudo apt-get install python3-venv


Activate the new virtual environment in the validator directory

// Change to validator directory

$ cd validator

// Create the virtual environment

$ python3.9 -m venv venvalidator

// Activate the virtual environment

$ source venvactivator/bin/activate

//Install Python dependencies

$ pip3 install -r requirements.txt

Verify if it works by running

$ python3 app.py


# Linux configuration

Run Gunicorn WSGI server to serve the Flask Application

$ gunicorn -b 0.0.0.0:8000 app:app . 

Gunicorn is running (Ctrl + C to exit gunicorn)!


Use systemd to manage Gunicorn


create a validator.service file in the /etc/systemd/system folder

$ sudo vim /etc/systemd/system/validator.service


Then add this into the file:


[Unit]

Description=Gunicorn instance for validation app

After=network.target

[Service]

User=admin

Group=www-data

WorkingDirectory=/home/admin/validator

ExecStart=/home/admin/validator/venvalidator/bin/gunicorn -b 0.0.0.0:8000 app:app

Restart=always

[Install]

WantedBy=multi-user.target



Then enable the service

$ sudo systemctl daemon-reload
$ sudo systemctl start validator
$ sudo systemctl status validator
$ sudo systemctl enable validator


Before run the test be sure to change the ip address
$ vim ./tests/topology_params.json


Finally run the tests
$ python3 -m pytest
