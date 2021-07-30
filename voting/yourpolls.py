from flask import Blueprint, session, url_for, render_template, redirect
from datetime import datetime

from . import db

bp = Blueprint("yourpolls", "yourpolls", url_prefix="/yourpolls")

@bp.route("/")
def yourpolls():
	
	if 'user' not in session:
		return redirect(url_for("login"))
		
	username = session['user']
	con = db.get_db()
	cur = con.cursor()
	
	cur.execute("select id, poll_name, start_time, end_time from POLL where creator = %s;", (username,))
	
	polls = cur.fetchall()
	time = datetime.now()
	
	#print(polls)
	
	return render_template('yourpolls.html', count = len(polls), polls = polls, time = time)



@bp.route("/<pollid>")
def polldetails(pollid):
	
	if 'user' not in session:
		return redirect(url_for("login"))
		
	username = session['user']
	
	con = db.get_db()
	cur = con.cursor()
	
	cur.execute("select creator from POLL where id = %s;", (pollid,))
	creator = cur.fetchall()[0][0]
	
	if creator != username:
		return render_template("sample.html")
	
	cur.execute("select p.id, p.poll_name, p.poll_description, p.start_time, p.end_time, o.op_name, o.op_count from POLL p, OPTIONS o where p.id = %s AND p.creator = %s AND o.pollid = %s;", (pollid, username, pollid,))
	
	details = cur.fetchall()
	
	cur.close()
	
	#print(details)
	count = 0
	
	for i in details:
		count += i[6]
		
	return render_template("polldetails.html", details = details, count = count)
	
