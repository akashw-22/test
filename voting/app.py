from flask import Flask, render_template, request, session, redirect, g, url_for

def create_app():
	app = Flask(__name__)
	app.secret_key = "#25%@#65^#jsd#%236@#56dsf9"
	
	app.config.from_mapping(DATABASE = "vote")
	
	from . import db
	from . import homebp
	from . import yourpolls
	
	db.init_app(app)
	
	app.register_blueprint(homebp.bp)
	app.register_blueprint(yourpolls.bp)
	
	@app.route("/")
	def index():	
		return redirect(url_for('login'))
	
		
	@app.route("/login", methods = ["POST", "GET"])
	def login():
		
		if request.method == "GET":
			return render_template("login.html")
			
		session.pop("user", None)
		session.pop("userid", None)
			
		username = request.form["username"]
		password = request.form["password"]
		
		conn = db.get_db()
		cursor = conn.cursor()
		
		cursor.execute("select username, password from users;")
		
		l = cursor.fetchall()
		#print(l)
		
		if (username, password,) in l:
			
			cursor.execute("select poll_name, poll_description, creator, end_time from poll where start_time < end_time")
			l = cursor.fetchall()
			
			session["user"] = username
			
			cursor.execute("select id from users where username = %s", (username,))
			userid = cursor.fetchall()
			session["userid"] = userid
			
			cursor.close()
			
			if 'redirect' in session:
				return redirect(url_for(session['redirect'], pollid = session['pollid']))
			
			return redirect(url_for("home.home"))
			
		else:
			return redirect(url_for("login"))
			
			
	
	@app.route("/signup", methods = ["POST", "GET"])	
	def signup():
		
		if request.method == "GET":
			return render_template("signup.html")
			
		name = request.form["name"]
		age = request.form["age"]
		username = request.form["username"]
		password = request.form["password"]
		confirm = request.form["confirm_p"]
		
		if confirm == password :
			conn = db.get_db()
			cursor = conn.cursor()
			
			cursor.execute("select username from users;")
			
			l = cursor.fetchall()

			if (username,) in l:
				#print("username present")
				return render_template("error.html")
				g.user = username
			else:
				cursor.execute(f"insert into USERS (name, age, username, password) values ('{name}', {age}, '{username}', '{password}');")
				cursor.close()
				conn.commit()
							
			return redirect("login")
			
		else:
			return redirect("signup")
			
	@app.route("/logout")
	def logout():
		session.clear()
		return redirect(url_for('login'))
			
			
		
	return app

