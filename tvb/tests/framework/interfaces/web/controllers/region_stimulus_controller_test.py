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
.. moduleauthor:: Bogdan Neacsa <bogdan.neacsa@codemart.ro>
"""
import unittest
from tvb.tests.framework.interfaces.web.controllers.base_controller_test import BaseTransactionalControllerTest
from tvb.interfaces.web.controllers.spatial.region_stimulus_controller import RegionStimulusController


class RegionsStimulusControllerTest(BaseTransactionalControllerTest):
    """ Unit tests for RegionStimulusController """
    
    def setUp(self):
        """
        Sets up the environment for testing;
        creates a `RegionStimulusController`
        """
        self.init()
        self.region_s_c = RegionStimulusController()


    def tearDown(self):
        """ Cleans the testing environment """
        self.cleanup()


    def test_step_1(self):
        """
        Verifies that result dictionary has the expected keys / values after call to
        `step_1_submit(...)`
        """
        self.region_s_c.step_1_submit(1, 1)
        result_dict = self.region_s_c.step_1()
        self.assertEqual(result_dict['equationViewerUrl'], '/spatial/stimulus/region/get_equation_chart')
        self.assertTrue('fieldsPrefixes' in result_dict)
        self.assertEqual(result_dict['loadExistentEntityUrl'], '/spatial/stimulus/region/load_region_stimulus')
        self.assertEqual(result_dict['mainContent'], 'spatial/stimulus_region_step1_main')
        self.assertEqual(result_dict['next_step_url'], '/spatial/stimulus/region/step_1_submit')

            
def suite():
    """
    Gather all the tests in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(RegionsStimulusControllerTest))
    return test_suite


if __name__ == "__main__":
    #So you can run tests individually.
    TEST_RUNNER = unittest.TextTestRunner()
    TEST_SUITE = suite()
    TEST_RUNNER.run(TEST_SUITE)