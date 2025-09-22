
CREATE TABLE public.categories (
    category_id integer NOT NULL,
    name character varying NOT NULL,
    type character varying,
    alias character varying NOT NULL,
    parent character varying
);


ALTER TABLE public.categories OWNER TO postgres;

CREATE SEQUENCE public.categories_category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.categories_category_id_seq OWNER TO postgres;

ALTER SEQUENCE public.categories_category_id_seq OWNED BY public.categories.category_id;

CREATE SEQUENCE public.food_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.food_id_seq OWNER TO postgres;

CREATE TABLE public.culture_stories (
    story_id integer NOT NULL,
    food_id integer DEFAULT nextval('public.food_id_seq'::regclass) NOT NULL,
    food_name character varying NOT NULL,
    image_url character varying,
    origin_country character varying,
    story_summary character varying,
    story character varying
);

ALTER TABLE public.culture_stories OWNER TO postgres;

CREATE SEQUENCE public.culture_stories_story_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.culture_stories_story_id_seq OWNER TO postgres;

ALTER SEQUENCE public.culture_stories_story_id_seq OWNED BY public.culture_stories.story_id;

CREATE TABLE public.favorites (
    favorite_id integer NOT NULL,
    user_id integer,
    restaurant_id integer
);

ALTER TABLE public.favorites OWNER TO postgres;

CREATE SEQUENCE public.favorites_favorite_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.favorites_favorite_id_seq OWNER TO postgres;

ALTER SEQUENCE public.favorites_favorite_id_seq OWNED BY public.favorites.favorite_id;

CREATE TABLE public.foods (
    food_id integer NOT NULL,
    restaurant_id integer,
    name character varying NOT NULL,
    description character varying,
    price double precision,
    category_id integer
);

ALTER TABLE public.foods OWNER TO postgres;

CREATE SEQUENCE public.foods_food_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.foods_food_id_seq OWNER TO postgres;

ALTER SEQUENCE public.foods_food_id_seq OWNED BY public.foods.food_id;

CREATE TABLE public.locations (
    location_id integer NOT NULL,
    address1 character varying,
    address2 character varying,
    address3 character varying,
    city character varying,
    zip_code character varying,
    country character varying,
    state character varying,
    display_address character varying
);

ALTER TABLE public.locations OWNER TO postgres;

CREATE SEQUENCE public.locations_location_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.locations_location_id_seq OWNER TO postgres;

ALTER SEQUENCE public.locations_location_id_seq OWNED BY public.locations.location_id;

CREATE TABLE public.operating_hours (
    id integer NOT NULL,
    location_id integer,
    day_of_week integer,
    open_time character varying,
    close_time character varying,
    is_overnight boolean,
    restaurant_id integer
);

ALTER TABLE public.operating_hours OWNER TO postgres;

CREATE SEQUENCE public.operating_hours_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.operating_hours_id_seq OWNER TO postgres;

ALTER SEQUENCE public.operating_hours_id_seq OWNED BY public.operating_hours.id;

CREATE TABLE public.payments (
    payment_id integer NOT NULL,
    user_id integer,
    amount double precision,
    payment_method character varying,
    "timestamp" timestamp without time zone,
    status character varying
);

ALTER TABLE public.payments OWNER TO postgres;

CREATE SEQUENCE public.payments_payment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.payments_payment_id_seq OWNER TO postgres;

ALTER SEQUENCE public.payments_payment_id_seq OWNED BY public.payments.payment_id;

CREATE TABLE public.photos (
    photo_id integer NOT NULL,
    restaurant_id integer,
    user_id integer,
    url character varying NOT NULL,
    caption character varying,
    uploaded_at timestamp without time zone
);

ALTER TABLE public.photos OWNER TO postgres;

CREATE SEQUENCE public.photos_photo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.photos_photo_id_seq OWNER TO postgres;

ALTER SEQUENCE public.photos_photo_id_seq OWNED BY public.photos.photo_id;

CREATE TABLE public.reservations (
    reservation_id integer NOT NULL,
    user_id integer,
    restaurant_id integer,
    reservation_time timestamp without time zone NOT NULL,
    party_size integer,
    status character varying
);


ALTER TABLE public.reservations OWNER TO postgres;

CREATE SEQUENCE public.reservations_reservation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reservations_reservation_id_seq OWNER TO postgres;

ALTER SEQUENCE public.reservations_reservation_id_seq OWNED BY public.reservations.reservation_id;

CREATE TABLE public.restaurant_categories (
    id integer NOT NULL,
    restaurant_id integer,
    category_id integer
);

ALTER TABLE public.restaurant_categories OWNER TO postgres;

CREATE SEQUENCE public.restaurant_categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.restaurant_categories_id_seq OWNER TO postgres;

ALTER SEQUENCE public.restaurant_categories_id_seq OWNED BY public.restaurant_categories.id;

CREATE TABLE public.restaurants (
    restaurant_id integer NOT NULL,
    yelp_id character varying,
    name character varying NOT NULL,
    alias character varying,
    image_url character varying,
    is_closed boolean,
    url character varying,
    review_count integer,
    rating double precision,
    price character varying,
    phone character varying,
    display_phone character varying,
    latitude double precision,
    longitude double precision,
    distance double precision,
    attributes json,
    location_id integer,
    restaurant_description character varying
);

ALTER TABLE public.restaurants OWNER TO postgres;

COMMENT ON COLUMN public.restaurants.restaurant_description IS 'LLM generated restaurant summary';

CREATE SEQUENCE public.restaurants_restaurant_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.restaurants_restaurant_id_seq OWNER TO postgres;

--
-- TOC entry 5052 (class 0 OID 0)
-- Dependencies: 232
-- Name: restaurants_restaurant_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.restaurants_restaurant_id_seq OWNED BY public.restaurants.restaurant_id;


--
-- TOC entry 243 (class 1259 OID 29876)
-- Name: reviews; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reviews (
    review_id integer NOT NULL,
    user_id integer,
    restaurant_id integer,
    rating double precision NOT NULL,
    comment character varying,
    created_at timestamp without time zone
);


ALTER TABLE public.reviews OWNER TO postgres;

--
-- TOC entry 242 (class 1259 OID 29875)
-- Name: reviews_review_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reviews_review_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reviews_review_id_seq OWNER TO postgres;

--
-- TOC entry 5053 (class 0 OID 0)
-- Dependencies: 242
-- Name: reviews_review_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reviews_review_id_seq OWNED BY public.reviews.review_id;


--
-- TOC entry 223 (class 1259 OID 28672)
-- Name: transaction_types; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.transaction_types (
    id integer NOT NULL,
    name character varying
);


ALTER TABLE public.transaction_types OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 28671)
-- Name: transaction_types_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.transaction_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.transaction_types_id_seq OWNER TO postgres;

--
-- TOC entry 5054 (class 0 OID 0)
-- Dependencies: 222
-- Name: transaction_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.transaction_types_id_seq OWNED BY public.transaction_types.id;


--
-- TOC entry 219 (class 1259 OID 28622)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying NOT NULL,
    email character varying NOT NULL,
    hashed_password character varying NOT NULL,
    role character varying,
    created_at timestamp without time zone
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 28621)
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_user_id_seq OWNER TO postgres;

--
-- TOC entry 5055 (class 0 OID 0)
-- Dependencies: 218
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- TOC entry 4809 (class 2604 OID 28651)
-- Name: categories category_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories ALTER COLUMN category_id SET DEFAULT nextval('public.categories_category_id_seq'::regclass);


--
-- TOC entry 4821 (class 2604 OID 29917)
-- Name: culture_stories story_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.culture_stories ALTER COLUMN story_id SET DEFAULT nextval('public.culture_stories_story_id_seq'::regclass);


--
-- TOC entry 4812 (class 2604 OID 28795)
-- Name: favorites favorite_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favorites ALTER COLUMN favorite_id SET DEFAULT nextval('public.favorites_favorite_id_seq'::regclass);


--
-- TOC entry 4811 (class 2604 OID 28735)
-- Name: foods food_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.foods ALTER COLUMN food_id SET DEFAULT nextval('public.foods_food_id_seq'::regclass);


--
-- TOC entry 4813 (class 2604 OID 29741)
-- Name: locations location_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locations ALTER COLUMN location_id SET DEFAULT nextval('public.locations_location_id_seq'::regclass);


--
-- TOC entry 4819 (class 2604 OID 29842)
-- Name: operating_hours id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.operating_hours ALTER COLUMN id SET DEFAULT nextval('public.operating_hours_id_seq'::regclass);


--
-- TOC entry 4814 (class 2604 OID 29753)
-- Name: payments payment_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments ALTER COLUMN payment_id SET DEFAULT nextval('public.payments_payment_id_seq'::regclass);


--
-- TOC entry 4818 (class 2604 OID 29822)
-- Name: photos photo_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.photos ALTER COLUMN photo_id SET DEFAULT nextval('public.photos_photo_id_seq'::regclass);


--
-- TOC entry 4817 (class 2604 OID 29802)
-- Name: reservations reservation_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reservations ALTER COLUMN reservation_id SET DEFAULT nextval('public.reservations_reservation_id_seq'::regclass);


--
-- TOC entry 4816 (class 2604 OID 29783)
-- Name: restaurant_categories id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.restaurant_categories ALTER COLUMN id SET DEFAULT nextval('public.restaurant_categories_id_seq'::regclass);


--
-- TOC entry 4815 (class 2604 OID 29767)
-- Name: restaurants restaurant_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.restaurants ALTER COLUMN restaurant_id SET DEFAULT nextval('public.restaurants_restaurant_id_seq'::regclass);


--
-- TOC entry 4820 (class 2604 OID 29879)
-- Name: reviews review_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews ALTER COLUMN review_id SET DEFAULT nextval('public.reviews_review_id_seq'::regclass);


--
-- TOC entry 4810 (class 2604 OID 28675)
-- Name: transaction_types id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transaction_types ALTER COLUMN id SET DEFAULT nextval('public.transaction_types_id_seq'::regclass);


--
-- TOC entry 4808 (class 2604 OID 28625)
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- TOC entry 4831 (class 2606 OID 28655)
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (category_id);


--
-- TOC entry 4874 (class 2606 OID 29922)
-- Name: culture_stories culture_stories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.culture_stories
    ADD CONSTRAINT culture_stories_pkey PRIMARY KEY (story_id);


--
-- TOC entry 4843 (class 2606 OID 28797)
-- Name: favorites favorites_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favorites
    ADD CONSTRAINT favorites_pkey PRIMARY KEY (favorite_id);


--
-- TOC entry 4840 (class 2606 OID 28739)
-- Name: foods foods_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.foods
    ADD CONSTRAINT foods_pkey PRIMARY KEY (food_id);


--
-- TOC entry 4847 (class 2606 OID 29745)
-- Name: locations locations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locations
    ADD CONSTRAINT locations_pkey PRIMARY KEY (location_id);


--
-- TOC entry 4867 (class 2606 OID 29846)
-- Name: operating_hours operating_hours_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.operating_hours
    ADD CONSTRAINT operating_hours_pkey PRIMARY KEY (id);


--
-- TOC entry 4851 (class 2606 OID 29757)
-- Name: payments payments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (payment_id);


--
-- TOC entry 4865 (class 2606 OID 29826)
-- Name: photos photos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.photos
    ADD CONSTRAINT photos_pkey PRIMARY KEY (photo_id);


--
-- TOC entry 4862 (class 2606 OID 29806)
-- Name: reservations reservations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reservations
    ADD CONSTRAINT reservations_pkey PRIMARY KEY (reservation_id);


--
-- TOC entry 4857 (class 2606 OID 29785)
-- Name: restaurant_categories restaurant_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.restaurant_categories
    ADD CONSTRAINT restaurant_categories_pkey PRIMARY KEY (id);


--
-- TOC entry 4855 (class 2606 OID 29771)
-- Name: restaurants restaurants_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.restaurants
    ADD CONSTRAINT restaurants_pkey PRIMARY KEY (restaurant_id);


--
-- TOC entry 4872 (class 2606 OID 29883)
-- Name: reviews reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (review_id);


--
-- TOC entry 4836 (class 2606 OID 28681)
-- Name: transaction_types transaction_types_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transaction_types
    ADD CONSTRAINT transaction_types_name_key UNIQUE (name);


--
-- TOC entry 4838 (class 2606 OID 28679)
-- Name: transaction_types transaction_types_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transaction_types
    ADD CONSTRAINT transaction_types_pkey PRIMARY KEY (id);


--
-- TOC entry 4834 (class 2606 OID 28657)
-- Name: categories uix_category_alias; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT uix_category_alias UNIQUE (alias);


--
-- TOC entry 4849 (class 2606 OID 29747)
-- Name: locations uix_location_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locations
    ADD CONSTRAINT uix_location_unique UNIQUE (address1, city, zip_code);


--
-- TOC entry 4869 (class 2606 OID 29848)
-- Name: operating_hours uix_operating_hours; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.operating_hours
    ADD CONSTRAINT uix_operating_hours UNIQUE (restaurant_id, location_id, day_of_week, open_time, close_time);


--
-- TOC entry 4859 (class 2606 OID 29787)
-- Name: restaurant_categories uix_restaurant_category; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.restaurant_categories
    ADD CONSTRAINT uix_restaurant_category UNIQUE (restaurant_id, category_id);


--
-- TOC entry 4825 (class 2606 OID 28633)
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- TOC entry 4827 (class 2606 OID 28629)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- TOC entry 4829 (class 2606 OID 28631)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- TOC entry 4832 (class 1259 OID 28658)
-- Name: ix_categories_category_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_categories_category_id ON public.categories USING btree (category_id);


--
-- TOC entry 4875 (class 1259 OID 29924)
-- Name: ix_culture_stories_food_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_culture_stories_food_id ON public.culture_stories USING btree (food_id);


--
-- TOC entry 4876 (class 1259 OID 29923)
-- Name: ix_culture_stories_story_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_culture_stories_story_id ON public.culture_stories USING btree (story_id);


--
-- TOC entry 4844 (class 1259 OID 28808)
-- Name: ix_favorites_favorite_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_favorites_favorite_id ON public.favorites USING btree (favorite_id);


--
-- TOC entry 4841 (class 1259 OID 28750)
-- Name: ix_foods_food_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_foods_food_id ON public.foods USING btree (food_id);


--
-- TOC entry 4845 (class 1259 OID 29748)
-- Name: ix_locations_location_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_locations_location_id ON public.locations USING btree (location_id);


--
-- TOC entry 4863 (class 1259 OID 29837)
-- Name: ix_photos_photo_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_photos_photo_id ON public.photos USING btree (photo_id);


--
-- TOC entry 4860 (class 1259 OID 29817)
-- Name: ix_reservations_reservation_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_reservations_reservation_id ON public.reservations USING btree (reservation_id);


--
-- TOC entry 4852 (class 1259 OID 29778)
-- Name: ix_restaurants_restaurant_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_restaurants_restaurant_id ON public.restaurants USING btree (restaurant_id);


--
-- TOC entry 4853 (class 1259 OID 29777)
-- Name: ix_restaurants_yelp_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_restaurants_yelp_id ON public.restaurants USING btree (yelp_id);


--
-- TOC entry 4870 (class 1259 OID 29894)
-- Name: ix_reviews_review_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_reviews_review_id ON public.reviews USING btree (review_id);


--
-- TOC entry 4823 (class 1259 OID 28634)
-- Name: ix_users_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_user_id ON public.users USING btree (user_id);


--
-- TOC entry 4878 (class 2606 OID 28798)
-- Name: favorites favorites_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favorites
    ADD CONSTRAINT favorites_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- TOC entry 4877 (class 2606 OID 28745)
-- Name: foods foods_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.foods
    ADD CONSTRAINT foods_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(category_id);


--
-- TOC entry 4887 (class 2606 OID 29849)
-- Name: operating_hours operating_hours_location_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.operating_hours
    ADD CONSTRAINT operating_hours_location_id_fkey FOREIGN KEY (location_id) REFERENCES public.locations(location_id);


--
-- TOC entry 4888 (class 2606 OID 29854)
-- Name: operating_hours operating_hours_restaurant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.operating_hours
    ADD CONSTRAINT operating_hours_restaurant_id_fkey FOREIGN KEY (restaurant_id) REFERENCES public.restaurants(restaurant_id);


--
-- TOC entry 4879 (class 2606 OID 29758)
-- Name: payments payments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- TOC entry 4885 (class 2606 OID 29827)
-- Name: photos photos_restaurant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.photos
    ADD CONSTRAINT photos_restaurant_id_fkey FOREIGN KEY (restaurant_id) REFERENCES public.restaurants(restaurant_id);


--
-- TOC entry 4886 (class 2606 OID 29832)
-- Name: photos photos_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.photos
    ADD CONSTRAINT photos_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- TOC entry 4883 (class 2606 OID 29812)
-- Name: reservations reservations_restaurant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reservations
    ADD CONSTRAINT reservations_restaurant_id_fkey FOREIGN KEY (restaurant_id) REFERENCES public.restaurants(restaurant_id);


--
-- TOC entry 4884 (class 2606 OID 29807)
-- Name: reservations reservations_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reservations
    ADD CONSTRAINT reservations_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- TOC entry 4881 (class 2606 OID 29793)
-- Name: restaurant_categories restaurant_categories_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.restaurant_categories
    ADD CONSTRAINT restaurant_categories_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(category_id);


--
-- TOC entry 4882 (class 2606 OID 29788)
-- Name: restaurant_categories restaurant_categories_restaurant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.restaurant_categories
    ADD CONSTRAINT restaurant_categories_restaurant_id_fkey FOREIGN KEY (restaurant_id) REFERENCES public.restaurants(restaurant_id);


--
-- TOC entry 4880 (class 2606 OID 29772)
-- Name: restaurants restaurants_location_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.restaurants
    ADD CONSTRAINT restaurants_location_id_fkey FOREIGN KEY (location_id) REFERENCES public.locations(location_id);


--
-- TOC entry 4889 (class 2606 OID 29889)
-- Name: reviews reviews_restaurant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_restaurant_id_fkey FOREIGN KEY (restaurant_id) REFERENCES public.restaurants(restaurant_id);


--
-- TOC entry 4890 (class 2606 OID 29884)
-- Name: reviews reviews_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


-- Completed on 2025-07-13 11:31:46

--
-- PostgreSQL database dump complete
--

