# flask-tutorial
The flask turtorial from official docs

And a few steps to push it to Heroku.

## Steps

Install `python3-venv`

Then do :

```term
$ python3 -m venv venv
```

To change to the virtual environment:

```term
$ . venv/bin/activate
```

Now install all the requirements:

```term
$ pip install flask
```

To list the installed packages use:

```term
$ pip list --format=columns
```

To create a `requirements.txt` file run:

```term
$ pip freeze > requirements.txt
```

See **Other Complications** below for some more details.

Now to run a flask app in `app.py`:

```term
$ export FLASK_APP=app.py
```

```term
$ flask run
```



### Heroku

Install Heroku CLI from :

```term
$ sudo snap install heroku --classic
```

Then login:

```term
$ heroku login
```

You should have a `Procfile` which helps Heroku to start the server correctly, here is a basic file which starts the flask's `app.py`:

```
web: gunicorn app:app
```



Now create a Heroku app:

```term
$ heroku create <app-name>
```

You can skip the app-name and Heroku will give you a random name.

Then deploy your code:

```term
$ git push heroku master
```

Just to make sure that the app has at least 1 dynamo running:

```term
$ heroku ps:scale web=1
```

Now to open the app:

```term
$ heroku open
```

You can view the logs with:

```term
$ heroku logs --tail
```

You can view information related to dynos etc using:

```term
$ heroku ps	
```

To scale an app to `n` (integer) dynos, run:

```ter
$ heroku ps:scale web=n
```



## Other Complications:

### Requirements.txt

You should install `gunicorn` server even if you don't use it locally. Heroku requires it in `requirements.txt` .

Also, the `pkg-resources==0.0.0` line in `pip freeze` is an bug due to some weird things, to escape it use a `Makefile` :

```makefile
freeze:
	pip freeze | grep -v "pkg-resources" > requirements.txt
```

This removes the `pkg-resources` line. More info can be found in this [StackOverflow Question](https://stackoverflow.com/questions/39577984/what-is-pkg-resources-0-0-0-in-output-of-pip-freeze-command).

### Venv

It is a pain to type `. venv/bin/activate` to activate the virtual environment every time you you start coding. To escape this, add an alias,

```bash
alias vactv8=". ./venv/bin/activate"
```

in your `.bashrc` . Now for every project using venv, you just need to run `vactv8`. As it is obvious `vactv8` is **v**env **act**i**v-8**(ate)

