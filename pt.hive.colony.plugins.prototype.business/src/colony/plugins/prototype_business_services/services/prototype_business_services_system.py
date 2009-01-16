#!/usr/bin/python
# -*- coding: Cp1252 -*-

# Hive Colony Framework
# Copyright (C) 2008 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Colony Framework. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import thread
import base64
import sqlite3

import os.path

SERVICE_ID = "prototype_business_services"
""" The service id """

DATABASE_FILE = "database.db"

TABLES = ["products", "customers", "suppliers", "sales", "sales_customers", "sales_products", "purchases", "purchases_suppliers", "purchases_products", "users"]

TABLE_SCHEMAS = {"products" : {"id" : "text",
                               "heading1" : "text",
                               "heading2" : "text",
                               "description" : "text",
                               "weight" : "number",
                               "height" : "number",
                               "quantity" : "number",
                               "picture_base64" : "text"},
                 "customers" : {"name" : "text",
                                "age" : "number",
                                "address" : "text",
                                "gender" : "text",
                                "picture_base64" : "text",
                                "email" : "text",
                                "phone" : "text",
                                "mobile" : "text",
                                "fax" : "text",
                                "description" : "text"},
                 "suppliers" : {"name" : "text",
                                "address" : "text",
                                "picture_base64" : "text"},
                 "sales" : {"id" : "text",
                            "payment_type" : "text",
                            "description" : "text"},
                 "sales_customers" : {"sale_id" : "text",
                                      "customer_name" : "text"},
                 "sales_products" : {"sale_id" : "text",
                                     "product_id" : "text",
                                     "quantity" : "number"},
                 "purchases" : {"id" : "text",
                                "description" : "text"},
                 "purchases_suppliers" : {"purchase_id" : "text",
                                          "supplier_name" : "text"},
                 "purchases_products" : {"purchase_id" : "text",
                                         "product_id" : "text",
                                         "quantity" : "number"},
                 "users" : {"username" : "text",
                            "password" : "text",
                            "picture_base64" : "text",
                            "secret_question" : "text",
                            "secret_answer" : "text"}}

TABLE_SCHEMA_KEYS = {"products" : ["id", "heading1", "heading2", "description", "weight", "height", "quantity", "picture_base64"],
                     "customers" : ["name", "age", "address", "gender", "picture_base64", "email", "phone", "mobile", "fax", "description"],
                     "suppliers" : ["name", "address", "picture_base64"],
                     "sales" : ["id", "payment_type", "description"],
                     "sales_customers" : ["sale_id", "customer_name"],
                     "sales_products" : ["sale_id", "product_id", "quantity"],
                     "purchases" : ["id", "description"],
                     "purchases_suppliers" : ["purchase_id", "supplier_name"],
                     "purchases_products" : ["purchase_id", "product_id", "quantity"],
                     "users" : ["username", "password", "picture_base64", "secret_question", "secret_answer"]}

class PrototypeBusinessServices:

    prototype_business_services_plugin = None

    connection_thread_id_map = {}

    def __init__(self, prototype_business_services_plugin):
        self.prototype_business_services_plugin = prototype_business_services_plugin

        self.connection_thread_id_map = {}

    def get_service_id(self):
        return SERVICE_ID

    def get_service_alias(self):
        return []

    def get_available_rpc_methods(self):
        return []

    def get_rpc_methods_alias(self):
        return {}

    def get_connection(self):
        # retrieves the resource manager plugin
        resource_manager_plugin = self.prototype_business_services_plugin.resource_manager_plugin

        # retrieves the user home path resource
        user_home_path_resource = resource_manager_plugin.get_resource("system.path.user_home")

        # retrieves the user home path value
        user_home_path = user_home_path_resource.data

        # gets the id of the current thread
        current_thread_id = thread.get_ident()

        # in case the database connection is not established
        if current_thread_id in self.connection_thread_id_map:
            # retrieves the available database connection
            connection = self.connection_thread_id_map[current_thread_id]
        else:
            # creates the database file path
            database_file_path = user_home_path + "/" + DATABASE_FILE

            # prints an info message
            self.prototype_business_services_plugin.info("Creating sqlite database in: %s" % database_file_path)

            # establishes connection with the database file
            connection = sqlite3.connect(database_file_path)

            # adds the created connection to the map that associates the thread id with the connection
            self.connection_thread_id_map[current_thread_id] = connection

        # return the database connection
        return connection

    def create_database(self):
        # retrieves the database connection
        connection = self.get_connection()

        # creates the cursor for the given connection
        cursor = connection.cursor()

        # selects all the names of existing tables
        cursor.execute("select name from SQLite_Master")

        # commits the changes to the connection
        connection.commit()

        # selects the table names from the cursor
        table_names_list = [value[0] for value in cursor]

        # selects the missing table names
        missing_table_names_list = [value for value in TABLES if value not in table_names_list]

        # iterates over all the missing table names
        for missing_table_name in missing_table_names_list:
            missing_table_values = TABLE_SCHEMAS[missing_table_name]
            missing_table_value_keys = TABLE_SCHEMA_KEYS[missing_table_name]

            # creates the initial query string value
            query_string_value = "create table " + missing_table_name + "("

            # the first flag to control the first field to be processed
            is_first = True

            # iterates over each of the missing table value keys
            for missing_table_value_key in missing_table_value_keys:                
                # retrieves the name of the current field (key)
                field_name = missing_table_value_key

                # retrieves the data type for the current field
                data_type = missing_table_values[missing_table_value_key]

                # in case is the first field to be processed
                if is_first:
                    # sets the is flag to false to start adding commas
                    is_first = False
                else:
                    # adds a comma to the query string value
                    query_string_value += ", "

                # extends the query string value
                query_string_value += field_name + " " + data_type

            # closes the query string value
            query_string_value += ")"

            # executes the query creating the table
            cursor.execute(query_string_value)

            # commits the changes to the connection
            connection.commit()

        # closes the cursor
        cursor.close()

    def create_user(self, username, password, picture_base64):
        # in case the user already exists
        if self.get_user(username):
            # returns invalid state (error)
            return False

        # retrieves the database connection
        connection = self.get_connection()

        # creates the cursor for the given connection
        cursor = connection.cursor()

        # creates the query string value
        query_string_value = "insert into users(username, password, picture_base64) values('" + username + "','" + password + "','" + picture_base64 + "')"

        # executes the query inserting the values
        cursor.execute(query_string_value)

        # commits the changes to the connection
        connection.commit()

        # closes the cursor
        cursor.close()

    def edit_user(self, username, field_names, field_values):
        # in case the user does not exist
        if not self.get_user(username):
            # returns invalid state (error)
            return False

        # in case the length of the two lists is not the same
        if not len(field_names) == len(field_values):
            # returns invalid state (error)
            return False

        # retrieves the database connection
        connection = self.get_connection()

        # creates the cursor for the given connection
        cursor = connection.cursor()

        # creates the query string value
        query_string_value = "update users set "

        # start the iteration index
        index = 0
        
        # the first flag to control the first field to be processed
        is_first = True

        # iterates over all the field names
        for field_name in field_names:
            # retrieves the field value
            field_value = field_values[index]

            # in case is the first field to be processed
            if is_first:
                # sets the is flag to false to start adding commas
                is_first = False
            else:
                # adds a comma to the query string value
                query_string_value += ","
            
            # adds the setting to the query string
            query_string_value += field_name + " = '" + str(field_value) + "' "

            # increments the iteration index
            index += 1

        # adds the where clause to the query string
        query_string_value += "where username = '" + username + "'"

        # executes the query inserting the values
        cursor.execute(query_string_value)

        # commits the changes to the connection
        connection.commit()

        # closes the cursor
        cursor.close()

    def remove_user(self, username):
        # retrieves the database connection
        connection = self.get_connection()

        # creates the cursor for the given connection
        cursor = connection.cursor()

        # creates the query string value
        query_string_value = "delete from users where username = '" + username + "'"

        # executes the query inserting the values
        cursor.execute(query_string_value)

        # commits the changes to the connection
        connection.commit()

        # closes the cursor
        cursor.close()

    def get_user(self, username):
        # retrieves the database connection
        connection = self.get_connection()

        # creates the cursor for the given connection
        cursor = connection.cursor()

        # creates the query string value
        query_string_value = "select * from users where username = '" + username + "'"

        # executes the query selecting the values
        cursor.execute(query_string_value)

        # commits the changes to the connection
        connection.commit()

        # selects the table names from the cursor
        users_list = [User(value[0], value[1], value[2]).set_values(value[3:]) for value in cursor]

        # closes the cursor
        cursor.close()

        # in case there is at least one user selected
        if len(users_list):
            # returns the first element of the list of users
            return users_list[0]
        # in case there is no user selected
        else:
            return False

    def get_all_users(self):
        # retrieves the database connection
        connection = self.get_connection()

        # creates the cursor for the given connection
        cursor = connection.cursor()

        # creates the query string value
        query_string_value = "select * from users"

        # executes the query selecting the values
        cursor.execute(query_string_value)

        # commits the changes to the connection
        connection.commit()

        # selects the users from the cursor
        users_list = [User(value[0], value[1], value[2]).set_values(value[3:]) for value in cursor]

        # closes the cursor
        cursor.close()

        # returns the list of users
        return users_list

    def create_customer(self, name, age, address, gender, picture_base64):
        # in case the customer already exists
        if self.get_customer(name):
            # returns invalid state (error)
            return False

        # retrieves the database connection
        connection = self.get_connection()

        # creates the cursor for the given connection
        cursor = connection.cursor()

        # creates the query string value
        query_string_value = "insert into customers(name, age, address, gender, picture_base64) values('" + name + "','" + str(age) + "','" + address + "','" + gender + "','" + picture_base64 + "')"

        # executes the query inserting the values
        cursor.execute(query_string_value)

        # commits the changes to the connection
        connection.commit()

        # closes the cursor
        cursor.close()

    def edit_customer(self, name, field_names, field_values):
        # in case the customer does not exist
        if not self.get_customer(name):
            # returns invalid state (error)
            return False

        # in case the length of the two lists is not the same
        if not len(field_names) == len(field_values):
            # returns invalid state (error)
            return False

        # retrieves the database connection
        connection = self.get_connection()

        # creates the cursor for the given connection
        cursor = connection.cursor()

        # creates the query string value
        query_string_value = "update customers set "

        # start the iteration index
        index = 0
        
        # the first flag to control the first field to be processed
        is_first = True

        # iterates over all the field names
        for field_name in field_names:
            # retrieves the field value
            field_value = field_values[index]

            # in case is the first field to be processed
            if is_first:
                # sets the is flag to false to start adding commas
                is_first = False
            else:
                # adds a comma to the query string value
                query_string_value += ","
            
            # adds the setting to the query string
            query_string_value += field_name + " = '" + str(field_value) + "' "

            # increments the iteration index
            index += 1

        # adds the where clause to the query string
        query_string_value += "where name = '" + name + "'"

        # executes the query inserting the values
        cursor.execute(query_string_value)

        # commits the changes to the connection
        connection.commit()

        # closes the cursor
        cursor.close()

    def remove_customer(self, name):
        # retrieves the database connection
        connection = self.get_connection()

        # creates the cursor for the given connection
        cursor = connection.cursor()

        # creates the query string value
        query_string_value = "delete from customers where name = '" + name + "'"

        # executes the query inserting the values
        cursor.execute(query_string_value)

        # commits the changes to the connection
        connection.commit()

        # closes the cursor
        cursor.close()

    def get_customer(self, name):
        # retrieves the database connection
        connection = self.get_connection()

        # creates the cursor for the given connection
        cursor = connection.cursor()

        # creates the query string value
        query_string_value = "select * from customers where name = '" + name + "'"

        # executes the query selecting the values
        cursor.execute(query_string_value)

        # commits the changes to the connection
        connection.commit()

        # selects the table names from the cursor
        customers_list = [Customer(value[0], value[1], value[2], value[3], value[4]).set_values(value[5:]) for value in cursor]

        # closes the cursor
        cursor.close()

        # in case there is at least one user selected
        if len(customers_list):
            # returns the first element of the list of users
            return customers_list[0]
        # in case there is no user selected
        else:
            return False

    def get_all_customers(self):
        # retrieves the database connection
        connection = self.get_connection()

        # creates the cursor for the given connection
        cursor = connection.cursor()

        # creates the query string value
        query_string_value = "select * from customers"

        # executes the query selecting the values
        cursor.execute(query_string_value)

        # commits the changes to the connection
        connection.commit()

        # selects the users from the cursor
        customers_list = [Customer(value[0], value[1], value[2], value[3], value[4]).set_values(value[5:]) for value in cursor]

        # closes the cursor
        cursor.close()

        # returns the list of users
        return customers_list

    def create_supplier(self, name, address, picture_base64):
        # in case the supplier already exists
        if self.get_supplier(name):
            # returns invalid state (error)
            return False

        # retrieves the database connection
        connection = self.get_connection()

        # creates the cursor for the given connection
        cursor = connection.cursor()

        # creates the query string value
        query_string_value = "insert into suppliers(name, address, picture_base64) values('" + name + "','" + address + "','" + picture_base64 + "')"

        # executes the query inserting the values
        cursor.execute(query_string_value)

        # commits the changes to the connection
        connection.commit()

        # closes the cursor
        cursor.close()

    def edit_supplier(self, name, field_names, field_values):
        # in case the supplier does not exist
        if not self.get_supplier(name):
            # returns invalid state (error)
            return False

        # in case the length of the two lists is not the same
        if not len(field_names) == len(field_values):
            # returns invalid state (error)
            return False

        # retrieves the database connection
        connection = self.get_connection()

        # creates the cursor for the given connection
        cursor = connection.cursor()

        # creates the query string value
        query_string_value = "update suppliers set "

        # start the iteration index
        index = 0
        
        # the first flag to control the first field to be processed
        is_first = True

        # iterates over all the field names
        for field_name in field_names:
            # retrieves the field value
            field_value = field_values[index]

            # in case is the first field to be processed
            if is_first:
                # sets the is flag to false to start adding commas
                is_first = False
            else:
                # adds a comma to the query string value
                query_string_value += ","
            
            # adds the setting to the query string
            query_string_value += field_name + " = '" + str(field_value) + "' "

            # increments the iteration index
            index += 1

        # adds the where clause to the query string
        query_string_value += "where name = '" + name + "'"

        # executes the query inserting the values
        cursor.execute(query_string_value)

        # commits the changes to the connection
        connection.commit()

        # closes the cursor
        cursor.close()

    def remove_supplier(self, name):
        # retrieves the database connection
        connection = self.get_connection()

        # creates the cursor for the given connection
        cursor = connection.cursor()

        # creates the query string value
        query_string_value = "delete from suppliers where name = '" + name + "'"

        # executes the query inserting the values
        cursor.execute(query_string_value)

        # commits the changes to the connection
        connection.commit()

        # closes the cursor
        cursor.close()

    def get_supplier(self, name):
        # retrieves the database connection
        connection = self.get_connection()

        # creates the cursor for the given connection
        cursor = connection.cursor()

        # creates the query string value
        query_string_value = "select * from suppliers where name = '" + name + "'"

        # executes the query selecting the values
        cursor.execute(query_string_value)

        # commits the changes to the connection
        connection.commit()

        # selects the supplier from the cursor
        suppliers_list = [Supplier(value[0], value[1], value[2]) for value in cursor]

        # closes the cursor
        cursor.close()

        # in case there is at least one supplier selected
        if len(suppliers_list):
            # returns the first element of the list of suppliers
            return suppliers_list[0]
        # in case there is no supplier selected
        else:
            return False
        
    def get_all_suppliers(self):
        # retrieves the database connection
        connection = self.get_connection()

        # creates the cursor for the given connection
        cursor = connection.cursor()

        # creates the query string value
        query_string_value = "select * from suppliers"

        # executes the query selecting the values
        cursor.execute(query_string_value)

        # commits the changes to the connection
        connection.commit()

        # selects the products from the cursor
        suppliers_list = [Supplier(value[0], value[1], value[2]) for value in cursor]

        # closes the cursor
        cursor.close()

        # returns the list of products
        return suppliers_list

    def create_product(self, id, heading1, heading2, description, weight, height, quantity, picture_base64):
        # in case the product already exists
        if self.get_product(id):
            # returns invalid state (error)
            return False

        # retrieves the database connection
        connection = self.get_connection()

        # creates the cursor for the given connection
        cursor = connection.cursor()

        # creates the query string value
        query_string_value = "insert into products(id, heading1, heading2, description, weight, height, quantity, picture_base64) values('" + id + "','" + heading1 + "','" + heading2 + "','" + description + "'," + str(weight) + "," + str(height) + "," + str(quantity) + ",'" + picture_base64 + "')"

        # executes the query inserting the values
        cursor.execute(query_string_value)

        # commits the changes to the connection
        connection.commit()

        # closes the cursor
        cursor.close()

    def edit_product(self, id, field_names, field_values):
        # in case the product does not exist
        if not self.get_product(id):
            # returns invalid state (error)
            return False

        # in case the length of the two lists is not the same
        if not len(field_names) == len(field_values):
            # returns invalid state (error)
            return False

        # retrieves the database connection
        connection = self.get_connection()

        # creates the cursor for the given connection
        cursor = connection.cursor()

        # creates the query string value
        query_string_value = "update products set "

        # start the iteration index
        index = 0
        
        # the first flag to control the first field to be processed
        is_first = True

        # iterates over all the field names
        for field_name in field_names:
            # retrieves the field value
            field_value = field_values[index]

            # in case is the first field to be processed
            if is_first:
                # sets the is flag to false to start adding commas
                is_first = False
            else:
                # adds a comma to the query string value
                query_string_value += ","

            # adds the setting to the query string
            query_string_value += field_name + " = '" + str(field_value) + "' "

            # increments the iteration index
            index += 1

        # adds the where clause to the query string
        query_string_value += "where id = '" + id + "'"

        # executes the query inserting the values
        cursor.execute(query_string_value)

        # commits the changes to the connection
        connection.commit()

        # closes the cursor
        cursor.close()

    def remove_product(self, id):
        # retrieves the database connection
        connection = self.get_connection()

        # creates the cursor for the given connection
        cursor = connection.cursor()

        # creates the query string value
        query_string_value = "delete from products where id = '" + id + "'"

        # executes the query inserting the values
        cursor.execute(query_string_value)

        # commits the changes to the connection
        connection.commit()

        # closes the cursor
        cursor.close()

    def get_product(self, id):
        # retrieves the database connection
        connection = self.get_connection()

        # creates the cursor for the given connection
        cursor = connection.cursor()

        # creates the query string value
        query_string_value = "select * from products where id = '" + id + "'"

        # executes the query selecting the values
        cursor.execute(query_string_value)

        # commits the changes to the connection
        connection.commit()

        # selects the products from the cursor
        products_list = [Product(value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7]) for value in cursor]

        # closes the cursor
        cursor.close()

        # in case there is at least one product selected
        if len(products_list):
            # returns the first element of the list of products
            return products_list[0]
        # in case there is no product selected
        else:
            return False

    def get_all_products(self):
        # retrieves the database connection
        connection = self.get_connection()

        # creates the cursor for the given connection
        cursor = connection.cursor()

        # creates the query string value
        query_string_value = "select * from products"

        # executes the query selecting the values
        cursor.execute(query_string_value)

        # commits the changes to the connection
        connection.commit()

        # selects the products from the cursor
        products_list = [Product(value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7]) for value in cursor]

        # closes the cursor
        cursor.close()

        # returns the list of products
        return products_list

    def create_sale(self, id, payment_type, description, customer_name, product_tuples):
        # in case the sale already exists
        if self.get_sale(id):
            # returns invalid state (error)
            return False

        # retrieves the database connection
        connection = self.get_connection()

        # creates the cursor for the given connection
        cursor = connection.cursor()

        # creates the query string value
        query_string_value = "insert into sales(id, payment_type, description) values('" + id + "','" + payment_type + "','" + description + "')"

        # executes the query inserting the values
        cursor.execute(query_string_value)

        # in case there is a supplier
        if customer_name:
            # creates the cursor for the given connection
            cursor = connection.cursor()

            # creates the query string value
            query_string_value = "insert into sales_customers values('" + id + "','" + customer_name + "')"

            # executes the query inserting the values
            cursor.execute(query_string_value)

        for product_tuple in product_tuples:
            # retrieves the product id and quantity
            product_id, quantity = product_tuple

            # creates the cursor for the given connection
            cursor = connection.cursor()

            # creates the query string value
            query_string_value = "insert into sales_products values('" + id + "','" + product_id + "'" + "," + str(quantity) + ")"

            # executes the query inserting the values
            cursor.execute(query_string_value)

        # commits the changes to the connection
        connection.commit()

        # closes the cursor
        cursor.close()        

    def get_sale(self, id):
        # retrieves the database connection
        connection = self.get_connection()

        # creates the cursor for the given connection
        cursor = connection.cursor()

        # creates the query string value
        query_string_value = "select * from sales where id = '" + id + "'"

        # executes the query selecting the values
        cursor.execute(query_string_value)

        # commits the changes to the connection
        connection.commit()

        # selects the sale from the cursor
        sales_list = [Sale(value[0], value[1]) for value in cursor]

        for sale in sales_list:
            # creates the query string value
            query_string_value = "select * from sales_customers where sale_id = '" + sale.id + "'"

            # executes the query selecting the values
            cursor.execute(query_string_value)

            # commits the changes to the connection
            connection.commit()

            # selects the customer name from the cursor
            customers_list = [value[1] for value in cursor]

            # in case there is at least one customer name selected
            if len(customers_list):
                sale.customer = self.get_customer(customers_list[0])
            else:
                sake.customer = False

            # creates the query string value
            query_string_value = "select * from sales_products where sale_id = '" + sale.id + "'"

            # executes the query selecting the values
            cursor.execute(query_string_value)

            # commits the changes to the connection
            connection.commit()

            # selects the product tuples from the cursor
            product_tuples_list = [(value[1], value[2]) for value in cursor]

            for product_tuple in product_tuples_list:
                product_id, quantity = product_tuple

                product = self.get_product(product_id)

                product_final_tuple = (product, quantity)

                sale.products.append(product_final_tuple)

        # closes the cursor
        cursor.close()

        # in case there is at least one sale selected
        if len(sales_list):
            # returns the first element of the list of sales
            return sales_list[0]
        # in case there is no sale selected
        else:
            return False

    def get_all_sales(self):
        # retrieves the database connection
        connection = self.get_connection()

        # creates the cursor for the given connection
        cursor = connection.cursor()

        # creates the query string value
        query_string_value = "select * from sales"

        # executes the query selecting the values
        cursor.execute(query_string_value)

        # commits the changes to the connection
        connection.commit()

        # selects the sale from the cursor
        sales_list = [Sale(value[0], value[1]) for value in cursor]

        for sale in sales_list:
            # creates the query string value
            query_string_value = "select * from sales_customers where sale_id = '" + sale.id + "'"

            # executes the query selecting the values
            cursor.execute(query_string_value)

            # commits the changes to the connection
            connection.commit()

            # selects the customer name from the cursor
            customers_list = [value[1] for value in cursor]

            # in case there is at least one customer name selected
            if len(customers_list):
                sale.customer = self.get_customer(customers_list[0])
            else:
                sake.customer = False

            # creates the query string value
            query_string_value = "select * from sales_products where sale_id = '" + sale.id + "'"

            # executes the query selecting the values
            cursor.execute(query_string_value)

            # commits the changes to the connection
            connection.commit()

            # selects the product tuples from the cursor
            product_tuples_list = [(value[1], value[2]) for value in cursor]

            for product_tuple in product_tuples_list:
                product_id, quantity = product_tuple

                product = self.get_product(product_id)

                product_final_tuple = (product, quantity)

                sale.products.append(product_final_tuple)

        # closes the cursor
        cursor.close()

        return sales_list

    def create_purchase(self, id, description, supplier_name, product_tuples):
        # in case the purchase already exists
        if self.get_purchase(id):
            # returns invalid state (error)
            return False

        # retrieves the database connection
        connection = self.get_connection()

        # creates the cursor for the given connection
        cursor = connection.cursor()

        # creates the query string value
        query_string_value = "insert into purchases(id, description) values('" + id + "','" + description + "')"

        # executes the query inserting the values
        cursor.execute(query_string_value)

        # in case there is a supplier
        if supplier_name:
            # creates the cursor for the given connection
            cursor = connection.cursor()

            # creates the query string value
            query_string_value = "insert into purchases_suppliers values('" + id + "','" + supplier_name + "')"

            # executes the query inserting the values
            cursor.execute(query_string_value)

        for product_tuple in product_tuples:
            # retrieves the product id and quantity
            product_id, quantity = product_tuple

            # creates the cursor for the given connection
            cursor = connection.cursor()

            # creates the query string value
            query_string_value = "insert into purchases_products values('" + id + "','" + product_id + "'" + "," + str(quantity) + ")"

            # executes the query inserting the values
            cursor.execute(query_string_value)

        # commits the changes to the connection
        connection.commit()

        # closes the cursor
        cursor.close()

    def get_purchase(self, id):
        # retrieves the database connection
        connection = self.get_connection()

        # creates the cursor for the given connection
        cursor = connection.cursor()

        # creates the query string value
        query_string_value = "select * from purchases where id = '" + id + "'"

        # executes the query selecting the values
        cursor.execute(query_string_value)

        # commits the changes to the connection
        connection.commit()

        # selects the purchase from the cursor
        purchases_list = [Purchase(value[0], value[1]) for value in cursor]

        for purchase in purchases_list:
            # creates the query string value
            query_string_value = "select * from purchases_suppliers where purchase_id = '" + purchase.id + "'"

            # executes the query selecting the values
            cursor.execute(query_string_value)

            # commits the changes to the connection
            connection.commit()

            # selects the supplier name from the cursor
            suppliers_list = [value[1] for value in cursor]

            # in case there is at least one supplier name selected
            if len(suppliers_list):
                purchase.supplier = self.get_supplier(suppliers_list[0])
            else:
                purchase.supplier = False

            # creates the query string value
            query_string_value = "select * from purchases_products where purchase_id = '" + purchase.id + "'"

            # executes the query selecting the values
            cursor.execute(query_string_value)

            # commits the changes to the connection
            connection.commit()

            # selects the product tuples from the cursor
            product_tuples_list = [(value[1], value[2]) for value in cursor]

            for product_tuple in product_tuples_list:
                product_id, quantity = product_tuple

                product = self.get_product(product_id)

                product_final_tuple = (product, quantity)

                purchase.products.append(product_final_tuple)

        # closes the cursor
        cursor.close()

        # in case there is at least one purchase selected
        if len(purchases_list):
            # returns the first element of the list of purchases
            return purchases_list[0]
        # in case there is no purchase selected
        else:
            return False

    def get_all_purchases(self):
       # retrieves the database connection
        connection = self.get_connection()

        # creates the cursor for the given connection
        cursor = connection.cursor()

        # creates the query string value
        query_string_value = "select * from purchases"

        # executes the query selecting the values
        cursor.execute(query_string_value)

        # commits the changes to the connection
        connection.commit()

        # selects the purchase from the cursor
        purchases_list = [Purchase(value[0], value[1]) for value in cursor]

        for purchase in purchases_list:
            # creates the query string value
            query_string_value = "select * from purchases_suppliers where purchase_id = '" + purchase.id + "'"

            # executes the query selecting the values
            cursor.execute(query_string_value)

            # commits the changes to the connection
            connection.commit()

            # selects the supplier name from the cursor
            suppliers_list = [value[1] for value in cursor]

            # in case there is at least one supplier name selected
            if len(suppliers_list):
                purchase.supplier = self.get_supplier(suppliers_list[0])
            else:
                purchase.supplier = False

            # creates the query string value
            query_string_value = "select * from purchases_products where purchase_id = '" + purchase.id + "'"

            # executes the query selecting the values
            cursor.execute(query_string_value)

            # commits the changes to the connection
            connection.commit()

            # selects the product tuples from the cursor
            product_tuples_list = [(value[1], value[2]) for value in cursor]

            for product_tuple in product_tuples_list:
                product_id, quantity = product_tuple

                product = self.get_product(product_id)

                product_final_tuple = (product, quantity)

                purchase.products.append(product_final_tuple)

        # closes the cursor
        cursor.close()

        return purchases_list

class User:

    username = "none"
    password = "none"
    picture_base64 = None

    secret_question = "none"
    secret_answer = "none"

    extra_values = ["secret_question", "secret_answer"]

    def __init__(self, username = "none", password = "none", picture_base64 = None, secret_question = "secret_question_none", secret_answer = "secret_answer_none"):
        self.username = username
        self.password = password 
        self.picture_base64 = picture_base64

        self.secret_question = secret_question
        self.secret_answer = secret_answer

    def set_values(self, values):
        # retrieves the length of the values
        length_values = len(values)

        # iterates over all the values
        for index in range(length_values):

            # retrieves the current value
            value = values[index]

            # in case the value is not None
            if value:
                # retrieves the value name for the extra value
                extra_value_name = self.extra_values[index]

                # sets the value of the extra value
                setattr(self, extra_value_name, value)

        # returns the instance
        return self

class Customer:

    name = "none"
    age = "none"
    address = "none"
    gender = "none"
    picture_base64 = None

    email = "none"
    phone = "none"
    mobile = "none"
    fax = "none"
    description = "none"

    extra_values = ["email", "phone", "mobile", "fax", "description"]

    def __init__(self, name = "none", age = "none", address = "none", gender = "none", picture_base64 = None, email = "email_none", phone = "phone_none", mobile = "mobile_none", fax = "fax_none", description = "description_none"):
        self.name = name
        self.age = age 
        self.address = address
        self.gender = gender
        self.picture_base64 = picture_base64

        self.email = email
        self.phone = phone
        self.mobile = mobile
        self.fax = fax
        self.description = description

    def set_values(self, values):
        # retrieves the length of the values
        length_values = len(values)

        # iterates over all the values
        for index in range(length_values):

            # retrieves the current value
            value = values[index]

            # in case the value is not None
            if value:
                # retrieves the value name for the extra value
                extra_value_name = self.extra_values[index]

                # sets the value of the extra value
                setattr(self, extra_value_name, value)

        # returns the instance
        return self

class Supplier:

    name = "none"
    address = "none"
    picture_base64 = None

    def __init__(self, name = "none", address = "none", picture_base64 = None):
        self.name = name
        self.address = address
        self.picture_base64 = picture_base64

class Product:

    id = "none"
    heading1 = "none"
    heading2 = "none"
    description = "none"
    weight = None
    height = None
    quantity = None
    picture_base64 = None

    def __init__(self, id = "none", heading1 = "none", heading2 = "none", description = "none", weight = None, height = None, quantity = None, picture_base64 = None):
        self.id = id
        self.heading1 = heading1
        self.heading2 = heading2
        self.description = description
        self.weight = weight
        self.height = height
        self.quantity = quantity
        self.picture_base64 = picture_base64

class Sale:

    id = "none"
    payment_type = "none"
    description = "none"
    customer = None
    products = []

    def __init__(self, id = "none", payment_type = "none", description = "none", customer = None):
        self.id = id
        self.payment_type = payment_type
        self.description = description
        self.customer = customer

        self.products = []

class Purchase:

    id = "none"
    description = "none"
    supplier = None
    products = []

    def __init__(self, id = "none", description = "none", supplier = None):
        self.id = id
        self.description = description
        self.supplier = supplier

        self.products = []
