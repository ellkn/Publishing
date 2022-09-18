CREATE DATABASE "pHouse"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;


CREATE TABLE IF NOT EXISTS public.users
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    lastname text NOT NULL,
    firstname text NOT NULL,
    email text NOT NULL,
    password text NOT NULL,
    role integer NOT NULL DEFAULT 1,
    PRIMARY KEY (id),
    CONSTRAINT email UNIQUE (email)
);

CREATE TABLE IF NOT EXISTS public.roles
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    role text NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.typographys
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    name text NOT NULL,
    address text NOT NULL,
    phone text NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.authors
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    user_id integer NOT NULL,
    info text,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.editions
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    code text,
    author_id integer,
    name text,
    "pageCount" integer,
    order_id integer,
    count_t integer,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.orders
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    order_taker_id integer,
    print_type integer,
    edition_id integer,
    typography_id integer,
    date_in date,
    date_out date,
    status_id integer,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.order_takers
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    users_id integer NOT NULL,
    address text NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.print_types
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    name text NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.statuses
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    name text NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS public.users
    ADD CONSTRAINT role_id FOREIGN KEY (role)
    REFERENCES public.roles (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.authors
    ADD CONSTRAINT user_id FOREIGN KEY (user_id)
    REFERENCES public.users (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.editions
    ADD CONSTRAINT author_id FOREIGN KEY (author_id)
    REFERENCES public.authors (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.editions
    ADD CONSTRAINT order_id FOREIGN KEY (order_id)
    REFERENCES public.orders (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.orders
    ADD CONSTRAINT order_taker_id FOREIGN KEY (order_taker_id)
    REFERENCES public.order_takers (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.orders
    ADD CONSTRAINT print_type FOREIGN KEY (print_type)
    REFERENCES public.print_types (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.orders
    ADD CONSTRAINT edition_id FOREIGN KEY (edition_id)
    REFERENCES public.editions (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.orders
    ADD CONSTRAINT typography_id FOREIGN KEY (typography_id)
    REFERENCES public.typographys (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.orders
    ADD CONSTRAINT status_id FOREIGN KEY (status_id)
    REFERENCES public.statuses (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.order_takers
    ADD CONSTRAINT user_id FOREIGN KEY (users_id)
    REFERENCES public.users (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


-- ЗАПОЛНЕНИЕ
INSERT INTO public.roles (role) VALUES ('USER'::text) returning id;
INSERT INTO public.roles (role) VALUES ('ADMIN'::text) returning id;
INSERT INTO public.roles (role) VALUES ('ORGANIZATION'::text) returning id;
INSERT INTO public.roles (role) VALUES ('PRIVATE'::text) returning id;

INSERT INTO public.statuses (name) VALUES ('OPEN'::text) returning id;
INSERT INTO public.statuses (name) VALUES ('WAITING PAY'::text) returning id;
INSERT INTO public.statuses (name) VALUES ('PAID'::text) returning id;
INSERT INTO public.statuses (name) VALUES ('IN PROCESS'::text) returning id;
INSERT INTO public.statuses (name) VALUES ('CANCELED'::text) returning id;

INSERT INTO public.print_types (name) VALUES ('BOOK'::text) returning id;
INSERT INTO public.print_types (name) VALUES ('BROCHURE'::text) returning id;
INSERT INTO public.print_types (name) VALUES ('ADVERTISING BOOKLET'::text) returning id;