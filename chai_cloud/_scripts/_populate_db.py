#!/usr/bin/env python

# Automation script.

# Populates database for first time use.
# Before this script is run, be sure to populate the following data files:
# store.data, menu.data, cust.data
# These should be placed in the same folder as this script.

import sqlite3
from pprint import pprint # For testing

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
        for line in r.readlines():
            details = {} # product details
            # Parse useful info
            line = line.strip().split("|")
            name = line[0]
            op = line[2] # name of option

            if out.has_key(name):
                # Name already exist, update options only
                # Calculate price difference for option

                op_price = str(
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
                options[op] = 0 # default price is 0
                details['options'] = options
                out[name] = details
    #pprint(out)
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
            line = line.strip().split("|")
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
            line = line.strip().split("|")
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
        '''insert or ignore into Stores 
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

    # Parse category data
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
    pprint(menu_qdata)


    conn.close()

def get_cat_id(fname, cat_name):
    """
    Return category name given category ID.
    Helper function.
    """
    conn = sqlite3.connect(fname)
    cur = conn.cursor()
    cur.execute("select cat_id from Category where cat_name=?", (cat_name,))
    cat_id = int(cur.fetchone()[0])
    return cat_id


if __name__ == '__main__':
    db_file = "db.sqlite3"
    # db_file = "../db.sqlite3"  # Uncomment this line to use on the main DB file
    menu = get_menu('menu.data')
    stores = get_stores('stores.data')
    cust = get_cust('cust.data')
    populate_db(db_file, menu, stores, cust)
