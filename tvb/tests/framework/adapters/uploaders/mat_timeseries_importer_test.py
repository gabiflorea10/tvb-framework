# -*- coding: utf-8 -*-
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

"""
Unit-test for mat_timeseries_importer and mat_parser.
.. moduleauthor:: Gabriel Florea <gabriel.florea@codemart.ro>
.. moduleauthor:: Mihai Andrei <mihai.andrei@codemart.ro>
"""

import os
import tvb_data
from cherrypy._cpreqbody import Part
from cherrypy.lib.httputil import HeaderMap
from tvb.adapters.uploaders.mat_timeseries_importer import MatTimeSeriesImporterForm
from tvb.tests.framework.core.base_testcase import TransactionalTestCase
from tvb.core.entities.file.files_helper import FilesHelper
from tvb.core.services.flow_service import FlowService
from tvb.tests.framework.core.factory import TestFactory
from tvb.core.entities.model.datatypes.connectivity import ConnectivityIndex
from tvb.core.entities.model.datatypes.time_series import TimeSeriesRegionIndex
from tvb.adapters.uploaders.zip_connectivity_importer import ZIPConnectivityImporterForm


class TestMatTimeSeriesImporter(TransactionalTestCase):

    base_pth = os.path.join(os.path.dirname(tvb_data.__file__), 'berlinSubjects', 'QL_20120814')
    bold_path = os.path.join(base_pth, 'QL_BOLD_regiontimecourse.mat')
    connectivity_path = os.path.join(base_pth, 'QL_20120814_Connectivity.zip')

    def transactional_setup_method(self):
        self.test_user = TestFactory.create_user('Mat_Timeseries_User')
        self.test_project = TestFactory.create_project(self.test_user, "Mat_Timeseries_Project")
        self._import_connectivity()


    def transactional_teardown_method(self):
        FilesHelper().remove_project_structure(self.test_project.name)


    def _import_connectivity(self):
        importer = TestFactory.create_adapter('tvb.adapters.uploaders.zip_connectivity_importer',
                                              'ZIPConnectivityImporter')

        form = ZIPConnectivityImporterForm()

        form.fill_from_post({'_uploaded': Part(self.connectivity_path, HeaderMap({}), ''),
                             '_normalization': 'region',
                             '_project_id': '1',
                             '_Data_Subject': 'John Doe'
                             })
        form.uploaded.data = self.connectivity_path
        importer.set_form(form)

        ### Launch Operation
        FlowService().fire_operation(importer, self.test_user, self.test_project.id,
                                     **form.get_form_values())


        self.connectivity = TestFactory.get_entity(self.test_project, ConnectivityIndex())


    def test_import_bold(self):
        ### Retrieve Adapter instance
        importer = TestFactory.create_adapter('tvb.adapters.uploaders.mat_timeseries_importer', 'MatTimeSeriesImporter')

        form = MatTimeSeriesImporterForm()
        form.fill_from_post({ '_data_file': Part(self.bold_path, HeaderMap({}), ''),
                              '_dataset_name': 'QL_20120824_DK_BOLD_timecourse',
                              '_structure_path': '',
                              '_transpose': 'False',
                              '_slice': '',
                              '_samling_rate': 100,
                              '_start_time': '0',
                              '_Data_Subject': 'QL'
                            })
        form.data_file.data = self.bold_path
        importer.set_form(form)

        ### Launch import Operation
        FlowService().fire_operation(importer, self.test_user, self.test_project.id, **form.get_form_values())

        tsr = TestFactory.get_entity(self.test_project, TimeSeriesRegionIndex())

        assert (661, 1, 68, 1) == tsr.read_data_shape()


