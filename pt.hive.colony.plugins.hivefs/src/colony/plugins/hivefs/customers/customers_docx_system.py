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

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 1615 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-08-07 18:45:11 +0100 (Qui, 07 Ago 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import tempfile
import random
import shutil
import base64

class ClientDocument:

    def __init__(self, parent_plugin):
        self.parent_plugin = parent_plugin
        self.clients_list = []
        self.prefixes_map = {}
        self.postfixes_map = {}
                       
        name_prefix = 'Nome:</w:t></w:r><w:r><w:rPr><w:b/><w:sz w:val="24"/><w:lang w:val="pt-PT"/></w:rPr><w:t xml:space="preserve">  </w:t></w:r><w:sdt><w:sdtPr><w:rPr><w:rStyle w:val="SubtleEmphasis"/></w:rPr><w:id w:val="68721389"/><w:placeholder><w:docPart w:val="5034AFDDCD3F4DA99C052D2359EEC287"/></w:placeholder><w:showingPlcHdr/><w:text/></w:sdtPr><w:sdtContent><w:r w:rsidR="00393BFE" w:rsidRPr="00BB503E"><w:rPr><w:rStyle w:val="PlaceholderText"/><w:lang w:val="pt-PT"/></w:rPr><w:t>'
        name_postfix = '</w:t></w:r></w:sdtContent></w:sdt></w:p><w:p w:rsidR="00355203" w:rsidRPr="0031313E" w:rsidRDefault="00585049"><w:pPr><w:rPr><w:b/><w:lang w:val="pt-PT"/></w:rPr></w:pPr><w:r w:rsidRPr="0031313E"><w:rPr><w:b/><w:sz w:val="24"/><w:lang w:val="pt-PT"/></w:rPr><w:t>'
        address_prefix = 'Morada:</w:t></w:r><w:r w:rsidR="0031313E"><w:rPr><w:b/><w:sz w:val="24"/><w:lang w:val="pt-PT"/></w:rPr><w:t xml:space="preserve">  </w:t></w:r><w:sdt><w:sdtPr><w:rPr><w:rStyle w:val="SubtleEmphasis"/></w:rPr><w:id w:val="68721416"/><w:placeholder><w:docPart w:val="CE8DF32774FF42028C480491A7F78054"/></w:placeholder><w:showingPlcHdr/><w:text/></w:sdtPr><w:sdtContent><w:r w:rsidR="00941D85" w:rsidRPr="00BB503E"><w:rPr><w:rStyle w:val="SubtleEmphasis"/><w:lang w:val="pt-PT"/></w:rPr><w:t>'
        address_postfix = '</w:t></w:r></w:sdtContent></w:sdt></w:p><w:p w:rsidR="00941D85" w:rsidRPr="0031313E" w:rsidRDefault="00941D85"><w:pPr><w:rPr><w:b/><w:lang w:val="pt-PT"/></w:rPr></w:pPr><w:r w:rsidRPr="0031313E"><w:rPr><w:b/><w:sz w:val="24"/><w:lang w:val="pt-PT"/></w:rPr><w:t>'
        age_prefix = 'Data de nascimento:</w:t></w:r><w:r w:rsidR="0031313E"><w:rPr><w:b/><w:sz w:val="24"/><w:lang w:val="pt-PT"/></w:rPr><w:t xml:space="preserve">  </w:t></w:r><w:sdt><w:sdtPr><w:rPr><w:rStyle w:val="SubtleEmphasis"/></w:rPr><w:id w:val="68721432"/><w:placeholder><w:docPart w:val="EA6DDAB43F95445EBFA2D52C4CE27535"/></w:placeholder><w:showingPlcHdr/><w:date><w:dateFormat w:val="dd-MM-yyyy"/><w:lid w:val="pt-PT"/><w:storeMappedDataAs w:val="dateTime"/><w:calendar w:val="gregorian"/></w:date></w:sdtPr><w:sdtContent><w:r w:rsidRPr="0031313E"><w:rPr><w:rStyle w:val="SubtleEmphasis"/><w:lang w:val="pt-PT"/></w:rPr><w:t>'
        age_postfix = '</w:t></w:r></w:sdtContent></w:sdt></w:p><w:p w:rsidR="00585049" w:rsidRPr="00941D85" w:rsidRDefault="00585049"><w:pPr><w:rPr><w:b/><w:lang w:val="pt-PT"/></w:rPr></w:pPr><w:r w:rsidRPr="0031313E"><w:rPr><w:b/><w:sz w:val="24"/><w:lang w:val="pt-PT"/></w:rPr><w:t>'
        phone_prefix = 'Telefone:</w:t></w:r><w:r w:rsidR="0031313E"><w:rPr><w:b/><w:sz w:val="24"/><w:lang w:val="pt-PT"/></w:rPr><w:t xml:space="preserve">  </w:t></w:r><w:sdt><w:sdtPr><w:rPr><w:rStyle w:val="SubtleEmphasis"/></w:rPr><w:id w:val="68721423"/><w:placeholder><w:docPart w:val="A1437988A4FF450E94AE25B2D2DA97B7"/></w:placeholder><w:showingPlcHdr/><w:text/></w:sdtPr><w:sdtContent><w:r w:rsidR="00941D85" w:rsidRPr="0031313E"><w:rPr><w:rStyle w:val="SubtleEmphasis"/><w:lang w:val="pt-PT"/></w:rPr><w:t>'
        phone_postfix = '</w:t></w:r></w:sdtContent></w:sdt></w:p><w:p w:rsidR="00585049" w:rsidRPr="00941D85" w:rsidRDefault="00585049"><w:pPr><w:rPr><w:b/><w:lang w:val="pt-PT"/></w:rPr></w:pPr><w:r w:rsidRPr="0031313E"><w:rPr><w:b/><w:sz w:val="24"/><w:lang w:val="pt-PT"/></w:rPr><w:t>'
        email_prefix = 'E-mail:</w:t></w:r><w:r w:rsidR="0031313E" w:rsidRPr="0031313E"><w:rPr><w:b/><w:lang w:val="pt-PT"/></w:rPr><w:t xml:space="preserve">  </w:t></w:r><w:sdt><w:sdtPr><w:rPr><w:rStyle w:val="SubtleEmphasis"/></w:rPr><w:id w:val="68721428"/><w:placeholder><w:docPart w:val="9BED99CDC7A441809D04970DD6EBDFA1"/></w:placeholder><w:showingPlcHdr/><w:text/></w:sdtPr><w:sdtContent><w:r w:rsidR="0031313E" w:rsidRPr="0031313E"><w:rPr><w:rStyle w:val="SubtleEmphasis"/><w:lang w:val="pt-PT"/></w:rPr><w:t xml:space="preserve"> '
        email_postfix = '</w:t></w:r></w:sdtContent></w:sdt><w:r w:rsidR="00941D85" w:rsidRPr="00941D85"><w:rPr><w:b/><w:lang w:val="pt-PT"/></w:rPr><w:t xml:space="preserve"> </w:t></w:r></w:p><w:sectPr w:rsidR="00585049" w:rsidRPr="00941D85" w:rsidSect="009F2CAB"><w:headerReference w:type="default" r:id="rId9"/><w:footerReference w:type="default" r:id="rId10"/><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1417" w:right="1701" w:bottom="1417" w:left="1701" w:header="708" w:footer="708" w:gutter="0"/><w:cols w:space="708"/><w:docGrid w:linePitch="360"/></w:sectPr></w:body></w:document>'
        self.prefixes_map["name"] = name_prefix
        self.postfixes_map["name"] = name_postfix
        self.prefixes_map["address"] = address_prefix
        self.postfixes_map["address"] = address_postfix
        self.prefixes_map["age"] = age_prefix
        self.postfixes_map["age"] = age_postfix
        self.prefixes_map["phone"] = phone_prefix
        self.postfixes_map["phone"] = phone_postfix
        self.prefixes_map["email"] = email_prefix
        self.postfixes_map["email"] = email_postfix
        
    def get_uid(self, data):
        return data["name"]
        
    def get_data(self):
        self.clients_list = self.parent_plugin.business_services_plugin.get_all_customers()
        return self.clients_list
    
    def get_handler(self, prefix, postfix, content):
        prefix_offset = original_content.find(prefix)
        prefix_length = len(prefix)
        postfix_offset = original_content.find(postfix)
        field_value = original_content[prefix_offset+prefix_length:postfix_offset]
        return field_value
    
    def update_handler(self, prefix, postfix, original_content, field_value):
        prefix_offset = original_content.find(prefix)
        prefix_length = len(prefix)
        postfix_offset = original_content.find(postfix)
        new_content = original_content[:prefix_offset+prefix_length] + str(field_value) + original_content[postfix_offset:]
        return new_content
    
    def update_name(self, original_content, field_value):
        prefix = self.prefixes_map["name"]
        postfix = self.postfixes_map["name"]
        return self.update_handler(prefix, postfix, original_content, field_value)
    
    def update_address(self, original_content, field_value):
        prefix = self.prefixes_map["address"]
        postfix = self.postfixes_map["address"]
        return self.update_handler(prefix, postfix, original_content, field_value)
    
    def update_age(self, original_content, field_value):
        prefix = self.prefixes_map["age"]
        postfix = self.postfixes_map["age"]
        return self.update_handler(prefix, postfix, original_content, field_value)
    
    def update_phone(self, original_content, field_value):
        prefix = self.prefixes_map["phone"]
        postfix = self.postfixes_map["phone"]
        return self.update_handler(prefix, postfix, original_content, field_value)
    
    def update_email(self, original_content, field_value):
        prefix = self.prefixes_map["email"]
        postfix = self.postfixes_map["email"]
        return self.update_handler(prefix, postfix, original_content, field_value)
    
    def get_name(self, content):
        prefix = self.prefixes_map["name"]
        postfix = self.postfixes_map["name"]
        return self.get_handler(prefix, postfix, content)
    
    def get_address(self, content):
        prefix = self.prefixes_map["address"]
        postfix = self.postfixes_map["address"]
        return self.get_handler(prefix, postfix, content)
    
    def get_age(self, content):
        prefix = self.prefixes_map["age"]
        postfix = self.postfixes_map["age"]
        return self.get_handler(prefix, postfix, content)
    
    def get_phone(self, content):
        prefix = self.prefixes_map["phone"]
        postfix = self.postfixes_map["phone"]
        return self.get_handler(prefix, postfix, content)

    def get_email(self, content):
        prefix = self.prefixes_map["email"]
        postfix = self.postfixes_map["email"]
        return self.get_handler(prefix, postfix, content)
        
class HiveFSCustomersDocx:

    parent_plugin = None
    openxml_plugin = None
    client_document = None
    clients = None
    
    def __init__(self, parent_plugin):
        self.client_document = ClientDocument(parent_plugin)
        self.parent_plugin = parent_plugin
        self.openxml_plugin = parent_plugin.openxml_plugin
        
    def get_files(self):
        document_contents_map = {}
        # get the full path to the client form template
        client_form_template_path = os.path.join(os.path.dirname(__file__), "customer_form_template.docx")
        # write a new file for every client
        for client in self.client_document.get_data():
            # copy the template to a temporary file
            client_form_temporary_file_path = os.path.join(tempfile.gettempdir(), "customer_form_template.docx")
            shutil.copyfile(client_form_template_path, client_form_temporary_file_path)
            # edit the temporary document
            client_form_document = self.openxml_plugin.open(client_form_temporary_file_path)
            document_path = client_form_document.get_full_path("word/document.xml")
            document_file = open(document_path, "r")
            content = document_file.read()
            document_file.close()
            document_file = open(document_path , "w")
            client_map = {}
            client_map["name"] = client.name
            client_map["address"] = client.address
            client_map["age"] = client.age
            client_map["phone"] = ""#client.phone
            client_map["email"] = ""#client.email
            for client_attribute in client_map:
                field_value = client_map[client_attribute]
                handler = getattr(self.client_document, "update_" + client_attribute)
                if handler:
                    content = handler(content, field_value)
            document_file.write(content)
            document_file.close()
            self.openxml_plugin.close(client_form_temporary_file_path)
            file = open(client_form_temporary_file_path, "rb")
            contents = file.read()
            contents_base64 = base64.b64encode(contents)
            document_contents_map[self.client_document.get_uid(client_map)] = contents_base64
            file.close()
            # copy the temporary file to the destination directory
            #shutil.copyfile(client_form_temporary_file_path, "c:\\" + self.client_document.get_name(client))
            #os.remove(client_form_temporary_file_path)
        return document_contents_map
    
    def get_template(self):
        client_form_template_path = os.path.join(os.path.dirname(__file__), "customer_form_template.docx")
        file = open(client_form_template_path, "rb")
        file_content = file.read()
        file.close()
        file_content = base64.b64encode(file_content)
        return file_content
    
    def update_file(self, uid, new_content):
        name = self.user_document.get_name(new_content)
        age = self.user_document.get_age(new_content)
        address = self.user_document.get_address(new_content)
        gender = self.user_document.get_gender(new_content)
        self.parent_plugin.business_services_plugin.edit_customer(uid, ["name", "age", "address", "gender"], [name, age, address, gender])
    
    def create_file(self, content):
        name = self.user_document.get_name(content)
        age = self.user_document.get_age(content)
        address = self.user_document.get_address(content)
        gender = self.user_document.get_gender(content)
        self.parent_plugin.business_services_plugin.create_customer(name, age, address, gender)         
                          