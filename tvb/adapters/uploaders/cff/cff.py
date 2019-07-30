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
import re as re_

etree_ = None
(   XMLParser_import_none, XMLParser_import_lxml,
    XMLParser_import_elementtree
    ) = list(range(3))
XMLParser_import_library = None
try:
    # lxml
    from lxml import etree as etree_
    XMLParser_import_library = XMLParser_import_lxml
except ImportError:
    try:
        # cElementTree from Python 2.5+
        import xml.etree.cElementTree as etree_
        XMLParser_import_library = XMLParser_import_elementtree
    except ImportError:
        try:
            # ElementTree from Python 2.5+
            import xml.etree.ElementTree as etree_
            XMLParser_import_library = XMLParser_import_elementtree
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree_
                XMLParser_import_library = XMLParser_import_elementtree
            except ImportError:
                try:
                    # normal ElementTree install
                    import elementtree.ElementTree as etree_
                    XMLParser_import_library = XMLParser_import_elementtree
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


def _cast(typ, value):
    if typ is None or value is None:
        return value
    return typ(value)

#
# Data representation classes.
#


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
    def __init__(self, connectome_meta=None, connectome_network=None, connectome_volume=None, connectome_track=None, connectome_timeseries=None, connectome_data=None, connectome_script=None, connectome_imagestack=None):
        self.connectome_meta = connectome_meta
        if connectome_network is None:
            self.connectome_network = []
        else:
            self.connectome_network = connectome_network
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
        elif nodeName_ == 'description':
            description_ = child_.text
            description_ = self.gds_validate_string(description_, node, 'description')
            self.description = description_
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
# end class CNetwork


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
        elif nodeName_ == 'metadata': 
            obj_ = metadata.factory()
            obj_.build(child_)
            self.set_metadata(obj_)
# end class CScript


USAGE_TEXT = """
Usage: python <Parser>.py [ -s ] <in_xml_file>
"""

def usage():
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
    "CData",
    "CMetadata",
    "CNetwork",
    "CScript",
    "CTimeseries",
    "CTrack",
    "CVolume",
    "connectome",
    "metadata",
    "tag"
    ]
