import settler_query_parser
import settler_query_generation

rootNode = settler_query_parser.parser.parse("select tobias from matias where age = \"asd\"\n")

query_structures_generation_visitor = settler_query_generation.QueryStructuresGenerationVisitor()

rootNode.accept_post_order(query_structures_generation_visitor)
