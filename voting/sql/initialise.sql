DROP TABLE IF EXISTS USERS cascade;
DROP TABLE IF EXISTS POLL cascade;
DROP TABLE IF EXISTS OPTIONS cascade;
DROP TABLE IF EXISTS PARTICIPATED;

CREATE TABLE USERS
(
	id serial primary key,
	name text,
	age integer,
	username text UNIQUE,
	password text
);

CREATE TABLE POLL(
	
	id serial primary key,
	creator text references USERS(username),
	poll_name text,
	poll_description text,
	start_time timestamp,
	end_time timestamp,
	UNIQUE (poll_name, poll_description)
);

CREATE TABLE OPTIONS(
	
	id serial primary key,
	pollid serial references POLL(id),
	op_name text,
	op_count integer,
	UNIQUE (pollid, op_name)
);

CREATE TABLE PARTICIPATED(
	
	userid serial references USERS(id),
	polls serial references POLL(id),
	opted serial references OPTIONS(id)
);



