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

from zipfile import ZipFile, ZIP_DEFLATED
from glob import glob
import os.path as op
import os
import json
import pickle

# NumPy
try:
    import numpy as np
except ImportError:
    raise ImportError("Failed to import numpy from any known place")

# Nibabel
try:
    import nibabel as ni
except ImportError:
    raise ImportError("Failed to import nibabel from any known place")

# NetworkX
try:
    import networkx as nx
except ImportError:
    pass
    #raise ImportError("Failed to import networkx from any known place")

# PyTables
try:
    import tables
except ImportError:
    pass
    #raise ImportError("Failed to import pytables from any known place")

class NotSupportedFormat(Exception):
    def __init__(self, fileformat, objtype):
        self.fileformat = fileformat
        self.objtype = objtype
    def __str__(self):
        return "Loading %s:\nFile format '%s' not supported by cfflib. Use your custom loader." % (self.objtype, self.fileformat)

def save_data(obj):

    objrep = str(type(obj))

    if hasattr(obj, 'data'):

        # it appears that there is no remove function for zip archives implemented to date
        # http://bugs.python.org/issue6818

        # the file was loaded, thus it exists a .tmpsrc pointing to
        # its absolute path. Use this path to overwrite the file by the
        # current .data data
        if hasattr(obj, 'tmpsrc'):
            tmpfname = obj.tmpsrc
        else:
            # if it has no .tmpsrc, i.e. it is not loaded from a file path
            # but it has a .data set
            raise Exception('Element %s cannot be saved. (It was never loaded)' % str(obj))

        dname = op.dirname(tmpfname)
        if not op.exists(dname):
            os.makedirs()

        if 'CVolume' in objrep:
            ni.save(obj.data, tmpfname)
        elif 'CNetwork' in objrep:
            if obj.fileformat == "GraphML":
                # write graph to temporary file
                nx.write_graphml(obj.data, tmpfname)
            elif obj.fileformat == "GEXF":
                nx.write_gexf(obj.data, tmpfname)
            elif obj.fileformat == "NXGPickle":
                nx.write_gpickle(obj.data, tmpfname)
            else:
                raise NotSupportedFormat("Other", str(obj))

        elif 'CSurface' in objrep:
            if obj.fileformat == "Gifti":
                import nibabel.gifti as nig
                nig.write(obj.data, tmpfname)
            else:
                raise NotSupportedFormat("Other", str(obj))

        elif 'CTrack' in objrep:
            if obj.fileformat == "TrackVis":
                ni.trackvis.write(tmpfname, obj.data[0], obj.data[1])
            else:
                raise NotSupportedFormat("Other", str(obj))

        elif 'CTimeserie' in objrep:
            if obj.fileformat == "HDF5":
                # flush the data of the buffers
                obj.data.flush()
                # close the file
                obj.data.close()
            elif obj.fileformat == "NumPy":
                load = np.save(tmpfname, obj.data)
            else:
                raise NotSupportedFormat("Other", str(obj))

        elif 'CData' in objrep:

            if obj.fileformat == "NumPy":
                load = np.save(tmpfname, obj.data)
            elif obj.fileformat == "HDF5":
                # flush the data of the buffers
                obj.data.flush()
                # close the file
                obj.data.close()
            elif obj.fileformat == "XML":
                f = open(tmpfname, 'w')
                f.write(obj.data)
                f.close()
            elif obj.fileformat == "JSON":
                f = open(tmpfname, 'w')
                json.dump(obj.data, f)
                f.close()
            elif obj.fileformat == "Pickle":
                f = open(tmpfname, 'w')
                pickle.dump(obj.data, f)
                f.close()
            elif obj.fileformat == "CSV" or obj.fileformat == "TXT":
                # write as text
                f = open(tmpfname, 'w')
                f.write(obj.data)
                f.close()
            else:
                raise NotSupportedFormat("Other", str(obj))

        elif 'CScript' in objrep:
                f = open(tmpfname, 'w')
                f.write(obj.data)
                f.close()

        return tmpfname

    else:
        # assumes the .src paths are given relative to the meta.cml
        # valid for iszip = True and iszip = False
        # either path to the .cff or to the meta.cml
        # return op.join(op.dirname(obj.parent_cfile.fname), obj.src)
        return ''

    
def load_data(obj):
        
    objrep = str(type(obj))
    if 'CVolume' in objrep:
        load = ni.load
    elif 'CNetwork' in objrep:
        if obj.fileformat == "GraphML":
            load = nx.read_graphml
        elif obj.fileformat == "GEXF":
            # works with networkx 1.4
            load = nx.read_gexf
        elif obj.fileformat == "NXGPickle":
            load = nx.read_gpickle
        else:
            raise NotSupportedFormat("Other", str(obj))
        
    elif 'CSurface' in objrep:
        if obj.fileformat == "Gifti":
            import nibabel.gifti as nig
            load = nig.read
        else:
            raise NotSupportedFormat("Other", str(obj))
        
    elif 'CTrack' in objrep:
        if obj.fileformat == "TrackVis":
            load = ni.trackvis.read
        else:
            raise NotSupportedFormat("Other", str(obj))
        
    elif 'CTimeserie' in objrep:
        if obj.fileformat == "HDF5":
            load = tables.openFile
        elif obj.fileformat == "NumPy":
            load = np.load 
        else:
            raise NotSupportedFormat("Other", str(obj))
        
    elif 'CData' in objrep:
        if obj.fileformat == "NumPy":
            load = np.load
        elif obj.fileformat == "HDF5":
            load = tables.openFile
        elif obj.fileformat == "XML":
            load = open
        elif obj.fileformat == "JSON":
            load = json.load
        elif obj.fileformat == "Pickle":
            load = pickle.load
        elif obj.fileformat == "CSV" or obj.fileformat == "TXT":
            # can use import csv on the returned object
            load = open
        else:
            raise NotSupportedFormat("Other", str(obj))
        
    elif 'CScript' in objrep:
        load = open
        
    elif 'CImagestack' in objrep:
        if obj.parent_cfile.iszip:
            _zipfile = ZipFile(obj.parent_cfile.src, 'r', ZIP_DEFLATED)
            try:
                namelist = _zipfile.namelist()
            except: # XXX: what is the correct exception for read error?
                raise RuntimeError('Can not extract %s from connectome file.' % str(obj.src) )
            finally:
                _zipfile.close()
            import fnmatch
            ret = []
            for ele in namelist:
                if fnmatch.fnmatch(ele, op.join(obj.src, obj.pattern)):
                    ret.append(ele)
            return ret
        else:
            # returned list should be absolute path
            if op.isabs(obj.src):
                return sorted(glob(op.join(obj.src, obj.pattern)))
            else:
                path2files = op.join(op.dirname(obj.parent_cfile.fname), obj.src, obj.pattern)
                return sorted(glob(path2files))

    ######
        
    if obj.parent_cfile.iszip:
        
        from tempfile import gettempdir

        # create a meaningful and unique temporary path to extract data files
        tmpdir = op.join(gettempdir(), obj.parent_cfile.get_unique_cff_name())

        # extract src from zipfile to temp
        _zipfile = ZipFile(obj.parent_cfile.src, 'r', ZIP_DEFLATED)
        try:
            exfile = _zipfile.extract(obj.src, tmpdir)
            obj.tmpsrc = exfile
            _zipfile.close()
            retload = load(exfile)
            return retload
        except: # XXX: what is the correct exception for read error?
            raise RuntimeError('Can not extract "%s" from connectome file using path %s. Please extract .cff and load meta.cml directly.' % (str(obj.name), str(obj.src)) )
      
        return None
        
        
    else:
        if hasattr(obj, 'tmpsrc'):
            # we have an absolute path
            obj.tmpsrc = obj.tmpsrc
            retload = load(obj.tmpsrc)
            return retload
        else:
            # otherwise, we need to join the meta.cml path with the current relative path
            path2file = op.join(op.dirname(obj.parent_cfile.fname), obj.src)
            obj.tmpsrc = path2file
            retload = load(path2file)
            return retload

def unify(t, n):
    """ Unify type and name """
    n = n.lower()
    n = n.replace(' ', '_')
    return '%s/%s' % (t, n)
