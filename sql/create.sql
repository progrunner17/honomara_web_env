-- create role (user)
-- CREATE ROLE IF NOT EXISTS honomara WITH LOGIN ENCRYPTED PASSWORD 'honomara';

-- create database
-- CREATE DATABASE IF NOT EXISTS honomara OWNER = honomara ENCODING = UTF8;

-- create scheme

-- create tables
SET client_min_messages TO WARNING;

CREATE TABLE IF NOT EXISTS   public.person (
    person_id integer NOT NULL,
    name character varying(20) NOT NULL,
    kana character varying(40) NOT NULL,
    after_name character varying(20),
    fullname character varying(20),
    sex integer NOT NULL,
    class integer NOT NULL,
    visible boolean NOT NULL,
    CONSTRAINT person_pkey PRIMARY KEY (person_id)
);
ALTER TABLE public.person OWNER TO honomara;



CREATE TABLE IF NOT EXISTS  public.after (
    id character varying(10) NOT NULL,
    date date NOT NULL,
    wday character varying(1) NOT NULL,
    training character varying(30) NOT NULL,
    after integer NOT NULL,
    restaurant character varying(50) NOT NULL,
    genre character varying(20) NOT NULL,
    tax boolean NOT NULL,
    charge boolean NOT NULL,
    cost_min integer NOT NULL,
    cost_max integer NOT NULL,
    quantity integer NOT NULL,
    taste integer NOT NULL,
    service integer NOT NULL,
    number_min integer NOT NULL,
    number_max integer NOT NULL,
    site character varying(20) NOT NULL,
    total integer NOT NULL,
    topic character varying(100) NOT NULL,
    comment text NOT NULL,
    CONSTRAINT after_pkey PRIMARY KEY (id)
);
ALTER TABLE public.after OWNER TO honomara;
CREATE INDEX IF NOT EXISTS after_date_index ON public.after USING btree (date);



CREATE TABLE IF NOT EXISTS  public.training (
    id character varying(10) NOT NULL,
    date date NOT NULL,
    wday character varying(1) NOT NULL,
    site character varying(20) NOT NULL,
    subject character varying(20) NOT NULL,
    weather character varying(20) NOT NULL,
    total integer NOT NULL,
    comment text NOT NULL,
    CONSTRAINT training_pkey PRIMARY KEY (id)
);
ALTER TABLE public.training OWNER TO honomara;
CREATE INDEX IF NOT EXISTS training_date_index ON public.training USING btree (date);




CREATE TABLE IF NOT EXISTS  public.participant (
    id character varying(10),
    person_id integer
);

ALTER TABLE public.participant OWNER TO honomara;
CREATE INDEX IF NOT EXISTS participant_id_index ON public.participant USING btree (id);

CREATE TABLE IF NOT EXISTS  public.race (
    race_id integer NOT NULL,
    race_name character varying,
    date date,
    year integer,
    CONSTRAINT race_pkey PRIMARY KEY (race_id)
);

ALTER TABLE public.race OWNER TO honomara;


CREATE TABLE IF NOT EXISTS  public.distance (
    distance_id integer NOT NULL,
    distance real,
    distance_name character varying,
    ranking integer,
    CONSTRAINT distance_pkey PRIMARY KEY (distance_id)
);

ALTER TABLE public.distance OWNER TO honomara;

CREATE TABLE IF NOT EXISTS  public.result (
    id integer NOT NULL,
    person_id integer,
    race_id integer,
    distance_id integer,
    "time" interval(0),
    display_time character varying,
    comment character varying(60)
);


