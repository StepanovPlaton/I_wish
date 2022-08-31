--
-- PostgreSQL database dump
--

-- Dumped from database version 14.1 (Debian 14.1-1.pgdg110+1)
-- Dumped by pg_dump version 14.2

-- Started on 2022-08-31 09:59:49

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

-- DROP DATABASE "I_want";

--
-- TOC entry 3323 (class 1262 OID 16629)
-- Name: I_want; Type: DATABASE; Schema: -; Owner: ispgdbuser
--

CREATE DATABASE "I_want" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_US.utf8';


ALTER DATABASE "I_want" OWNER TO iwpgdbuser;

\connect "I_want"

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
-- TOC entry 210 (class 1259 OID 16666)
-- Name: Users; Type: TABLE; Schema: public; Owner: iwpgdbuser
--

CREATE TABLE public."Users" (
    "ID" integer NOT NULL,
    "Login" text NOT NULL,
    "HashOfPassword" text,
    "Avatar" text,
    "AboutMe" text,
    "Telegram" text
);


ALTER TABLE public."Users" OWNER TO iwpgdbuser;

--
-- TOC entry 209 (class 1259 OID 16665)
-- Name: Users_ID_seq; Type: SEQUENCE; Schema: public; Owner: iwpgdbuser
--

CREATE SEQUENCE public."Users_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Users_ID_seq" OWNER TO iwpgdbuser;

--
-- TOC entry 3324 (class 0 OID 0)
-- Dependencies: 209
-- Name: Users_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: iwpgdbuser
--

ALTER SEQUENCE public."Users_ID_seq" OWNED BY public."Users"."ID";


--
-- TOC entry 212 (class 1259 OID 16707)
-- Name: Wishes; Type: TABLE; Schema: public; Owner: iwpgdbuser
--

CREATE TABLE public."Wishes" (
    "ID" integer NOT NULL,
    "Wish" text NOT NULL,
    "Owner" integer NOT NULL,
    "Image" text,
    "Description" text,
    "Price" integer,
    "Link" text,
    "Anonymous" boolean DEFAULT false NOT NULL,
    "HidingDate" text
);


ALTER TABLE public."Wishes" OWNER TO iwpgdbuser;

--
-- TOC entry 211 (class 1259 OID 16706)
-- Name: Wishes_ID_seq; Type: SEQUENCE; Schema: public; Owner: iwpgdbuser
--

CREATE SEQUENCE public."Wishes_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Wishes_ID_seq" OWNER TO iwpgdbuser;

--
-- TOC entry 3325 (class 0 OID 0)
-- Dependencies: 211
-- Name: Wishes_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: iwpgdbuser
--

ALTER SEQUENCE public."Wishes_ID_seq" OWNED BY public."Wishes"."ID";


--
-- TOC entry 3172 (class 2604 OID 16669)
-- Name: Users ID; Type: DEFAULT; Schema: public; Owner: iwpgdbuser
--

ALTER TABLE ONLY public."Users" ALTER COLUMN "ID" SET DEFAULT nextval('public."Users_ID_seq"'::regclass);


--
-- TOC entry 3173 (class 2604 OID 16710)
-- Name: Wishes ID; Type: DEFAULT; Schema: public; Owner: iwpgdbuser
--

ALTER TABLE ONLY public."Wishes" ALTER COLUMN "ID" SET DEFAULT nextval('public."Wishes_ID_seq"'::regclass);


--
-- TOC entry 3176 (class 2606 OID 16673)
-- Name: Users pk_users_id; Type: CONSTRAINT; Schema: public; Owner: iwpgdbuser
--

ALTER TABLE ONLY public."Users"
    ADD CONSTRAINT pk_users_id PRIMARY KEY ("ID");


--
-- TOC entry 3178 (class 2606 OID 16714)
-- Name: Wishes pk_wishes_id; Type: CONSTRAINT; Schema: public; Owner: iwpgdbuser
--

ALTER TABLE ONLY public."Wishes"
    ADD CONSTRAINT pk_wishes_id PRIMARY KEY ("ID");


-- Completed on 2022-08-31 09:59:49

--
-- PostgreSQL database dump complete
--
