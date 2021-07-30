from flask import Blueprint
from flask import render_template, request, jsonify, g, url_for, redirect, session
import datetime

from . import db

bp = Blueprint("home", "home", url_prefix = "/home")

@bp.route("/", methods = ["POST", "GET"])
def home():
	if "user" not in session:
		return redirect(url_for("login"))
	
	#print(session["user"])
	
	if request.method == "POST":
		return render_template("createpoll.html")
		
	userid = session['userid'][0]
		
	conn = db.get_db()
	cursor = conn.cursor()
	
	cursor.execute("select name from USERS where id = %s", (userid,))
	username = cursor.fetchall()[0][0]
	
	time = datetime.datetime.now()
	
	cursor.execute("select poll_name, creator, end_time, id from POLL where %s < end_time;",(time,))
	details = cursor.fetchall()
	cursor.close()
	return render_template("home.html", name = username, count = len(details), l = details)
	
	

@bp.route("/createpoll", methods = ["POST", "GET"])
def createpoll():
	
	if request.method == "GET":
		return redirect(url_for("login"))
	
	if 'user' not in session:
		return redirect(url_for("login"))
		
	starttime = str(datetime.datetime.now())[:-7]
	pollname = request.form["pollname"]
	polldp = request.form["polldp"]
	endtime = str(request.form["endtime"])
	
	username = session['user']
	
	s = set()
	s.add(str(request.form["A"]))
	s.add(str(request.form["B"]))
	conn = db.get_db()
	cursor = conn.cursor()
	
	endtime = endtime.replace("T", " ")
		
	#print(starttime + " " + endtime)
		
	cursor.execute("select poll_name, poll_description from POLL where poll_name = %s AND poll_description = %s;",(pollname, polldp))
	
	test = cursor.fetchall()
	
	if len(test) > 0:
		return render_template('error.html')
	
	cursor.execute("insert into POLL (creator, poll_name, poll_description, start_time, end_time) values (%s, %s, %s, %s, %s);", (username, pollname, polldp, starttime,endtime))

	for option in s:
		cursor.execute("insert into options (pollid, op_name, op_count) values ((select id from POLL where poll_name = %s AND poll_description = %s), %s, 0);", (pollname, polldp, option))
	cursor.close()
	conn.commit()
	
	#print("Poll added")
	
	return redirect(url_for("home.home"))



#function for participating in the polls and storing options in the server	
@bp.route("/poll/<pollid>", methods = ["POST", "GET"])
def poll(pollid):

	if 'user' not in session:
		session['redirect'] = "home.poll"
		session['pollid'] = pollid
		
		return redirect(url_for("login"))
	
	userid = session['userid'][0]
	
	con = db.get_db()
	cur = con.cursor()
	
	cur.execute("select p.userid, o.op_name, o.id from PARTICIPATED p, OPTIONS o where polls = %s AND o.id = p.opted AND p.userid = %s order by op_name desc;", (pollid, userid,))
	
	selected = cur.fetchall()
	
	if len(selected) == 0:
		s = "Chose Your Option"
	else:
		s = f"You chose: {selected[0][1]}"
	
	if request.method == "POST":
		
		#print(session['userid'])
		optionid = request.form["option"]
		
		if s != "Chose Your Option" and selected[0][2] != optionid:
			cur.execute('update OPTIONS set op_count = op_count + 1 where id = %s;', (optionid,))
			cur.execute('update OPTIONS set op_count = op_count - 1 where id = %s;', (selected[0][2],))	
			cur.execute("delete from PARTICIPATED where userid = %s AND polls = %s;", (userid, pollid,))	
			cur.execute("insert into PARTICIPATED values (%s, %s, %s);", (userid, pollid, optionid,))
		elif s == "Chose Your Option":
			cur.execute('update OPTIONS set op_count = op_count + 1 where id = %s;', (optionid,))
			cur.execute("insert into PARTICIPATED values (%s, %s, %s);", (userid, pollid, optionid,))
		
		cur.close()
		con.commit()
		
		return redirect(url_for("home.poll", pollid = pollid))
	
	#print(pollid)
	
	session.pop('redirect', None)
	session.pop('pollid', None)
	
	#return render_template('sample.html')
	
	cur.execute("select creator, poll_name, poll_description, start_time, end_time, id from POLL where id = %s;", (pollid,))
	pollinfo = cur.fetchall()
	#print(pollinfo)
	
	cur.execute("select o.id, o.op_name from POLL p, OPTIONS o where p.id = %s AND o.pollid = p.id;", (pollid,))
	options = cur.fetchall()
		
	cur.close()
	
	return render_template('poll.html', pollinfo = pollinfo, options = options, s = s)
		
	
