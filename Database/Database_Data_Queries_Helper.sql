-- Helper view : current (active) products per customer
CREATE OR REPLACE VIEW v_customer_active_products AS
SELECT customer_id, product_id
FROM public.contracts
WHERE is_enabled = true
AND contract_status IN ('Active', 'Pending');