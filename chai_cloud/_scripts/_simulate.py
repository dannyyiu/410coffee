import sqlite3

def populate_stores(fname):
    """
    Populate all stores with some random menu items, random orders.
    """
    conn = sqlite3.connect(fname)
    cur = conn.cursor()

    # Get all store IDs
    cur.execute('''select store_id from Stores''')
    store_ids = [i[0] for i in cur.fetchall()] # List of store IDs
    cur.execute('''select cat_id, cat_name from Category''')
    # Get all categories {int: str}
    categories = dict(cur.fetchall())
    # Get all prod IDs and base price from menu {str:float}
    cur.execute('''select prod_name, price from Menu''')
    menu = dict(cur.fetchall())
    # Get customer IDs (for orders)
    cur.execute('''select cust_id from Customer''')
    customers = [i[0] for i in cur.fetchall()]
    #print customers
    
    for store_id in store_ids:
        # Generate random menu for each store
        # All categories, 70%-100% of Menu for each
        # 50%-100% of options for each menu item.
        pass



if __name__ == '__main__':
    # ====== STATIC STORE SIMULATION =====
    # Populate all dynamic tables (tables for each store)
    assign_customers('db.sqlite3')
    populate_stores('db.sqlite3')

    # ====== DYNAMIC STORE SIMULATION =====
    # 