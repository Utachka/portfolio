--
-- PostgreSQL database dump
--

-- Dumped from database version 14.7
-- Dumped by pg_dump version 14.7

-- Started on 2023-05-22 10:57:41

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 212 (class 1259 OID 65710)
-- Name: aircrafts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.aircrafts (
    id_air bigint NOT NULL,
    name character varying(50) NOT NULL,
    count_sits integer NOT NULL
);


ALTER TABLE public.aircrafts OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 65709)
-- Name: aircrafts_id_air_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.aircrafts ALTER COLUMN id_air ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.aircrafts_id_air_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 214 (class 1259 OID 65716)
-- Name: countrys; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.countrys (
    id_country bigint NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.countrys OWNER TO postgres;

--
-- TOC entry 213 (class 1259 OID 65715)
-- Name: countrys_id_country_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.countrys ALTER COLUMN id_country ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.countrys_id_country_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 210 (class 1259 OID 65704)
-- Name: flights; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.flights (
    id_flight bigint NOT NULL,
    country_source_id bigint NOT NULL,
    country_target_id bigint NOT NULL,
    id_air bigint NOT NULL,
    departure_time timestamp without time zone NOT NULL,
    arrival_time timestamp without time zone NOT NULL
);


ALTER TABLE public.flights OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 65703)
-- Name: flights_id_flight_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.flights ALTER COLUMN id_flight ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.flights_id_flight_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 216 (class 1259 OID 65722)
-- Name: tickets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tickets (
    id_ticket bigint NOT NULL,
    id_flight bigint NOT NULL,
    seat_number integer NOT NULL
);


ALTER TABLE public.tickets OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 65721)
-- Name: tickets_id_ticket_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.tickets ALTER COLUMN id_ticket ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.tickets_id_ticket_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 3329 (class 0 OID 65710)
-- Dependencies: 212
-- Data for Name: aircrafts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.aircrafts (id_air, name, count_sits) FROM stdin;
1	FG_1	10
2	FG_2	120
3	FG_3	130
\.


--
-- TOC entry 3331 (class 0 OID 65716)
-- Dependencies: 214
-- Data for Name: countrys; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.countrys (id_country, name) FROM stdin;
1	Russia
2	Turkey
3	Indonesia
4	France
5	German
\.


--
-- TOC entry 3327 (class 0 OID 65704)
-- Dependencies: 210
-- Data for Name: flights; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.flights (id_flight, country_source_id, country_target_id, id_air, departure_time, arrival_time) FROM stdin;
1	1	2	1	2021-01-01 12:30:00	2021-01-01 19:16:00
2	2	1	2	2021-01-10 10:00:00	2021-01-10 17:50:00
3	3	4	3	2021-02-01 09:30:00	2021-02-01 13:00:00
4	1	2	123	2023-05-02 12:00:00	2023-05-02 15:00:00
\.


--
-- TOC entry 3333 (class 0 OID 65722)
-- Dependencies: 216
-- Data for Name: tickets; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tickets (id_ticket, id_flight, seat_number) FROM stdin;
1	1	1
2	1	2
3	1	3
4	1	4
5	1	5
6	1	6
7	1	7
8	1	8
9	1	9
10	1	10
\.


--
-- TOC entry 3339 (class 0 OID 0)
-- Dependencies: 211
-- Name: aircrafts_id_air_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.aircrafts_id_air_seq', 3, true);


--
-- TOC entry 3340 (class 0 OID 0)
-- Dependencies: 213
-- Name: countrys_id_country_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.countrys_id_country_seq', 5, true);


--
-- TOC entry 3341 (class 0 OID 0)
-- Dependencies: 209
-- Name: flights_id_flight_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.flights_id_flight_seq', 5, true);


--
-- TOC entry 3342 (class 0 OID 0)
-- Dependencies: 215
-- Name: tickets_id_ticket_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tickets_id_ticket_seq', 10, true);


--
-- TOC entry 3182 (class 2606 OID 65714)
-- Name: aircrafts aircrafts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.aircrafts
    ADD CONSTRAINT aircrafts_pkey PRIMARY KEY (id_air);


--
-- TOC entry 3184 (class 2606 OID 65720)
-- Name: countrys countrys_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.countrys
    ADD CONSTRAINT countrys_pkey PRIMARY KEY (id_country);


--
-- TOC entry 3180 (class 2606 OID 65708)
-- Name: flights flights_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.flights
    ADD CONSTRAINT flights_pkey PRIMARY KEY (id_flight);


--
-- TOC entry 3186 (class 2606 OID 65726)
-- Name: tickets tickets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tickets
    ADD CONSTRAINT tickets_pkey PRIMARY KEY (id_ticket);


-- Completed on 2023-05-22 10:57:41

--
-- PostgreSQL database dump complete
--

