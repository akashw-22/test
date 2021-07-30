#for database specific functions

import psycopg2
import click
from flask import current_app, g
from flask.cli import with_appcontext

def create_db(cur, dbname):
	cur.execute(f"create database {dbname}")
	print("database created succesfully :)")
	return psycopg2.connect(dbname = f"{dbname}")
	

def get_db():

	#print(g)
	if 'db' not in g:
		dbname = current_app.config['DATABASE']
		#print("test")
		
		try:
			con = psycopg2.connect(dbname = 'postgres')
			#print("conected to postgres server")
		except:
			print("!!unable to connect to postgres server!!")
		
		if con is not None:
			con.autocommit = True
			cur = con.cursor()
			
			cur.execute("select datname from pg_database;")
			databases = cur.fetchall()
			
			if (dbname,) not in databases:			
				g.db = create_db(cur, dbname)
			
			else:
				g.db = psycopg2.connect(dbname = f"{dbname}")
			
			con.close()
		
			
	return g.db
			
def close_db(e = None):
	db = g.pop('db', None)
	
	if db is not None:
		db.close()
	
def init_db():
	db = get_db()
	f = current_app.open_resource("sql/initialise.sql")
	sqlcode = f.read().decode("ascii")
	cur = db.cursor()
	cur.execute(sqlcode)
	cur.close()
	db.commit()
	close_db()

@click.command('initdb', help = "initialise the database")
@with_appcontext
def init():
	init_db()
	click.echo("Database initialised...")
	
def init_app(app):
	app.teardown_appcontext(close_db)	#hook: close_db will be called when the app finishes execution
	app.cli.add_command(init)	#for initialising the initdb command
			
