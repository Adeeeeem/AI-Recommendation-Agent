"""
==============================================
 main.py - Entry point for Insurance Recommender
==============================================
This script :
 1. Connects to PostgreSQL database
 2. Creates a training table (merges customers + contracts + claims)
 3. Loads data into pandas
 4. Engineers features (e.g., convert birthdate → age)
 5. Prepares features and handles missing values
 6. Builds a Machine Learning model (Random Forest)
 7. Trains the model and evaluates accuracy
 8. Makes product recommendations for a specific customer
"""

# ---------------------------
# 1. IMPORT LIBRARIES
# ---------------------------
import pandas as pd										# DataFrames & data manipulation
import numpy as np										# Math operations
from sqlalchemy import create_engine, text					# PostgreSQL connection & SQL execution
from sklearn.model_selection import train_test_split			# Train/test split
from sklearn.preprocessing import OneHotEncoder, StandardScaler	# Encode categorical & scale numerical
from sklearn.impute import SimpleImputer					# Fill missing values
from sklearn.compose import ColumnTransformer				# Apply transformations by column type
from sklearn.pipeline import Pipeline						# Chain preprocessing + model
from sklearn.ensemble import RandomForestClassifier			# Random Forest classifier

# ---------------------------
# 2. DATABASE CONNECTION
# ---------------------------
engine = create_engine("postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/Next")

# ---------------------------
# 3. CREATE TRAINING TABLE IN POSTGRES
# ---------------------------
# Each time we run the script, we drop & recreate a simplified table for training.
print("Step 1 : Creating training table...")
sql_script = """
		DROP TABLE IF EXISTS public.ml_training_data;
		CREATE TABLE public.ml_training_data AS
		SELECT CU.id customer_id,					-- customer unique id
				CU.entity_type,					-- PP (person) or PM (company)
				CU.gender,						-- M / F
				CU.family_status,					-- Single, Married, etc.
				CU.birth_date,						-- Used later to compute age
				CU.sector,						-- Professional sector
				CU.sub_sector,						-- Sub-sector / profession
				CU.city,							-- City of residence
				CU.governorate,					-- Governorate (region)
				CO.product_id,						-- Which product they already own
				CO.total_premium,					-- Amount they pay (economic indicator)
				CO.contract_status,					-- Active / Terminated / Expired
				CO.payment_status,					-- Paid / Unpaid
				COALESCE(COUNT(CL.id), 0) claims_count	-- Number of claims filed
		FROM public.customers CU
		LEFT JOIN public.contracts CO ON CU.id = CO.customer_id
		LEFT JOIN public.claims CL ON CL.contract_id = CO.id
		WHERE CU.is_enabled = TRUE
		GROUP BY CU.id, CO.product_id, CO.total_premium, CO.contract_status, CO.payment_status;
	"""
with engine.begin() as conn:
	conn.execute(text(sql_script))
print("Training table created.")

# ---------------------------
# 4. LOAD TRAINING DATA INTO PANDAS
# ---------------------------
print("Step 2 : Loading data into pandas...")
# We now read the freshly created table into a pandas DataFrame.
df = pd.read_sql("SELECT * FROM public.ml_training_data", engine)
print("Step 3 : Number of rows loaded :", len(df))

# Load product mapping table for readable recommendations
product_mapping_sql = """
SELECT P.id AS product_id, P.product_name, 
	SB.id AS sub_branch_id, SB.sub_branch_name, 
	B.id AS branch_id, B.branch_name
FROM public.products P
JOIN public.sub_branches SB ON P.sub_branch_id = SB.id
JOIN public.branches B ON SB.branch_id = B.id
"""
product_mapping = pd.read_sql(product_mapping_sql, engine)

# ---------------------------
# 5. FEATURE ENGINEERING
# ---------------------------
print("Step 4 : Computing age from birth_date...")
# Compute age from birth_date, used as a numerical feature
df["age"] = pd.to_datetime("today").year - pd.to_datetime(df["birth_date"]).dt.year

# ---------------------------
# 5.1 HANDLE MISSING TARGETS
# ---------------------------
print("Step 4.1 : Removing rows with missing product_id (target)...")
df = df[df["product_id"].notna()]
print("Rows remaining after removing missing targets :", len(df))

# ---------------------------
# 6. PREPARE FEATURES AND TARGET
# ---------------------------
features = ["entity_type", "gender", "family_status", "sector", "sub_sector",
			"city", "governorate", "age", "total_premium", "claims_count"]
target = "product_id"

X = df[features]
y = df[target]

# Check which features still have missing values
print("Step 5 : Checking missing values per column :")
print(X.isnull().sum())

# ---------------------------
# 7. BUILD PREPROCESSING + MODEL PIPELINE WITH IMPUTATION
# ---------------------------
categorical = ["entity_type", "gender", "family_status", "sector", "sub_sector", "city", "governorate"]
numerical = ["age", "total_premium", "claims_count"]

# Categorical : fill missing with most frequent, then OneHotEncode
cat_transformer = Pipeline([
	("imputer", SimpleImputer(strategy="most_frequent")),
	("onehot", OneHotEncoder(handle_unknown="ignore"))
])

# Numerical : fill missing with median, then standardize
num_transformer = Pipeline([
	("imputer", SimpleImputer(strategy="median")),
	("scaler", StandardScaler())
])

# Combine preprocessing for both categorical and numerical features
preprocessor = ColumnTransformer([
	("cat", cat_transformer, categorical),
	("num", num_transformer, numerical)
])

# Create full pipeline: preprocessing + Random Forest classifier
model = Pipeline([
	("preprocessor", preprocessor),
	("classifier", RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1))
])

# ---------------------------
# 8. SPLIT TRAIN / TEST
# ---------------------------
print("Step 6 : Splitting train/test...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ---------------------------
# 9. TRAIN MODEL
# ---------------------------
print("Step 7 : Training RandomForest...")
model.fit(X_train, y_train)
print("Model training completed.")

# ---------------------------
# 10. EVALUATE MODEL
# ---------------------------
accuracy = model.score(X_test, y_test)
print("Model Accuracy :", round(accuracy, 4))

# ---------------------------
# 11. FUNCTION TO RECOMMEND PRODUCTS FOR SPECIFIC CUSTOMER
# ---------------------------
def recommend_for_customer(customer_id):
	"""
	Input : customer_id
	Output : top 3 recommended products with probabilities
	"""
	# Filter features for this customer
	customer_row = X[df["customer_id"] == customer_id]
	
	if customer_row.empty:
		print(f"No customer found with ID {customer_id}")
		return

	# Keep as DataFrame for ColumnTransformer compatibility
	customer_features_df = customer_row
	
	# Predict probabilities for all products
	probs = model.predict_proba(customer_features_df)[0]
	classes = model.named_steps["classifier"].classes_

	# Get list of products already owned by customer
	owned_products = df[df["customer_id"] == customer_id]["product_id"].tolist()
	
	# Get top 3 products
	top_idx = [i for i in np.argsort(probs)[::-1] if probs[i] > 0][:3]
	recommendations = []

	for i in top_idx:
		pid = classes[i]
		prob = probs[i]
		if pid in owned_products:  # skip products the customer already has
			continue
		# Map product_id to human-readable names and include IDs
		prod_info = product_mapping[product_mapping["product_id"] == pid].iloc[0]
		recommendations.append({
			"product_id": prod_info["product_id"],
			"product_name": prod_info["product_name"],
			"sub_branch_id": prod_info["sub_branch_id"],
			"sub_branch_name": prod_info["sub_branch_name"],
			"branch_id": prod_info["branch_id"],
			"branch_name": prod_info["branch_name"],
			"probability": round(prob, 3) # Probability that the customer will choose this product
		})
		if len(recommendations) == 3:  # stop after top 3
			break

	# Print recommendations nicely
	print(f"Recommended Products for customer {customer_id} :")
	for r in recommendations:
		print(f"Product : {r['product_id']} -> {r['product_name']} | "
			f"Sub-branch : {r['sub_branch_id']} -> {r['sub_branch_name']} | "
			f"Branch : {r['branch_id']} -> {r['branch_name']} | "
			f"Probability : {r['probability']}")