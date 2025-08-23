-- =============================
-- Customers (PP & PM)
-- =============================
CREATE TABLE public.customers
(
	id BIGSERIAL PRIMARY KEY,
	created_at TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP NOT NULL,
	is_enabled BOOLEAN DEFAULT TRUE NOT NULL,
	customer_code VARCHAR(50) UNIQUE NOT NULL,
	first_name VARCHAR(100),
	last_name VARCHAR(100),
	business_name VARCHAR(255),
	whole_name VARCHAR(255),
	entity_type CHAR(2) CHECK (entity_type IN ('PP', 'PM')) NOT NULL, -- PP = Personne Physique, PM = Personne Morale
	id_number VARCHAR(50) NOT NULL, -- CIN or passport for PP, Fiscal number For PM
	birth_date DATE,
	birth_place VARCHAR(50),
	gender CHAR(1) CHECK (gender IN ('M', 'F')), -- Male, Female
	family_status CHAR(1) CHECK (family_status IN ('S', 'M', 'D', 'W')), -- Single, Married, Divorced, Widowed
	sector VARCHAR(255), -- LIB_SECTEUR_ACTIVITE for both PP and PM
	sub_sector VARCHAR(500), -- PP : LIB_PROFESSION, PM : LIB_ACTIVITE
	governorate VARCHAR(20),
	city VARCHAR(50)
);

-- =============================
-- Branches & Products
-- =============================
CREATE TABLE public.branches
(
	id BIGSERIAL PRIMARY KEY,
	created_at TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP NOT NULL,
	is_enabled BOOLEAN DEFAULT TRUE NOT NULL,
	branch_name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE public.sub_branches
(
	id BIGSERIAL PRIMARY KEY,
	created_at TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP NOT NULL,
	is_enabled BOOLEAN DEFAULT TRUE NOT NULL,
	sub_branch_name VARCHAR(255) NOT NULL,
	branch_id BIGINT NOT NULL REFERENCES public.branches(id),
	UNIQUE(branch_id, sub_branch_name)
);

CREATE TABLE public.products
(
	id BIGSERIAL PRIMARY KEY,
	created_at TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP NOT NULL,
	is_enabled BOOLEAN DEFAULT TRUE NOT NULL,
	product_name VARCHAR(255) NOT NULL,
	sub_branch_id BIGINT NOT NULL REFERENCES public.sub_branches(id),
	UNIQUE(product_name, sub_branch_id)
);

-- =============================
-- Contracts
-- =============================
CREATE TABLE public.contracts
(
	id BIGSERIAL PRIMARY KEY,
	created_at TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP NOT NULL,
	is_enabled BOOLEAN DEFAULT TRUE NOT NULL,
	contract_code VARCHAR(50) UNIQUE NOT NULL, -- NUM_CONTRAT
	customer_id BIGINT NOT NULL REFERENCES public.customers(id),
	product_id BIGINT NOT NULL REFERENCES public.products(id),
	effective_date DATE, -- EFFET_CONTRAT
	expiration_date DATE, -- DATE_EXPIRATION
	due_date DATE, -- PROCHAIN_TERME
	contract_status VARCHAR(20) CHECK (contract_status IN ('Active','Terminated','Suspended', 'Expired', 'Reduced', 'Pending')),
	payment_status VARCHAR(10) CHECK (payment_status IN ('Paid', 'Unpaid')),
	total_premium NUMERIC(20,3), -- SOMME_QUITTANCES
	insured_capital NUMERIC(20,3) CHECK (insured_capital >= 0) -- CAPITAL_ASSURE
);

-- =============================
-- Guarantees linked to Contracts
-- =============================
CREATE TABLE guarantees
(
	id BIGSERIAL PRIMARY KEY,
	created_at TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP NOT NULL,
	guarantee_code VARCHAR(50) NOT NULL,
	contract_id BIGINT NOT NULL REFERENCES public.contracts(id),
	guarantee_name VARCHAR(255) NOT NULL,
	capital_assured NUMERIC(15,2),
	UNIQUE(contract_id, guarantee_code, capital_assured)
);

-- =============================
-- Claims (Sinistres)
-- =============================
CREATE TABLE public.claims
(
	id BIGSERIAL PRIMARY KEY,
	created_at TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP NOT NULL,
	claim_code VARCHAR(50) UNIQUE NOT NULL, -- NUM_SINISTRE
	contract_id BIGINT NOT NULL REFERENCES public.contracts(id),
	nature VARCHAR(255), -- NATURE_SINISTRE
	type VARCHAR(255), -- LIB_TYPE_SINISTRE
	responsibility_rate NUMERIC(5,2), -- TAUX_RESPONSABILITE
	occurrence_date DATE, -- DATE_SURVENANCE
	declaration_date DATE, -- DATE_DECLARATION
	opening_date DATE, -- DATE_OUVERTURE
	claim_status VARCHAR(20) CHECK (claim_status IN ('CLOSED', 'UPDATED', 'OPENED', 'REOPENED', 'RESUMED')), -- LIB_ETAT_SINISTRE
	location VARCHAR(255),
	reopening_reason TEXT,
	collected_amount NUMERIC(20,3), -- MONTANT_ENCAISSE
	due_amount NUMERIC(20,3), -- MONTANT_A_ENCAISSER
	observations TEXT
);

-- =============================
-- Sales Opportunities
-- =============================
CREATE TABLE public.opportunities
(
	id BIGSERIAL PRIMARY KEY,
	created_at TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP NOT NULL,
	customer_id BIGINT NOT NULL REFERENCES public.customers(id),
	product_id BIGINT NOT NULL REFERENCES public.products(id),
	sales_pitch TEXT,
	status VARCHAR(15) CHECK (status IN ('Rejected', 'Proposed', 'In Discussion')),
	UNIQUE(customer_id, product_id, created_at)
);
