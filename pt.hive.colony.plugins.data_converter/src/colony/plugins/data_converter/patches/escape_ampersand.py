# 200905081420

# replaces occurences of & with "and" due to a template engine encoding bug

#Replacing 194 transactional merchandise names with "&" character, for the expression " and "
#Done...
def up(entity_manager):
    entity_manager.create_transaction("ampersand_transaction")

    # report on current status
    filters = [{"filter_type" : "like",
                "filter_fields" : [{"field_name" : "name",
                                    "field_value" : " and "}]}]
    transactional_merchandise_options = {"filters" : filters}
    transactional_merchandise_class = entity_manager.get_entity_class("TransactionalMerchandise")
    transactional_merchandise = entity_manager._find_all_options(transactional_merchandise_class, transactional_merchandise_options)

    if(len(transactional_merchandise) != 0):
        print "Found %d transactional merchandise with the expression \" and \", conflicts will occur!" % len(transactional_merchandise)

    filters = [{"filter_type" : "like",
                "filter_fields" : [{"field_name" : "name",
                                    "field_value" : "&"}]}]
    transactional_merchandise_options = {"eager_loading_relations": {"consignments" : {}},
                                         "filters" : filters}
    transactional_merchandise_class = entity_manager.get_entity_class("TransactionalMerchandise")
    transactional_merchandise = entity_manager._find_all_options(transactional_merchandise_class, transactional_merchandise_options)

    print "Replacing %d transactional merchandise names with \"&\" character, for the expression \" and \"" % len(transactional_merchandise)
    for item in transactional_merchandise:
         # replace "&" with "and"
         item.name = item.name.replace("&", " and ")
         # escape quotes, due to ORM bug
         item.name = item.name.replace("'", "''")
         # update the item
         entity_manager.update(item)

    print "Done..."

    entity_manager.commit_transaction("ampersand_transaction")

def down(entity_manager):
    entity_manager.create_transaction("ampersand_transaction")

    # report on current status
    filters = [{"filter_type" : "like",
                "filter_fields" : [{"field_name" : "name",
                                    "field_value" : "&"}]}]
    transactional_merchandise_options = {"filters" : filters}
    transactional_merchandise_class = entity_manager.get_entity_class("TransactionalMerchandise")
    transactional_merchandise = entity_manager._find_all_options(transactional_merchandise_class, transactional_merchandise_options)

    if(len(transactional_merchandise) != 0):
        print "Found %d transactional merchandise with the expression \" and \", conflicts will occur!" % len(transactional_merchandise)

    filters = [{"filter_type" : "like",
                "filter_fields" : [{"field_name" : "name",
                                    "field_value" : " and "}]}]
    transactional_merchandise_options = {"eager_loading_relations": {"consignments" : {}},
                                         "filters" : filters}
    transactional_merchandise_class = entity_manager.get_entity_class("TransactionalMerchandise")
    transactional_merchandise = entity_manager._find_all_options(transactional_merchandise_class, transactional_merchandise_options)

    print "Replacing %d transactional merchandise names with the \" and \" expression, for the \"&\" character" % len(transactional_merchandise)
    for item in transactional_merchandise:
         # replace "&" with "and"
         item.name = item.name.replace(" and ", "&")
         # escape quotes, due to ORM bug
         item.name = item.name.replace("'", "''")
         # update the item
         entity_manager.update(item)

    print "Done..."

    entity_manager.commit_transaction("ampersand_transaction")
