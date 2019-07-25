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
