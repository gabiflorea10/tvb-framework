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

from . import cfflib2 as cf

import os.path as op
from zipfile import ZipFile, ZIP_DEFLATED

def load(filename):
    """ Load a connectome file either from meta.cml (default)
    or from a zipped .cff file
    
    Parameter
    ---------
    filename : string
        File to load, either a connectome markup file with ending .cml
        or a zipped connectome file with ending .cff
        
    Notes
    -----
    By the file name ending, the appropriate load function is selected.
    They can be either .cml or .cff for unzipped or zipped connectome
    files respectively.
    """

    if isinstance(filename, str):
        # check if file exists
        from os.path import isfile, abspath
        
        if isfile(filename):
            if filename.endswith('.cff'):
                fname = abspath(filename)
                return _load_from_cff(fname)
            elif filename.endswith('.cml'):
                fname = abspath(filename)
                return _load_from_meta_cml(fname)
            else:
                raise RuntimeError('%s must end with either .cml or .cff' % filename)       
        else:
            raise RuntimeError('%s seems not to be a valid file string' % filename)
    else:
        raise RuntimeError('%s seems not to be a valid file string' % filename)


def _load_from_meta_cml(filename):
    """ Load connectome file from a meta.cml file. """
    
    with open(filename, 'r') as metacml:
        metastr = metacml.read()
        
    connectome = cf.parseString(metastr)
    # update references
    connectome._update_parent_reference()
    connectome.iszip = False
    connectome.fname = op.abspath(filename)
    # check if names are unique!
    connectome.check_names_unique()
    
    return connectome

def _load_from_url(url, to_filename):
    """ First downloads the connectome file to a file to_filename
    load it and return the reference to the connectome object
    
    Not tested.
    """
    
    from .util import download    
    download(url, to_filename)
    return _load_from_cff(to_filename)
    
    
def _load_from_cff(filename, *args, **kwargs):
    """ Load connectome file given filename
    
        Returns
        -------
        connectome : ``Connectome``
                Connectome Instance
                
    """
    
    # XXX: take care to have allowZip64 = True (but not supported by unix zip/unzip, same for ubuntu?) ?
    _zipfile = ZipFile(filename, 'a', ZIP_DEFLATED)
    try:
        metadata_string = _zipfile.read('meta.cml')
        metadata_string = metadata_string.decode('UTF-8')
    except: # XXX: what is the correct exception for read error?
        raise RuntimeError('Can not extract meta.cml from connectome file.')
    
    # create connectome instance
    connectome = cf.parseString(metadata_string)
    
    # update references
    connectome._update_parent_reference()
    
    # add additional attributes
    connectome.src = filename
    
    # it is from the zip file
    connectome.iszip = True
    # if it is a zip file, we can assume that the src paths are given relatively
    
    connectome._zipfile = _zipfile
    
    # check if all referenced container elements exist in the archive
    connectome.check_file_in_cff()
    
    # check if names are unique!
    connectome.check_names_unique()
    
    return connectome

def save_to_meta_cml(connectome, filename = 'meta.cml'):
    """ Stores a Connectome Markup File to filename """
    if connectome.get_connectome_meta() == None:
        print("ERROR - there is no connectome metadata in this connectome")
        return
    elif connectome.get_connectome_meta().title == None or connectome.get_connectome_meta().title == '':
        print("ERROR - the connectome metadata have to contain a unique title")
        return
    f = open(filename, 'w')
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    connectome.export(f, 0, namespacedef_='xmlns="http://www.connectomics.org/cff-2" xmlns:cml="http://www.connectomics.org/cff-2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:dcterms="http://purl.org/dc/terms/" xsi:schemaLocation="http://www.connectomics.org/cff-2 connectome.xsd"')
    f.close()


def save_to_cff(connectome, filename):
    """ Save connectome file to new .cff file on disk """
    if connectome.get_connectome_meta() == None:
        print("ERROR - there is no connectome metadata in this connectome")
        return
    elif connectome.get_connectome_meta().title == None or connectome.get_connectome_meta().title == '':
        print("ERROR - the connectome metadata have to contain a unique title")
        return
    
    _newzip = ZipFile(filename, 'w', ZIP_DEFLATED, allowZip64 = True)
    
    allcobj = connectome.get_all()
    
    # tmpdir
    import tempfile
    import os
    tmpdir = tempfile.gettempdir()
    
    # check if names are unique!
    connectome.check_names_unique()

    for ele in allcobj:
        print("----")
        print("Storing element: ", str(ele))
        
        # discover the relative path to use for the save
        if hasattr(ele, 'src'):
            if ele.src == '':
                wt = ele.get_unique_relpath()
                print("Created a unique path for element %s: %s" % (str(ele), wt))
            else:
                wt = ele.src
                print("Used .src attribute for relative path: %s" % wt)
        else:            
            ele.src = ele.get_unique_relpath()
            wt = ele.src
            print("Element has no .src attribute. Create it and set it to %s" % ele.src)
        
        if not hasattr(ele, 'data'):
            if connectome.iszip:
                # extract zip content and add it to new zipfile
                if not wt in connectome._zipfile.namelist():
                    msg = """There exists no file %s in the connectome file you want to save to
                    "Please create .data and set the attributes right
                    "according to the documentation"""
                    raise Exception(msg)
                else:
                    ftmp = connectome._zipfile.extract(wt)
            else:
                if not hasattr(connectome, 'fname'):
                    connectome.fname = op.abspath(filename)
                
                if hasattr(ele, 'tmpsrc'):
                    try:
                        ele.save()
                    except:
                        pass
                    ftmp = ele.tmpsrc
                else:
                    # save the element
                    try:
                        ele.save()
                    except:
                        # e.g. there is nothing to save exception
                        ftmp = op.join(op.dirname(connectome.fname), wt)
                
                if not op.exists(ftmp):
                    msg = """There exists no file %s for element %s. 
                    "Cannot save connectome file. Please update the element or bug report if it should work.""" % (ftmp, str(ele))
                    raise Exception(msg)
            
            _newzip.write(ftmp, wt)
            
        else:
            
            # save content to a temporary file according to the objects specs
            ele.save()
            
            # get the path
            ftmp = ele.tmpsrc
            
            _newzip.write(ftmp, wt)
        
        if connectome.iszip:
            # remove file
            os.remove(ftmp)
        
        # update ele.src
        ele.src = wt
  
    # export and store meta.cml
    mpth = op.join(tmpdir, 'meta.cml')
    f = open(mpth, 'w')
    f.write(connectome.to_xml())
    f.close()
    
    _newzip.write(mpth, 'meta.cml')
    os.remove(mpth)
    
    _newzip.close()
    
    print("New connectome file written to %s " % op.abspath(filename))
    
