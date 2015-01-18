#!/usr/bin/env python
import sqlite3
import random


def populate_inventory(fname, release=False):
    """
    Populate all stores with some random menu items.
    """
    conn = sqlite3.connect(fname)
    cur = conn.cursor()

    # Get all store info; Dynamic for production, static for testing.
    if release:
        query = "select store_id, name from Store"
    else:
        query = "select store_id, name from Store where name='api'"
    cur.execute(query)
    stores = dict(cur.fetchall())

    # Get all categories {int: str}
    cur.execute('''select cat_id, cat_name from Category''')

    categories = dict(cur.fetchall())

    # Get customer IDs (for orders)
    cur.execute('''select cust_id from Customer''')
    customers = [i[0] for i in cur.fetchall()]
    #print customers
    for store_id in stores:
        print "[DEBUG] Generating inventory for %s..." % stores[store_id]
        # Generate random menu for each store
        # At least one of every category, 50%-100% of Menu for each
        # 50%-100% of options for each menu item.

        prods = [] # products to add per store
        for cat_id in categories:
            # Menu subset within category
            cur.execute(
                '''select prod_id, price from Menu where cat_id=?''',
                (cat_id,))
            menu = dict(cur.fetchall())
            # Random number of menu items, no less than 50%
            total_menu = int(random.uniform(0.5, 1.0)*len(menu))
            
            # Get product IDs for insert 
            prods += random.sample(menu, total_menu)
        insert_list = []
        for prod_id in prods:
            stock = random.randint(200,1000) # random inventory stock
            active = 1
            discount = 1.0
            insert_list += [(prod_id, stock, discount, active,)]
        print "[DEBUG] Inventory generated successfully."
        store_db_insert(fname, stores[store_id], "inventory", insert_list)


def store_db_insert(dbname, store_prefix, table, data):
    """
    Insert into dynamic store tables, given store name and table type.
    Data must be a list of tuples for insert.
    """

    table_name = "%s_%s" % (store_prefix, table)
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    if table == "inventory":
        query = "insert or ignore into %s (prod_id, stock," % table_name + \
                " discount, active) values (?, ?, ?, ?)"
        print "[DEBUG] Inserting data into table %s..." % table_name
        cur.executemany(query, data)
        conn.commit()
        print "[DEBUG] Inventory inserted successfully."
        
    elif table == "order":
        query = "insert into %s (cust_id, " % table_name + \
                "total_sale, time) values (?, ?, ?)"
        



if __name__ == '__main__':
    # ====== STATIC STORE SIMULATION =====
    # Populate all dynamic tables (tables for each store)
    populate_inventory('db.sqlite3')
    #assign_customers('db.sqlite3')
    #random_orders('db.sqlite3')

    # ====== DYNAMIC STORE SIMULATION =====
    # 