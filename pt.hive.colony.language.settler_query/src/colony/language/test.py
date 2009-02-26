import settler_query_structures
import settler_query_structures_visitor
import settler_query_structures_associative_array_visitor

ARRAY = {"Person" : [{"name" : "Tobias", "nationality" : "Portuguese", "age" : 12},
                     {"name" : "Matias", "nationality" : "Portuguese", "age" : 56},
                     {"name" : "Matias", "nationality" : "English", "age" : 23}],
         "User" : [{"username" : "joamag", "password" : "123123"},
                   {"username" : "tiagooo", "password" : "234"}]}

# creates a new select query
select_query = settler_query_structures.SelectQuery()

name_field = settler_query_structures.SimpleField()
name_field.field_name = "name"

# adds a new select field
select_query.add_select_field(name_field)

person_entity = settler_query_structures.SimpleEntity()
person_entity.entity_name = "Person"

# adds a new select entity
select_query.add_select_entity(person_entity)

nationality_field = settler_query_structures.SimpleFieldReference()
nationality_field.field_name = "nationality"

portuguese_value = settler_query_structures.Value()
portuguese_value.value = "Portuguese"

nationality_filter = settler_query_structures.EqualTermFilter()
nationality_filter.first_operand = nationality_field
nationality_filter.second_operand = portuguese_value

# adds a new select filter
select_query.add_select_filters(nationality_filter)

age_field = settler_query_structures.SimpleFieldReference()
age_field.field_name = "age"

age_value = settler_query_structures.Value()
age_value.value = 14

adult_age_filter = settler_query_structures.GreaterTermFilter()
adult_age_filter.first_operand = age_field
adult_age_filter.second_operand = age_value

# adds a new select filter
select_query.add_select_filters(adult_age_filter)

associative_array_visitor = settler_query_structures_associative_array_visitor.AssociativeArrayVisitor()

associative_array_visitor.set_associative_array(ARRAY)

visitor = settler_query_structures_visitor.Visitor()

#select_query.accept_post_order(visitor)
select_query.accept_post_order(associative_array_visitor)

print associative_array_visitor.data_stack[-1]

#print [value["age"] for value in ARRAY["Person"] if value["nationality"] == "Portuguese" and value["age"] > 14]
