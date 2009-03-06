import settler_query_parser
import settler_query_visitor
import settler_query_generation

import settler_query_structures_associative_array_visitor

ARRAY = {"Person" : [{"name" : "Tobias", "nationality" : "Portuguese", "age" : 12},
                     {"name" : "Matias", "nationality" : "Portuguese", "age" : 56},
                     {"name" : "Matias", "nationality" : "English", "age" : 23}],
         "User" : [{"username" : "joamag", "password" : "123123"},
                   {"username" : "tiagooo", "password" : "234"}]}

rootNode = settler_query_parser.parser.parse("select age from Person where age > 22 and nationality = \"Portuguese\"\n")

query_visitor = settler_query_visitor.Visitor()
query_structures_generation_visitor = settler_query_generation.QueryStructuresGenerationVisitor()

rootNode.accept_post_order(query_visitor)
rootNode.accept_post_order(query_structures_generation_visitor)

query = query_structures_generation_visitor.query

associative_array_visitor = settler_query_structures_associative_array_visitor.AssociativeArrayVisitor()

associative_array_visitor.set_associative_array(ARRAY)

query.accept_post_order(associative_array_visitor)

print associative_array_visitor.data_stack[-1]
