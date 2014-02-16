drop table if exists entries;
create table entries (
	   id integer primary key autoincrement,
	   title string not null,
	   text string not null
);

drop table if exists logins;
create table logins (
	   id integer primary key autoincrement,
	   username string not null,
	   password string not null
);

insert into logins (username, password)
values ('admin', 'default');
