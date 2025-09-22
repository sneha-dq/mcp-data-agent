def load_table_schemas():
    # You could introspect Postgres here. Hardcode for demo.
    return {
        "public.customer_shopping": ["invoice_no", "customer_id", "gender", "age", "category", "quantity", "price", "payment_method", "invoice_date", "shopping_mall"],
        "public.datablist_customers": ["index_no", "customer_id", "first_name", "last_name", "company", "city", "country", "phone1", "phone2", "email", "subscription_date", "website"],
    }