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

class UserDocument:

    def __init__(self, parent_plugin):
        self.parent_plugin = parent_plugin
        self.users_list = []
        username_prefix = 'Nome de utilizador</w:t></w:r><w:r w:rsidR="0031313E" w:rsidRPr="0031313E"><w:rPr><w:b/><w:sz w:val="24"/><w:lang w:val="pt-PT"/></w:rPr><w:t>:</w:t></w:r><w:r w:rsidR="0031313E"><w:rPr><w:b/><w:sz w:val="24"/><w:lang w:val="pt-PT"/></w:rPr><w:t xml:space="preserve">  </w:t></w:r><w:sdt><w:sdtPr><w:rPr><w:rStyle w:val="SubtleEmphasis"/></w:rPr><w:id w:val="68721389"/><w:placeholder><w:docPart w:val="5034AFDDCD3F4DA99C052D2359EEC287"/></w:placeholder><w:showingPlcHdr/><w:text/></w:sdtPr><w:sdtContent><w:r w:rsidR="00941D85" w:rsidRPr="0031313E"><w:rPr><w:rStyle w:val="SubtleEmphasis"/><w:lang w:val="pt-PT"/></w:rPr><w:t>'
        username_postfix = '</w:t></w:r></w:sdtContent></w:sdt></w:p><w:p w:rsidR="00355203" w:rsidRPr="0031313E" w:rsidRDefault="00BF5174" w:rsidP="00BF5174"><w:pPr><w:jc w:val="center"/><w:rPr><w:b/><w:lang w:val="pt-PT"/></w:rPr></w:pPr><w:proofErr w:type="spellStart"/><w:r><w:rPr><w:b/><w:sz w:val="24"/><w:lang w:val="pt-PT"/></w:rPr><w:t>'
        password_prefix = 'Palavra-passe</w:t></w:r><w:proofErr w:type="spellEnd"/><w:r w:rsidR="00585049" w:rsidRPr="0031313E"><w:rPr><w:b/><w:sz w:val="24"/><w:lang w:val="pt-PT"/></w:rPr><w:t>:</w:t></w:r><w:r w:rsidR="0031313E"><w:rPr><w:b/><w:sz w:val="24"/><w:lang w:val="pt-PT"/></w:rPr><w:t xml:space="preserve">  </w:t></w:r><w:sdt><w:sdtPr><w:rPr><w:rStyle w:val="SubtleEmphasis"/></w:rPr><w:id w:val="68721416"/><w:placeholder><w:docPart w:val="CE8DF32774FF42028C480491A7F78054"/></w:placeholder><w:showingPlcHdr/><w:text/></w:sdtPr><w:sdtContent><w:r w:rsidR="00941D85" w:rsidRPr="0031313E"><w:rPr><w:rStyle w:val="SubtleEmphasis"/></w:rPr><w:t>'
        password_postfix = '</w:t></w:r></w:sdtContent></w:sdt></w:p><w:p w:rsidR="00BF5174" w:rsidRDefault="00BF5174"><w:pPr><w:rPr><w:b/><w:sz w:val="24"/><w:lang w:val="pt-PT"/></w:rPr></w:pPr></w:p><w:p w:rsidR="00585049" w:rsidRPr="00941D85" w:rsidRDefault="00941D85" w:rsidP="00BF5174"><w:pPr><w:ind w:firstLine="0"/><w:rPr><w:b/><w:lang w:val="pt-PT"/></w:rPr></w:pPr><w:r w:rsidRPr="00941D85"><w:rPr><w:b/><w:lang w:val="pt-PT"/></w:rPr><w:t xml:space="preserve"> </w:t></w:r></w:p><w:sectPr w:rsidR="00585049" w:rsidRPr="00941D85" w:rsidSect="009F2CAB"><w:headerReference w:type="default" r:id="rId9"/><w:footerReference w:type="default" r:id="rId10"/><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1417" w:right="1701" w:bottom="1417" w:left="1701" w:header="708" w:footer="708" w:gutter="0"/><w:cols w:space="708"/><w:docGrid w:linePitch="360"/></w:sectPr></w:body></w:document>'
        self.prefixes_map = {}
        self.postfixes_map = {}
        self.prefixes_map["username"] = username_prefix
        self.prefixes_map["password"] = password_prefix
        self.postfixes_map["username"] = username_postfix
        self.postfixes_map["password"] = password_postfix
            
    def get_uid(self, data):
        return data["username"]
        
    def get_data(self):
        self.users_list = self.parent_plugin.business_services_plugin.get_all_users()
        return self.users_list
    
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
    
    def update_username(self, original_content, field_value):
        prefix = self.prefixes_map["username"]
        postfix = self.postfixes_map["username"]
        return self.update_handler(prefix, postfix, original_content, field_value)
    
    def update_password(self, original_content, field_value):
        prefix = self.prefixes_map["password"]
        postfix = self.postfixes_map["password"]
        return self.update_handler(prefix, postfix, original_content, field_value)
    
    def get_username(self, content):
        prefix = self.prefixes_map["password"]
        postfix = self.postfixes_map["password"]
        return self.get_handler(prefix, postfix, content)
    
    def get_password(self, content):
        prefix = self.prefixes_map["password"]
        postfix = self.postfixes_map["password"]
        return self.get_handler(prefix, postfix, content)
    
class HiveFSUsersDocx:

    parent_plugin = None
    openxml_plugin = None
    user_document = None
    users = None
    
    def __init__(self, parent_plugin):
        self.user_document = UserDocument(parent_plugin)
        self.parent_plugin = parent_plugin
        self.openxml_plugin = parent_plugin.openxml_plugin
        
    def get_files(self):
        document_contents_map = {}
        # get the full path to the user form template
        user_form_template_path = os.path.join(os.path.dirname(__file__), "user_form_template.docx")
        # write a new file for every user
        for user in self.user_document.get_data():
            # copy the template to a temporary file
            user_form_temporary_file_path = os.path.join(tempfile.gettempdir(), "user_form_template.docx")
            shutil.copyfile(user_form_template_path, user_form_temporary_file_path)
            # edit the temporary document
            user_form_document = self.openxml_plugin.open(user_form_temporary_file_path)
            document_path = user_form_document.get_full_path("word/document.xml")
            document_file = open(document_path, "r")
            content = document_file.read()
            document_file.close()
            document_file = open(document_path , "w")
            user_map = {}
            user_map["username"] = user.username
            user_map["password"] = user.password
            for user_attribute in user_map:
                field_value = user_map[user_attribute]
                handler = getattr(self.user_document, "update_" + user_attribute)
                if handler:
                    content = handler(content, field_value)
            document_file.write(content)
            document_file.close()
            self.openxml_plugin.close(user_form_temporary_file_path)
            file = open(user_form_temporary_file_path, "rb")
            contents = file.read()
            contents_base64 = base64.b64encode(contents)
            document_contents_map[self.user_document.get_uid(user_map)] = contents_base64
            file.close()
            # copy the temporary file to the destination directory
            #shutil.copyfile(user_form_temporary_file_path, "c:\\" + self.user_document.get_name(user))
            #os.remove(user_form_temporary_file_path)
        return document_contents_map

    def get_template(self):
        user_form_template_path = os.path.join(os.path.dirname(__file__), "user_form_template.docx")
        file = open(user_form_template_path, "rb")
        file_content = file.read()
        file.close()
        file_content = base64.b64encode(file_content)
        return file_content
    
    def update_file(self, uid, new_content):
        username = self.user_document.get_username(new_content)
        password = self.user_document.get_password(new_content)
        self.parent_plugin.business_services_plugin.edit_user(uid, ["username","password"], [username, password])

    def create_file(self, content):
        username = self.user_document.get_username(content)
        password = self.user_document.get_password(content)
        self.parent_plugin.business_services_plugin.create_user(username, password)
