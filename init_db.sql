/*Commandes à l’origine des tables SQL sous PostgreSQL. */
CREATE TABLE categorie(
    id_cat INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    label text
);

CREATE TABLE annonce (
    id_annonce INT PRIMARY KEY NOT NULL AUTO_INCREMENT=120,
    city text,
    url_image text,
    source text,
    id_cat integer,
    price integer,
    surface text,
    room text,
    agency text,
    title text,
    description text,
    sell bool DEFAULT False,
    FOREIGN KEY (id_cat) REFERENCES categorie(id_cat)
);

CREATE TABLE utilisateur (
    id_user INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    nom varchar(50),
    prenom varchar(50),
    email varchar(50),
    birth_date date,
    zip_code varchar(50),
    password text,
    type int,
    tel int,
    adresse varchar(50),
    date_inscription date
);

CREATE TABLE historic (
    id_annonce INT,
    id_user INT,
    date_recherche char(50),
    FOREIGN KEY (id_annonce) REFERENCES annonce(id_annonce),
    FOREIGN KEY (id_user) REFERENCES utilisateur(id_user)
);

CREATE TABLE wishlist (
    id_annonce INT,
    id_user INT,
    FOREIGN KEY (id_annonce) REFERENCES annonce(id_annonce),
    FOREIGN KEY (id_user) REFERENCES utilisateur(id_user)
);

CREATE TABLE message (
    message text,
    id_user INT,
    FOREIGN KEY (id_user) REFERENCES utilisateur(id_user)
);