drop table if exists "points" cascade;
drop table if exists "routes" cascade;
drop table if exists "route_stages" cascade;
drop table if exists "cyclists" cascade;
drop table if exists "trips" cascade;


CREATE TABLE public.points (
    id_point integer PRIMARY KEY,
    name text,
    geog geography,
    description text
);

CREATE TABLE public.routes (
    id_route integer PRIMARY KEY
);

CREATE TABLE public.route_stages (
    id_route integer REFERENCES routes(id_route),
    day integer,
    id_point integer REFERENCES points(id_point)
);

CREATE TABLE public.cyclists (
    name text PRIMARY KEY
);

CREATE TABLE public.trips (
    id_trip SERIAL PRIMARY KEY,
    id_route integer REFERENCES routes(id_route),
    cyclist_name text REFERENCES cyclists(name),
    start_date date,
    end_date date
);


COPY public.points FROM stdin;
123	Instytut	 SRID=4326;POINT(17.053878 51.111066)	bardzo miłe miejsce
124	Biskupin	SRID=4326;POINT(17.108984 51.101050)	duzo zieleni
125	Jelcz	SRID=4326;POINT(17.038538 51.107883)	fajnie
126	Oporow	SRID=4326;POINT(17.038538 51.107883)	tez polecam
127	Pawlowice	SRID=4326;POINT(17.038538 51.107883)	fajnie
128	Leśnica	SRID=4326;POINT(17.038538 51.107883)	fajnie
129	Oława	SRID=4326;POINT(17.038538 51.107883)	fajnie
130	Brzeg	SRID=4326;POINT(17.038538 51.107883)	super
\.

COPY public.routes (id_route) FROM stdin;
26
27
28
\.

COPY public.route_stages (id_route, day, id_point) FROM stdin;
26	0	 123
26	1	 124
26	2	 125
26	3	 130
27	0	 127
27	1	 123
27	2	 128
28	0	 128
28	1	 129
\.

COPY public.cyclists (name) FROM stdin;
szymon
grzegorz
ania
kasia
marzena
\.

COPY public.trips (id_route, cyclist_name, start_date, end_date) FROM stdin;
28	ania	2020-02-29 00:00:00	2020-02-29 00:00:00
\.

