import colony.libs.test_util

class ${out value=scaffold_attributes.class_name /}Test:
    def __init__(self, ${out value=scaffold_attributes.variable_name /}_plugin):
        self.${out value=scaffold_attributes.variable_name /}_plugin = ${out value=scaffold_attributes.variable_name /}_plugin

    def get_plugin_test_case_bundle(self):
        return (
            ${out value=scaffold_attributes.class_name /}TestPluginTestCase,
        )

class ${out value=scaffold_attributes.class_name /}TestCase(colony.libs.test_util.ColonyTestCase):

    def setUp(self):
        self.plugin.info("Setting up ${out value=scaffold_attributes.short_name_lowercase /} test case...")

    def tearDown(self):
        self.plugin.info("Tearing down ${out value=scaffold_attributes.short_name_lowercase /} test case...")

    def test_dummy_method(self):
        dummy_result = self.plugin.dummy_method()
        self.assertEquals(dummy_result, "dummy_result")

class ${out value=scaffold_attributes.class_name /}TestPluginTestCase:

    @staticmethod
    def get_test_case():
        return ${out value=scaffold_attributes.class_name /}TestCase

    @staticmethod
    def get_pre_conditions():
        return None

    @staticmethod
    def get_description():
        return "${out value=scaffold_attributes.short_name /} plugin test case"
