#!/usr/bin/env python
import sqlite3
import random


def populate_inventory(fname, release=False):
    """
    Populate all stores with some random menu items.
    """
    conn = sqlite3.connect(fname)
    cur = conn.cursor()

    # Get all store IDs
    cur.execute('''select store_id from Stores''')
    if release:
        store_ids = [i[0] for i in cur.fetchall()] # List of store IDs
    else:
        
    cur.execute('''select cat_id, cat_name from Category''')
    # Get all categories {int: str}
    categories = dict(cur.fetchall())

    # Get customer IDs (for orders)
    cur.execute('''select cust_id from Customer''')
    customers = [i[0] for i in cur.fetchall()]
    #print customers
    
    for store_id in store_ids:

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
            insert_list += (prod_id, stock, discount, active,)


def store_db_insert(table, data):

    table_name = "%s_%s" % (store_prefix, table)
    if table == "inventory":
        query = """insert



if __name__ == '__main__':
    # ====== STATIC STORE SIMULATION =====
    # Populate all dynamic tables (tables for each store)
    populate_inventory('db.sqlite3')
    #assign_customers('db.sqlite3')
    #random_orders('db.sqlite3')

    # ====== DYNAMIC STORE SIMULATION =====
    # 