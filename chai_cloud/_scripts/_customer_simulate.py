#!/usr/bin/env python
import sqlite3
import random
import os, sys

# This script generates customer orders through HTTP POST requests,
# simulating requests from Customer apps.

# Usage: 
# ./_customer_simulate.py
# Generates one random order to 'api' store
# ./_customer_simulate.py 5
# Generates 5 random orders to 'api' store

def random_order(store_name):
    """
    Add an order to a store with a random customer, random inventory item.
    Uses HTTP POST request to localhost:8000.
    """
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()

    # Get random customer email
    cur.execute("select max(cust_id) from Customer")
    max_id = cur.fetchone()[0]
    cur.execute(
        "select email from Customer where cust_id=?", 
        (random.randint(1,max_id),)
    )
    email = cur.fetchone()[0]

    # Generate random order list of 1-5 items
    cur.execute(
        "select store_id from Store where name=?",
        (store_name,)
    )
    store_id = cur.fetchone()[0]
    cur.execute(
        "select prod_id from Inventory where store_id=?",
        (store_id,)
    )
    prod_id_list = random.sample(
        [i[0] for i in cur.fetchall()],
        random.randint(1,5)
    )
    order_str = "" # string format for order list
    for prod_id in prod_id_list:
        # Get random option for each product
        cur.execute(
            "select op_id from Option where prod_id=?",
            (prod_id,)
        )
        op_id = random.choice([i[0] for i in cur.fetchall()])
        order_str += "{'prod_id': %d, 'op_id':%d}, " % (prod_id, op_id)
    order_str = "[%s]" % order_str
    
    # Create POST call
    command = "http -f POST :8000/order/ order_list=\"%s\"" % order_str + \
              " store_name=%s email=%s" % (store_name, email)
    with open('randorder', 'w') as w:
        w.write(command + "\n")
    os.system(command)
    #os.system("chmod +x randorder")
    #os.system("./randorder")



def order_batch(store_name, x=4):
    """
    Add orders x times.
    """
    for i in range(x):
        random_order(store_name)


    
if __name__ == '__main__':
    if len(sys.argv) == 2:
        order_batch(sys.argv[1])
    random_order('api')