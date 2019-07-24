# -*- coding: utf-8 -*-
#
#
# Copyright (C) 2009-2011, Ecole Polytechnique Fédérale de Lausanne (EPFL) and
# Hospital Center and University of Lausanne (UNIL-CHUV), Switzerland
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the Ecole Polytechnique Fédérale de Lausanne (EPFL)
#       and Hospital Center and University of Lausanne (UNIL-CHUV) nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL "Ecole Polytechnique Fédérale de Lausanne (EPFL) and
# Hospital Center and University of Lausanne (UNIL-CHUV)" BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#
# Library adapted by The Virtual Brain team - July 2019
#
#
# TheVirtualBrain-Framework Package. This package holds all Data Management, and
# Web-UI helpful to run brain-simulations. To use it, you also need do download
# TheVirtualBrain-Scientific Package (for simulators). See content of the
# documentation-folder for more details. See also http://www.thevirtualbrain.org
#
# (c) 2012-2017, Baycrest Centre for Geriatric Care ("Baycrest") and others
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#   CITATION:
# When using The Virtual Brain for scientific publications, please cite it as follows:
#
#   Paula Sanz Leon, Stuart A. Knock, M. Marmaduke Woodman, Lia Domide,
#   Jochen Mersmann, Anthony R. McIntosh, Viktor Jirsa (2013)
#       The Virtual Brain: a simulator of primate brain network dynamics.
#   Frontiers in Neuroinformatics (7:10. doi: 10.3389/fninf.2013.00010)
#
#

import sys
import getopt
import re as re_

etree_ = None
Verbose_import_ = False
(   XMLParser_import_none, XMLParser_import_lxml,
    XMLParser_import_elementtree
    ) = list(range(3))
XMLParser_import_library = None
try:
    # lxml
    from lxml import etree as etree_
    XMLParser_import_library = XMLParser_import_lxml
    if Verbose_import_:
        print("running with lxml.etree")
except ImportError:
    try:
        # cElementTree from Python 2.5+
        import xml.etree.cElementTree as etree_
        XMLParser_import_library = XMLParser_import_elementtree
        if Verbose_import_:
            print("running with cElementTree on Python 2.5+")
    except ImportError:
        try:
            # ElementTree from Python 2.5+
            import xml.etree.ElementTree as etree_
            XMLParser_import_library = XMLParser_import_elementtree
            if Verbose_import_:
                print("running with ElementTree on Python 2.5+")
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree_
                XMLParser_import_library = XMLParser_import_elementtree
                if Verbose_import_:
                    print("running with cElementTree")
            except ImportError:
                try:
                    # normal ElementTree install
                    import elementtree.ElementTree as etree_
                    XMLParser_import_library = XMLParser_import_elementtree
                    if Verbose_import_:
                        print("running with ElementTree")
                except ImportError:
                    raise ImportError("Failed to import ElementTree from any known place")

def parsexml_(*args, **kwargs):
    if (XMLParser_import_library == XMLParser_import_lxml and
        'parser' not in kwargs):
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        kwargs['parser'] = etree_.ETCompatXMLParser()
    doc = etree_.parse(*args, **kwargs)
    return doc

#
# User methods
#
# Calls to the methods in these classes are generated by generateDS.py.
# You can replace these methods by re-implementing the following class
#   in a module named generatedssuper.py.

try:
    from generatedssuper import GeneratedsSuper
except ImportError as exp:

    class GeneratedsSuper(object):
        def gds_format_string(self, input_data, input_name=''):
            return input_data
        def gds_validate_string(self, input_data, node, input_name=''):
            return input_data
        def gds_format_integer(self, input_data, input_name=''):
            return '%d' % input_data
        def gds_validate_integer(self, input_data, node, input_name=''):
            return input_data
        def gds_format_integer_list(self, input_data, input_name=''):
            return '%s' % input_data
        def gds_validate_integer_list(self, input_data, node, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    fvalue = float(value)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(node, 'Requires sequence of integers')
            return input_data
        def gds_format_float(self, input_data, input_name=''):
            return '%f' % input_data
        def gds_validate_float(self, input_data, node, input_name=''):
            return input_data
        def gds_format_float_list(self, input_data, input_name=''):
            return '%s' % input_data
        def gds_validate_float_list(self, input_data, node, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    fvalue = float(value)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(node, 'Requires sequence of floats')
            return input_data
        def gds_format_double(self, input_data, input_name=''):
            return '%e' % input_data
        def gds_validate_double(self, input_data, node, input_name=''):
            return input_data
        def gds_format_double_list(self, input_data, input_name=''):
            return '%s' % input_data
        def gds_validate_double_list(self, input_data, node, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    fvalue = float(value)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(node, 'Requires sequence of doubles')
            return input_data
        def gds_format_boolean(self, input_data, input_name=''):
            return '%s' % input_data
        def gds_validate_boolean(self, input_data, node, input_name=''):
            return input_data
        def gds_format_boolean_list(self, input_data, input_name=''):
            return '%s' % input_data
        def gds_validate_boolean_list(self, input_data, node, input_name=''):
            values = input_data.split()
            for value in values:
                if value not in ('true', '1', 'false', '0', ):
                    raise_parse_error(node, 'Requires sequence of booleans ("true", "1", "false", "0")')
            return input_data
        def gds_str_lower(self, instring):
            return instring.lower()
        def get_path_(self, node):
            path_list = []
            self.get_path_list_(node, path_list)
            path_list.reverse()
            path = '/'.join(path_list)
            return path
        Tag_strip_pattern_ = re_.compile(r'\{.*\}')
        def get_path_list_(self, node, path_list):
            if node is None:
                return
            tag = GeneratedsSuper.Tag_strip_pattern_.sub('', node.tag)
            if tag:
                path_list.append(tag)
            self.get_path_list_(node.getparent(), path_list)


#
# If you have installed IPython you can uncomment and use the following.
# IPython is available from http://ipython.scipy.org/.
#

## from IPython.Shell import IPShellEmbed
## args = ''
## ipshell = IPShellEmbed(args,
##     banner = 'Dropping into IPython',
##     exit_msg = 'Leaving Interpreter, back to program.')

# Then use the following line where and when you want to drop into the
# IPython shell:
#    ipshell('<some message> -- Entering ipshell.\nHit Ctrl-D to exit')

#
# Globals
#

ExternalEncoding = 'ascii'
Tag_pattern_ = re_.compile(r'({.*})?(.*)')
STRING_CLEANUP_PAT = re_.compile(r"[\n\r\s]+")

#
# Support/utility functions.
#

def showIndent(outfile, level):
    for idx in range(level):
        outfile.write('    ')

def quote_xml(inStr):
    if not inStr:
        return ''
    s1 = (isinstance(inStr, str) and inStr or
          '%s' % inStr)
    s1 = s1.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    return s1

def quote_attrib(inStr):
    s1 = (isinstance(inStr, str) and inStr or
          '%s' % inStr)
    s1 = s1.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    if '"' in s1:
        if "'" in s1:
            s1 = '"%s"' % s1.replace('"', "&quot;")
        else:
            s1 = "'%s'" % s1
    else:
        s1 = '"%s"' % s1
    return s1

def quote_python(inStr):
    s1 = inStr
    if s1.find("'") == -1:
        if s1.find('\n') == -1:
            return "'%s'" % s1
        else:
            return "'''%s'''" % s1
    else:
        if s1.find('"') != -1:
            s1 = s1.replace('"', '\\"')
        if s1.find('\n') == -1:
            return '"%s"' % s1
        else:
            return '"""%s"""' % s1


def get_all_text_(node):
    if node.text is not None:
        text = node.text
    else:
        text = ''
    for child in node:
        if child.tail is not None:
            text += child.tail
    return text


class GDSParseError(Exception):
    pass

def raise_parse_error(node, msg):
    if XMLParser_import_library == XMLParser_import_lxml:
        msg = '%s (element %s/line %d)' % (msg, node.tag, node.sourceline, )
    else:
        msg = '%s (element %s)' % (msg, node.tag, )
    raise GDSParseError(msg)


class MixedContainer:
    # Constants for category:
    CategoryNone = 0
    CategoryText = 1
    CategorySimple = 2
    CategoryComplex = 3
    # Constants for content_type:
    TypeNone = 0
    TypeText = 1
    TypeString = 2
    TypeInteger = 3
    TypeFloat = 4
    TypeDecimal = 5
    TypeDouble = 6
    TypeBoolean = 7
    def __init__(self, category, content_type, name, value):
        self.category = category
        self.content_type = content_type
        self.name = name
        self.value = value
    def getCategory(self):
        return self.category
    def getContenttype(self, content_type):
        return self.content_type
    def getValue(self):
        return self.value
    def getName(self):
        return self.name
    def export(self, outfile, level, name, namespace):
        if self.category == MixedContainer.CategoryText:
            # Prevent exporting empty content as empty lines.
            if self.value.strip(): 
                outfile.write(self.value)
        elif self.category == MixedContainer.CategorySimple:
            self.exportSimple(outfile, level, name)
        else:    # category == MixedContainer.CategoryComplex
            self.value.export(outfile, level, namespace,name)
    def exportSimple(self, outfile, level, name):
        if self.content_type == MixedContainer.TypeString:
            outfile.write('<%s>%s</%s>' % (self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeInteger or \
                self.content_type == MixedContainer.TypeBoolean:
            outfile.write('<%s>%d</%s>' % (self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeFloat or \
                self.content_type == MixedContainer.TypeDecimal:
            outfile.write('<%s>%f</%s>' % (self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeDouble:
            outfile.write('<%s>%g</%s>' % (self.name, self.value, self.name))
    def exportLiteral(self, outfile, level, name):
        if self.category == MixedContainer.CategoryText:
            showIndent(outfile, level)
            outfile.write('model_.MixedContainer(%d, %d, "%s", "%s"),\n' % \
                (self.category, self.content_type, self.name, self.value))
        elif self.category == MixedContainer.CategorySimple:
            showIndent(outfile, level)
            outfile.write('model_.MixedContainer(%d, %d, "%s", "%s"),\n' % \
                (self.category, self.content_type, self.name, self.value))
        else:    # category == MixedContainer.CategoryComplex
            showIndent(outfile, level)
            outfile.write('model_.MixedContainer(%d, %d, "%s",\n' % \
                (self.category, self.content_type, self.name,))
            self.value.exportLiteral(outfile, level + 1)
            showIndent(outfile, level)
            outfile.write(')\n')


class MemberSpec_(object):
    def __init__(self, name='', data_type='', container=0):
        self.name = name
        self.data_type = data_type
        self.container = container
    def set_name(self, name): self.name = name
    def get_name(self): return self.name
    def set_data_type(self, data_type): self.data_type = data_type
    def get_data_type_chain(self): return self.data_type
    def get_data_type(self):
        if isinstance(self.data_type, list):
            if len(self.data_type) > 0:
                return self.data_type[-1]
            else:
                return 'xs:string'
        else:
            return self.data_type
    def set_container(self, container): self.container = container
    def get_container(self): return self.container

def _cast(typ, value):
    if typ is None or value is None:
        return value
    return typ(value)

#
# Data representation classes.
#

class property(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, name=None, value=None, type_=None, uncertainty=None, unit=None):
        self.name = name
        self.value = value
        self.type_ = type_
        self.uncertainty = uncertainty
        self.unit = unit
    def factory(*args_, **kwargs_):
        if property.subclass:
            return property.subclass(*args_, **kwargs_)
        else:
            return property(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_name(self): return self.name
    def set_name(self, name): self.name = name
    def get_value(self): return self.value
    def set_value(self, value): self.value = value
    def get_type(self): return self.type_
    def set_type(self, type_): self.type_ = type_
    def get_uncertainty(self): return self.uncertainty
    def set_uncertainty(self, uncertainty): self.uncertainty = uncertainty
    def get_unit(self): return self.unit
    def set_unit(self, unit): self.unit = unit
    def export(self, outfile, level, namespace_='cml:', name_='property', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='property')
        if self.hasContent_():
            outfile.write('>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='property'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='property'):
        if self.name is not None:
            showIndent(outfile, level)
            outfile.write('<%sname>%s</%sname>\n' % (namespace_, self.gds_format_string(quote_xml(self.name).encode(ExternalEncoding), input_name='name'), namespace_))
        if self.value is not None:
            showIndent(outfile, level)
            outfile.write('<%svalue>%s</%svalue>\n' % (namespace_, self.gds_format_string(quote_xml(self.value).encode(ExternalEncoding), input_name='value'), namespace_))
        if self.type_ is not None:
            showIndent(outfile, level)
            outfile.write('<%stype>%s</%stype>\n' % (namespace_, self.gds_format_string(quote_xml(self.type_).encode(ExternalEncoding), input_name='type'), namespace_))
        if self.uncertainty is not None:
            showIndent(outfile, level)
            outfile.write('<%suncertainty>%s</%suncertainty>\n' % (namespace_, self.gds_format_string(quote_xml(self.uncertainty).encode(ExternalEncoding), input_name='uncertainty'), namespace_))
        if self.unit is not None:
            showIndent(outfile, level)
            outfile.write('<%sunit>%s</%sunit>\n' % (namespace_, self.gds_format_string(quote_xml(self.unit).encode(ExternalEncoding), input_name='unit'), namespace_))
    def hasContent_(self):
        if (
            self.name is not None or
            self.value is not None or
            self.type_ is not None or
            self.uncertainty is not None or
            self.unit is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='property'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        if self.name is not None:
            showIndent(outfile, level)
            outfile.write('name=%s,\n' % quote_python(self.name).encode(ExternalEncoding))
        if self.value is not None:
            showIndent(outfile, level)
            outfile.write('value=%s,\n' % quote_python(self.value).encode(ExternalEncoding))
        if self.type_ is not None:
            showIndent(outfile, level)
            outfile.write('type_=%s,\n' % quote_python(self.type_).encode(ExternalEncoding))
        if self.uncertainty is not None:
            showIndent(outfile, level)
            outfile.write('uncertainty=%s,\n' % quote_python(self.uncertainty).encode(ExternalEncoding))
        if self.unit is not None:
            showIndent(outfile, level)
            outfile.write('unit=%s,\n' % quote_python(self.unit).encode(ExternalEncoding))
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        if nodeName_ == 'name':
            name_ = child_.text
            name_ = self.gds_validate_string(name_, node, 'name')
            self.name = name_
        elif nodeName_ == 'value':
            value_ = child_.text
            value_ = self.gds_validate_string(value_, node, 'value')
            self.value = value_
        elif nodeName_ == 'type':
            type_ = child_.text
            type_ = self.gds_validate_string(type_, node, 'type')
            self.type_ = type_
        elif nodeName_ == 'uncertainty':
            uncertainty_ = child_.text
            uncertainty_ = self.gds_validate_string(uncertainty_, node, 'uncertainty')
            self.uncertainty = uncertainty_
        elif nodeName_ == 'unit':
            unit_ = child_.text
            unit_ = self.gds_validate_string(unit_, node, 'unit')
            self.unit = unit_
# end class property


class section(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, title=None, name=None, type_=None, property=None):
        self.title = _cast(None, title)
        self.name = name
        self.type_ = type_
        if property is None:
            self.property = []
        else:
            self.property = property
    def factory(*args_, **kwargs_):
        if section.subclass:
            return section.subclass(*args_, **kwargs_)
        else:
            return section(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_name(self): return self.name
    def set_name(self, name): self.name = name
    def get_type(self): return self.type_
    def set_type(self, type_): self.type_ = type_
    def get_property(self): return self.property
    def set_property(self, property): self.property = property
    def add_property(self, value): self.property.append(value)
    def insert_property(self, index, value): self.property[index] = value
    def get_title(self): return self.title
    def set_title(self, title): self.title = title
    def export(self, outfile, level, namespace_='cml:', name_='section', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='section')
        if self.hasContent_():
            outfile.write('>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='section'):
        if self.title is not None and 'title' not in already_processed:
            already_processed.append('title')
            outfile.write(' title=%s' % (self.gds_format_string(quote_attrib(self.title).encode(ExternalEncoding), input_name='title'), ))
    def exportChildren(self, outfile, level, namespace_='cml:', name_='section'):
        if self.name is not None:
            showIndent(outfile, level)
            outfile.write('<%sname>%s</%sname>\n' % (namespace_, self.gds_format_string(quote_xml(self.name).encode(ExternalEncoding), input_name='name'), namespace_))
        if self.type_ is not None:
            showIndent(outfile, level)
            outfile.write('<%stype>%s</%stype>\n' % (namespace_, self.gds_format_string(quote_xml(self.type_).encode(ExternalEncoding), input_name='type'), namespace_))
        for property_ in self.property:
            property_.export(outfile, level, namespace_, name_='property')
    def hasContent_(self):
        if (
            self.name is not None or
            self.type_ is not None or
            self.property
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='section'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.title is not None and 'title' not in already_processed:
            already_processed.append('title')
            showIndent(outfile, level)
            outfile.write('title = "%s",\n' % (self.title,))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.name is not None:
            showIndent(outfile, level)
            outfile.write('name=%s,\n' % quote_python(self.name).encode(ExternalEncoding))
        if self.type_ is not None:
            showIndent(outfile, level)
            outfile.write('type_=%s,\n' % quote_python(self.type_).encode(ExternalEncoding))
        showIndent(outfile, level)
        outfile.write('property=[\n')
        level += 1
        for property_ in self.property:
            showIndent(outfile, level)
            outfile.write('model_.property(\n')
            property_.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('title')
        if value is not None and 'title' not in already_processed:
            already_processed.append('title')
            self.title = value
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        if nodeName_ == 'name':
            name_ = child_.text
            name_ = self.gds_validate_string(name_, node, 'name')
            self.name = name_
        elif nodeName_ == 'type':
            type_ = child_.text
            type_ = self.gds_validate_string(type_, node, 'type')
            self.type_ = type_
        elif nodeName_ == 'property': 
            obj_ = property.factory()
            obj_.build(child_)
            self.property.append(obj_)
# end class section


class metadata(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, tag=None, section=None):
        if tag is None:
            self.tag = []
        else:
            self.tag = tag
        if section is None:
            self.section = []
        else:
            self.section = section
    def factory(*args_, **kwargs_):
        if metadata.subclass:
            return metadata.subclass(*args_, **kwargs_)
        else:
            return metadata(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_tag(self): return self.tag
    def set_tag(self, tag): self.tag = tag
    def add_tag(self, value): self.tag.append(value)
    def insert_tag(self, index, value): self.tag[index] = value
    def get_section(self): return self.section
    def set_section(self, section): self.section = section
    def add_section(self, value): self.section.append(value)
    def insert_section(self, index, value): self.section[index] = value
    def export(self, outfile, level, namespace_='cml:', name_='metadata', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='metadata')
        if self.hasContent_():
            outfile.write('>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='metadata'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='metadata'):
        for tag_ in self.tag:
            tag_.export(outfile, level, namespace_, name_='tag')
        for section_ in self.section:
            section_.export(outfile, level, namespace_, name_='section')
    def hasContent_(self):
        if (
            self.tag or
            self.section
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='metadata'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('tag=[\n')
        level += 1
        for tag_ in self.tag:
            showIndent(outfile, level)
            outfile.write('model_.tag(\n')
            tag_.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('section=[\n')
        level += 1
        for section_ in self.section:
            showIndent(outfile, level)
            outfile.write('model_.section(\n')
            section_.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        if nodeName_ == 'tag': 
            obj_ = tag.factory()
            obj_.build(child_)
            self.tag.append(obj_)
        elif nodeName_ == 'section': 
            obj_ = section.factory()
            obj_.build(child_)
            self.section.append(obj_)
# end class metadata


class tag(GeneratedsSuper):
    """A tag element contains a key attribute and the value The key to be
    used later in the dictionary"""
    subclass = None
    superclass = None
    def __init__(self, key=None, valueOf_=None):
        self.key = _cast(None, key)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if tag.subclass:
            return tag.subclass(*args_, **kwargs_)
        else:
            return tag(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_key(self): return self.key
    def set_key(self, key): self.key = key
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='tag', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='tag')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='tag'):
        if self.key is not None and 'key' not in already_processed:
            already_processed.append('key')
            outfile.write(' key=%s' % (self.gds_format_string(quote_attrib(self.key).encode(ExternalEncoding), input_name='key'), ))
    def exportChildren(self, outfile, level, namespace_='cml:', name_='tag'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='tag'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.key is not None and 'key' not in already_processed:
            already_processed.append('key')
            showIndent(outfile, level)
            outfile.write('key = "%s",\n' % (self.key,))
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('key')
        if value is not None and 'key' not in already_processed:
            already_processed.append('key')
            self.key = value
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class tag


class connectome(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, connectome_meta=None, connectome_network=None, connectome_surface=None, connectome_volume=None, connectome_track=None, connectome_timeseries=None, connectome_data=None, connectome_script=None, connectome_imagestack=None):
        self.connectome_meta = connectome_meta
        if connectome_network is None:
            self.connectome_network = []
        else:
            self.connectome_network = connectome_network
        if connectome_surface is None:
            self.connectome_surface = []
        else:
            self.connectome_surface = connectome_surface
        if connectome_volume is None:
            self.connectome_volume = []
        else:
            self.connectome_volume = connectome_volume
        if connectome_track is None:
            self.connectome_track = []
        else:
            self.connectome_track = connectome_track
        if connectome_timeseries is None:
            self.connectome_timeseries = []
        else:
            self.connectome_timeseries = connectome_timeseries
        if connectome_data is None:
            self.connectome_data = []
        else:
            self.connectome_data = connectome_data
        if connectome_script is None:
            self.connectome_script = []
        else:
            self.connectome_script = connectome_script
        if connectome_imagestack is None:
            self.connectome_imagestack = []
        else:
            self.connectome_imagestack = connectome_imagestack
    def factory(*args_, **kwargs_):
        if connectome.subclass:
            return connectome.subclass(*args_, **kwargs_)
        else:
            return connectome(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_connectome_meta(self): return self.connectome_meta
    def set_connectome_meta(self, connectome_meta): self.connectome_meta = connectome_meta
    def get_connectome_network(self): return self.connectome_network
    def set_connectome_network(self, connectome_network): self.connectome_network = connectome_network
    def add_connectome_network(self, value): self.connectome_network.append(value)
    def insert_connectome_network(self, index, value): self.connectome_network[index] = value
    def get_connectome_surface(self): return self.connectome_surface
    def set_connectome_surface(self, connectome_surface): self.connectome_surface = connectome_surface
    def add_connectome_surface(self, value): self.connectome_surface.append(value)
    def insert_connectome_surface(self, index, value): self.connectome_surface[index] = value
    def get_connectome_volume(self): return self.connectome_volume
    def set_connectome_volume(self, connectome_volume): self.connectome_volume = connectome_volume
    def add_connectome_volume(self, value): self.connectome_volume.append(value)
    def insert_connectome_volume(self, index, value): self.connectome_volume[index] = value
    def get_connectome_track(self): return self.connectome_track
    def set_connectome_track(self, connectome_track): self.connectome_track = connectome_track
    def add_connectome_track(self, value): self.connectome_track.append(value)
    def insert_connectome_track(self, index, value): self.connectome_track[index] = value
    def get_connectome_timeseries(self): return self.connectome_timeseries
    def set_connectome_timeseries(self, connectome_timeseries): self.connectome_timeseries = connectome_timeseries
    def add_connectome_timeseries(self, value): self.connectome_timeseries.append(value)
    def insert_connectome_timeseries(self, index, value): self.connectome_timeseries[index] = value
    def get_connectome_data(self): return self.connectome_data
    def set_connectome_data(self, connectome_data): self.connectome_data = connectome_data
    def add_connectome_data(self, value): self.connectome_data.append(value)
    def insert_connectome_data(self, index, value): self.connectome_data[index] = value
    def get_connectome_script(self): return self.connectome_script
    def set_connectome_script(self, connectome_script): self.connectome_script = connectome_script
    def add_connectome_script(self, value): self.connectome_script.append(value)
    def insert_connectome_script(self, index, value): self.connectome_script[index] = value
    def get_connectome_imagestack(self): return self.connectome_imagestack
    def set_connectome_imagestack(self, connectome_imagestack): self.connectome_imagestack = connectome_imagestack
    def add_connectome_imagestack(self, value): self.connectome_imagestack.append(value)
    def insert_connectome_imagestack(self, index, value): self.connectome_imagestack[index] = value
    def export(self, outfile, level, namespace_='cml:', name_='connectome', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='connectome')
        if self.hasContent_():
            outfile.write('>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='connectome'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='connectome'):
        if self.connectome_meta:
            self.connectome_meta.export(outfile, level, namespace_, name_='connectome-meta', )
        for connectome_network_ in self.connectome_network:
            connectome_network_.export(outfile, level, namespace_, name_='connectome-network')
        for connectome_surface_ in self.connectome_surface:
            connectome_surface_.export(outfile, level, namespace_, name_='connectome-surface')
        for connectome_volume_ in self.connectome_volume:
            connectome_volume_.export(outfile, level, namespace_, name_='connectome-volume')
        for connectome_track_ in self.connectome_track:
            connectome_track_.export(outfile, level, namespace_, name_='connectome-track')
        for connectome_timeseries_ in self.connectome_timeseries:
            connectome_timeseries_.export(outfile, level, namespace_, name_='connectome-timeseries')
        for connectome_data_ in self.connectome_data:
            connectome_data_.export(outfile, level, namespace_, name_='connectome-data')
        for connectome_script_ in self.connectome_script:
            connectome_script_.export(outfile, level, namespace_, name_='connectome-script')
        for connectome_imagestack_ in self.connectome_imagestack:
            connectome_imagestack_.export(outfile, level, namespace_, name_='connectome-imagestack')
    def hasContent_(self):
        if (
            self.connectome_meta is not None or
            self.connectome_network or
            self.connectome_surface or
            self.connectome_volume or
            self.connectome_track or
            self.connectome_timeseries or
            self.connectome_data or
            self.connectome_script or
            self.connectome_imagestack
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='connectome'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        if self.connectome_meta is not None:
            showIndent(outfile, level)
            outfile.write('connectome_meta=model_.CMetadata(\n')
            self.connectome_meta.exportLiteral(outfile, level, name_='connectome_meta')
            showIndent(outfile, level)
            outfile.write('),\n')
        showIndent(outfile, level)
        outfile.write('connectome_network=[\n')
        level += 1
        for connectome_network_ in self.connectome_network:
            showIndent(outfile, level)
            outfile.write('model_.CNetwork(\n')
            connectome_network_.exportLiteral(outfile, level, name_='CNetwork')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('connectome_surface=[\n')
        level += 1
        for connectome_surface_ in self.connectome_surface:
            showIndent(outfile, level)
            outfile.write('model_.CSurface(\n')
            connectome_surface_.exportLiteral(outfile, level, name_='CSurface')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('connectome_volume=[\n')
        level += 1
        for connectome_volume_ in self.connectome_volume:
            showIndent(outfile, level)
            outfile.write('model_.CVolume(\n')
            connectome_volume_.exportLiteral(outfile, level, name_='CVolume')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('connectome_track=[\n')
        level += 1
        for connectome_track_ in self.connectome_track:
            showIndent(outfile, level)
            outfile.write('model_.CTrack(\n')
            connectome_track_.exportLiteral(outfile, level, name_='CTrack')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('connectome_timeseries=[\n')
        level += 1
        for connectome_timeseries_ in self.connectome_timeseries:
            showIndent(outfile, level)
            outfile.write('model_.CTimeseries(\n')
            connectome_timeseries_.exportLiteral(outfile, level, name_='CTimeseries')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('connectome_data=[\n')
        level += 1
        for connectome_data_ in self.connectome_data:
            showIndent(outfile, level)
            outfile.write('model_.CData(\n')
            connectome_data_.exportLiteral(outfile, level, name_='CData')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('connectome_script=[\n')
        level += 1
        for connectome_script_ in self.connectome_script:
            showIndent(outfile, level)
            outfile.write('model_.CScript(\n')
            connectome_script_.exportLiteral(outfile, level, name_='CScript')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        showIndent(outfile, level)
        outfile.write('connectome_imagestack=[\n')
        level += 1
        for connectome_imagestack_ in self.connectome_imagestack:
            showIndent(outfile, level)
            outfile.write('model_.CImagestack(\n')
            connectome_imagestack_.exportLiteral(outfile, level, name_='CImagestack')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        if nodeName_ == 'connectome-meta': 
            obj_ = CMetadata.factory()
            obj_.build(child_)
            self.set_connectome_meta(obj_)
        elif nodeName_ == 'connectome-network': 
            obj_ = CNetwork.factory()
            obj_.build(child_)
            self.connectome_network.append(obj_)
        elif nodeName_ == 'connectome-surface': 
            obj_ = CSurface.factory()
            obj_.build(child_)
            self.connectome_surface.append(obj_)
        elif nodeName_ == 'connectome-volume': 
            obj_ = CVolume.factory()
            obj_.build(child_)
            self.connectome_volume.append(obj_)
        elif nodeName_ == 'connectome-track': 
            obj_ = CTrack.factory()
            obj_.build(child_)
            self.connectome_track.append(obj_)
        elif nodeName_ == 'connectome-timeseries': 
            obj_ = CTimeseries.factory()
            obj_.build(child_)
            self.connectome_timeseries.append(obj_)
        elif nodeName_ == 'connectome-data': 
            obj_ = CData.factory()
            obj_.build(child_)
            self.connectome_data.append(obj_)
        elif nodeName_ == 'connectome-script': 
            obj_ = CScript.factory()
            obj_.build(child_)
            self.connectome_script.append(obj_)
        elif nodeName_ == 'connectome-imagestack': 
            obj_ = CImagestack.factory()
            obj_.build(child_)
            self.connectome_imagestack.append(obj_)
# end class connectome


class CMetadata(GeneratedsSuper):
    """Defines the version of the Connectome Schema Definition the current
    Connectome File is compatible with. Should be 2.0"""
    subclass = None
    superclass = None
    def __init__(self, version=None, title=None, creator=None, publisher=None, created=None, modified=None, rights=None, license=None, references=None, relation=None, description=None, generator=None, species=None, email=None, metadata=None):
        self.version = _cast(None, version)
        self.title = title
        self.creator = creator
        self.publisher = publisher
        self.created = created
        self.modified = modified
        self.rights = rights
        self.license = license
        self.references = references
        self.relation = relation
        self.description = description
        self.generator = generator
        self.species = species
        self.email = email
        self.metadata = metadata
    def factory(*args_, **kwargs_):
        if CMetadata.subclass:
            return CMetadata.subclass(*args_, **kwargs_)
        else:
            return CMetadata(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_title(self): return self.title
    def set_title(self, title): self.title = title
    def get_creator(self): return self.creator
    def set_creator(self, creator): self.creator = creator
    def get_publisher(self): return self.publisher
    def set_publisher(self, publisher): self.publisher = publisher
    def get_created(self): return self.created
    def set_created(self, created): self.created = created
    def get_modified(self): return self.modified
    def set_modified(self, modified): self.modified = modified
    def get_rights(self): return self.rights
    def set_rights(self, rights): self.rights = rights
    def get_license(self): return self.license
    def set_license(self, license): self.license = license
    def get_references(self): return self.references
    def set_references(self, references): self.references = references
    def get_relation(self): return self.relation
    def set_relation(self, relation): self.relation = relation
    def get_description(self): return self.description
    def set_description(self, description): self.description = description
    def get_generator(self): return self.generator
    def set_generator(self, generator): self.generator = generator
    def get_species(self): return self.species
    def set_species(self, species): self.species = species
    def get_email(self): return self.email
    def set_email(self, email): self.email = email
    def get_metadata(self): return self.metadata
    def set_metadata(self, metadata): self.metadata = metadata
    def get_version(self): return self.version
    def set_version(self, version): self.version = version
    def export(self, outfile, level, namespace_='cml:', name_='CMetadata', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='CMetadata')
        if self.hasContent_():
            outfile.write('>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='CMetadata'):
        if self.version is not None and 'version' not in already_processed:
            already_processed.append('version')
            outfile.write(' version=%s' % (self.gds_format_string(quote_attrib(self.version).encode(ExternalEncoding), input_name='version'), ))
    def exportChildren(self, outfile, level, namespace_='cml:', name_='CMetadata'):
        if self.title is not None:
            showIndent(outfile, level)
            outfile.write('<%stitle>%s</%stitle>\n' % (namespace_, self.gds_format_string(quote_xml(self.title).encode(ExternalEncoding), input_name='title'), namespace_))
        if self.creator is not None:
            showIndent(outfile, level)
            outfile.write('<%screator>%s</%screator>\n' % (namespace_, self.gds_format_string(quote_xml(self.creator).encode(ExternalEncoding), input_name='creator'), namespace_))
        if self.publisher is not None:
            showIndent(outfile, level)
            outfile.write('<%spublisher>%s</%spublisher>\n' % (namespace_, self.gds_format_string(quote_xml(self.publisher).encode(ExternalEncoding), input_name='publisher'), namespace_))
        if self.created is not None:
            showIndent(outfile, level)
            outfile.write('<%screated>%s</%screated>\n' % (namespace_, self.gds_format_string(quote_xml(self.created).encode(ExternalEncoding), input_name='created'), namespace_))
        if self.modified is not None:
            showIndent(outfile, level)
            outfile.write('<%smodified>%s</%smodified>\n' % (namespace_, self.gds_format_string(quote_xml(self.modified).encode(ExternalEncoding), input_name='modified'), namespace_))
        if self.rights is not None:
            showIndent(outfile, level)
            outfile.write('<%srights>%s</%srights>\n' % (namespace_, self.gds_format_string(quote_xml(self.rights).encode(ExternalEncoding), input_name='rights'), namespace_))
        if self.license is not None:
            showIndent(outfile, level)
            outfile.write('<%slicense>%s</%slicense>\n' % (namespace_, self.gds_format_string(quote_xml(self.license).encode(ExternalEncoding), input_name='license'), namespace_))
        if self.references is not None:
            showIndent(outfile, level)
            outfile.write('<%sreferences>%s</%sreferences>\n' % (namespace_, self.gds_format_string(quote_xml(self.references).encode(ExternalEncoding), input_name='references'), namespace_))
        if self.relation is not None:
            showIndent(outfile, level)
            outfile.write('<%srelation>%s</%srelation>\n' % (namespace_, self.gds_format_string(quote_xml(self.relation).encode(ExternalEncoding), input_name='relation'), namespace_))
        if self.description is not None:
            showIndent(outfile, level)
            outfile.write('<%sdescription>%s</%sdescription>\n' % (namespace_, self.gds_format_string(quote_xml(self.description).encode(ExternalEncoding), input_name='description'), namespace_))
        if self.generator is not None:
            showIndent(outfile, level)
            outfile.write('<%sgenerator>%s</%sgenerator>\n' % (namespace_, self.gds_format_string(quote_xml(self.generator).encode(ExternalEncoding), input_name='generator'), namespace_))
        if self.species is not None:
            showIndent(outfile, level)
            outfile.write('<%sspecies>%s</%sspecies>\n' % (namespace_, self.gds_format_string(quote_xml(self.species).encode(ExternalEncoding), input_name='species'), namespace_))
        if self.email is not None:
            showIndent(outfile, level)
            outfile.write('<%semail>%s</%semail>\n' % (namespace_, self.gds_format_string(quote_xml(self.email).encode(ExternalEncoding), input_name='email'), namespace_))
        if self.metadata:
            self.metadata.export(outfile, level, namespace_, name_='metadata')
    def hasContent_(self):
        if (
            self.title is not None or
            self.creator is not None or
            self.publisher is not None or
            self.created is not None or
            self.modified is not None or
            self.rights is not None or
            self.license is not None or
            self.references is not None or
            self.relation is not None or
            self.description is not None or
            self.generator is not None or
            self.species is not None or
            self.email is not None or
            self.metadata is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='CMetadata'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.version is not None and 'version' not in already_processed:
            already_processed.append('version')
            showIndent(outfile, level)
            outfile.write('version = "%s",\n' % (self.version,))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.title is not None:
            showIndent(outfile, level)
            outfile.write('title=%s,\n' % quote_python(self.title).encode(ExternalEncoding))
        if self.creator is not None:
            showIndent(outfile, level)
            outfile.write('creator=%s,\n' % quote_python(self.creator).encode(ExternalEncoding))
        if self.publisher is not None:
            showIndent(outfile, level)
            outfile.write('publisher=%s,\n' % quote_python(self.publisher).encode(ExternalEncoding))
        if self.created is not None:
            showIndent(outfile, level)
            outfile.write('created=%s,\n' % quote_python(self.created).encode(ExternalEncoding))
        if self.modified is not None:
            showIndent(outfile, level)
            outfile.write('modified=%s,\n' % quote_python(self.modified).encode(ExternalEncoding))
        if self.rights is not None:
            showIndent(outfile, level)
            outfile.write('rights=%s,\n' % quote_python(self.rights).encode(ExternalEncoding))
        if self.license is not None:
            showIndent(outfile, level)
            outfile.write('license=%s,\n' % quote_python(self.license).encode(ExternalEncoding))
        if self.references is not None:
            showIndent(outfile, level)
            outfile.write('references=%s,\n' % quote_python(self.references).encode(ExternalEncoding))
        if self.relation is not None:
            showIndent(outfile, level)
            outfile.write('relation=%s,\n' % quote_python(self.relation).encode(ExternalEncoding))
        if self.description is not None:
            showIndent(outfile, level)
            outfile.write('description=%s,\n' % quote_python(self.description).encode(ExternalEncoding))
        if self.generator is not None:
            showIndent(outfile, level)
            outfile.write('generator=%s,\n' % quote_python(self.generator).encode(ExternalEncoding))
        if self.species is not None:
            showIndent(outfile, level)
            outfile.write('species=%s,\n' % quote_python(self.species).encode(ExternalEncoding))
        if self.email is not None:
            showIndent(outfile, level)
            outfile.write('email=%s,\n' % quote_python(self.email).encode(ExternalEncoding))
        if self.metadata is not None:
            showIndent(outfile, level)
            outfile.write('metadata=model_.metadata(\n')
            self.metadata.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('version')
        if value is not None and 'version' not in already_processed:
            already_processed.append('version')
            self.version = value
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        if nodeName_ == 'title':
            title_ = child_.text
            title_ = self.gds_validate_string(title_, node, 'title')
            self.title = title_
        elif nodeName_ == 'alternative': 
            obj_ = alternative.factory()
            obj_.build(child_)
            self.set_title(obj_)
        elif nodeName_ == 'creator':
            creator_ = child_.text
            creator_ = self.gds_validate_string(creator_, node, 'creator')
            self.creator = creator_
        elif nodeName_ == 'publisher':
            publisher_ = child_.text
            publisher_ = self.gds_validate_string(publisher_, node, 'publisher')
            self.publisher = publisher_
        elif nodeName_ == 'created':
            created_ = child_.text
            created_ = self.gds_validate_string(created_, node, 'created')
            self.created = created_
        elif nodeName_ == 'modified':
            modified_ = child_.text
            modified_ = self.gds_validate_string(modified_, node, 'modified')
            self.modified = modified_
        elif nodeName_ == 'rights':
            rights_ = child_.text
            rights_ = self.gds_validate_string(rights_, node, 'rights')
            self.rights = rights_
        elif nodeName_ == 'accessRights': 
            obj_ = accessRights.factory()
            obj_.build(child_)
            self.set_rights(obj_)
        elif nodeName_ == 'license': 
            obj_ = license.factory()
            obj_.build(child_)
            self.set_rights(obj_)
        elif nodeName_ == 'license':
            license_ = child_.text
            license_ = self.gds_validate_string(license_, node, 'license')
            self.license = license_
        elif nodeName_ == 'references':
            references_ = child_.text
            references_ = self.gds_validate_string(references_, node, 'references')
            self.references = references_
        elif nodeName_ == 'relation':
            relation_ = child_.text
            relation_ = self.gds_validate_string(relation_, node, 'relation')
            self.relation = relation_
        elif nodeName_ == 'isVersionOf': 
            obj_ = isVersionOf.factory()
            obj_.build(child_)
            self.set_relation(obj_)
        elif nodeName_ == 'hasVersion': 
            obj_ = hasVersion.factory()
            obj_.build(child_)
            self.set_relation(obj_)
        elif nodeName_ == 'isReplacedBy': 
            obj_ = isReplacedBy.factory()
            obj_.build(child_)
            self.set_relation(obj_)
        elif nodeName_ == 'replaces': 
            obj_ = replaces.factory()
            obj_.build(child_)
            self.set_relation(obj_)
        elif nodeName_ == 'isRequiredBy': 
            obj_ = isRequiredBy.factory()
            obj_.build(child_)
            self.set_relation(obj_)
        elif nodeName_ == 'requires': 
            obj_ = requires.factory()
            obj_.build(child_)
            self.set_relation(obj_)
        elif nodeName_ == 'isPartOf': 
            obj_ = isPartOf.factory()
            obj_.build(child_)
            self.set_relation(obj_)
        elif nodeName_ == 'hasPart': 
            obj_ = hasPart.factory()
            obj_.build(child_)
            self.set_relation(obj_)
        elif nodeName_ == 'isReferencedBy': 
            obj_ = isReferencedBy.factory()
            obj_.build(child_)
            self.set_relation(obj_)
        elif nodeName_ == 'references': 
            obj_ = references.factory()
            obj_.build(child_)
            self.set_relation(obj_)
        elif nodeName_ == 'isFormatOf': 
            obj_ = isFormatOf.factory()
            obj_.build(child_)
            self.set_relation(obj_)
        elif nodeName_ == 'hasFormat': 
            obj_ = hasFormat.factory()
            obj_.build(child_)
            self.set_relation(obj_)
        elif nodeName_ == 'conformsTo': 
            obj_ = conformsTo.factory()
            obj_.build(child_)
            self.set_relation(obj_)
        elif nodeName_ == 'description':
            description_ = child_.text
            description_ = self.gds_validate_string(description_, node, 'description')
            self.description = description_
        elif nodeName_ == 'tableOfContents': 
            obj_ = tableOfContents.factory()
            obj_.build(child_)
            self.set_description(obj_)
        elif nodeName_ == 'abstract': 
            obj_ = abstract.factory()
            obj_.build(child_)
            self.set_description(obj_)
        elif nodeName_ == 'generator':
            generator_ = child_.text
            generator_ = self.gds_validate_string(generator_, node, 'generator')
            self.generator = generator_
        elif nodeName_ == 'species':
            species_ = child_.text
            species_ = self.gds_validate_string(species_, node, 'species')
            self.species = species_
        elif nodeName_ == 'email':
            email_ = child_.text
            email_ = self.gds_validate_string(email_, node, 'email')
            self.email = email_
        elif nodeName_ == 'metadata': 
            obj_ = metadata.factory()
            obj_.build(child_)
            self.set_metadata(obj_)
# end class CMetadata


class CNetwork(GeneratedsSuper):
    """The short name of the network The path to the file according to
    location attribute Is the network stored it "GEXF" or "GraphML"
    format, "NXGPickle" as NetworkX pickled object, or "Other"
    format? - dtype="AttributeNetwork" A network with arbitrary
    number of attributes for nodes and edges. -
    dtype="DynamicNetwork" Network with either with lifespan
    attributes for nodes and edges (See GEXF) or timeseries on nodes
    and edges. - dtype="HierarchicalNetwork" Network with
    hierarchical structure. - dtype="StructuralNetwork" A structural
    network e.g. derived from Diffusion MRI -
    dtype="FunctionalNetwork" Networks derived from functional
    measures such as EEG/MEG/fMRI/PET etc. -
    dtype="EffectiveNetwork" Networks representing effective
    connectivity - dtype="Other" Other kind of network."""
    subclass = None
    superclass = None
    def __init__(self, src=None, dtype='AttributeNetwork', name=None, fileformat='GraphML', metadata=None, description=None):
        self.src = _cast(None, src)
        self.dtype = _cast(None, dtype)
        self.name = _cast(None, name)
        self.fileformat = _cast(None, fileformat)
        self.metadata = metadata
        self.description = description
    def factory(*args_, **kwargs_):
        if CNetwork.subclass:
            return CNetwork.subclass(*args_, **kwargs_)
        else:
            return CNetwork(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_metadata(self): return self.metadata
    def set_metadata(self, metadata): self.metadata = metadata
    def get_description(self): return self.description
    def set_description(self, description): self.description = description
    def get_src(self): return self.src
    def set_src(self, src): self.src = src
    def get_dtype(self): return self.dtype
    def set_dtype(self, dtype): self.dtype = dtype
    def validate_networkEnumDType(self, value):
        # Validate type networkEnumDType, a restriction on xsd:string.
        pass
    def get_name(self): return self.name
    def set_name(self, name): self.name = name
    def get_fileformat(self): return self.fileformat
    def set_fileformat(self, fileformat): self.fileformat = fileformat
    def validate_networkFileFormat(self, value):
        # Validate type networkFileFormat, a restriction on xsd:string.
        pass
    def export(self, outfile, level, namespace_='cml:', name_='CNetwork', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='CNetwork')
        if self.hasContent_():
            outfile.write('>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='CNetwork'):
        if self.src is not None and 'src' not in already_processed:
            already_processed.append('src')
            outfile.write(' src=%s' % (self.gds_format_string(quote_attrib(self.src).encode(ExternalEncoding), input_name='src'), ))
        if self.dtype is not None and 'dtype' not in already_processed:
            already_processed.append('dtype')
            outfile.write(' dtype=%s' % (quote_attrib(self.dtype), ))
        if self.name is not None and 'name' not in already_processed:
            already_processed.append('name')
            outfile.write(' name=%s' % (self.gds_format_string(quote_attrib(self.name).encode(ExternalEncoding), input_name='name'), ))
        if self.fileformat is not None and 'fileformat' not in already_processed:
            already_processed.append('fileformat')
            outfile.write(' fileformat=%s' % (quote_attrib(self.fileformat), ))
    def exportChildren(self, outfile, level, namespace_='cml:', name_='CNetwork'):
        if self.metadata:
            self.metadata.export(outfile, level, namespace_, name_='metadata')
        if self.description is not None:
            showIndent(outfile, level)
            outfile.write('<%sdescription>%s</%sdescription>\n' % (namespace_, self.gds_format_string(quote_xml(self.description).encode(ExternalEncoding), input_name='description'), namespace_))
    def hasContent_(self):
        if (
            self.metadata is not None or
            self.description is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='CNetwork'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.src is not None and 'src' not in already_processed:
            already_processed.append('src')
            showIndent(outfile, level)
            outfile.write('src = "%s",\n' % (self.src,))
        if self.dtype is not None and 'dtype' not in already_processed:
            already_processed.append('dtype')
            showIndent(outfile, level)
            outfile.write('dtype = "%s",\n' % (self.dtype,))
        if self.name is not None and 'name' not in already_processed:
            already_processed.append('name')
            showIndent(outfile, level)
            outfile.write('name = "%s",\n' % (self.name,))
        if self.fileformat is not None and 'fileformat' not in already_processed:
            already_processed.append('fileformat')
            showIndent(outfile, level)
            outfile.write('fileformat = "%s",\n' % (self.fileformat,))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.metadata is not None:
            showIndent(outfile, level)
            outfile.write('metadata=model_.metadata(\n')
            self.metadata.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        if self.description is not None:
            showIndent(outfile, level)
            outfile.write('description=%s,\n' % quote_python(self.description).encode(ExternalEncoding))
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('src')
        if value is not None and 'src' not in already_processed:
            already_processed.append('src')
            self.src = value
        value = attrs.get('dtype')
        if value is not None and 'dtype' not in already_processed:
            already_processed.append('dtype')
            self.dtype = value
            self.validate_networkEnumDType(self.dtype)    # validate type networkEnumDType
        value = attrs.get('name')
        if value is not None and 'name' not in already_processed:
            already_processed.append('name')
            self.name = value
        value = attrs.get('fileformat')
        if value is not None and 'fileformat' not in already_processed:
            already_processed.append('fileformat')
            self.fileformat = value
            self.validate_networkFileFormat(self.fileformat)    # validate type networkFileFormat
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        if nodeName_ == 'metadata': 
            obj_ = metadata.factory()
            obj_.build(child_)
            self.set_metadata(obj_)
        elif nodeName_ == 'description':
            description_ = child_.text
            description_ = self.gds_validate_string(description_, node, 'description')
            self.description = description_
        elif nodeName_ == 'tableOfContents': 
            obj_ = tableOfContents.factory()
            obj_.build(child_)
            self.set_description(obj_)
        elif nodeName_ == 'abstract': 
            obj_ = abstract.factory()
            obj_.build(child_)
            self.set_description(obj_)
# end class CNetwork


class CSurface(GeneratedsSuper):
    """Descriptive name of the surface. The path to the file according to
    location attribute Set to "gifti" to use the only supported
    Gifti format by cfflib. See
    http://www.nitrc.org/frs/download.php/158/gifti.xsd for schema
    information Use "Other" for other formats with custom IO
    Handling What type of surface does the Gifti file contain: -
    type="Labeling" The Gifti file contains surface labels. This
    file can be referenced in connectome-network with either the
    name attribute or in addition to another surface defined by name
    and using the labelname attribute and matching labelid. If
    referenced in such a way, the networks' nodes attribute
    dn_intensityvalue value may match the label array integers,
    thereby relating a network node to a surface patch (a region of
    interest defined on the surface). See also example datasets. -
    type="Surfaceset" The Gifti file contains a set of surfaces
    where the metadata tag AnatomicalStructurePrimary match.
    Individual elements of the set are distinguished by the metadta
    tag AnatomicalStructureSecondary. The Gifti file contains
    information about the coordinate system used. -
    type="Surfaceset+Labeling" If the Gifti file contains data as
    described for both surfaceset and label above. - type="Other"
    Any other kind of data storable in a Gifti file."""
    subclass = None
    superclass = None
    def __init__(self, src=None, dtype='Surfaceset', name=None, fileformat=None, description=None, metadata=None):
        self.src = _cast(None, src)
        self.dtype = _cast(None, dtype)
        self.name = _cast(None, name)
        self.fileformat = _cast(None, fileformat)
        self.description = description
        self.metadata = metadata
    def factory(*args_, **kwargs_):
        if CSurface.subclass:
            return CSurface.subclass(*args_, **kwargs_)
        else:
            return CSurface(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_description(self): return self.description
    def set_description(self, description): self.description = description
    def get_metadata(self): return self.metadata
    def set_metadata(self, metadata): self.metadata = metadata
    def get_src(self): return self.src
    def set_src(self, src): self.src = src
    def get_dtype(self): return self.dtype
    def set_dtype(self, dtype): self.dtype = dtype
    def validate_surfaceEnumDType(self, value):
        # Validate type surfaceEnumDType, a restriction on xsd:string.
        pass
    def get_name(self): return self.name
    def set_name(self, name): self.name = name
    def get_fileformat(self): return self.fileformat
    def set_fileformat(self, fileformat): self.fileformat = fileformat
    def validate_surfaceFileFormat(self, value):
        # Validate type surfaceFileFormat, a restriction on xsd:string.
        pass
    def export(self, outfile, level, namespace_='cml:', name_='CSurface', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='CSurface')
        if self.hasContent_():
            outfile.write('>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='CSurface'):
        if self.src is not None and 'src' not in already_processed:
            already_processed.append('src')
            outfile.write(' src=%s' % (self.gds_format_string(quote_attrib(self.src).encode(ExternalEncoding), input_name='src'), ))
        if self.dtype is not None and 'dtype' not in already_processed:
            already_processed.append('dtype')
            outfile.write(' dtype=%s' % (quote_attrib(self.dtype), ))
        if self.name is not None and 'name' not in already_processed:
            already_processed.append('name')
            outfile.write(' name=%s' % (self.gds_format_string(quote_attrib(self.name).encode(ExternalEncoding), input_name='name'), ))
        if self.fileformat is not None and 'fileformat' not in already_processed:
            already_processed.append('fileformat')
            outfile.write(' fileformat=%s' % (quote_attrib(self.fileformat), ))
    def exportChildren(self, outfile, level, namespace_='cml:', name_='CSurface'):
        if self.description is not None:
            showIndent(outfile, level)
            outfile.write('<%sdescription>%s</%sdescription>\n' % (namespace_, self.gds_format_string(quote_xml(self.description).encode(ExternalEncoding), input_name='description'), namespace_))
        if self.metadata:
            self.metadata.export(outfile, level, namespace_, name_='metadata', )
    def hasContent_(self):
        if (
            self.description is not None or
            self.metadata is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='CSurface'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.src is not None and 'src' not in already_processed:
            already_processed.append('src')
            showIndent(outfile, level)
            outfile.write('src = "%s",\n' % (self.src,))
        if self.dtype is not None and 'dtype' not in already_processed:
            already_processed.append('dtype')
            showIndent(outfile, level)
            outfile.write('dtype = "%s",\n' % (self.dtype,))
        if self.name is not None and 'name' not in already_processed:
            already_processed.append('name')
            showIndent(outfile, level)
            outfile.write('name = "%s",\n' % (self.name,))
        if self.fileformat is not None and 'fileformat' not in already_processed:
            already_processed.append('fileformat')
            showIndent(outfile, level)
            outfile.write('fileformat = "%s",\n' % (self.fileformat,))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.description is not None:
            showIndent(outfile, level)
            outfile.write('description=%s,\n' % quote_python(self.description).encode(ExternalEncoding))
        if self.metadata is not None:
            showIndent(outfile, level)
            outfile.write('metadata=model_.metadata(\n')
            self.metadata.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('src')
        if value is not None and 'src' not in already_processed:
            already_processed.append('src')
            self.src = value
        value = attrs.get('dtype')
        if value is not None and 'dtype' not in already_processed:
            already_processed.append('dtype')
            self.dtype = value
            self.validate_surfaceEnumDType(self.dtype)    # validate type surfaceEnumDType
        value = attrs.get('name')
        if value is not None and 'name' not in already_processed:
            already_processed.append('name')
            self.name = value
        value = attrs.get('fileformat')
        if value is not None and 'fileformat' not in already_processed:
            already_processed.append('fileformat')
            self.fileformat = value
            self.validate_surfaceFileFormat(self.fileformat)    # validate type surfaceFileFormat
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        if nodeName_ == 'description':
            description_ = child_.text
            description_ = self.gds_validate_string(description_, node, 'description')
            self.description = description_
        elif nodeName_ == 'tableOfContents': 
            obj_ = tableOfContents.factory()
            obj_.build(child_)
            self.set_description(obj_)
        elif nodeName_ == 'abstract': 
            obj_ = abstract.factory()
            obj_.build(child_)
            self.set_description(obj_)
        elif nodeName_ == 'metadata': 
            obj_ = metadata.factory()
            obj_.build(child_)
            self.set_metadata(obj_)
# end class CSurface


class CVolume(GeneratedsSuper):
    """Name of the volume. The path to the file according to location
    attribute Set to "Nifti1" to use the only supported Nifti
    format. This works also for compressed files with name ending
    .nii.gz The Nifti file contains information about the coordinate
    system used. Set type of volume the Nifti file contains: -
    type="Segmentation" The Nifti file contains a single volume
    where the voxel values are integers, representing a segmented
    Region of Interest. If this volume is referenced by a
    connectome-network, its nodes dn_intensityvalue attribute may
    match these integer values. Such a segmentation volume can
    referenced in a connectome-volume by the segmentationname
    attribute in addition to another, e.g. T1-weighted volume which
    is referenced by the name attribute. See also example datasets.
    - type="T1-weighted" The Nifti file contains a T1-weighted
    volume. - type="T2-weighted" The Nifti file contains a
    T2-weighted volume. - type="PD-weighted" The voxel values
    represent a proton-density weighted signal. - type="fMRI" The
    Nifti file contains functional MRI time series data. -
    type="Probabilitymap" Voxel values are in the range [0,1]. Can
    stand for tissue probability maps. - type="MD" Diffusion-related
    signal. Stands for mean diffusivity. - type="FA" Diffusion-
    related signal. Stands for fractional anisotropy. - type="LD"
    Diffusion-related signal. Stands for longitudinal diffusivity. -
    type="TD" Diffusion-related signal. Stands for transversal
    diffusivity. - type="FLAIR" Stands for Fluid attenuated
    inversion recovery - type="MRA" Stands for Magnetic resonance
    angiography - type="MRS" Stands for Magnetic resonance
    spectroscopy"""
    subclass = None
    superclass = None
    def __init__(self, src=None, dtype=None, name=None, fileformat='Nifti1', description=None, metadata=None):
        self.src = _cast(None, src)
        self.dtype = _cast(None, dtype)
        self.name = _cast(None, name)
        self.fileformat = _cast(None, fileformat)
        self.description = description
        self.metadata = metadata
    def factory(*args_, **kwargs_):
        if CVolume.subclass:
            return CVolume.subclass(*args_, **kwargs_)
        else:
            return CVolume(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_description(self): return self.description
    def set_description(self, description): self.description = description
    def get_metadata(self): return self.metadata
    def set_metadata(self, metadata): self.metadata = metadata
    def get_src(self): return self.src
    def set_src(self, src): self.src = src
    def get_dtype(self): return self.dtype
    def set_dtype(self, dtype): self.dtype = dtype
    def validate_volumeEnumDType(self, value):
        # Validate type volumeEnumDType, a restriction on xsd:string.
        pass
    def get_name(self): return self.name
    def set_name(self, name): self.name = name
    def get_fileformat(self): return self.fileformat
    def set_fileformat(self, fileformat): self.fileformat = fileformat
    def validate_volumeFileFormat(self, value):
        # Validate type volumeFileFormat, a restriction on xsd:string.
        pass
    def export(self, outfile, level, namespace_='cml:', name_='CVolume', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='CVolume')
        if self.hasContent_():
            outfile.write('>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='CVolume'):
        if self.src is not None and 'src' not in already_processed:
            already_processed.append('src')
            outfile.write(' src=%s' % (self.gds_format_string(quote_attrib(self.src).encode(ExternalEncoding), input_name='src'), ))
        if self.dtype is not None and 'dtype' not in already_processed:
            already_processed.append('dtype')
            outfile.write(' dtype=%s' % (quote_attrib(self.dtype), ))
        if self.name is not None and 'name' not in already_processed:
            already_processed.append('name')
            outfile.write(' name=%s' % (self.gds_format_string(quote_attrib(self.name).encode(ExternalEncoding), input_name='name'), ))
        if self.fileformat is not None and 'fileformat' not in already_processed:
            already_processed.append('fileformat')
            outfile.write(' fileformat=%s' % (quote_attrib(self.fileformat), ))
    def exportChildren(self, outfile, level, namespace_='cml:', name_='CVolume'):
        if self.description is not None:
            showIndent(outfile, level)
            outfile.write('<%sdescription>%s</%sdescription>\n' % (namespace_, self.gds_format_string(quote_xml(self.description).encode(ExternalEncoding), input_name='description'), namespace_))
        if self.metadata:
            self.metadata.export(outfile, level, namespace_, name_='metadata', )
    def hasContent_(self):
        if (
            self.description is not None or
            self.metadata is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='CVolume'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.src is not None and 'src' not in already_processed:
            already_processed.append('src')
            showIndent(outfile, level)
            outfile.write('src = "%s",\n' % (self.src,))
        if self.dtype is not None and 'dtype' not in already_processed:
            already_processed.append('dtype')
            showIndent(outfile, level)
            outfile.write('dtype = "%s",\n' % (self.dtype,))
        if self.name is not None and 'name' not in already_processed:
            already_processed.append('name')
            showIndent(outfile, level)
            outfile.write('name = "%s",\n' % (self.name,))
        if self.fileformat is not None and 'fileformat' not in already_processed:
            already_processed.append('fileformat')
            showIndent(outfile, level)
            outfile.write('fileformat = "%s",\n' % (self.fileformat,))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.description is not None:
            showIndent(outfile, level)
            outfile.write('description=%s,\n' % quote_python(self.description).encode(ExternalEncoding))
        if self.metadata is not None:
            showIndent(outfile, level)
            outfile.write('metadata=model_.metadata(\n')
            self.metadata.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('src')
        if value is not None and 'src' not in already_processed:
            already_processed.append('src')
            self.src = value
        value = attrs.get('dtype')
        if value is not None and 'dtype' not in already_processed:
            already_processed.append('dtype')
            self.dtype = value
            self.validate_volumeEnumDType(self.dtype)    # validate type volumeEnumDType
        value = attrs.get('name')
        if value is not None and 'name' not in already_processed:
            already_processed.append('name')
            self.name = value
        value = attrs.get('fileformat')
        if value is not None and 'fileformat' not in already_processed:
            already_processed.append('fileformat')
            self.fileformat = value
            self.validate_volumeFileFormat(self.fileformat)    # validate type volumeFileFormat
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        if nodeName_ == 'description':
            description_ = child_.text
            description_ = self.gds_validate_string(description_, node, 'description')
            self.description = description_
        elif nodeName_ == 'tableOfContents': 
            obj_ = tableOfContents.factory()
            obj_.build(child_)
            self.set_description(obj_)
        elif nodeName_ == 'abstract': 
            obj_ = abstract.factory()
            obj_.build(child_)
            self.set_description(obj_)
        elif nodeName_ == 'metadata': 
            obj_ = metadata.factory()
            obj_.build(child_)
            self.set_metadata(obj_)
# end class CVolume


class CTrack(GeneratedsSuper):
    """Name of the track file. The path to the file according to location
    attribute Set to "TrackVis" (default) to use the only supported
    TrackVis file format. The TrackVis file format allows to store
    any number of additional numerical data on the individual
    fibers."""
    subclass = None
    superclass = None
    def __init__(self, src=None, dtype=None, name=None, fileformat='TrackVis', description=None, metadata=None):
        self.src = _cast(None, src)
        self.dtype = _cast(None, dtype)
        self.name = _cast(None, name)
        self.fileformat = _cast(None, fileformat)
        self.description = description
        self.metadata = metadata
    def factory(*args_, **kwargs_):
        if CTrack.subclass:
            return CTrack.subclass(*args_, **kwargs_)
        else:
            return CTrack(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_description(self): return self.description
    def set_description(self, description): self.description = description
    def get_metadata(self): return self.metadata
    def set_metadata(self, metadata): self.metadata = metadata
    def get_src(self): return self.src
    def set_src(self, src): self.src = src
    def get_dtype(self): return self.dtype
    def set_dtype(self, dtype): self.dtype = dtype
    def get_name(self): return self.name
    def set_name(self, name): self.name = name
    def get_fileformat(self): return self.fileformat
    def set_fileformat(self, fileformat): self.fileformat = fileformat
    def validate_trackFileFormat(self, value):
        # Validate type trackFileFormat, a restriction on xsd:string.
        pass
    def export(self, outfile, level, namespace_='cml:', name_='CTrack', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='CTrack')
        if self.hasContent_():
            outfile.write('>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='CTrack'):
        if self.src is not None and 'src' not in already_processed:
            already_processed.append('src')
            outfile.write(' src=%s' % (self.gds_format_string(quote_attrib(self.src).encode(ExternalEncoding), input_name='src'), ))
        if self.dtype is not None and 'dtype' not in already_processed:
            already_processed.append('dtype')
            outfile.write(' dtype=%s' % (self.gds_format_string(quote_attrib(self.dtype).encode(ExternalEncoding), input_name='dtype'), ))
        if self.name is not None and 'name' not in already_processed:
            already_processed.append('name')
            outfile.write(' name=%s' % (self.gds_format_string(quote_attrib(self.name).encode(ExternalEncoding), input_name='name'), ))
        if self.fileformat is not None and 'fileformat' not in already_processed:
            already_processed.append('fileformat')
            outfile.write(' fileformat=%s' % (quote_attrib(self.fileformat), ))
    def exportChildren(self, outfile, level, namespace_='cml:', name_='CTrack'):
        if self.description is not None:
            showIndent(outfile, level)
            outfile.write('<%sdescription>%s</%sdescription>\n' % (namespace_, self.gds_format_string(quote_xml(self.description).encode(ExternalEncoding), input_name='description'), namespace_))
        if self.metadata:
            self.metadata.export(outfile, level, namespace_, name_='metadata', )
    def hasContent_(self):
        if (
            self.description is not None or
            self.metadata is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='CTrack'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.src is not None and 'src' not in already_processed:
            already_processed.append('src')
            showIndent(outfile, level)
            outfile.write('src = "%s",\n' % (self.src,))
        if self.dtype is not None and 'dtype' not in already_processed:
            already_processed.append('dtype')
            showIndent(outfile, level)
            outfile.write('dtype = "%s",\n' % (self.dtype,))
        if self.name is not None and 'name' not in already_processed:
            already_processed.append('name')
            showIndent(outfile, level)
            outfile.write('name = "%s",\n' % (self.name,))
        if self.fileformat is not None and 'fileformat' not in already_processed:
            already_processed.append('fileformat')
            showIndent(outfile, level)
            outfile.write('fileformat = "%s",\n' % (self.fileformat,))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.description is not None:
            showIndent(outfile, level)
            outfile.write('description=%s,\n' % quote_python(self.description).encode(ExternalEncoding))
        if self.metadata is not None:
            showIndent(outfile, level)
            outfile.write('metadata=model_.metadata(\n')
            self.metadata.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('src')
        if value is not None and 'src' not in already_processed:
            already_processed.append('src')
            self.src = value
        value = attrs.get('dtype')
        if value is not None and 'dtype' not in already_processed:
            already_processed.append('dtype')
            self.dtype = value
        value = attrs.get('name')
        if value is not None and 'name' not in already_processed:
            already_processed.append('name')
            self.name = value
        value = attrs.get('fileformat')
        if value is not None and 'fileformat' not in already_processed:
            already_processed.append('fileformat')
            self.fileformat = value
            self.validate_trackFileFormat(self.fileformat)    # validate type trackFileFormat
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        if nodeName_ == 'description':
            description_ = child_.text
            description_ = self.gds_validate_string(description_, node, 'description')
            self.description = description_
        elif nodeName_ == 'tableOfContents': 
            obj_ = tableOfContents.factory()
            obj_.build(child_)
            self.set_description(obj_)
        elif nodeName_ == 'abstract': 
            obj_ = abstract.factory()
            obj_.build(child_)
            self.set_description(obj_)
        elif nodeName_ == 'metadata': 
            obj_ = metadata.factory()
            obj_.build(child_)
            self.set_metadata(obj_)
# end class CTrack


class CTimeseries(GeneratedsSuper):
    """Name of the timeseries. The path to the file according to location
    attribute Set to "HDF5" (default) to use the only supported
    Hierarchical Data File format. The HDF5 allows to store any
    number of time series or other large homogeneous data."""
    subclass = None
    superclass = None
    def __init__(self, src=None, dtype=None, name=None, fileformat='HDF5', description=None, metadata=None):
        self.src = _cast(None, src)
        self.dtype = _cast(None, dtype)
        self.name = _cast(None, name)
        self.fileformat = _cast(None, fileformat)
        self.description = description
        self.metadata = metadata
    def factory(*args_, **kwargs_):
        if CTimeseries.subclass:
            return CTimeseries.subclass(*args_, **kwargs_)
        else:
            return CTimeseries(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_description(self): return self.description
    def set_description(self, description): self.description = description
    def get_metadata(self): return self.metadata
    def set_metadata(self, metadata): self.metadata = metadata
    def get_src(self): return self.src
    def set_src(self, src): self.src = src
    def get_dtype(self): return self.dtype
    def set_dtype(self, dtype): self.dtype = dtype
    def get_name(self): return self.name
    def set_name(self, name): self.name = name
    def get_fileformat(self): return self.fileformat
    def set_fileformat(self, fileformat): self.fileformat = fileformat
    def validate_timeserieFileFormat(self, value):
        # Validate type timeserieFileFormat, a restriction on xsd:string.
        pass
    def export(self, outfile, level, namespace_='cml:', name_='CTimeseries', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='CTimeseries')
        if self.hasContent_():
            outfile.write('>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='CTimeseries'):
        if self.src is not None and 'src' not in already_processed:
            already_processed.append('src')
            outfile.write(' src=%s' % (self.gds_format_string(quote_attrib(self.src).encode(ExternalEncoding), input_name='src'), ))
        if self.dtype is not None and 'dtype' not in already_processed:
            already_processed.append('dtype')
            outfile.write(' dtype=%s' % (self.gds_format_string(quote_attrib(self.dtype).encode(ExternalEncoding), input_name='dtype'), ))
        if self.name is not None and 'name' not in already_processed:
            already_processed.append('name')
            outfile.write(' name=%s' % (self.gds_format_string(quote_attrib(self.name).encode(ExternalEncoding), input_name='name'), ))
        if self.fileformat is not None and 'fileformat' not in already_processed:
            already_processed.append('fileformat')
            outfile.write(' fileformat=%s' % (quote_attrib(self.fileformat), ))
    def exportChildren(self, outfile, level, namespace_='cml:', name_='CTimeseries'):
        if self.description is not None:
            showIndent(outfile, level)
            outfile.write('<%sdescription>%s</%sdescription>\n' % (namespace_, self.gds_format_string(quote_xml(self.description).encode(ExternalEncoding), input_name='description'), namespace_))
        if self.metadata:
            self.metadata.export(outfile, level, namespace_, name_='metadata', )
    def hasContent_(self):
        if (
            self.description is not None or
            self.metadata is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='CTimeseries'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.src is not None and 'src' not in already_processed:
            already_processed.append('src')
            showIndent(outfile, level)
            outfile.write('src = "%s",\n' % (self.src,))
        if self.dtype is not None and 'dtype' not in already_processed:
            already_processed.append('dtype')
            showIndent(outfile, level)
            outfile.write('dtype = "%s",\n' % (self.dtype,))
        if self.name is not None and 'name' not in already_processed:
            already_processed.append('name')
            showIndent(outfile, level)
            outfile.write('name = "%s",\n' % (self.name,))
        if self.fileformat is not None and 'fileformat' not in already_processed:
            already_processed.append('fileformat')
            showIndent(outfile, level)
            outfile.write('fileformat = "%s",\n' % (self.fileformat,))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.description is not None:
            showIndent(outfile, level)
            outfile.write('description=%s,\n' % quote_python(self.description).encode(ExternalEncoding))
        if self.metadata is not None:
            showIndent(outfile, level)
            outfile.write('metadata=model_.metadata(\n')
            self.metadata.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('src')
        if value is not None and 'src' not in already_processed:
            already_processed.append('src')
            self.src = value
        value = attrs.get('dtype')
        if value is not None and 'dtype' not in already_processed:
            already_processed.append('dtype')
            self.dtype = value
        value = attrs.get('name')
        if value is not None and 'name' not in already_processed:
            already_processed.append('name')
            self.name = value
        value = attrs.get('fileformat')
        if value is not None and 'fileformat' not in already_processed:
            already_processed.append('fileformat')
            self.fileformat = value
            self.validate_timeserieFileFormat(self.fileformat)    # validate type timeserieFileFormat
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        if nodeName_ == 'description':
            description_ = child_.text
            description_ = self.gds_validate_string(description_, node, 'description')
            self.description = description_
        elif nodeName_ == 'tableOfContents': 
            obj_ = tableOfContents.factory()
            obj_.build(child_)
            self.set_description(obj_)
        elif nodeName_ == 'abstract': 
            obj_ = abstract.factory()
            obj_.build(child_)
            self.set_description(obj_)
        elif nodeName_ == 'metadata': 
            obj_ = metadata.factory()
            obj_.build(child_)
            self.set_metadata(obj_)
# end class CTimeseries


class CData(GeneratedsSuper):
    """Name of the data file The path to the file according to location
    attribute Use one of 'NumPy', 'HDF5', 'XML', 'Other'"""
    subclass = None
    superclass = None
    def __init__(self, src=None, dtype=None, name=None, fileformat=None, description=None, metadata=None):
        self.src = _cast(None, src)
        self.dtype = _cast(None, dtype)
        self.name = _cast(None, name)
        self.fileformat = _cast(None, fileformat)
        self.description = description
        self.metadata = metadata
    def factory(*args_, **kwargs_):
        if CData.subclass:
            return CData.subclass(*args_, **kwargs_)
        else:
            return CData(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_description(self): return self.description
    def set_description(self, description): self.description = description
    def get_metadata(self): return self.metadata
    def set_metadata(self, metadata): self.metadata = metadata
    def get_src(self): return self.src
    def set_src(self, src): self.src = src
    def get_dtype(self): return self.dtype
    def set_dtype(self, dtype): self.dtype = dtype
    def get_name(self): return self.name
    def set_name(self, name): self.name = name
    def get_fileformat(self): return self.fileformat
    def set_fileformat(self, fileformat): self.fileformat = fileformat
    def validate_dataFileFormat(self, value):
        # Validate type dataFileFormat, a restriction on xsd:string.
        pass
    def export(self, outfile, level, namespace_='cml:', name_='CData', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='CData')
        if self.hasContent_():
            outfile.write('>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='CData'):
        if self.src is not None and 'src' not in already_processed:
            already_processed.append('src')
            outfile.write(' src=%s' % (self.gds_format_string(quote_attrib(self.src).encode(ExternalEncoding), input_name='src'), ))
        if self.dtype is not None and 'dtype' not in already_processed:
            already_processed.append('dtype')
            outfile.write(' dtype=%s' % (self.gds_format_string(quote_attrib(self.dtype).encode(ExternalEncoding), input_name='dtype'), ))
        if self.name is not None and 'name' not in already_processed:
            already_processed.append('name')
            outfile.write(' name=%s' % (self.gds_format_string(quote_attrib(self.name).encode(ExternalEncoding), input_name='name'), ))
        if self.fileformat is not None and 'fileformat' not in already_processed:
            already_processed.append('fileformat')
            outfile.write(' fileformat=%s' % (quote_attrib(self.fileformat), ))
    def exportChildren(self, outfile, level, namespace_='cml:', name_='CData'):
        if self.description is not None:
            showIndent(outfile, level)
            outfile.write('<%sdescription>%s</%sdescription>\n' % (namespace_, self.gds_format_string(quote_xml(self.description).encode(ExternalEncoding), input_name='description'), namespace_))
        if self.metadata:
            self.metadata.export(outfile, level, namespace_, name_='metadata', )
    def hasContent_(self):
        if (
            self.description is not None or
            self.metadata is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='CData'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.src is not None and 'src' not in already_processed:
            already_processed.append('src')
            showIndent(outfile, level)
            outfile.write('src = "%s",\n' % (self.src,))
        if self.dtype is not None and 'dtype' not in already_processed:
            already_processed.append('dtype')
            showIndent(outfile, level)
            outfile.write('dtype = "%s",\n' % (self.dtype,))
        if self.name is not None and 'name' not in already_processed:
            already_processed.append('name')
            showIndent(outfile, level)
            outfile.write('name = "%s",\n' % (self.name,))
        if self.fileformat is not None and 'fileformat' not in already_processed:
            already_processed.append('fileformat')
            showIndent(outfile, level)
            outfile.write('fileformat = "%s",\n' % (self.fileformat,))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.description is not None:
            showIndent(outfile, level)
            outfile.write('description=%s,\n' % quote_python(self.description).encode(ExternalEncoding))
        if self.metadata is not None:
            showIndent(outfile, level)
            outfile.write('metadata=model_.metadata(\n')
            self.metadata.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('src')
        if value is not None and 'src' not in already_processed:
            already_processed.append('src')
            self.src = value
        value = attrs.get('dtype')
        if value is not None and 'dtype' not in already_processed:
            already_processed.append('dtype')
            self.dtype = value
        value = attrs.get('name')
        if value is not None and 'name' not in already_processed:
            already_processed.append('name')
            self.name = value
        value = attrs.get('fileformat')
        if value is not None and 'fileformat' not in already_processed:
            already_processed.append('fileformat')
            self.fileformat = value
            self.validate_dataFileFormat(self.fileformat)    # validate type dataFileFormat
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        if nodeName_ == 'description':
            description_ = child_.text
            description_ = self.gds_validate_string(description_, node, 'description')
            self.description = description_
        elif nodeName_ == 'tableOfContents': 
            obj_ = tableOfContents.factory()
            obj_.build(child_)
            self.set_description(obj_)
        elif nodeName_ == 'abstract': 
            obj_ = abstract.factory()
            obj_.build(child_)
            self.set_description(obj_)
        elif nodeName_ == 'metadata': 
            obj_ = metadata.factory()
            obj_.build(child_)
            self.set_metadata(obj_)
# end class CData


class CScript(GeneratedsSuper):
    """Name of the script file The path to the file according to location
    attribute What kind of script. Use one of "Python" (default),
    "Bash", "Matlab", or "Other"."""
    subclass = None
    superclass = None
    def __init__(self, src=None, dtype='Python', name=None, fileformat='UTF-8', description=None, metadata=None):
        self.src = _cast(None, src)
        self.dtype = _cast(None, dtype)
        self.name = _cast(None, name)
        self.fileformat = _cast(None, fileformat)
        self.description = description
        self.metadata = metadata
    def factory(*args_, **kwargs_):
        if CScript.subclass:
            return CScript.subclass(*args_, **kwargs_)
        else:
            return CScript(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_description(self): return self.description
    def set_description(self, description): self.description = description
    def get_metadata(self): return self.metadata
    def set_metadata(self, metadata): self.metadata = metadata
    def get_src(self): return self.src
    def set_src(self, src): self.src = src
    def get_dtype(self): return self.dtype
    def set_dtype(self, dtype): self.dtype = dtype
    def validate_scriptEnumType(self, value):
        # Validate type scriptEnumType, a restriction on xsd:string.
        pass
    def get_name(self): return self.name
    def set_name(self, name): self.name = name
    def get_fileformat(self): return self.fileformat
    def set_fileformat(self, fileformat): self.fileformat = fileformat
    def validate_scriptFileFormat(self, value):
        # Validate type scriptFileFormat, a restriction on xsd:string.
        pass
    def export(self, outfile, level, namespace_='cml:', name_='CScript', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='CScript')
        if self.hasContent_():
            outfile.write('>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='CScript'):
        if self.src is not None and 'src' not in already_processed:
            already_processed.append('src')
            outfile.write(' src=%s' % (self.gds_format_string(quote_attrib(self.src).encode(ExternalEncoding), input_name='src'), ))
        if self.dtype is not None and 'dtype' not in already_processed:
            already_processed.append('dtype')
            outfile.write(' dtype=%s' % (quote_attrib(self.dtype), ))
        if self.name is not None and 'name' not in already_processed:
            already_processed.append('name')
            outfile.write(' name=%s' % (self.gds_format_string(quote_attrib(self.name).encode(ExternalEncoding), input_name='name'), ))
        if self.fileformat is not None and 'fileformat' not in already_processed:
            already_processed.append('fileformat')
            outfile.write(' fileformat=%s' % (quote_attrib(self.fileformat), ))
    def exportChildren(self, outfile, level, namespace_='cml:', name_='CScript'):
        if self.description is not None:
            showIndent(outfile, level)
            outfile.write('<%sdescription>%s</%sdescription>\n' % (namespace_, self.gds_format_string(quote_xml(self.description).encode(ExternalEncoding), input_name='description'), namespace_))
        if self.metadata:
            self.metadata.export(outfile, level, namespace_, name_='metadata', )
    def hasContent_(self):
        if (
            self.description is not None or
            self.metadata is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='CScript'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.src is not None and 'src' not in already_processed:
            already_processed.append('src')
            showIndent(outfile, level)
            outfile.write('src = "%s",\n' % (self.src,))
        if self.dtype is not None and 'dtype' not in already_processed:
            already_processed.append('dtype')
            showIndent(outfile, level)
            outfile.write('dtype = "%s",\n' % (self.dtype,))
        if self.name is not None and 'name' not in already_processed:
            already_processed.append('name')
            showIndent(outfile, level)
            outfile.write('name = "%s",\n' % (self.name,))
        if self.fileformat is not None and 'fileformat' not in already_processed:
            already_processed.append('fileformat')
            showIndent(outfile, level)
            outfile.write('fileformat = "%s",\n' % (self.fileformat,))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.description is not None:
            showIndent(outfile, level)
            outfile.write('description=%s,\n' % quote_python(self.description).encode(ExternalEncoding))
        if self.metadata is not None:
            showIndent(outfile, level)
            outfile.write('metadata=model_.metadata(\n')
            self.metadata.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('src')
        if value is not None and 'src' not in already_processed:
            already_processed.append('src')
            self.src = value
        value = attrs.get('dtype')
        if value is not None and 'dtype' not in already_processed:
            already_processed.append('dtype')
            self.dtype = value
            self.validate_scriptEnumType(self.dtype)    # validate type scriptEnumType
        value = attrs.get('name')
        if value is not None and 'name' not in already_processed:
            already_processed.append('name')
            self.name = value
        value = attrs.get('fileformat')
        if value is not None and 'fileformat' not in already_processed:
            already_processed.append('fileformat')
            self.fileformat = value
            self.validate_scriptFileFormat(self.fileformat)    # validate type scriptFileFormat
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        if nodeName_ == 'description':
            description_ = child_.text
            description_ = self.gds_validate_string(description_, node, 'description')
            self.description = description_
        elif nodeName_ == 'tableOfContents': 
            obj_ = tableOfContents.factory()
            obj_.build(child_)
            self.set_description(obj_)
        elif nodeName_ == 'abstract': 
            obj_ = abstract.factory()
            obj_.build(child_)
            self.set_description(obj_)
        elif nodeName_ == 'metadata': 
            obj_ = metadata.factory()
            obj_.build(child_)
            self.set_metadata(obj_)
# end class CScript


class CImagestack(GeneratedsSuper):
    """Name of the image stack The path to the enumerated files according
    to location attribute The file name pattern that may contain
    simple shell-style wildcards a la fnmatch. Use one of 'PNG',
    'JPG', 'TIFF', 'Other'"""
    subclass = None
    superclass = None
    def __init__(self, src=None, fileformat=None, name=None, pattern=None, description=None, metadata=None):
        self.src = _cast(None, src)
        self.fileformat = _cast(None, fileformat)
        self.name = _cast(None, name)
        self.pattern = _cast(None, pattern)
        self.description = description
        self.metadata = metadata
    def factory(*args_, **kwargs_):
        if CImagestack.subclass:
            return CImagestack.subclass(*args_, **kwargs_)
        else:
            return CImagestack(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_description(self): return self.description
    def set_description(self, description): self.description = description
    def get_metadata(self): return self.metadata
    def set_metadata(self, metadata): self.metadata = metadata
    def get_src(self): return self.src
    def set_src(self, src): self.src = src
    def get_fileformat(self): return self.fileformat
    def set_fileformat(self, fileformat): self.fileformat = fileformat
    def validate_imagestackFileFormat(self, value):
        # Validate type imagestackFileFormat, a restriction on xsd:string.
        pass
    def get_name(self): return self.name
    def set_name(self, name): self.name = name
    def get_pattern(self): return self.pattern
    def set_pattern(self, pattern): self.pattern = pattern
    def export(self, outfile, level, namespace_='cml:', name_='CImagestack', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='CImagestack')
        if self.hasContent_():
            outfile.write('>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='CImagestack'):
        if self.src is not None and 'src' not in already_processed:
            already_processed.append('src')
            outfile.write(' src=%s' % (self.gds_format_string(quote_attrib(self.src).encode(ExternalEncoding), input_name='src'), ))
        if self.fileformat is not None and 'fileformat' not in already_processed:
            already_processed.append('fileformat')
            outfile.write(' fileformat=%s' % (quote_attrib(self.fileformat), ))
        if self.name is not None and 'name' not in already_processed:
            already_processed.append('name')
            outfile.write(' name=%s' % (self.gds_format_string(quote_attrib(self.name).encode(ExternalEncoding), input_name='name'), ))
        if self.pattern is not None and 'pattern' not in already_processed:
            already_processed.append('pattern')
            outfile.write(' pattern=%s' % (self.gds_format_string(quote_attrib(self.pattern).encode(ExternalEncoding), input_name='pattern'), ))
    def exportChildren(self, outfile, level, namespace_='cml:', name_='CImagestack'):
        if self.description is not None:
            showIndent(outfile, level)
            outfile.write('<%sdescription>%s</%sdescription>\n' % (namespace_, self.gds_format_string(quote_xml(self.description).encode(ExternalEncoding), input_name='description'), namespace_))
        if self.metadata:
            self.metadata.export(outfile, level, namespace_, name_='metadata', )
    def hasContent_(self):
        if (
            self.description is not None or
            self.metadata is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='CImagestack'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.src is not None and 'src' not in already_processed:
            already_processed.append('src')
            showIndent(outfile, level)
            outfile.write('src = "%s",\n' % (self.src,))
        if self.fileformat is not None and 'fileformat' not in already_processed:
            already_processed.append('fileformat')
            showIndent(outfile, level)
            outfile.write('fileformat = "%s",\n' % (self.fileformat,))
        if self.name is not None and 'name' not in already_processed:
            already_processed.append('name')
            showIndent(outfile, level)
            outfile.write('name = "%s",\n' % (self.name,))
        if self.pattern is not None and 'pattern' not in already_processed:
            already_processed.append('pattern')
            showIndent(outfile, level)
            outfile.write('pattern = "%s",\n' % (self.pattern,))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.description is not None:
            showIndent(outfile, level)
            outfile.write('description=%s,\n' % quote_python(self.description).encode(ExternalEncoding))
        if self.metadata is not None:
            showIndent(outfile, level)
            outfile.write('metadata=model_.metadata(\n')
            self.metadata.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('src')
        if value is not None and 'src' not in already_processed:
            already_processed.append('src')
            self.src = value
        value = attrs.get('fileformat')
        if value is not None and 'fileformat' not in already_processed:
            already_processed.append('fileformat')
            self.fileformat = value
            self.validate_imagestackFileFormat(self.fileformat)    # validate type imagestackFileFormat
        value = attrs.get('name')
        if value is not None and 'name' not in already_processed:
            already_processed.append('name')
            self.name = value
        value = attrs.get('pattern')
        if value is not None and 'pattern' not in already_processed:
            already_processed.append('pattern')
            self.pattern = value
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        if nodeName_ == 'description':
            description_ = child_.text
            description_ = self.gds_validate_string(description_, node, 'description')
            self.description = description_
        elif nodeName_ == 'tableOfContents': 
            obj_ = tableOfContents.factory()
            obj_.build(child_)
            self.set_description(obj_)
        elif nodeName_ == 'abstract': 
            obj_ = abstract.factory()
            obj_.build(child_)
            self.set_description(obj_)
        elif nodeName_ == 'metadata': 
            obj_ = metadata.factory()
            obj_.build(child_)
            self.set_metadata(obj_)
# end class CImagestack


class title(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if title.subclass:
            return title.subclass(*args_, **kwargs_)
        else:
            return title(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='title', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='title')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='title'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='title'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='title'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class title


class creator(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if creator.subclass:
            return creator.subclass(*args_, **kwargs_)
        else:
            return creator(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='creator', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='creator')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='creator'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='creator'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='creator'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class creator


class subject(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if subject.subclass:
            return subject.subclass(*args_, **kwargs_)
        else:
            return subject(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='subject', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='subject')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='subject'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='subject'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='subject'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class subject


class description(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if description.subclass:
            return description.subclass(*args_, **kwargs_)
        else:
            return description(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='description', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='description')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='description'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='description'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='description'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class description


class publisher(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if publisher.subclass:
            return publisher.subclass(*args_, **kwargs_)
        else:
            return publisher(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='publisher', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='publisher')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='publisher'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='publisher'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='publisher'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class publisher


class contributor(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if contributor.subclass:
            return contributor.subclass(*args_, **kwargs_)
        else:
            return contributor(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='contributor', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='contributor')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='contributor'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='contributor'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='contributor'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class contributor


class date(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if date.subclass:
            return date.subclass(*args_, **kwargs_)
        else:
            return date(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='date', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='date')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='date'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='date'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='date'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class date


class type_(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if type_.subclass:
            return type_.subclass(*args_, **kwargs_)
        else:
            return type_(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='type', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='type')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='type'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='type'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='type'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class type_


class format(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if format.subclass:
            return format.subclass(*args_, **kwargs_)
        else:
            return format(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='format', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='format')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='format'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='format'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='format'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class format


class identifier(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if identifier.subclass:
            return identifier.subclass(*args_, **kwargs_)
        else:
            return identifier(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='identifier', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='identifier')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='identifier'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='identifier'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='identifier'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class identifier


class source(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if source.subclass:
            return source.subclass(*args_, **kwargs_)
        else:
            return source(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='source', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='source')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='source'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='source'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='source'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class source


class language(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if language.subclass:
            return language.subclass(*args_, **kwargs_)
        else:
            return language(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='language', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='language')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='language'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='language'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='language'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class language


class relation(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if relation.subclass:
            return relation.subclass(*args_, **kwargs_)
        else:
            return relation(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='relation', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='relation')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='relation'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='relation'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='relation'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class relation


class coverage(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if coverage.subclass:
            return coverage.subclass(*args_, **kwargs_)
        else:
            return coverage(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='coverage', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='coverage')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='coverage'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='coverage'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='coverage'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class coverage


class rights(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if rights.subclass:
            return rights.subclass(*args_, **kwargs_)
        else:
            return rights(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='rights', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='rights')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='rights'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='rights'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='rights'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class rights


class alternative(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if alternative.subclass:
            return alternative.subclass(*args_, **kwargs_)
        else:
            return alternative(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='alternative', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='alternative')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='alternative'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='alternative'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='alternative'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class alternative


class tableOfContents(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if tableOfContents.subclass:
            return tableOfContents.subclass(*args_, **kwargs_)
        else:
            return tableOfContents(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='tableOfContents', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='tableOfContents')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='tableOfContents'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='tableOfContents'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='tableOfContents'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class tableOfContents


class abstract(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if abstract.subclass:
            return abstract.subclass(*args_, **kwargs_)
        else:
            return abstract(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='abstract', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='abstract')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='abstract'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='abstract'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='abstract'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class abstract


class created(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if created.subclass:
            return created.subclass(*args_, **kwargs_)
        else:
            return created(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='created', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='created')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='created'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='created'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='created'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class created


class valid(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if valid.subclass:
            return valid.subclass(*args_, **kwargs_)
        else:
            return valid(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='valid', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='valid')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='valid'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='valid'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='valid'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class valid


class available(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if available.subclass:
            return available.subclass(*args_, **kwargs_)
        else:
            return available(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='available', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='available')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='available'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='available'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='available'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class available


class issued(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if issued.subclass:
            return issued.subclass(*args_, **kwargs_)
        else:
            return issued(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='issued', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='issued')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='issued'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='issued'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='issued'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class issued


class modified(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if modified.subclass:
            return modified.subclass(*args_, **kwargs_)
        else:
            return modified(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='modified', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='modified')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='modified'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='modified'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='modified'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class modified


class dateAccepted(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if dateAccepted.subclass:
            return dateAccepted.subclass(*args_, **kwargs_)
        else:
            return dateAccepted(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='dateAccepted', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='dateAccepted')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='dateAccepted'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='dateAccepted'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='dateAccepted'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class dateAccepted


class dateCopyrighted(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if dateCopyrighted.subclass:
            return dateCopyrighted.subclass(*args_, **kwargs_)
        else:
            return dateCopyrighted(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='dateCopyrighted', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='dateCopyrighted')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='dateCopyrighted'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='dateCopyrighted'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='dateCopyrighted'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class dateCopyrighted


class dateSubmitted(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if dateSubmitted.subclass:
            return dateSubmitted.subclass(*args_, **kwargs_)
        else:
            return dateSubmitted(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='dateSubmitted', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='dateSubmitted')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='dateSubmitted'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='dateSubmitted'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='dateSubmitted'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class dateSubmitted


class extent(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if extent.subclass:
            return extent.subclass(*args_, **kwargs_)
        else:
            return extent(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='extent', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='extent')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='extent'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='extent'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='extent'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class extent


class medium(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if medium.subclass:
            return medium.subclass(*args_, **kwargs_)
        else:
            return medium(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='medium', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='medium')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='medium'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='medium'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='medium'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class medium


class isVersionOf(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if isVersionOf.subclass:
            return isVersionOf.subclass(*args_, **kwargs_)
        else:
            return isVersionOf(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='isVersionOf', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='isVersionOf')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='isVersionOf'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='isVersionOf'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='isVersionOf'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class isVersionOf


class hasVersion(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if hasVersion.subclass:
            return hasVersion.subclass(*args_, **kwargs_)
        else:
            return hasVersion(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='hasVersion', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='hasVersion')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='hasVersion'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='hasVersion'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='hasVersion'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class hasVersion


class isReplacedBy(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if isReplacedBy.subclass:
            return isReplacedBy.subclass(*args_, **kwargs_)
        else:
            return isReplacedBy(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='isReplacedBy', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='isReplacedBy')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='isReplacedBy'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='isReplacedBy'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='isReplacedBy'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class isReplacedBy


class replaces(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if replaces.subclass:
            return replaces.subclass(*args_, **kwargs_)
        else:
            return replaces(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='replaces', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='replaces')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='replaces'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='replaces'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='replaces'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class replaces


class isRequiredBy(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if isRequiredBy.subclass:
            return isRequiredBy.subclass(*args_, **kwargs_)
        else:
            return isRequiredBy(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='isRequiredBy', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='isRequiredBy')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='isRequiredBy'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='isRequiredBy'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='isRequiredBy'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class isRequiredBy


class requires(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if requires.subclass:
            return requires.subclass(*args_, **kwargs_)
        else:
            return requires(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='requires', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='requires')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='requires'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='requires'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='requires'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class requires


class isPartOf(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if isPartOf.subclass:
            return isPartOf.subclass(*args_, **kwargs_)
        else:
            return isPartOf(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='isPartOf', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='isPartOf')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='isPartOf'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='isPartOf'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='isPartOf'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class isPartOf


class hasPart(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if hasPart.subclass:
            return hasPart.subclass(*args_, **kwargs_)
        else:
            return hasPart(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='hasPart', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='hasPart')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='hasPart'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='hasPart'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='hasPart'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class hasPart


class isReferencedBy(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if isReferencedBy.subclass:
            return isReferencedBy.subclass(*args_, **kwargs_)
        else:
            return isReferencedBy(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='isReferencedBy', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='isReferencedBy')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='isReferencedBy'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='isReferencedBy'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='isReferencedBy'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class isReferencedBy


class references(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if references.subclass:
            return references.subclass(*args_, **kwargs_)
        else:
            return references(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='references', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='references')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='references'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='references'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='references'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class references


class isFormatOf(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if isFormatOf.subclass:
            return isFormatOf.subclass(*args_, **kwargs_)
        else:
            return isFormatOf(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='isFormatOf', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='isFormatOf')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='isFormatOf'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='isFormatOf'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='isFormatOf'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class isFormatOf


class hasFormat(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if hasFormat.subclass:
            return hasFormat.subclass(*args_, **kwargs_)
        else:
            return hasFormat(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='hasFormat', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='hasFormat')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='hasFormat'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='hasFormat'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='hasFormat'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class hasFormat


class conformsTo(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if conformsTo.subclass:
            return conformsTo.subclass(*args_, **kwargs_)
        else:
            return conformsTo(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='conformsTo', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='conformsTo')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='conformsTo'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='conformsTo'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='conformsTo'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class conformsTo


class spatial(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if spatial.subclass:
            return spatial.subclass(*args_, **kwargs_)
        else:
            return spatial(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='spatial', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='spatial')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='spatial'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='spatial'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='spatial'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class spatial


class temporal(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if temporal.subclass:
            return temporal.subclass(*args_, **kwargs_)
        else:
            return temporal(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='temporal', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='temporal')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='temporal'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='temporal'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='temporal'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class temporal


class audience(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if audience.subclass:
            return audience.subclass(*args_, **kwargs_)
        else:
            return audience(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='audience', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='audience')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='audience'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='audience'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='audience'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class audience


class accrualMethod(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if accrualMethod.subclass:
            return accrualMethod.subclass(*args_, **kwargs_)
        else:
            return accrualMethod(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='accrualMethod', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='accrualMethod')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='accrualMethod'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='accrualMethod'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='accrualMethod'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class accrualMethod


class accrualPeriodicity(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if accrualPeriodicity.subclass:
            return accrualPeriodicity.subclass(*args_, **kwargs_)
        else:
            return accrualPeriodicity(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='accrualPeriodicity', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='accrualPeriodicity')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='accrualPeriodicity'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='accrualPeriodicity'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='accrualPeriodicity'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class accrualPeriodicity


class accrualPolicy(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if accrualPolicy.subclass:
            return accrualPolicy.subclass(*args_, **kwargs_)
        else:
            return accrualPolicy(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='accrualPolicy', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='accrualPolicy')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='accrualPolicy'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='accrualPolicy'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='accrualPolicy'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class accrualPolicy


class instructionalMethod(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if instructionalMethod.subclass:
            return instructionalMethod.subclass(*args_, **kwargs_)
        else:
            return instructionalMethod(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='instructionalMethod', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='instructionalMethod')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='instructionalMethod'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='instructionalMethod'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='instructionalMethod'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class instructionalMethod


class provenance(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if provenance.subclass:
            return provenance.subclass(*args_, **kwargs_)
        else:
            return provenance(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='provenance', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='provenance')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='provenance'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='provenance'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='provenance'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class provenance


class rightsHolder(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if rightsHolder.subclass:
            return rightsHolder.subclass(*args_, **kwargs_)
        else:
            return rightsHolder(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='rightsHolder', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='rightsHolder')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='rightsHolder'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='rightsHolder'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='rightsHolder'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class rightsHolder


class mediator(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if mediator.subclass:
            return mediator.subclass(*args_, **kwargs_)
        else:
            return mediator(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='mediator', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='mediator')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='mediator'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='mediator'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='mediator'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class mediator


class educationLevel(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if educationLevel.subclass:
            return educationLevel.subclass(*args_, **kwargs_)
        else:
            return educationLevel(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='educationLevel', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='educationLevel')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='educationLevel'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='educationLevel'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='educationLevel'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class educationLevel


class accessRights(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if accessRights.subclass:
            return accessRights.subclass(*args_, **kwargs_)
        else:
            return accessRights(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='accessRights', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='accessRights')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='accessRights'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='accessRights'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='accessRights'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class accessRights


class license(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if license.subclass:
            return license.subclass(*args_, **kwargs_)
        else:
            return license(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='license', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='license')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='license'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='license'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='license'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class license


class bibliographicCitation(GeneratedsSuper):
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None):
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if bibliographicCitation.subclass:
            return bibliographicCitation.subclass(*args_, **kwargs_)
        else:
            return bibliographicCitation(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='bibliographicCitation', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='bibliographicCitation')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='bibliographicCitation'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='bibliographicCitation'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='bibliographicCitation'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class bibliographicCitation


class elementOrRefinementContainer(GeneratedsSuper):
    """This is included as a convenience for schema authors who need to
    define a root or container element for all of the DC elements
    and element refinements."""
    subclass = None
    superclass = None
    def __init__(self, any=None):
        if any is None:
            self.any = []
        else:
            self.any = any
    def factory(*args_, **kwargs_):
        if elementOrRefinementContainer.subclass:
            return elementOrRefinementContainer.subclass(*args_, **kwargs_)
        else:
            return elementOrRefinementContainer(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_any(self): return self.any
    def set_any(self, any): self.any = any
    def add_any(self, value): self.any.append(value)
    def insert_any(self, index, value): self.any[index] = value
    def export(self, outfile, level, namespace_='cml:', name_='elementOrRefinementContainer', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='elementOrRefinementContainer')
        if self.hasContent_():
            outfile.write('>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='elementOrRefinementContainer'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='elementOrRefinementContainer'):
        for any_ in self.get_any():
            any_.export(outfile, level, namespace_, name_='any')
    def hasContent_(self):
        if (
            self.any
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='elementOrRefinementContainer'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('any=[\n')
        level += 1
        for any_ in self.any:
            showIndent(outfile, level)
            outfile.write('model_.any(\n')
            any_.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        if nodeName_ == 'any': 
            type_name_ = child_.attrib.get('{http://www.w3.org/2001/XMLSchema-instance}type')
            if type_name_ is None:
                type_name_ = child_.attrib.get('type')
            if type_name_ is not None:
                type_names_ = type_name_.split(':')
                if len(type_names_) == 1:
                    type_name_ = type_names_[0]
                else:
                    type_name_ = type_names_[1]
                class_ = globals()[type_name_]
                obj_ = class_.factory()
                obj_.build(child_)
            else:
                raise NotImplementedError(
                    'Class not implemented for <any> element')
            self.any.append(obj_)
        elif nodeName_ == 'title': 
            obj_ = title.factory()
            obj_.build(child_)
            self.title.append(obj_)
        elif nodeName_ == 'creator': 
            obj_ = creator.factory()
            obj_.build(child_)
            self.creator.append(obj_)
        elif nodeName_ == 'subject': 
            obj_ = subject.factory()
            obj_.build(child_)
            self.subject.append(obj_)
        elif nodeName_ == 'description': 
            obj_ = description.factory()
            obj_.build(child_)
            self.description.append(obj_)
        elif nodeName_ == 'publisher': 
            obj_ = publisher.factory()
            obj_.build(child_)
            self.publisher.append(obj_)
        elif nodeName_ == 'contributor': 
            obj_ = contributor.factory()
            obj_.build(child_)
            self.contributor.append(obj_)
        elif nodeName_ == 'date': 
            obj_ = date.factory()
            obj_.build(child_)
            self.date.append(obj_)
        elif nodeName_ == 'type': 
            obj_ = type_.factory()
            obj_.build(child_)
            self.type_.append(obj_)
        elif nodeName_ == 'format': 
            obj_ = format.factory()
            obj_.build(child_)
            self.format.append(obj_)
        elif nodeName_ == 'identifier': 
            obj_ = identifier.factory()
            obj_.build(child_)
            self.identifier.append(obj_)
        elif nodeName_ == 'source': 
            obj_ = source.factory()
            obj_.build(child_)
            self.source.append(obj_)
        elif nodeName_ == 'language': 
            obj_ = language.factory()
            obj_.build(child_)
            self.language.append(obj_)
        elif nodeName_ == 'relation': 
            obj_ = relation.factory()
            obj_.build(child_)
            self.relation.append(obj_)
        elif nodeName_ == 'coverage': 
            obj_ = coverage.factory()
            obj_.build(child_)
            self.coverage.append(obj_)
        elif nodeName_ == 'rights': 
            obj_ = rights.factory()
            obj_.build(child_)
            self.rights.append(obj_)
        elif nodeName_ == 'alternative': 
            obj_ = alternative.factory()
            obj_.build(child_)
            self.alternative.append(obj_)
        elif nodeName_ == 'tableOfContents': 
            obj_ = tableOfContents.factory()
            obj_.build(child_)
            self.tableOfContents.append(obj_)
        elif nodeName_ == 'abstract': 
            obj_ = abstract.factory()
            obj_.build(child_)
            self.abstract.append(obj_)
        elif nodeName_ == 'created': 
            obj_ = created.factory()
            obj_.build(child_)
            self.created.append(obj_)
        elif nodeName_ == 'valid': 
            obj_ = valid.factory()
            obj_.build(child_)
            self.valid.append(obj_)
        elif nodeName_ == 'available': 
            obj_ = available.factory()
            obj_.build(child_)
            self.available.append(obj_)
        elif nodeName_ == 'issued': 
            obj_ = issued.factory()
            obj_.build(child_)
            self.issued.append(obj_)
        elif nodeName_ == 'modified': 
            obj_ = modified.factory()
            obj_.build(child_)
            self.modified.append(obj_)
        elif nodeName_ == 'dateAccepted': 
            obj_ = dateAccepted.factory()
            obj_.build(child_)
            self.dateAccepted.append(obj_)
        elif nodeName_ == 'dateCopyrighted': 
            obj_ = dateCopyrighted.factory()
            obj_.build(child_)
            self.dateCopyrighted.append(obj_)
        elif nodeName_ == 'dateSubmitted': 
            obj_ = dateSubmitted.factory()
            obj_.build(child_)
            self.dateSubmitted.append(obj_)
        elif nodeName_ == 'extent': 
            obj_ = extent.factory()
            obj_.build(child_)
            self.extent.append(obj_)
        elif nodeName_ == 'medium': 
            obj_ = medium.factory()
            obj_.build(child_)
            self.medium.append(obj_)
        elif nodeName_ == 'bibliographicCitation': 
            obj_ = bibliographicCitation.factory()
            obj_.build(child_)
            self.bibliographicCitation.append(obj_)
        elif nodeName_ == 'isVersionOf': 
            obj_ = isVersionOf.factory()
            obj_.build(child_)
            self.isVersionOf.append(obj_)
        elif nodeName_ == 'hasVersion': 
            obj_ = hasVersion.factory()
            obj_.build(child_)
            self.hasVersion.append(obj_)
        elif nodeName_ == 'isReplacedBy': 
            obj_ = isReplacedBy.factory()
            obj_.build(child_)
            self.isReplacedBy.append(obj_)
        elif nodeName_ == 'replaces': 
            obj_ = replaces.factory()
            obj_.build(child_)
            self.replaces.append(obj_)
        elif nodeName_ == 'isRequiredBy': 
            obj_ = isRequiredBy.factory()
            obj_.build(child_)
            self.isRequiredBy.append(obj_)
        elif nodeName_ == 'requires': 
            obj_ = requires.factory()
            obj_.build(child_)
            self.requires.append(obj_)
        elif nodeName_ == 'isPartOf': 
            obj_ = isPartOf.factory()
            obj_.build(child_)
            self.isPartOf.append(obj_)
        elif nodeName_ == 'hasPart': 
            obj_ = hasPart.factory()
            obj_.build(child_)
            self.hasPart.append(obj_)
        elif nodeName_ == 'isReferencedBy': 
            obj_ = isReferencedBy.factory()
            obj_.build(child_)
            self.isReferencedBy.append(obj_)
        elif nodeName_ == 'references': 
            obj_ = references.factory()
            obj_.build(child_)
            self.references.append(obj_)
        elif nodeName_ == 'isFormatOf': 
            obj_ = isFormatOf.factory()
            obj_.build(child_)
            self.isFormatOf.append(obj_)
        elif nodeName_ == 'hasFormat': 
            obj_ = hasFormat.factory()
            obj_.build(child_)
            self.hasFormat.append(obj_)
        elif nodeName_ == 'conformsTo': 
            obj_ = conformsTo.factory()
            obj_.build(child_)
            self.conformsTo.append(obj_)
        elif nodeName_ == 'spatial': 
            obj_ = spatial.factory()
            obj_.build(child_)
            self.spatial.append(obj_)
        elif nodeName_ == 'temporal': 
            obj_ = temporal.factory()
            obj_.build(child_)
            self.temporal.append(obj_)
        elif nodeName_ == 'accessRights': 
            obj_ = accessRights.factory()
            obj_.build(child_)
            self.accessRights.append(obj_)
        elif nodeName_ == 'license': 
            obj_ = license.factory()
            obj_.build(child_)
            self.license.append(obj_)
# end class elementOrRefinementContainer


class SimpleLiteral(GeneratedsSuper):
    """This is the default type for all of the DC elements. It permits text
    content only with optional xml:lang attribute. Text is allowed
    because mixed="true", but sub-elements are disallowed because
    minOccurs="0" and maxOccurs="0" are on the xs:any tag. This
    complexType allows for restriction or extension permitting child
    elements."""
    subclass = None
    superclass = None
    def __init__(self, lang=None, valueOf_=None):
        self.lang = _cast(None, lang)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if SimpleLiteral.subclass:
            return SimpleLiteral.subclass(*args_, **kwargs_)
        else:
            return SimpleLiteral(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_lang(self): return self.lang
    def set_lang(self, lang): self.lang = lang
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='SimpleLiteral', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='SimpleLiteral')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='SimpleLiteral'):
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            outfile.write(' lang=%s' % (self.gds_format_string(quote_attrib(self.lang).encode(ExternalEncoding), input_name='lang'), ))
    def exportChildren(self, outfile, level, namespace_='cml:', name_='SimpleLiteral'):
        pass
    def hasContent_(self):
        if (
            self.valueOf_
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='SimpleLiteral'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            showIndent(outfile, level)
            outfile.write('lang = "%s",\n' % (self.lang,))
    def exportLiteralChildren(self, outfile, level, name_):
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('lang')
        if value is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            self.lang = value
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        pass
# end class SimpleLiteral


class elementContainer(GeneratedsSuper):
    """This complexType is included as a convenience for schema authors who
    need to define a root or container element for all of the DC
    elements."""
    subclass = None
    superclass = None
    def __init__(self, any=None):
        if any is None:
            self.any = []
        else:
            self.any = any
    def factory(*args_, **kwargs_):
        if elementContainer.subclass:
            return elementContainer.subclass(*args_, **kwargs_)
        else:
            return elementContainer(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_any(self): return self.any
    def set_any(self, any): self.any = any
    def add_any(self, value): self.any.append(value)
    def insert_any(self, index, value): self.any[index] = value
    def export(self, outfile, level, namespace_='cml:', name_='elementContainer', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='elementContainer')
        if self.hasContent_():
            outfile.write('>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='elementContainer'):
        pass
    def exportChildren(self, outfile, level, namespace_='cml:', name_='elementContainer'):
        for any_ in self.get_any():
            any_.export(outfile, level, namespace_, name_='any')
    def hasContent_(self):
        if (
            self.any
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='elementContainer'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('any=[\n')
        level += 1
        for any_ in self.any:
            showIndent(outfile, level)
            outfile.write('model_.any(\n')
            any_.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        if nodeName_ == 'any': 
            type_name_ = child_.attrib.get('{http://www.w3.org/2001/XMLSchema-instance}type')
            if type_name_ is None:
                type_name_ = child_.attrib.get('type')
            if type_name_ is not None:
                type_names_ = type_name_.split(':')
                if len(type_names_) == 1:
                    type_name_ = type_names_[0]
                else:
                    type_name_ = type_names_[1]
                class_ = globals()[type_name_]
                obj_ = class_.factory()
                obj_.build(child_)
            else:
                raise NotImplementedError(
                    'Class not implemented for <any> element')
            self.any.append(obj_)
        elif nodeName_ == 'title': 
            obj_ = title.factory()
            obj_.build(child_)
            self.title.append(obj_)
        elif nodeName_ == 'creator': 
            obj_ = creator.factory()
            obj_.build(child_)
            self.creator.append(obj_)
        elif nodeName_ == 'subject': 
            obj_ = subject.factory()
            obj_.build(child_)
            self.subject.append(obj_)
        elif nodeName_ == 'description': 
            obj_ = description.factory()
            obj_.build(child_)
            self.description.append(obj_)
        elif nodeName_ == 'publisher': 
            obj_ = publisher.factory()
            obj_.build(child_)
            self.publisher.append(obj_)
        elif nodeName_ == 'contributor': 
            obj_ = contributor.factory()
            obj_.build(child_)
            self.contributor.append(obj_)
        elif nodeName_ == 'date': 
            obj_ = date.factory()
            obj_.build(child_)
            self.date.append(obj_)
        elif nodeName_ == 'type': 
            obj_ = type_.factory()
            obj_.build(child_)
            self.type_.append(obj_)
        elif nodeName_ == 'format': 
            obj_ = format.factory()
            obj_.build(child_)
            self.format.append(obj_)
        elif nodeName_ == 'identifier': 
            obj_ = identifier.factory()
            obj_.build(child_)
            self.identifier.append(obj_)
        elif nodeName_ == 'source': 
            obj_ = source.factory()
            obj_.build(child_)
            self.source.append(obj_)
        elif nodeName_ == 'language': 
            obj_ = language.factory()
            obj_.build(child_)
            self.language.append(obj_)
        elif nodeName_ == 'relation': 
            obj_ = relation.factory()
            obj_.build(child_)
            self.relation.append(obj_)
        elif nodeName_ == 'coverage': 
            obj_ = coverage.factory()
            obj_.build(child_)
            self.coverage.append(obj_)
        elif nodeName_ == 'rights': 
            obj_ = rights.factory()
            obj_.build(child_)
            self.rights.append(obj_)
        elif nodeName_ == 'alternative': 
            obj_ = alternative.factory()
            obj_.build(child_)
            self.alternative.append(obj_)
        elif nodeName_ == 'tableOfContents': 
            obj_ = tableOfContents.factory()
            obj_.build(child_)
            self.tableOfContents.append(obj_)
        elif nodeName_ == 'abstract': 
            obj_ = abstract.factory()
            obj_.build(child_)
            self.abstract.append(obj_)
        elif nodeName_ == 'created': 
            obj_ = created.factory()
            obj_.build(child_)
            self.created.append(obj_)
        elif nodeName_ == 'valid': 
            obj_ = valid.factory()
            obj_.build(child_)
            self.valid.append(obj_)
        elif nodeName_ == 'available': 
            obj_ = available.factory()
            obj_.build(child_)
            self.available.append(obj_)
        elif nodeName_ == 'issued': 
            obj_ = issued.factory()
            obj_.build(child_)
            self.issued.append(obj_)
        elif nodeName_ == 'modified': 
            obj_ = modified.factory()
            obj_.build(child_)
            self.modified.append(obj_)
        elif nodeName_ == 'dateAccepted': 
            obj_ = dateAccepted.factory()
            obj_.build(child_)
            self.dateAccepted.append(obj_)
        elif nodeName_ == 'dateCopyrighted': 
            obj_ = dateCopyrighted.factory()
            obj_.build(child_)
            self.dateCopyrighted.append(obj_)
        elif nodeName_ == 'dateSubmitted': 
            obj_ = dateSubmitted.factory()
            obj_.build(child_)
            self.dateSubmitted.append(obj_)
        elif nodeName_ == 'extent': 
            obj_ = extent.factory()
            obj_.build(child_)
            self.extent.append(obj_)
        elif nodeName_ == 'medium': 
            obj_ = medium.factory()
            obj_.build(child_)
            self.medium.append(obj_)
        elif nodeName_ == 'bibliographicCitation': 
            obj_ = bibliographicCitation.factory()
            obj_.build(child_)
            self.bibliographicCitation.append(obj_)
        elif nodeName_ == 'isVersionOf': 
            obj_ = isVersionOf.factory()
            obj_.build(child_)
            self.isVersionOf.append(obj_)
        elif nodeName_ == 'hasVersion': 
            obj_ = hasVersion.factory()
            obj_.build(child_)
            self.hasVersion.append(obj_)
        elif nodeName_ == 'isReplacedBy': 
            obj_ = isReplacedBy.factory()
            obj_.build(child_)
            self.isReplacedBy.append(obj_)
        elif nodeName_ == 'replaces': 
            obj_ = replaces.factory()
            obj_.build(child_)
            self.replaces.append(obj_)
        elif nodeName_ == 'isRequiredBy': 
            obj_ = isRequiredBy.factory()
            obj_.build(child_)
            self.isRequiredBy.append(obj_)
        elif nodeName_ == 'requires': 
            obj_ = requires.factory()
            obj_.build(child_)
            self.requires.append(obj_)
        elif nodeName_ == 'isPartOf': 
            obj_ = isPartOf.factory()
            obj_.build(child_)
            self.isPartOf.append(obj_)
        elif nodeName_ == 'hasPart': 
            obj_ = hasPart.factory()
            obj_.build(child_)
            self.hasPart.append(obj_)
        elif nodeName_ == 'isReferencedBy': 
            obj_ = isReferencedBy.factory()
            obj_.build(child_)
            self.isReferencedBy.append(obj_)
        elif nodeName_ == 'references': 
            obj_ = references.factory()
            obj_.build(child_)
            self.references.append(obj_)
        elif nodeName_ == 'isFormatOf': 
            obj_ = isFormatOf.factory()
            obj_.build(child_)
            self.isFormatOf.append(obj_)
        elif nodeName_ == 'hasFormat': 
            obj_ = hasFormat.factory()
            obj_.build(child_)
            self.hasFormat.append(obj_)
        elif nodeName_ == 'conformsTo': 
            obj_ = conformsTo.factory()
            obj_.build(child_)
            self.conformsTo.append(obj_)
        elif nodeName_ == 'spatial': 
            obj_ = spatial.factory()
            obj_.build(child_)
            self.spatial.append(obj_)
        elif nodeName_ == 'temporal': 
            obj_ = temporal.factory()
            obj_.build(child_)
            self.temporal.append(obj_)
        elif nodeName_ == 'accessRights': 
            obj_ = accessRights.factory()
            obj_.build(child_)
            self.accessRights.append(obj_)
        elif nodeName_ == 'license': 
            obj_ = license.factory()
            obj_.build(child_)
            self.license.append(obj_)
# end class elementContainer


class TGN(SimpleLiteral):
    subclass = None
    superclass = SimpleLiteral
    def __init__(self, lang=None, valueOf_=None):
        super(TGN, self).__init__(lang, valueOf_, )
        self.lang = _cast(None, lang)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if TGN.subclass:
            return TGN.subclass(*args_, **kwargs_)
        else:
            return TGN(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_lang(self): return self.lang
    def set_lang(self, lang): self.lang = lang
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='TGN', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='TGN')
        outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        outfile.write(' xsi:type="TGN"')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='TGN'):
        super(TGN, self).exportAttributes(outfile, level, already_processed, namespace_, name_='TGN')
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            outfile.write(' lang=%s' % (self.gds_format_string(quote_attrib(self.lang).encode(ExternalEncoding), input_name='lang'), ))
    def exportChildren(self, outfile, level, namespace_='cml:', name_='TGN'):
        super(TGN, self).exportChildren(outfile, level, namespace_, name_)
        pass
    def hasContent_(self):
        if (
            self.valueOf_ or
            super(TGN, self).hasContent_()
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='TGN'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            showIndent(outfile, level)
            outfile.write('lang = "%s",\n' % (self.lang,))
        super(TGN, self).exportLiteralAttributes(outfile, level, already_processed, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        super(TGN, self).exportLiteralChildren(outfile, level, name_)
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('lang')
        if value is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            self.lang = value
        super(TGN, self).buildAttributes(node, attrs, already_processed)
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        super(TGN, self).buildChildren(child_, node, nodeName_, True)
        pass
# end class TGN


class Box(SimpleLiteral):
    subclass = None
    superclass = SimpleLiteral
    def __init__(self, lang=None, valueOf_=None):
        super(Box, self).__init__(lang, valueOf_, )
        self.lang = _cast(None, lang)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if Box.subclass:
            return Box.subclass(*args_, **kwargs_)
        else:
            return Box(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_lang(self): return self.lang
    def set_lang(self, lang): self.lang = lang
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='Box', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='Box')
        outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        outfile.write(' xsi:type="Box"')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='Box'):
        super(Box, self).exportAttributes(outfile, level, already_processed, namespace_, name_='Box')
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            outfile.write(' lang=%s' % (self.gds_format_string(quote_attrib(self.lang).encode(ExternalEncoding), input_name='lang'), ))
    def exportChildren(self, outfile, level, namespace_='cml:', name_='Box'):
        super(Box, self).exportChildren(outfile, level, namespace_, name_)
        pass
    def hasContent_(self):
        if (
            self.valueOf_ or
            super(Box, self).hasContent_()
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='Box'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            showIndent(outfile, level)
            outfile.write('lang = "%s",\n' % (self.lang,))
        super(Box, self).exportLiteralAttributes(outfile, level, already_processed, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        super(Box, self).exportLiteralChildren(outfile, level, name_)
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('lang')
        if value is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            self.lang = value
        super(Box, self).buildAttributes(node, attrs, already_processed)
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        super(Box, self).buildChildren(child_, node, nodeName_, True)
        pass
# end class Box


class ISO3166(SimpleLiteral):
    subclass = None
    superclass = SimpleLiteral
    def __init__(self, lang=None, valueOf_=None):
        super(ISO3166, self).__init__(lang, valueOf_, )
        self.lang = _cast(None, lang)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if ISO3166.subclass:
            return ISO3166.subclass(*args_, **kwargs_)
        else:
            return ISO3166(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_lang(self): return self.lang
    def set_lang(self, lang): self.lang = lang
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='ISO3166', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='ISO3166')
        outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        outfile.write(' xsi:type="ISO3166"')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='ISO3166'):
        super(ISO3166, self).exportAttributes(outfile, level, already_processed, namespace_, name_='ISO3166')
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            outfile.write(' lang=%s' % (self.gds_format_string(quote_attrib(self.lang).encode(ExternalEncoding), input_name='lang'), ))
    def exportChildren(self, outfile, level, namespace_='cml:', name_='ISO3166'):
        super(ISO3166, self).exportChildren(outfile, level, namespace_, name_)
        pass
    def hasContent_(self):
        if (
            self.valueOf_ or
            super(ISO3166, self).hasContent_()
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='ISO3166'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            showIndent(outfile, level)
            outfile.write('lang = "%s",\n' % (self.lang,))
        super(ISO3166, self).exportLiteralAttributes(outfile, level, already_processed, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        super(ISO3166, self).exportLiteralChildren(outfile, level, name_)
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('lang')
        if value is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            self.lang = value
        super(ISO3166, self).buildAttributes(node, attrs, already_processed)
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        super(ISO3166, self).buildChildren(child_, node, nodeName_, True)
        pass
# end class ISO3166


class Point(SimpleLiteral):
    subclass = None
    superclass = SimpleLiteral
    def __init__(self, lang=None, valueOf_=None):
        super(Point, self).__init__(lang, valueOf_, )
        self.lang = _cast(None, lang)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if Point.subclass:
            return Point.subclass(*args_, **kwargs_)
        else:
            return Point(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_lang(self): return self.lang
    def set_lang(self, lang): self.lang = lang
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='Point', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='Point')
        outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        outfile.write(' xsi:type="Point"')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='Point'):
        super(Point, self).exportAttributes(outfile, level, already_processed, namespace_, name_='Point')
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            outfile.write(' lang=%s' % (self.gds_format_string(quote_attrib(self.lang).encode(ExternalEncoding), input_name='lang'), ))
    def exportChildren(self, outfile, level, namespace_='cml:', name_='Point'):
        super(Point, self).exportChildren(outfile, level, namespace_, name_)
        pass
    def hasContent_(self):
        if (
            self.valueOf_ or
            super(Point, self).hasContent_()
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='Point'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            showIndent(outfile, level)
            outfile.write('lang = "%s",\n' % (self.lang,))
        super(Point, self).exportLiteralAttributes(outfile, level, already_processed, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        super(Point, self).exportLiteralChildren(outfile, level, name_)
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('lang')
        if value is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            self.lang = value
        super(Point, self).buildAttributes(node, attrs, already_processed)
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        super(Point, self).buildChildren(child_, node, nodeName_, True)
        pass
# end class Point


class RFC4646(SimpleLiteral):
    subclass = None
    superclass = SimpleLiteral
    def __init__(self, lang=None, valueOf_=None):
        super(RFC4646, self).__init__(lang, valueOf_, )
        self.lang = _cast(None, lang)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if RFC4646.subclass:
            return RFC4646.subclass(*args_, **kwargs_)
        else:
            return RFC4646(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_lang(self): return self.lang
    def set_lang(self, lang): self.lang = lang
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='RFC4646', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='RFC4646')
        outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        outfile.write(' xsi:type="RFC4646"')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='RFC4646'):
        super(RFC4646, self).exportAttributes(outfile, level, already_processed, namespace_, name_='RFC4646')
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            outfile.write(' lang=%s' % (self.gds_format_string(quote_attrib(self.lang).encode(ExternalEncoding), input_name='lang'), ))
    def exportChildren(self, outfile, level, namespace_='cml:', name_='RFC4646'):
        super(RFC4646, self).exportChildren(outfile, level, namespace_, name_)
        pass
    def hasContent_(self):
        if (
            self.valueOf_ or
            super(RFC4646, self).hasContent_()
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='RFC4646'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            showIndent(outfile, level)
            outfile.write('lang = "%s",\n' % (self.lang,))
        super(RFC4646, self).exportLiteralAttributes(outfile, level, already_processed, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        super(RFC4646, self).exportLiteralChildren(outfile, level, name_)
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('lang')
        if value is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            self.lang = value
        super(RFC4646, self).buildAttributes(node, attrs, already_processed)
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        super(RFC4646, self).buildChildren(child_, node, nodeName_, True)
        pass
# end class RFC4646


class RFC3066(SimpleLiteral):
    subclass = None
    superclass = SimpleLiteral
    def __init__(self, lang=None, valueOf_=None):
        super(RFC3066, self).__init__(lang, valueOf_, )
        self.lang = _cast(None, lang)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if RFC3066.subclass:
            return RFC3066.subclass(*args_, **kwargs_)
        else:
            return RFC3066(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_lang(self): return self.lang
    def set_lang(self, lang): self.lang = lang
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='RFC3066', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='RFC3066')
        outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        outfile.write(' xsi:type="RFC3066"')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='RFC3066'):
        super(RFC3066, self).exportAttributes(outfile, level, already_processed, namespace_, name_='RFC3066')
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            outfile.write(' lang=%s' % (self.gds_format_string(quote_attrib(self.lang).encode(ExternalEncoding), input_name='lang'), ))
    def exportChildren(self, outfile, level, namespace_='cml:', name_='RFC3066'):
        super(RFC3066, self).exportChildren(outfile, level, namespace_, name_)
        pass
    def hasContent_(self):
        if (
            self.valueOf_ or
            super(RFC3066, self).hasContent_()
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='RFC3066'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            showIndent(outfile, level)
            outfile.write('lang = "%s",\n' % (self.lang,))
        super(RFC3066, self).exportLiteralAttributes(outfile, level, already_processed, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        super(RFC3066, self).exportLiteralChildren(outfile, level, name_)
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('lang')
        if value is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            self.lang = value
        super(RFC3066, self).buildAttributes(node, attrs, already_processed)
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        super(RFC3066, self).buildChildren(child_, node, nodeName_, True)
        pass
# end class RFC3066


class RFC1766(SimpleLiteral):
    subclass = None
    superclass = SimpleLiteral
    def __init__(self, lang=None, valueOf_=None):
        super(RFC1766, self).__init__(lang, valueOf_, )
        self.lang = _cast(None, lang)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if RFC1766.subclass:
            return RFC1766.subclass(*args_, **kwargs_)
        else:
            return RFC1766(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_lang(self): return self.lang
    def set_lang(self, lang): self.lang = lang
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='RFC1766', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='RFC1766')
        outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        outfile.write(' xsi:type="RFC1766"')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='RFC1766'):
        super(RFC1766, self).exportAttributes(outfile, level, already_processed, namespace_, name_='RFC1766')
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            outfile.write(' lang=%s' % (self.gds_format_string(quote_attrib(self.lang).encode(ExternalEncoding), input_name='lang'), ))
    def exportChildren(self, outfile, level, namespace_='cml:', name_='RFC1766'):
        super(RFC1766, self).exportChildren(outfile, level, namespace_, name_)
        pass
    def hasContent_(self):
        if (
            self.valueOf_ or
            super(RFC1766, self).hasContent_()
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='RFC1766'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            showIndent(outfile, level)
            outfile.write('lang = "%s",\n' % (self.lang,))
        super(RFC1766, self).exportLiteralAttributes(outfile, level, already_processed, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        super(RFC1766, self).exportLiteralChildren(outfile, level, name_)
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('lang')
        if value is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            self.lang = value
        super(RFC1766, self).buildAttributes(node, attrs, already_processed)
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        super(RFC1766, self).buildChildren(child_, node, nodeName_, True)
        pass
# end class RFC1766


class ISO639_3(SimpleLiteral):
    subclass = None
    superclass = SimpleLiteral
    def __init__(self, lang=None, valueOf_=None):
        super(ISO639_3, self).__init__(lang, valueOf_, )
        self.lang = _cast(None, lang)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if ISO639_3.subclass:
            return ISO639_3.subclass(*args_, **kwargs_)
        else:
            return ISO639_3(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_lang(self): return self.lang
    def set_lang(self, lang): self.lang = lang
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='ISO639-3', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='ISO639-3')
        outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        outfile.write(' xsi:type="ISO639-3"')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='ISO639-3'):
        super(ISO639_3, self).exportAttributes(outfile, level, already_processed, namespace_, name_='ISO639-3')
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            outfile.write(' lang=%s' % (self.gds_format_string(quote_attrib(self.lang).encode(ExternalEncoding), input_name='lang'), ))
    def exportChildren(self, outfile, level, namespace_='cml:', name_='ISO639-3'):
        super(ISO639_3, self).exportChildren(outfile, level, namespace_, name_)
        pass
    def hasContent_(self):
        if (
            self.valueOf_ or
            super(ISO639_3, self).hasContent_()
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='ISO639-3'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            showIndent(outfile, level)
            outfile.write('lang = "%s",\n' % (self.lang,))
        super(ISO639_3, self).exportLiteralAttributes(outfile, level, already_processed, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        super(ISO639_3, self).exportLiteralChildren(outfile, level, name_)
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('lang')
        if value is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            self.lang = value
        super(ISO639_3, self).buildAttributes(node, attrs, already_processed)
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        super(ISO639_3, self).buildChildren(child_, node, nodeName_, True)
        pass
# end class ISO639_3


class ISO639_2(SimpleLiteral):
    subclass = None
    superclass = SimpleLiteral
    def __init__(self, lang=None, valueOf_=None):
        super(ISO639_2, self).__init__(lang, valueOf_, )
        self.lang = _cast(None, lang)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if ISO639_2.subclass:
            return ISO639_2.subclass(*args_, **kwargs_)
        else:
            return ISO639_2(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_lang(self): return self.lang
    def set_lang(self, lang): self.lang = lang
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='ISO639-2', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='ISO639-2')
        outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        outfile.write(' xsi:type="ISO639-2"')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='ISO639-2'):
        super(ISO639_2, self).exportAttributes(outfile, level, already_processed, namespace_, name_='ISO639-2')
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            outfile.write(' lang=%s' % (self.gds_format_string(quote_attrib(self.lang).encode(ExternalEncoding), input_name='lang'), ))
    def exportChildren(self, outfile, level, namespace_='cml:', name_='ISO639-2'):
        super(ISO639_2, self).exportChildren(outfile, level, namespace_, name_)
        pass
    def hasContent_(self):
        if (
            self.valueOf_ or
            super(ISO639_2, self).hasContent_()
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='ISO639-2'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            showIndent(outfile, level)
            outfile.write('lang = "%s",\n' % (self.lang,))
        super(ISO639_2, self).exportLiteralAttributes(outfile, level, already_processed, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        super(ISO639_2, self).exportLiteralChildren(outfile, level, name_)
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('lang')
        if value is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            self.lang = value
        super(ISO639_2, self).buildAttributes(node, attrs, already_processed)
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        super(ISO639_2, self).buildChildren(child_, node, nodeName_, True)
        pass
# end class ISO639_2


class URI(SimpleLiteral):
    subclass = None
    superclass = SimpleLiteral
    def __init__(self, lang=None, valueOf_=None):
        super(URI, self).__init__(lang, valueOf_, )
        self.lang = _cast(None, lang)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if URI.subclass:
            return URI.subclass(*args_, **kwargs_)
        else:
            return URI(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_lang(self): return self.lang
    def set_lang(self, lang): self.lang = lang
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='URI', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='URI')
        outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        outfile.write(' xsi:type="URI"')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='URI'):
        super(URI, self).exportAttributes(outfile, level, already_processed, namespace_, name_='URI')
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            outfile.write(' lang=%s' % (self.gds_format_string(quote_attrib(self.lang).encode(ExternalEncoding), input_name='lang'), ))
    def exportChildren(self, outfile, level, namespace_='cml:', name_='URI'):
        super(URI, self).exportChildren(outfile, level, namespace_, name_)
        pass
    def hasContent_(self):
        if (
            self.valueOf_ or
            super(URI, self).hasContent_()
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='URI'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            showIndent(outfile, level)
            outfile.write('lang = "%s",\n' % (self.lang,))
        super(URI, self).exportLiteralAttributes(outfile, level, already_processed, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        super(URI, self).exportLiteralChildren(outfile, level, name_)
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('lang')
        if value is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            self.lang = value
        super(URI, self).buildAttributes(node, attrs, already_processed)
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        super(URI, self).buildChildren(child_, node, nodeName_, True)
        pass
# end class URI


class IMT(SimpleLiteral):
    subclass = None
    superclass = SimpleLiteral
    def __init__(self, lang=None, valueOf_=None):
        super(IMT, self).__init__(lang, valueOf_, )
        self.lang = _cast(None, lang)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if IMT.subclass:
            return IMT.subclass(*args_, **kwargs_)
        else:
            return IMT(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_lang(self): return self.lang
    def set_lang(self, lang): self.lang = lang
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='IMT', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='IMT')
        outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        outfile.write(' xsi:type="IMT"')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='IMT'):
        super(IMT, self).exportAttributes(outfile, level, already_processed, namespace_, name_='IMT')
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            outfile.write(' lang=%s' % (self.gds_format_string(quote_attrib(self.lang).encode(ExternalEncoding), input_name='lang'), ))
    def exportChildren(self, outfile, level, namespace_='cml:', name_='IMT'):
        super(IMT, self).exportChildren(outfile, level, namespace_, name_)
        pass
    def hasContent_(self):
        if (
            self.valueOf_ or
            super(IMT, self).hasContent_()
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='IMT'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            showIndent(outfile, level)
            outfile.write('lang = "%s",\n' % (self.lang,))
        super(IMT, self).exportLiteralAttributes(outfile, level, already_processed, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        super(IMT, self).exportLiteralChildren(outfile, level, name_)
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('lang')
        if value is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            self.lang = value
        super(IMT, self).buildAttributes(node, attrs, already_processed)
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        super(IMT, self).buildChildren(child_, node, nodeName_, True)
        pass
# end class IMT


class DCMIType(SimpleLiteral):
    subclass = None
    superclass = SimpleLiteral
    def __init__(self, lang=None, valueOf_=None):
        super(DCMIType, self).__init__(lang, valueOf_, )
        self.lang = _cast(None, lang)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if DCMIType.subclass:
            return DCMIType.subclass(*args_, **kwargs_)
        else:
            return DCMIType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_lang(self): return self.lang
    def set_lang(self, lang): self.lang = lang
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='DCMIType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='DCMIType')
        outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        outfile.write(' xsi:type="DCMIType"')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='DCMIType'):
        super(DCMIType, self).exportAttributes(outfile, level, already_processed, namespace_, name_='DCMIType')
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            outfile.write(' lang=%s' % (self.gds_format_string(quote_attrib(self.lang).encode(ExternalEncoding), input_name='lang'), ))
    def exportChildren(self, outfile, level, namespace_='cml:', name_='DCMIType'):
        super(DCMIType, self).exportChildren(outfile, level, namespace_, name_)
        pass
    def hasContent_(self):
        if (
            self.valueOf_ or
            super(DCMIType, self).hasContent_()
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='DCMIType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            showIndent(outfile, level)
            outfile.write('lang = "%s",\n' % (self.lang,))
        super(DCMIType, self).exportLiteralAttributes(outfile, level, already_processed, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        super(DCMIType, self).exportLiteralChildren(outfile, level, name_)
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('lang')
        if value is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            self.lang = value
        super(DCMIType, self).buildAttributes(node, attrs, already_processed)
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        super(DCMIType, self).buildChildren(child_, node, nodeName_, True)
        pass
# end class DCMIType


class W3CDTF(SimpleLiteral):
    subclass = None
    superclass = SimpleLiteral
    def __init__(self, lang=None, valueOf_=None):
        super(W3CDTF, self).__init__(lang, valueOf_, )
        self.lang = _cast(None, lang)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if W3CDTF.subclass:
            return W3CDTF.subclass(*args_, **kwargs_)
        else:
            return W3CDTF(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_lang(self): return self.lang
    def set_lang(self, lang): self.lang = lang
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='W3CDTF', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='W3CDTF')
        outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        outfile.write(' xsi:type="W3CDTF"')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='W3CDTF'):
        super(W3CDTF, self).exportAttributes(outfile, level, already_processed, namespace_, name_='W3CDTF')
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            outfile.write(' lang=%s' % (self.gds_format_string(quote_attrib(self.lang).encode(ExternalEncoding), input_name='lang'), ))
    def exportChildren(self, outfile, level, namespace_='cml:', name_='W3CDTF'):
        super(W3CDTF, self).exportChildren(outfile, level, namespace_, name_)
        pass
    def hasContent_(self):
        if (
            self.valueOf_ or
            super(W3CDTF, self).hasContent_()
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='W3CDTF'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            showIndent(outfile, level)
            outfile.write('lang = "%s",\n' % (self.lang,))
        super(W3CDTF, self).exportLiteralAttributes(outfile, level, already_processed, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        super(W3CDTF, self).exportLiteralChildren(outfile, level, name_)
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('lang')
        if value is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            self.lang = value
        super(W3CDTF, self).buildAttributes(node, attrs, already_processed)
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        super(W3CDTF, self).buildChildren(child_, node, nodeName_, True)
        pass
# end class W3CDTF


class Period(SimpleLiteral):
    subclass = None
    superclass = SimpleLiteral
    def __init__(self, lang=None, valueOf_=None):
        super(Period, self).__init__(lang, valueOf_, )
        self.lang = _cast(None, lang)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if Period.subclass:
            return Period.subclass(*args_, **kwargs_)
        else:
            return Period(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_lang(self): return self.lang
    def set_lang(self, lang): self.lang = lang
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='Period', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='Period')
        outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        outfile.write(' xsi:type="Period"')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='Period'):
        super(Period, self).exportAttributes(outfile, level, already_processed, namespace_, name_='Period')
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            outfile.write(' lang=%s' % (self.gds_format_string(quote_attrib(self.lang).encode(ExternalEncoding), input_name='lang'), ))
    def exportChildren(self, outfile, level, namespace_='cml:', name_='Period'):
        super(Period, self).exportChildren(outfile, level, namespace_, name_)
        pass
    def hasContent_(self):
        if (
            self.valueOf_ or
            super(Period, self).hasContent_()
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='Period'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            showIndent(outfile, level)
            outfile.write('lang = "%s",\n' % (self.lang,))
        super(Period, self).exportLiteralAttributes(outfile, level, already_processed, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        super(Period, self).exportLiteralChildren(outfile, level, name_)
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('lang')
        if value is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            self.lang = value
        super(Period, self).buildAttributes(node, attrs, already_processed)
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        super(Period, self).buildChildren(child_, node, nodeName_, True)
        pass
# end class Period


class UDC(SimpleLiteral):
    subclass = None
    superclass = SimpleLiteral
    def __init__(self, lang=None, valueOf_=None):
        super(UDC, self).__init__(lang, valueOf_, )
        self.lang = _cast(None, lang)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if UDC.subclass:
            return UDC.subclass(*args_, **kwargs_)
        else:
            return UDC(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_lang(self): return self.lang
    def set_lang(self, lang): self.lang = lang
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='UDC', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='UDC')
        outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        outfile.write(' xsi:type="UDC"')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='UDC'):
        super(UDC, self).exportAttributes(outfile, level, already_processed, namespace_, name_='UDC')
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            outfile.write(' lang=%s' % (self.gds_format_string(quote_attrib(self.lang).encode(ExternalEncoding), input_name='lang'), ))
    def exportChildren(self, outfile, level, namespace_='cml:', name_='UDC'):
        super(UDC, self).exportChildren(outfile, level, namespace_, name_)
        pass
    def hasContent_(self):
        if (
            self.valueOf_ or
            super(UDC, self).hasContent_()
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='UDC'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            showIndent(outfile, level)
            outfile.write('lang = "%s",\n' % (self.lang,))
        super(UDC, self).exportLiteralAttributes(outfile, level, already_processed, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        super(UDC, self).exportLiteralChildren(outfile, level, name_)
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('lang')
        if value is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            self.lang = value
        super(UDC, self).buildAttributes(node, attrs, already_processed)
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        super(UDC, self).buildChildren(child_, node, nodeName_, True)
        pass
# end class UDC


class LCC(SimpleLiteral):
    subclass = None
    superclass = SimpleLiteral
    def __init__(self, lang=None, valueOf_=None):
        super(LCC, self).__init__(lang, valueOf_, )
        self.lang = _cast(None, lang)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if LCC.subclass:
            return LCC.subclass(*args_, **kwargs_)
        else:
            return LCC(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_lang(self): return self.lang
    def set_lang(self, lang): self.lang = lang
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='LCC', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='LCC')
        outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        outfile.write(' xsi:type="LCC"')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='LCC'):
        super(LCC, self).exportAttributes(outfile, level, already_processed, namespace_, name_='LCC')
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            outfile.write(' lang=%s' % (self.gds_format_string(quote_attrib(self.lang).encode(ExternalEncoding), input_name='lang'), ))
    def exportChildren(self, outfile, level, namespace_='cml:', name_='LCC'):
        super(LCC, self).exportChildren(outfile, level, namespace_, name_)
        pass
    def hasContent_(self):
        if (
            self.valueOf_ or
            super(LCC, self).hasContent_()
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='LCC'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            showIndent(outfile, level)
            outfile.write('lang = "%s",\n' % (self.lang,))
        super(LCC, self).exportLiteralAttributes(outfile, level, already_processed, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        super(LCC, self).exportLiteralChildren(outfile, level, name_)
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('lang')
        if value is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            self.lang = value
        super(LCC, self).buildAttributes(node, attrs, already_processed)
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        super(LCC, self).buildChildren(child_, node, nodeName_, True)
        pass
# end class LCC


class DDC(SimpleLiteral):
    subclass = None
    superclass = SimpleLiteral
    def __init__(self, lang=None, valueOf_=None):
        super(DDC, self).__init__(lang, valueOf_, )
        self.lang = _cast(None, lang)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if DDC.subclass:
            return DDC.subclass(*args_, **kwargs_)
        else:
            return DDC(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_lang(self): return self.lang
    def set_lang(self, lang): self.lang = lang
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='DDC', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='DDC')
        outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        outfile.write(' xsi:type="DDC"')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='DDC'):
        super(DDC, self).exportAttributes(outfile, level, already_processed, namespace_, name_='DDC')
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            outfile.write(' lang=%s' % (self.gds_format_string(quote_attrib(self.lang).encode(ExternalEncoding), input_name='lang'), ))
    def exportChildren(self, outfile, level, namespace_='cml:', name_='DDC'):
        super(DDC, self).exportChildren(outfile, level, namespace_, name_)
        pass
    def hasContent_(self):
        if (
            self.valueOf_ or
            super(DDC, self).hasContent_()
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='DDC'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            showIndent(outfile, level)
            outfile.write('lang = "%s",\n' % (self.lang,))
        super(DDC, self).exportLiteralAttributes(outfile, level, already_processed, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        super(DDC, self).exportLiteralChildren(outfile, level, name_)
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('lang')
        if value is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            self.lang = value
        super(DDC, self).buildAttributes(node, attrs, already_processed)
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        super(DDC, self).buildChildren(child_, node, nodeName_, True)
        pass
# end class DDC


class MESH(SimpleLiteral):
    subclass = None
    superclass = SimpleLiteral
    def __init__(self, lang=None, valueOf_=None):
        super(MESH, self).__init__(lang, valueOf_, )
        self.lang = _cast(None, lang)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if MESH.subclass:
            return MESH.subclass(*args_, **kwargs_)
        else:
            return MESH(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_lang(self): return self.lang
    def set_lang(self, lang): self.lang = lang
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='MESH', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='MESH')
        outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        outfile.write(' xsi:type="MESH"')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='MESH'):
        super(MESH, self).exportAttributes(outfile, level, already_processed, namespace_, name_='MESH')
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            outfile.write(' lang=%s' % (self.gds_format_string(quote_attrib(self.lang).encode(ExternalEncoding), input_name='lang'), ))
    def exportChildren(self, outfile, level, namespace_='cml:', name_='MESH'):
        super(MESH, self).exportChildren(outfile, level, namespace_, name_)
        pass
    def hasContent_(self):
        if (
            self.valueOf_ or
            super(MESH, self).hasContent_()
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='MESH'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            showIndent(outfile, level)
            outfile.write('lang = "%s",\n' % (self.lang,))
        super(MESH, self).exportLiteralAttributes(outfile, level, already_processed, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        super(MESH, self).exportLiteralChildren(outfile, level, name_)
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('lang')
        if value is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            self.lang = value
        super(MESH, self).buildAttributes(node, attrs, already_processed)
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        super(MESH, self).buildChildren(child_, node, nodeName_, True)
        pass
# end class MESH


class LCSH(SimpleLiteral):
    subclass = None
    superclass = SimpleLiteral
    def __init__(self, lang=None, valueOf_=None):
        super(LCSH, self).__init__(lang, valueOf_, )
        self.lang = _cast(None, lang)
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if LCSH.subclass:
            return LCSH.subclass(*args_, **kwargs_)
        else:
            return LCSH(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_lang(self): return self.lang
    def set_lang(self, lang): self.lang = lang
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def export(self, outfile, level, namespace_='cml:', name_='LCSH', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        self.exportAttributes(outfile, level, [], namespace_, name_='LCSH')
        outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        outfile.write(' xsi:type="LCSH"')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.valueOf_)
            self.exportChildren(outfile, level + 1, namespace_, name_)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='cml:', name_='LCSH'):
        super(LCSH, self).exportAttributes(outfile, level, already_processed, namespace_, name_='LCSH')
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            outfile.write(' lang=%s' % (self.gds_format_string(quote_attrib(self.lang).encode(ExternalEncoding), input_name='lang'), ))
    def exportChildren(self, outfile, level, namespace_='cml:', name_='LCSH'):
        super(LCSH, self).exportChildren(outfile, level, namespace_, name_)
        pass
    def hasContent_(self):
        if (
            self.valueOf_ or
            super(LCSH, self).hasContent_()
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='LCSH'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
        showIndent(outfile, level)
        outfile.write('valueOf_ = """%s""",\n' % (self.valueOf_,))
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.lang is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            showIndent(outfile, level)
            outfile.write('lang = "%s",\n' % (self.lang,))
        super(LCSH, self).exportLiteralAttributes(outfile, level, already_processed, name_)
    def exportLiteralChildren(self, outfile, level, name_):
        super(LCSH, self).exportLiteralChildren(outfile, level, name_)
        pass
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = attrs.get('lang')
        if value is not None and 'lang' not in already_processed:
            already_processed.append('lang')
            self.lang = value
        super(LCSH, self).buildAttributes(node, attrs, already_processed)
    def buildChildren(self, child_, node, nodeName_, from_subclass=False):
        super(LCSH, self).buildChildren(child_, node, nodeName_, True)
        pass
# end class LCSH


USAGE_TEXT = """
Usage: python <Parser>.py [ -s ] <in_xml_file>
"""

def usage():
    print(USAGE_TEXT)
    sys.exit(1)


def get_root_tag(node):
    tag = Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = globals().get(tag)
    return tag, rootClass


def parse(inFileName):
    doc = parsexml_(inFileName)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'property'
        rootClass = property
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0, name_=rootTag, 
        namespacedef_='xmlns:cml="http://www.connectomics.org/cff-2" xmlns:dcterms="http://purl.org/dc/terms/"')
    return rootObj


def parseString(inString):
    from io import StringIO
    doc = parsexml_(StringIO(str(inString)))
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'property'
        rootClass = property
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0, name_="property",
        namespacedef_='xmlns:cml="http://www.connectomics.org/cff-2" xmlns:dcterms="http://purl.org/dc/terms/"')
    return rootObj


def parseLiteral(inFileName):
    doc = parsexml_(inFileName)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'property'
        rootClass = property
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('#from cff import *\n\n')
    sys.stdout.write('import cff as model_\n\n')
    sys.stdout.write('rootObj = model_.rootTag(\n')
    rootObj.exportLiteral(sys.stdout, 0, name_=rootTag)
    sys.stdout.write(')\n')
    return rootObj


def main():
    args = sys.argv[1:]
    if len(args) == 1:
        parse(args[0])
    else:
        usage()


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()


__all__ = [
    "Box",
    "CData",
    "CImagestack",
    "CMetadata",
    "CNetwork",
    "CScript",
    "CSurface",
    "CTimeseries",
    "CTrack",
    "CVolume",
    "DCMIType",
    "DDC",
    "IMT",
    "ISO3166",
    "ISO639_2",
    "ISO639_3",
    "LCC",
    "LCSH",
    "MESH",
    "Period",
    "Point",
    "RFC1766",
    "RFC3066",
    "RFC4646",
    "SimpleLiteral",
    "TGN",
    "UDC",
    "URI",
    "W3CDTF",
    "abstract",
    "accessRights",
    "accrualMethod",
    "accrualPeriodicity",
    "accrualPolicy",
    "alternative",
    "audience",
    "available",
    "bibliographicCitation",
    "conformsTo",
    "connectome",
    "contributor",
    "coverage",
    "created",
    "creator",
    "date",
    "dateAccepted",
    "dateCopyrighted",
    "dateSubmitted",
    "description",
    "educationLevel",
    "elementContainer",
    "elementOrRefinementContainer",
    "extent",
    "format",
    "hasFormat",
    "hasPart",
    "hasVersion",
    "identifier",
    "instructionalMethod",
    "isFormatOf",
    "isPartOf",
    "isReferencedBy",
    "isReplacedBy",
    "isRequiredBy",
    "isVersionOf",
    "issued",
    "language",
    "license",
    "mediator",
    "medium",
    "metadata",
    "modified",
    "property",
    "provenance",
    "publisher",
    "references",
    "relation",
    "replaces",
    "requires",
    "rights",
    "rightsHolder",
    "section",
    "source",
    "spatial",
    "subject",
    "tableOfContents",
    "tag",
    "temporal",
    "title",
    "type_",
    "valid"
    ]
