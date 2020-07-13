drop table if exists "points" cascade;
drop table if exists "routes" cascade;
drop table if exists "route_stages" cascade;
drop table if exists "cyclists" cascade;
drop table if exists "trips" cascade;


CREATE TABLE public.points (
    id_point integer PRIMARY KEY,
    name text,
    geog geography(Point),
    description text
);

CREATE INDEX ON points USING GIST(geog);

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
    start_date date
);
