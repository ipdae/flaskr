drop table if exists entries;
create table entries (
	   id integer primary key autoincrement,
	   title string not null,
	   text string not null,
	   password string not null
);

drop table if exists logins;
create table logins (
	   id integer primary key autoincrement,
	   username string not null,
	   password string not null
);

drop table if exists contents;
create table contents (
	   id integer primary key autoincrement,
	   entry_id integer not null,
	   author string not null,
	   comment string not null,
	   password string not null
);

insert into logins (username, password)
values ('admin', 'default');
