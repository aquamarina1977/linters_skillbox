DROP TABLE IF EXISTS actors;
DROP TABLE IF EXISTS movie;
DROP TABLE IF EXISTS director;
DROP TABLE IF EXISTS movie_cast;
DROP TABLE IF EXISTS oscar_awarded;
DROP TABLE IF EXISTS movie_direction;

CREATE TABLE actors
(
	act_id               INT PRIMARY KEY AUTO_INCREMENT,
	act_first_name       VARCHAR(50),
	act_last_name        VARCHAR(50),
	act_gender           VARCHAR(1)
);

CREATE TABLE movie
(
	mov_id              INT PRIMARY KEY AUTO_INCREMENT,
	mov_title           VARCHAR(50)
);

CREATE TABLE director
(
	dir_id              INT PRIMARY KEY AUTO_INCREMENT,
	dir_first_name      VARCHAR(50),
	dir_last_name       VARCHAR(50)
);

CREATE TABLE movie_cast
(
	act_id              INT,
	mov_id              INT,
	role                VARCHAR(50),
	FOREIGN KEY (act_id) REFERENCES actors (act_id) ON DELETE SET NULL,
	FOREIGN KEY (mov_id) REFERENCES movie (mov_id) ON DELETE SET NULL
);

CREATE TABLE oscar_awarded
(
	oscar_id            INT PRIMARY KEY AUTO_INCREMENT,
	mov_id              INT,
	FOREIGN KEY (mov_id) REFERENCES movie (mov_id) ON DELETE SET NULL
);

CREATE TABLE movie_direction
(
	dir_id             INT,
	mov_id             INT,
	FOREIGN KEY (dir_id) REFERENCES director (dir_id) ON DELETE SET NULL,
	FOREIGN KEY (mov_id) REFERENCES movie (mov_id) ON DELETE SET NULL
);
