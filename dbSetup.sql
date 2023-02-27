CREATE TABLE "Customers" (
"customer_id" TEXT, -- customer_id
"customer_postal_code" INTEGER, -- customer_zip_code_prefix
PRIMARY KEY("customer_id")
);

CREATE TABLE "Sellers" (
"seller_id" TEXT, -- seller_id
"seller_postal_code" INTEGER, -- seller_zip_code_prefix
PRIMARY KEY("seller_id")
);

CREATE TABLE "Orders" (
"order_id" TEXT, -- order_id
"customer_id" TEXT, -- customer_id
PRIMARY KEY("order_id"),
FOREIGN KEY("customer_id") REFERENCES "Customers"("customer_id")
);

CREATE TABLE "Order_items" (
"order_id" TEXT, -- order_id
"order_item_id" INTEGER, -- order_item_id
"product_id" TEXT, -- product_id
"seller_id" TEXT, -- seller_id
PRIMARY KEY("order_id","order_item_id","product_id","seller_id"),
FOREIGN KEY("seller_id") REFERENCES "Sellers"("seller_id")
FOREIGN KEY("order_id") REFERENCES "Orders"("order_id")
);