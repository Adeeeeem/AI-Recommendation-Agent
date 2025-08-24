# ================================
# main.py - FastAPI API for DB access
# ================================

from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
import os

# ================================
# STEP 1 : Database Connection
# ================================
DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/Next"
engine = create_engine(DATABASE_URL)

# ================================
# STEP 2 : FastAPI App
# ================================
app = FastAPI(
	title="Customer Product Recommendation API",
	description="Suggests the best product for customers based on their data.",
	version="1.0.0"
)

# ================================
# STEP 3 : Root endpoint
# ================================
@app.get("/")
def read_root():
	"""
	Root endpoint - confirms API is running.
	"""
	return {"message": "Welcome to the Customer Product Recommendation API !"}

# ================================
# STEP 4 : Get a specific customer by ID
# ================================
@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
	"""
	Fetch a single customer by ID
	"""
	with engine.connect() as conn:
		result = conn.execute(
			text("SELECT * FROM public.customers WHERE is_enabled = true AND id = :id"),
			{"id": customer_id}
		).mappings().first()
	if not result:
		raise HTTPException(status_code=404, detail="Customer not found")
	return dict(result)

# ================================
# STEP 5 : Fetch a single contract by ID
# ================================
@app.get("/contracts/{contract_id}")
def get_contract(contract_id: int):
	"""
	Fetch a single contract by ID
	"""
	with engine.connect() as conn:
		result = conn.execute(
			text("SELECT * FROM public.contracts WHERE is_enabled = true AND id = :id"),
			{"id": contract_id}
		).mappings().first()
	if not result:
		raise HTTPException(status_code=404, detail="Contract not found")
	return dict(result)

# ================================
# STEP 6 : Fetch a single contract by ID
# ================================
@app.get("/recommendations/{customer_id}")
def get_recommendations(customer_id: int):
	# TODO: Replace with real AI logic
	return {"customer_id": customer_id, "recommended_products": ["Life Insurance", "Car Insurance"]}
