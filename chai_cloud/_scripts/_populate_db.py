#!/usr/bin/env python

# Automation script.

# Populates database for first time use.
# Before this script is run, be sure to populate the following data files:
# store.data, menu.data, cust.data
# These should be placed in the same folder as this script.

import sqlite3
from pprint import pprint # For testing
import random # for random populating per store
from math import ceil
import bcrypt


def generate_customers(filename, no=500):
    """
    Generate dummy customers for testing.
    Using name DB for random names.
    """
    # Get a full list of names from name DB
    dummy_names = []
    with open('raw-data/fullnames.data', 'r') as r:
        raw = r.readlines()
    for line in raw:
        line = line.strip()
        if "&" not in line and \
                len(line.split(" ")) > 2 and \
                "." not in line.split(" ")[0] and \
                "-" not in line and \
                len(line.split(" ")[-1]) > 3:
            dummy_names.append(line.strip())

    # Get a subset of random names (500 by default)
    random_names = [ 
        dummy_names[i] 
        for i in random.sample(range(0, len(dummy_names)-1), no)
    ]
    for name in random_names:
        [fname, lname] = name.rsplit(" ", 1)
        email = "-".join(name.replace(".", "").split(" ")) + "@chai.com"
        print "Hashing pw for", name, "..."
        passw = bcrypt.hashpw(name.replace(".", "").replace(" ", ""), bcrypt.gensalt())
    
    # Write it all in a data file
    with open(filename, 'w') as w:
        out = ""
        for name in random_names:
            [fname, lname] = name.rsplit(" ", 1)
            email = "-".join(name.replace(".", "").split(" ")) + "@chai.com"
            passw = name.replace(".", "").replace(" ", "")
            out += "%s|\n" % "|".join([fname, lname, email, passw])
        w.write(out)

def generate_stores(filename, no=20):
    """
    Generate stores from file containing Tim Hortons addresses.
    """
    addresses = set()
    with open('raw-data/timmies_urbanspoon_raw', 'r') as r:
        raw = r.readlines()

    for line in raw:
        if line[0] == "$": # line with address inside
            # find index of number
            address_index = None
            for i, c in enumerate(line):
                if c.isdigit():
                    address_index = i
                    break
            # get address
            if address_index:
                address = line[address_index:]
                addresses.add(
                    address.strip().replace(
                        " West", " W").replace(
                        " East", " E").replace(
                        " Drive", " Dr").replace(
                        " Road", " Rd").replace(
                        " Street", " St").replace(
                        " Boulevard", " Blvd").replace(
                        " Avenue", " Ave").replace(
                        " Ave Rd", " Avenue Rd").rsplit(",", 1)[0]
                )
    addresses = list(addresses)
    random_addresses = [
        addresses[i]
        for i in random.sample(range(0, len(addresses)-1), no)
    ]

    with open(filename, 'w') as w:
        out = ""
        for address in random_addresses:
            address = address.title().strip()
            phone = "(416) 218-9039" # dummy number
            name = "_".join(address.lower().split(" "))
            out += "%s\n" % "|".join([name, address, phone])
        w.write(out)


def get_menu(fname):
    """
    Return a dict containing menu info:
    { 
        name: {
            'base price': base price,
            'cat': category,
            'desc': description
            'img': image url
            options: {
                option name: option price diff
            }
        }
    }
    """
    out = {}
    with open(fname, 'r') as r:
        raw = r.readlines()
        for line in raw:
            details = {} # product details
            # Parse useful info
            # Must use unicode for DB inserts
            line = line.decode('utf-8').strip().split("|")
            name = line[0]
            op = line[2] # name of option

            if out.has_key(name):
                # Name already exist, update options only
                # Calculate price difference for option

                op_price = unicode(
                    float(line[3]) - float(out[name]['base_price']))
                out[name]['options'][op] = op_price

            else:
                # New item, default option
                details = {} # product details
                options = {} # product options
                details['base_price'] = line[3]
                details['cat'] = line[1]
                details['img'] = line[4]
                details['desc'] = line[5]
                options[op] = unicode(0) # default price is 0
                details['options'] = options
                out[name] = details
    ###print out
    return out

def get_stores(fname):
    """
    Return a dict containing store info:
    {
        store_name: {
            'desc': store desc, 
            'phone': store_phone
        }
    }
    """
    out = {}
    with open(fname, 'r') as r:
        for line in r.readlines():
            details = {}
            line = line.strip().decode('utf-8').split("|")
            details['desc'] = line[1]
            details['phone'] = line[2]
            out[line[0]] = details
    #pprint(out)
    return out

def get_cust(fname):
    """
    Return a dict containing customer info:
    {
        email: {
            'fname' = fname,
            'lname' = lname,
            'passhash' = passhash (will be hashed upon deployment release)
            'store_id' = store ID
        }
    }
    """
    out = {}
    with open(fname, 'r') as r:
        for line in r.readlines():
            details = {}
            line = line.decode('utf-8').strip().split("|")
            details['fname'] = line[0]
            details['lname'] = line[1]
            details['passhash'] = line[3]
            details['store_id'] = line[4]
            email = line[2]
            out[email] = details
    return out

def populate_db(fname, menu, stores, cust):
    """
    Insert all menu, option, category, store, customer info into 
    django database.
    Assumed all tables generated by syncdb already.
    """
    conn = sqlite3.connect(fname)
    cur = conn.cursor()

    # Parse store data to sqlite-friendly list
    store_qdata = [
        (
            name, 
            stores[name]['desc'], 
            stores[name]['phone'], 
            1,
        ) 
        for name in stores
    ]

    # Insert store data
    cur.executemany(
        '''insert or ignore into Store 
           (name, desc, phone, active) values (?, ?, ?, ?)''', 
        store_qdata
    )
    conn.commit()

    # Parse customer data
    cust_qdata = [
        (
            email, 
            cust[email]['fname'], 
            cust[email]['lname'], 
            cust[email]['passhash'],
            cust[email]['store_id'],
        )
        for email in cust
    ]

    # Insert customer data
    cur.executemany(
        '''insert or ignore into Customer (email, 
           fname, lname, passhash, store_id) values (?, ?, ?, ?, ?)''',
        cust_qdata
    )
    conn.commit()

    # Parse and insert category data
    # Note: converted to set first for unique elements only
    cat_qdata = [(cat,) for cat in {menu[name]['cat'] for name in menu}]
    cur.executemany(
        '''insert or ignore into Category (cat_name) values (?)''',
        cat_qdata
    )
    conn.commit()

    # Parse menu data
    menu_qdata = [
        (
            name, 
            get_cat_id(fname, menu[name]['cat']), 
            menu[name]['img'], 
            menu[name]['base_price'],
            menu[name]['desc'],
        )
        for name in menu
    ]

    # Insert menu data
    cur.executemany(
        '''insert or ignore into Menu 
           (prod_name, cat_id, img_path, price, desc) values (?,?,?,?,?)''',
           menu_qdata
    )
    conn.commit()

    # Parse and insert option data
    op_qdata = [
        [
            (
                get_prod_id(fname, name), 
                op, 
                menu[name]['options'][op]
            ) 
            for op in menu[name]['options']
        ] 
        for name in menu
    ]
    # since option info is unordered from set, order before insert
    for opset in op_qdata:
        opset.sort(key=lambda x: x[2])
    #pprint(op_qdata)

    op_qdata = [inner for outer in op_qdata for inner in outer] # combine
    cur.executemany(
        '''insert or ignore into Option (prod_id, op_name, price) values
           (?, ?, ?)''',
           op_qdata
    )
    conn.commit()

    conn.close()

def get_cat_id(fname, cat_name):
    """
    Return category id given category name.
    Helper function.
    """
    conn = sqlite3.connect(fname)
    cur = conn.cursor()
    cur.execute("select cat_id from Category where cat_name=?", (cat_name,))
    cat_id = int(cur.fetchone()[0])
    return cat_id

def get_prod_id(fname, prod_name):
    """
    Return product id given product name.
    Helper function.
    """
    conn = sqlite3.connect(fname)
    cur = conn.cursor()
    cur.execute("select prod_id from Menu where prod_name=?", (prod_name,))
    prod_id = int(cur.fetchone()[0])
    return prod_id


if __name__ == '__main__':
    db_file = "db.sqlite3"
    # db_file = "../db.sqlite3"  # Uncomment this line to use on the main DB file

    # Generate random customer names (default 500)
    generate_customers('raw-data/cust.data')
    #generate_stores('raw-data/stores.data')

    # Get retrieve data for DB inserts
    menu = get_menu('raw-data/menu.data')
    stores = get_stores('raw-data/stores.data')
    cust = get_cust('raw-data/cust.data')

    # Populate all static tables
    populate_db(db_file, menu, stores, cust)



