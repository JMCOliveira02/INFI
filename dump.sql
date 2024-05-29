--
-- PostgreSQL database dump
--

-- Dumped from database version 11.22 (Ubuntu 11.22-4.pgdg22.04+1)
-- Dumped by pg_dump version 11.22 (Ubuntu 11.22-4.pgdg22.04+1)

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

--
-- Name: erp_mes; Type: SCHEMA; Schema: -; Owner: infind202407
--

CREATE SCHEMA erp_mes;


ALTER SCHEMA erp_mes OWNER TO infind202407;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: client; Type: TABLE; Schema: erp_mes; Owner: infind202407
--

CREATE TABLE erp_mes.client (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE erp_mes.client OWNER TO infind202407;

--
-- Name: client_id_seq; Type: SEQUENCE; Schema: erp_mes; Owner: infind202407
--

CREATE SEQUENCE erp_mes.client_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE erp_mes.client_id_seq OWNER TO infind202407;

--
-- Name: client_id_seq; Type: SEQUENCE OWNED BY; Schema: erp_mes; Owner: infind202407
--

ALTER SEQUENCE erp_mes.client_id_seq OWNED BY erp_mes.client.id;


--
-- Name: client_order; Type: TABLE; Schema: erp_mes; Owner: infind202407
--

CREATE TABLE erp_mes.client_order (
    id integer NOT NULL,
    client_id integer,
    number character varying(50) NOT NULL,
    quantity integer NOT NULL,
    duedate integer NOT NULL,
    latepen integer,
    earlypen integer,
    piece character varying(50) NOT NULL
);


ALTER TABLE erp_mes.client_order OWNER TO infind202407;

--
-- Name: client_order_id_seq; Type: SEQUENCE; Schema: erp_mes; Owner: infind202407
--

CREATE SEQUENCE erp_mes.client_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE erp_mes.client_order_id_seq OWNER TO infind202407;

--
-- Name: client_order_id_seq; Type: SEQUENCE OWNED BY; Schema: erp_mes; Owner: infind202407
--

ALTER SEQUENCE erp_mes.client_order_id_seq OWNED BY erp_mes.client_order.id;


--
-- Name: delivery; Type: TABLE; Schema: erp_mes; Owner: infind202407
--

CREATE TABLE erp_mes.delivery (
    id integer NOT NULL,
    day integer,
    "P1_qty" integer,
    "P2_qty" integer
);


ALTER TABLE erp_mes.delivery OWNER TO infind202407;

--
-- Name: delivery_id_seq; Type: SEQUENCE; Schema: erp_mes; Owner: infind202407
--

CREATE SEQUENCE erp_mes.delivery_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE erp_mes.delivery_id_seq OWNER TO infind202407;

--
-- Name: delivery_id_seq; Type: SEQUENCE OWNED BY; Schema: erp_mes; Owner: infind202407
--

ALTER SEQUENCE erp_mes.delivery_id_seq OWNED BY erp_mes.delivery.id;


--
-- Name: expedition_order; Type: TABLE; Schema: erp_mes; Owner: infind202407
--

CREATE TABLE erp_mes.expedition_order (
    id integer NOT NULL,
    client_order_id integer,
    piece character varying(50) NOT NULL,
    quantity integer NOT NULL,
    expedition_date integer NOT NULL
);


ALTER TABLE erp_mes.expedition_order OWNER TO infind202407;

--
-- Name: expedition_order_id_seq; Type: SEQUENCE; Schema: erp_mes; Owner: infind202407
--

CREATE SEQUENCE erp_mes.expedition_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE erp_mes.expedition_order_id_seq OWNER TO infind202407;

--
-- Name: expedition_order_id_seq; Type: SEQUENCE OWNED BY; Schema: erp_mes; Owner: infind202407
--

ALTER SEQUENCE erp_mes.expedition_order_id_seq OWNED BY erp_mes.expedition_order.id;


--
-- Name: expedition_status; Type: TABLE; Schema: erp_mes; Owner: infind202407
--

CREATE TABLE erp_mes.expedition_status (
    id integer NOT NULL,
    expedition_order_id integer,
    end_date integer NOT NULL
);


ALTER TABLE erp_mes.expedition_status OWNER TO infind202407;

--
-- Name: expedition_status_id_seq; Type: SEQUENCE; Schema: erp_mes; Owner: infind202407
--

CREATE SEQUENCE erp_mes.expedition_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE erp_mes.expedition_status_id_seq OWNER TO infind202407;

--
-- Name: expedition_status_id_seq; Type: SEQUENCE OWNED BY; Schema: erp_mes; Owner: infind202407
--

ALTER SEQUENCE erp_mes.expedition_status_id_seq OWNED BY erp_mes.expedition_status.id;


--
-- Name: mes_active_recipes; Type: TABLE; Schema: erp_mes; Owner: infind202407
--

CREATE TABLE erp_mes.mes_active_recipes (
    order_id integer,
    global_id integer,
    recipe_id integer,
    machine_id integer,
    piece_in integer,
    piece_out integer,
    target_piece integer,
    tool integer,
    "time" integer,
    "end" boolean,
    current_transformation integer[],
    sended_date integer,
    finished_date integer
);


ALTER TABLE erp_mes.mes_active_recipes OWNER TO infind202407;

--
-- Name: mes_carriers_occupied; Type: TABLE; Schema: erp_mes; Owner: infind202407
--

CREATE TABLE erp_mes.mes_carriers_occupied (
    order_id integer
);


ALTER TABLE erp_mes.mes_carriers_occupied OWNER TO infind202407;

--
-- Name: mes_completed_deliveries; Type: TABLE; Schema: erp_mes; Owner: infind202407
--

CREATE TABLE erp_mes.mes_completed_deliveries (
    order_id integer,
    client_id integer,
    target_piece integer,
    quantity integer,
    expedition_date integer,
    quantity_sent integer,
    status character varying(50)
);


ALTER TABLE erp_mes.mes_completed_deliveries OWNER TO infind202407;

--
-- Name: mes_completed_production_orders; Type: TABLE; Schema: erp_mes; Owner: infind202407
--

CREATE TABLE erp_mes.mes_completed_production_orders (
    order_id integer,
    client_id integer,
    target_piece integer,
    quantity integer,
    start_date integer,
    quantity_done integer,
    status character varying(50)
);


ALTER TABLE erp_mes.mes_completed_production_orders OWNER TO infind202407;

--
-- Name: mes_completed_supply_orders; Type: TABLE; Schema: erp_mes; Owner: infind202407
--

CREATE TABLE erp_mes.mes_completed_supply_orders (
    id integer,
    day integer,
    num_pieces integer
);


ALTER TABLE erp_mes.mes_completed_supply_orders OWNER TO infind202407;

--
-- Name: mes_deliveries; Type: TABLE; Schema: erp_mes; Owner: infind202407
--

CREATE TABLE erp_mes.mes_deliveries (
    order_id integer,
    client_id integer,
    target_piece integer,
    quantity integer,
    expedition_date integer,
    quantity_sent integer,
    status character varying(50)
);


ALTER TABLE erp_mes.mes_deliveries OWNER TO infind202407;

--
-- Name: mes_production_orders; Type: TABLE; Schema: erp_mes; Owner: infind202407
--

CREATE TABLE erp_mes.mes_production_orders (
    order_id integer,
    client_id integer,
    target_piece integer,
    quantity integer,
    start_date integer,
    quantity_done integer,
    status character varying(50)
);


ALTER TABLE erp_mes.mes_production_orders OWNER TO infind202407;

--
-- Name: mes_recipes; Type: TABLE; Schema: erp_mes; Owner: infind202407
--

CREATE TABLE erp_mes.mes_recipes (
    order_id integer,
    global_id integer,
    recipe_id integer,
    machine_id integer,
    piece_in integer,
    piece_out integer,
    target_piece integer,
    tool integer,
    "time" integer,
    "end" boolean,
    current_transformation integer[],
    sended_date integer,
    finished_date integer
);


ALTER TABLE erp_mes.mes_recipes OWNER TO infind202407;

--
-- Name: mes_stashed_recipes; Type: TABLE; Schema: erp_mes; Owner: infind202407
--

CREATE TABLE erp_mes.mes_stashed_recipes (
    order_id integer,
    global_id integer,
    recipe_id integer,
    machine_id integer,
    piece_in integer,
    piece_out integer,
    target_piece integer,
    tool integer,
    "time" integer,
    "end" boolean,
    current_transformation integer[],
    sended_date integer,
    finished_date integer
);


ALTER TABLE erp_mes.mes_stashed_recipes OWNER TO infind202407;

--
-- Name: mes_supply_orders; Type: TABLE; Schema: erp_mes; Owner: infind202407
--

CREATE TABLE erp_mes.mes_supply_orders (
    id integer,
    day integer,
    num_pieces integer
);


ALTER TABLE erp_mes.mes_supply_orders OWNER TO infind202407;

--
-- Name: mes_terminated_recipes; Type: TABLE; Schema: erp_mes; Owner: infind202407
--

CREATE TABLE erp_mes.mes_terminated_recipes (
    order_id integer,
    global_id integer,
    recipe_id integer,
    machine_id integer,
    piece_in integer,
    piece_out integer,
    target_piece integer,
    tool integer,
    "time" integer,
    "end" boolean,
    current_transformation integer[],
    sended_date integer,
    finished_date integer
);


ALTER TABLE erp_mes.mes_terminated_recipes OWNER TO infind202407;

--
-- Name: mes_waiting_recipes; Type: TABLE; Schema: erp_mes; Owner: infind202407
--

CREATE TABLE erp_mes.mes_waiting_recipes (
    order_id integer,
    global_id integer,
    recipe_id integer,
    machine_id integer,
    piece_in integer,
    piece_out integer,
    target_piece integer,
    tool integer,
    "time" integer,
    "end" boolean,
    current_transformation integer[],
    sended_date integer,
    finished_date integer
);


ALTER TABLE erp_mes.mes_waiting_recipes OWNER TO infind202407;

--
-- Name: piece_info; Type: TABLE; Schema: erp_mes; Owner: infind202407
--

CREATE TABLE erp_mes.piece_info (
    client_order_id integer,
    piece character varying(50),
    total_time integer
);


ALTER TABLE erp_mes.piece_info OWNER TO infind202407;

--
-- Name: production_order; Type: TABLE; Schema: erp_mes; Owner: infind202407
--

CREATE TABLE erp_mes.production_order (
    id integer NOT NULL,
    client_order_id integer,
    piece character varying(50) NOT NULL,
    quantity integer NOT NULL,
    start_date integer NOT NULL
);


ALTER TABLE erp_mes.production_order OWNER TO infind202407;

--
-- Name: production_order_id_seq; Type: SEQUENCE; Schema: erp_mes; Owner: infind202407
--

CREATE SEQUENCE erp_mes.production_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE erp_mes.production_order_id_seq OWNER TO infind202407;

--
-- Name: production_order_id_seq; Type: SEQUENCE OWNED BY; Schema: erp_mes; Owner: infind202407
--

ALTER SEQUENCE erp_mes.production_order_id_seq OWNED BY erp_mes.production_order.id;


--
-- Name: production_raw_material; Type: TABLE; Schema: erp_mes; Owner: infind202407
--

CREATE TABLE erp_mes.production_raw_material (
    client_order_id integer,
    piece character varying(50) NOT NULL,
    quantity integer NOT NULL,
    start_date integer NOT NULL
);


ALTER TABLE erp_mes.production_raw_material OWNER TO infind202407;

--
-- Name: production_status; Type: TABLE; Schema: erp_mes; Owner: infind202407
--

CREATE TABLE erp_mes.production_status (
    id integer NOT NULL,
    production_order_id integer,
    end_date integer NOT NULL
);


ALTER TABLE erp_mes.production_status OWNER TO infind202407;

--
-- Name: production_status_id_seq; Type: SEQUENCE; Schema: erp_mes; Owner: infind202407
--

CREATE SEQUENCE erp_mes.production_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE erp_mes.production_status_id_seq OWNER TO infind202407;

--
-- Name: production_status_id_seq; Type: SEQUENCE OWNED BY; Schema: erp_mes; Owner: infind202407
--

ALTER SEQUENCE erp_mes.production_status_id_seq OWNED BY erp_mes.production_status.id;


--
-- Name: start_time; Type: TABLE; Schema: erp_mes; Owner: infind202407
--

CREATE TABLE erp_mes.start_time (
    initial_time timestamp without time zone,
    reset boolean,
    id integer
);


ALTER TABLE erp_mes.start_time OWNER TO infind202407;

--
-- Name: stock; Type: TABLE; Schema: erp_mes; Owner: infind202407
--

CREATE TABLE erp_mes.stock (
    id integer NOT NULL,
    day integer NOT NULL,
    piece character varying(50) NOT NULL,
    quantity integer NOT NULL
);


ALTER TABLE erp_mes.stock OWNER TO infind202407;

--
-- Name: stock_id_seq; Type: SEQUENCE; Schema: erp_mes; Owner: infind202407
--

CREATE SEQUENCE erp_mes.stock_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE erp_mes.stock_id_seq OWNER TO infind202407;

--
-- Name: stock_id_seq; Type: SEQUENCE OWNED BY; Schema: erp_mes; Owner: infind202407
--

ALTER SEQUENCE erp_mes.stock_id_seq OWNED BY erp_mes.stock.id;


--
-- Name: supplier; Type: TABLE; Schema: erp_mes; Owner: infind202407
--

CREATE TABLE erp_mes.supplier (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    piece character varying(50) NOT NULL,
    min_order integer NOT NULL,
    price_per_piece integer NOT NULL,
    delivery_time integer NOT NULL
);


ALTER TABLE erp_mes.supplier OWNER TO infind202407;

--
-- Name: supplier_id_seq; Type: SEQUENCE; Schema: erp_mes; Owner: infind202407
--

CREATE SEQUENCE erp_mes.supplier_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE erp_mes.supplier_id_seq OWNER TO infind202407;

--
-- Name: supplier_id_seq; Type: SEQUENCE OWNED BY; Schema: erp_mes; Owner: infind202407
--

ALTER SEQUENCE erp_mes.supplier_id_seq OWNED BY erp_mes.supplier.id;


--
-- Name: supply_order; Type: TABLE; Schema: erp_mes; Owner: infind202407
--

CREATE TABLE erp_mes.supply_order (
    id integer NOT NULL,
    client_order_id integer,
    piece character varying(50) NOT NULL,
    quantity integer NOT NULL,
    buy_date integer NOT NULL
);


ALTER TABLE erp_mes.supply_order OWNER TO infind202407;

--
-- Name: supply_order_id_seq; Type: SEQUENCE; Schema: erp_mes; Owner: infind202407
--

CREATE SEQUENCE erp_mes.supply_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE erp_mes.supply_order_id_seq OWNER TO infind202407;

--
-- Name: supply_order_id_seq; Type: SEQUENCE OWNED BY; Schema: erp_mes; Owner: infind202407
--

ALTER SEQUENCE erp_mes.supply_order_id_seq OWNED BY erp_mes.supply_order.id;


--
-- Name: total_costs; Type: TABLE; Schema: erp_mes; Owner: infind202407
--

CREATE TABLE erp_mes.total_costs (
    client_order_id integer,
    piece character varying,
    quantity integer,
    depreciation_days integer,
    raw_material_cost integer,
    depreciation_cost integer,
    production_cost integer
);


ALTER TABLE erp_mes.total_costs OWNER TO infind202407;

--
-- Name: transformations; Type: TABLE; Schema: erp_mes; Owner: infind202407
--

CREATE TABLE erp_mes.transformations (
    starting_piece character varying(50),
    produced_piece character varying(50),
    tool character varying(50),
    processing_time integer
);


ALTER TABLE erp_mes.transformations OWNER TO infind202407;

--
-- Name: client id; Type: DEFAULT; Schema: erp_mes; Owner: infind202407
--

ALTER TABLE ONLY erp_mes.client ALTER COLUMN id SET DEFAULT nextval('erp_mes.client_id_seq'::regclass);


--
-- Name: client_order id; Type: DEFAULT; Schema: erp_mes; Owner: infind202407
--

ALTER TABLE ONLY erp_mes.client_order ALTER COLUMN id SET DEFAULT nextval('erp_mes.client_order_id_seq'::regclass);


--
-- Name: delivery id; Type: DEFAULT; Schema: erp_mes; Owner: infind202407
--

ALTER TABLE ONLY erp_mes.delivery ALTER COLUMN id SET DEFAULT nextval('erp_mes.delivery_id_seq'::regclass);


--
-- Name: expedition_order id; Type: DEFAULT; Schema: erp_mes; Owner: infind202407
--

ALTER TABLE ONLY erp_mes.expedition_order ALTER COLUMN id SET DEFAULT nextval('erp_mes.expedition_order_id_seq'::regclass);


--
-- Name: expedition_status id; Type: DEFAULT; Schema: erp_mes; Owner: infind202407
--

ALTER TABLE ONLY erp_mes.expedition_status ALTER COLUMN id SET DEFAULT nextval('erp_mes.expedition_status_id_seq'::regclass);


--
-- Name: production_order id; Type: DEFAULT; Schema: erp_mes; Owner: infind202407
--

ALTER TABLE ONLY erp_mes.production_order ALTER COLUMN id SET DEFAULT nextval('erp_mes.production_order_id_seq'::regclass);


--
-- Name: production_status id; Type: DEFAULT; Schema: erp_mes; Owner: infind202407
--

ALTER TABLE ONLY erp_mes.production_status ALTER COLUMN id SET DEFAULT nextval('erp_mes.production_status_id_seq'::regclass);


--
-- Name: stock id; Type: DEFAULT; Schema: erp_mes; Owner: infind202407
--

ALTER TABLE ONLY erp_mes.stock ALTER COLUMN id SET DEFAULT nextval('erp_mes.stock_id_seq'::regclass);


--
-- Name: supplier id; Type: DEFAULT; Schema: erp_mes; Owner: infind202407
--

ALTER TABLE ONLY erp_mes.supplier ALTER COLUMN id SET DEFAULT nextval('erp_mes.supplier_id_seq'::regclass);


--
-- Name: supply_order id; Type: DEFAULT; Schema: erp_mes; Owner: infind202407
--

ALTER TABLE ONLY erp_mes.supply_order ALTER COLUMN id SET DEFAULT nextval('erp_mes.supply_order_id_seq'::regclass);


--
-- Data for Name: client; Type: TABLE DATA; Schema: erp_mes; Owner: infind202407
--



--
-- Data for Name: client_order; Type: TABLE DATA; Schema: erp_mes; Owner: infind202407
--



--
-- Data for Name: delivery; Type: TABLE DATA; Schema: erp_mes; Owner: infind202407
--



--
-- Data for Name: expedition_order; Type: TABLE DATA; Schema: erp_mes; Owner: infind202407
--



--
-- Data for Name: expedition_status; Type: TABLE DATA; Schema: erp_mes; Owner: infind202407
--



--
-- Data for Name: mes_active_recipes; Type: TABLE DATA; Schema: erp_mes; Owner: infind202407
--



--
-- Data for Name: mes_carriers_occupied; Type: TABLE DATA; Schema: erp_mes; Owner: infind202407
--



--
-- Data for Name: mes_completed_deliveries; Type: TABLE DATA; Schema: erp_mes; Owner: infind202407
--



--
-- Data for Name: mes_completed_production_orders; Type: TABLE DATA; Schema: erp_mes; Owner: infind202407
--



--
-- Data for Name: mes_completed_supply_orders; Type: TABLE DATA; Schema: erp_mes; Owner: infind202407
--



--
-- Data for Name: mes_deliveries; Type: TABLE DATA; Schema: erp_mes; Owner: infind202407
--



--
-- Data for Name: mes_production_orders; Type: TABLE DATA; Schema: erp_mes; Owner: infind202407
--



--
-- Data for Name: mes_recipes; Type: TABLE DATA; Schema: erp_mes; Owner: infind202407
--



--
-- Data for Name: mes_stashed_recipes; Type: TABLE DATA; Schema: erp_mes; Owner: infind202407
--



--
-- Data for Name: mes_supply_orders; Type: TABLE DATA; Schema: erp_mes; Owner: infind202407
--



--
-- Data for Name: mes_terminated_recipes; Type: TABLE DATA; Schema: erp_mes; Owner: infind202407
--



--
-- Data for Name: mes_waiting_recipes; Type: TABLE DATA; Schema: erp_mes; Owner: infind202407
--



--
-- Data for Name: piece_info; Type: TABLE DATA; Schema: erp_mes; Owner: infind202407
--



--
-- Data for Name: production_order; Type: TABLE DATA; Schema: erp_mes; Owner: infind202407
--



--
-- Data for Name: production_raw_material; Type: TABLE DATA; Schema: erp_mes; Owner: infind202407
--



--
-- Data for Name: production_status; Type: TABLE DATA; Schema: erp_mes; Owner: infind202407
--



--
-- Data for Name: start_time; Type: TABLE DATA; Schema: erp_mes; Owner: infind202407
--



--
-- Data for Name: stock; Type: TABLE DATA; Schema: erp_mes; Owner: infind202407
--



--
-- Data for Name: supplier; Type: TABLE DATA; Schema: erp_mes; Owner: infind202407
--

INSERT INTO erp_mes.supplier VALUES (1, 'SupplierA', 'P1', 16, 30, 4);
INSERT INTO erp_mes.supplier VALUES (2, 'SupplierA', 'P2', 16, 10, 4);
INSERT INTO erp_mes.supplier VALUES (3, 'SupplierB', 'P1', 8, 45, 2);
INSERT INTO erp_mes.supplier VALUES (4, 'SupplierB', 'P2', 8, 15, 2);
INSERT INTO erp_mes.supplier VALUES (5, 'SupplierC', 'P1', 4, 55, 1);
INSERT INTO erp_mes.supplier VALUES (6, 'SupplierC', 'P2', 4, 18, 1);


--
-- Data for Name: supply_order; Type: TABLE DATA; Schema: erp_mes; Owner: infind202407
--



--
-- Data for Name: total_costs; Type: TABLE DATA; Schema: erp_mes; Owner: infind202407
--



--
-- Data for Name: transformations; Type: TABLE DATA; Schema: erp_mes; Owner: infind202407
--

INSERT INTO erp_mes.transformations VALUES ('P1', 'P3', 'T1', 45);
INSERT INTO erp_mes.transformations VALUES ('P3', 'P4', 'T2', 15);
INSERT INTO erp_mes.transformations VALUES ('P3', 'P4', 'T3', 25);
INSERT INTO erp_mes.transformations VALUES ('P4', 'P5', 'T4', 25);
INSERT INTO erp_mes.transformations VALUES ('P4', 'P6', 'T2', 25);
INSERT INTO erp_mes.transformations VALUES ('P4', 'P7', 'T3', 15);
INSERT INTO erp_mes.transformations VALUES ('P2', 'P8', 'T1', 45);
INSERT INTO erp_mes.transformations VALUES ('P8', 'P7', 'T6', 15);
INSERT INTO erp_mes.transformations VALUES ('P8', 'P9', 'T5', 45);


--
-- Name: client_id_seq; Type: SEQUENCE SET; Schema: erp_mes; Owner: infind202407
--

SELECT pg_catalog.setval('erp_mes.client_id_seq', 1, false);


--
-- Name: client_order_id_seq; Type: SEQUENCE SET; Schema: erp_mes; Owner: infind202407
--

SELECT pg_catalog.setval('erp_mes.client_order_id_seq', 1, false);


--
-- Name: delivery_id_seq; Type: SEQUENCE SET; Schema: erp_mes; Owner: infind202407
--

SELECT pg_catalog.setval('erp_mes.delivery_id_seq', 1, false);


--
-- Name: expedition_order_id_seq; Type: SEQUENCE SET; Schema: erp_mes; Owner: infind202407
--

SELECT pg_catalog.setval('erp_mes.expedition_order_id_seq', 1, false);


--
-- Name: expedition_status_id_seq; Type: SEQUENCE SET; Schema: erp_mes; Owner: infind202407
--

SELECT pg_catalog.setval('erp_mes.expedition_status_id_seq', 1, false);


--
-- Name: production_order_id_seq; Type: SEQUENCE SET; Schema: erp_mes; Owner: infind202407
--

SELECT pg_catalog.setval('erp_mes.production_order_id_seq', 1, false);


--
-- Name: production_status_id_seq; Type: SEQUENCE SET; Schema: erp_mes; Owner: infind202407
--

SELECT pg_catalog.setval('erp_mes.production_status_id_seq', 1, false);


--
-- Name: stock_id_seq; Type: SEQUENCE SET; Schema: erp_mes; Owner: infind202407
--

SELECT pg_catalog.setval('erp_mes.stock_id_seq', 1, false);


--
-- Name: supplier_id_seq; Type: SEQUENCE SET; Schema: erp_mes; Owner: infind202407
--

SELECT pg_catalog.setval('erp_mes.supplier_id_seq', 6, true);


--
-- Name: supply_order_id_seq; Type: SEQUENCE SET; Schema: erp_mes; Owner: infind202407
--

SELECT pg_catalog.setval('erp_mes.supply_order_id_seq', 1, false);


--
-- Name: client_order client_order_pkey; Type: CONSTRAINT; Schema: erp_mes; Owner: infind202407
--

ALTER TABLE ONLY erp_mes.client_order
    ADD CONSTRAINT client_order_pkey PRIMARY KEY (id);


--
-- Name: client client_pkey; Type: CONSTRAINT; Schema: erp_mes; Owner: infind202407
--

ALTER TABLE ONLY erp_mes.client
    ADD CONSTRAINT client_pkey PRIMARY KEY (id);


--
-- Name: expedition_order expedition_order_pkey; Type: CONSTRAINT; Schema: erp_mes; Owner: infind202407
--

ALTER TABLE ONLY erp_mes.expedition_order
    ADD CONSTRAINT expedition_order_pkey PRIMARY KEY (id);


--
-- Name: expedition_status expedition_status_pkey; Type: CONSTRAINT; Schema: erp_mes; Owner: infind202407
--

ALTER TABLE ONLY erp_mes.expedition_status
    ADD CONSTRAINT expedition_status_pkey PRIMARY KEY (id);


--
-- Name: production_order production_order_pkey; Type: CONSTRAINT; Schema: erp_mes; Owner: infind202407
--

ALTER TABLE ONLY erp_mes.production_order
    ADD CONSTRAINT production_order_pkey PRIMARY KEY (id);


--
-- Name: production_status production_status_pkey; Type: CONSTRAINT; Schema: erp_mes; Owner: infind202407
--

ALTER TABLE ONLY erp_mes.production_status
    ADD CONSTRAINT production_status_pkey PRIMARY KEY (id);


--
-- Name: stock stock_pkey; Type: CONSTRAINT; Schema: erp_mes; Owner: infind202407
--

ALTER TABLE ONLY erp_mes.stock
    ADD CONSTRAINT stock_pkey PRIMARY KEY (id);


--
-- Name: supplier supplier_pkey; Type: CONSTRAINT; Schema: erp_mes; Owner: infind202407
--

ALTER TABLE ONLY erp_mes.supplier
    ADD CONSTRAINT supplier_pkey PRIMARY KEY (id);


--
-- Name: supply_order supply_order_pkey; Type: CONSTRAINT; Schema: erp_mes; Owner: infind202407
--

ALTER TABLE ONLY erp_mes.supply_order
    ADD CONSTRAINT supply_order_pkey PRIMARY KEY (id);


--
-- Name: client_order client_order_client_id_fkey; Type: FK CONSTRAINT; Schema: erp_mes; Owner: infind202407
--

ALTER TABLE ONLY erp_mes.client_order
    ADD CONSTRAINT client_order_client_id_fkey FOREIGN KEY (client_id) REFERENCES erp_mes.client(id);


--
-- Name: expedition_order expedition_order_client_order_id_fkey; Type: FK CONSTRAINT; Schema: erp_mes; Owner: infind202407
--

ALTER TABLE ONLY erp_mes.expedition_order
    ADD CONSTRAINT expedition_order_client_order_id_fkey FOREIGN KEY (client_order_id) REFERENCES erp_mes.client_order(id);


--
-- Name: expedition_status expedition_status_expedition_order_id_fkey; Type: FK CONSTRAINT; Schema: erp_mes; Owner: infind202407
--

ALTER TABLE ONLY erp_mes.expedition_status
    ADD CONSTRAINT expedition_status_expedition_order_id_fkey FOREIGN KEY (expedition_order_id) REFERENCES erp_mes.expedition_order(id);


--
-- Name: production_order production_order_client_order_id_fkey; Type: FK CONSTRAINT; Schema: erp_mes; Owner: infind202407
--

ALTER TABLE ONLY erp_mes.production_order
    ADD CONSTRAINT production_order_client_order_id_fkey FOREIGN KEY (client_order_id) REFERENCES erp_mes.client_order(id);


--
-- Name: production_status production_status_production_order_id_fkey; Type: FK CONSTRAINT; Schema: erp_mes; Owner: infind202407
--

ALTER TABLE ONLY erp_mes.production_status
    ADD CONSTRAINT production_status_production_order_id_fkey FOREIGN KEY (production_order_id) REFERENCES erp_mes.production_order(id);


--
-- Name: supply_order supply_order_client_order_id_fkey; Type: FK CONSTRAINT; Schema: erp_mes; Owner: infind202407
--

ALTER TABLE ONLY erp_mes.supply_order
    ADD CONSTRAINT supply_order_client_order_id_fkey FOREIGN KEY (client_order_id) REFERENCES erp_mes.client_order(id);


--
-- PostgreSQL database dump complete
--

