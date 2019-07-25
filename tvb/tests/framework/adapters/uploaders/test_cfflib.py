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


# ================================================================================== #
# TEST functions for the cfflib files
# ================================================================================== #


# ---------------------------------------------------------------------------------- #
from numpy.ma.testutils import assert_not_equal
from numpy.testing import assert_equal
from sklearn.utils.testing import assert_true

from tvb.adapters.uploaders.cff import *
import tempfile
import os.path as op
# ---------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------- #
# Load and store data locations
DATA = op.join(op.dirname(__file__),'data/')
TMP  = tempfile.gettempdir()
# ---------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------- #
# Test the connectome object and the CMetadata
def test_connectome():

    c = connectome()
    
    # Check for the default CMetadata
    assert_not_equal(c.connectome_meta, None)
    assert_equal(c.get_connectome_meta().get_title(), 'newconnectome')
    assert_equal(c.get_connectome_meta().get_generator(), 'cfflib')
    assert_equal(c.get_connectome_meta().get_version(), '2.0')
    
    # Check for the possibility to specify a name to the connectome
    c = connectome('Test connectome')
    assert_equal(c.get_connectome_meta().get_title(), 'Test connectome')
    
    # Check for the content and the CObjects
    assert_equal(c.get_all(), [])
    assert_true(c.hasContent_())
    
    # Check to set the CMetadata attributes
    c.connectome_meta.set_title('My first connectome')
    assert_equal(c.connectome_meta.get_title(), 'My first connectome')
    c.connectome_meta.set_creator('Connectome Tutorial')
    assert_equal(c.connectome_meta.get_creator(), 'Connectome Tutorial')    
    c.connectome_meta.set_publisher('EPFL')
    assert_equal( c.connectome_meta.get_publisher(), 'EPFL')    
    c.connectome_meta.set_created('2010-10-26')
    assert_equal(c.connectome_meta.get_created(), '2010-10-26')    
    c.connectome_meta.set_relation('www.connectome.ch')
    assert_equal(c.connectome_meta.get_relation(), 'www.connectome.ch')
    
    # Check the description in CMetadata
    c.connectome_meta.set_description('First connectome object created with the tutorial.')
    assert_equal(c.connectome_meta.get_description(), 'First connectome object created with the tutorial.')
    
    # Check to remove the CMetadata
    c.connectome_meta = None
# ---------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------- #
# Test the connectome network
# With nxgraph
def test_cnetwork_nxgraph():

    c = connectome()
    
    # Check the default values
    n = CNetwork()
    assert_equal(n.get_name(), 'mynetwork')
    assert_equal(n.get_dtype(), 'AttributeNetwork')
    assert_equal(n.get_fileformat(), 'GraphML')
    assert_equal(n.get_metadata_as_dict(), {})
    
    # Check given values
    n = CNetwork('Test network')
    n.update_metadata({'number':1024})
    assert_equal(n.get_name(), 'Test network')
    assert_true('number' in n.get_metadata_as_dict())
    assert_equal(n.get_metadata_as_dict()['number'], '1024')
    
    g = nx.Graph()
    g.add_node(0)
    g.add_node(1)
    g.add_node(2)
    g.add_edge(0,1)
    g.add_edge(2,1)
    g.add_edge(0,2)
    
    # Check the properties when the network is set with a nxgraph
    n.set_with_nxgraph(g)
    assert_equal(n.get_name(), 'Test network')
    assert_equal(n.get_src(), 'CNetwork/test_network.gpickle')
    assert_equal(n.get_dtype(), 'AttributeNetwork')
    assert_equal(n.get_fileformat(), 'NXGPickle')
    
    # Check the add function to connectome
    c.add_connectome_network(n)
    assert_not_equal(c.get_connectome_network(), [])
    assert_equal(len(c.get_connectome_network()), 1)
    assert_not_equal(c.get_all(), [])
    
    # Check to change the name of the nework directly from the connectome
    c.get_connectome_network()[0].set_name('modif')
    assert_equal(n.get_name(), 'modif')
    
    # Check the 2nd way to add a nxgraph network
    c.add_connectome_network_from_nxgraph('2nd nxgraph', g)
    assert_equal(c.get_connectome_network()[1].get_name(), '2nd nxgraph')

    # Check save/load the CNetwork
    name = n.data.name
    n.data.name = 'test name'
    n.save()
    n.load()
    assert_not_equal(n.data.name, name)
    n.data.name = ''
    n.save()


# With graphml
def test_cnetwork_graphml():

    c = connectome()
    
    # Check the classmethod and default attributes
    n = CNetwork.create_from_graphml('GraphML net', op.join(DATA,'CNetwork/network_res83.graphml'))
    assert_equal(n.get_name(), 'GraphML net')
    assert_equal(n.get_fileformat(), 'GraphML')
    assert_equal(n.get_src(), 'CNetwork/graphml_net.graphml')
    assert_equal(n.get_dtype(), 'AttributeNetwork')
    
    # Check to add to the connectome
    c.add_connectome_network(n)
    assert_not_equal(c.get_connectome_network(), [])
    assert_equal(c.get_connectome_network()[0].get_src(), 'CNetwork/graphml_net.graphml')
    
    # Check to directly add to the connectome
    c.add_connectome_network_from_graphml('2nd graphml', op.join(DATA,'CNetwork/network_res83.graphml'))
    assert_equal(len(c.get_connectome_network()), 2)
    assert_equal(c.get_connectome_network()[1].get_name(), '2nd graphml')

    # Check save/load the CNetwork
    n.load()

# ---------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------- #
# Test the description and metadata
def test_desc_meta():

    c = connectome('desc & meta connectome')
    
    # Check the updated keys and corresponding values
    n = CNetwork()
    n.update_metadata({'m0':'v0', 'm1':'v1', 'm2':121})
    assert_not_equal(n.get_metadata_as_dict(), None)
    assert_true('m0' in n.get_metadata_as_dict())
    assert_true('m1' in n.get_metadata_as_dict())
    assert_true('m2' in n.get_metadata_as_dict())
    assert_equal(n.get_metadata_as_dict()['m0'], 'v0')
    assert_equal(n.get_metadata_as_dict()['m1'], 'v1')
    assert_equal(n.get_metadata_as_dict()['m2'], '121')
    
    # Check the update of an existing key 
    n.update_metadata({'m1':'v2'})
    assert_equal(n.get_metadata_as_dict()['m1'], 'v2')
    
    #  Check the description 
    n.set_description('An useless description...')
    assert_equal(n.get_description(),'An useless description...')
# ---------------------------------------------------------------------------------- #
    
    
# ---------------------------------------------------------------------------------- #
# Test CVolume
def test_cvolume_nifti1():

    c = connectome()
    
    # Check the default values
    v1 = CVolume()
    assert_equal(v1.get_name(), 'myvolume')
    assert_equal(v1.get_fileformat(), 'Nifti1')
    assert_equal(v1.get_metadata_as_dict(), {})
    
    # Check the specified values
    v2 = CVolume('Second volume')
    v2.update_metadata({'m0':123})
    assert_equal(v2.get_name(), 'Second volume')
    assert_not_equal(v2.get_metadata_as_dict(), {})
    assert_true('m0' in v2.get_metadata_as_dict())
    assert_equal(v2.get_metadata_as_dict()['m0'], '123')
    
    # Check classmethod
    v = CVolume.create_from_nifti('CVolume', op.join(DATA,'CVolume/sample.nii.gz'))
    assert_equal(v.get_name(), 'CVolume')
    
    # Check changing the name
    v.set_name('My volume')
    assert_equal(v.get_name(), 'My volume')
    
    # Check the description
    v.set_description('My first CVolume')
    assert_equal(v.get_description(), 'My first CVolume')
    
    # Check updating the metadata
    v.update_metadata({'meta1':'only T1 scan of this patient'})
    assert_equal(v.get_metadata_as_dict()['meta1'], 'only T1 scan of this patient')
    
    # Check add to the connectome
    c.add_connectome_volume(v)
    assert_not_equal(c.get_connectome_volume(), [])
    assert_equal(len(c.get_connectome_volume()), 1)

# ---------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------- #
# Test CTrack
def test_ctrack_trk():

    c = connectome()
    
    # Check default values
    t = CTrack()
    assert_equal(t.get_fileformat(), 'TrackVis')
    assert_equal(t.get_metadata_as_dict(), {})
    
    # Check the specified values
    t = CTrack('Spec tracks')
    t.update_metadata({'fib':1})
    assert_equal(t.get_name(), 'Spec tracks')
    assert_true('fib' in t.get_metadata_as_dict())
    assert_equal(t.get_metadata_as_dict()['fib'], '1')
    
    # 
    t = CTrack(name='my track',
                     src=op.join(DATA,'CTrack/fibers.trk'),
                      fileformat='TrackVis', dtype='Fibers')
    assert_equal(t.get_name(), 'my track')
    assert_equal(t.get_unique_relpath(), 'CTrack/my_track.trk')

    # Check add to the connectome
    c.add_connectome_track(t)
    assert_not_equal(c.get_connectome_track(), [])
    assert_equal(len(c.get_connectome_track()), 1)

# ---------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------- #
# Test CTimeserie
def test_ctimeserie_hdf5():

    c = connectome()
    
    # Check default values
    t = CTimeseries()
    assert_equal(t.get_fileformat(), 'HDF5')
    assert_equal(t.get_metadata_as_dict(), {})
    
    # Check the specified values
    t = CTimeseries('Spec timeserie')
    t.update_metadata({'ts':'val'})
    assert_equal(t.get_name(), 'Spec timeserie')
    assert_true('ts' in t.get_metadata_as_dict())
    assert_equal(t.get_metadata_as_dict()['ts'], 'val')
    
    # Check classmethod from hdf5
    t = CTimeseries(name='my timeserie', src= op.join(DATA,'CTimeserie/generatedseries.hdf5'))
    assert_equal(t.get_name(), 'my timeserie')
    assert_equal(t.get_unique_relpath(), 'CTimeserie/my_timeserie.h5')

    # Check add to the connectome
    c.add_connectome_timeseries(t)
    assert_not_equal(c.get_connectome_timeseries(), [])
    assert_equal(len(c.get_connectome_timeseries()), 1)

# ---------------------------------------------------------------------------------- #
   
    
# ---------------------------------------------------------------------------------- #
# Test CSurface
def test_csurface_gifti():

    c = connectome()
    
    # Check default values
    s = CSurface()
    assert_equal(s.get_fileformat(), 'Gifti')
    assert_equal(s.get_dtype(), 'Surfaceset')
    assert_equal(s.get_metadata_as_dict(), {})
    
    # Check the specified values
    s = CSurface('Spec surface')
    s.update_metadata({'surf':'ace'})
    assert_equal(s.get_name(), 'Spec surface')
    assert_true('surf' in s.get_metadata_as_dict())
    assert_equal(s.get_metadata_as_dict()['surf'], 'ace')
    
    # Check classmethod from gifti
    s = CSurface.create_from_gifti('my surface', op.join(DATA,'CSurface/labels.gii'))
    assert_equal(s.get_name(), 'my surface')
    assert_equal(s.get_src(), 'CSurface/my_surface.gii')

    # Check add to the connectome
    c.add_connectome_surface(s)
    assert_not_equal(c.get_connectome_surface(), [])
    assert_equal(len(c.get_connectome_surface()), 1)

    # Check save/load the CSurface
    s.save()
    s.load()

# ---------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------- #
# Test CData
def test_cdata():

    c = connectome()
    
    # Check default values
    d = CData()    
    assert_equal(d.get_fileformat(), None)
    assert_equal(d.get_metadata_as_dict(), {})
    
    # Check given values
    d = CData(name='Test data', fileformat='XML', src='data/CData/mydata.npy')
    d.update_metadata({'m1':'v1'})
    assert_equal(d.get_name(), 'Test data')
    assert_equal(d.get_fileformat(), 'XML')
    assert_equal(d.get_metadata_as_dict(), {'m1':'v1'})
    
    # Check NumPy
    d            = CData('data numpy')
    d.tmpsrc     = op.abspath(op.join(DATA,'CData/mydata.npy'))
    d.fileformat = "NumPy"
    d.src        = d.get_unique_relpath()
    c.add_connectome_data(d)
    d.load()
    assert_true(hasattr(d,'data'))
    if hasattr(d,'data'):
        assert_not_equal(d.data, None)
    
    # Check XML 
    d            = CData('data xml')
    d.tmpsrc     = op.abspath(op.join(DATA,'CData/mydata.xml'))
    d.fileformat = "XML"
    d.src        = d.get_unique_relpath()
    c.add_connectome_data(d)
    d.load()
    assert_true(hasattr(d,'data'))
    if hasattr(d,'data'):
        assert_not_equal(d.data, None)
# ---------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------- #
# Test CScript
def test_cscript():

    c = connectome()
    
    # Check default values
    s = CScript()
    assert_equal(s.get_fileformat(), 'UTF-8')
    assert_equal(s.get_dtype(), 'Python')
    assert_equal(s.get_metadata_as_dict(), {})
    
    # Check given values
    s = CScript(name='Test script', dtype='Bash', src=op.join(DATA,'CScript/analysis01.py'))
    s.update_metadata({'m1':'v1'})
    assert_equal(s.get_name(), 'Test script')
    assert_equal(s.get_dtype(), 'Bash')
    assert_equal(s.get_metadata_as_dict(), {'m1':'v1'})
        
    # Check create from file 
    s = CScript(name='my script', src = op.join(DATA, 'CScript/analysis01.py'))
    assert_equal(s.get_name(), 'my script')
    assert_equal(s.get_unique_relpath(), 'CScript/my_script.py')
    
    # Check add to the connectome
    c.add_connectome_script(s)
    assert_equal(len(c.get_connectome_script()), 1)
    

    
# ---------------------------------------------------------------------------------- #
# ================================================================================== #
   
