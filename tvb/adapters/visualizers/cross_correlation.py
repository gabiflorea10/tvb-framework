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
A displayer for cross correlation.

.. moduleauthor:: Lia Domide <lia.domide@codemart.ro>
.. moduleauthor:: Marmaduke Woodman <mw@eml.cc>

"""
from tvb.adapters.visualizers.matrix_viewer import MappedArraySVGVisualizerMixin
from tvb.core.adapters.abcdisplayer import ABCDisplayer
from tvb.datatypes.temporal_correlations import CrossCorrelation


class CrossCorrelationVisualizer(MappedArraySVGVisualizerMixin, ABCDisplayer):
    _ui_name = "Cross Correlation Visualizer"
    _ui_subsection = "correlation"


    def get_input_tree(self):
        """Inform caller of the data we need as input """

        return [{"name": "datatype", "type": CrossCorrelation,
                 "label": "Cross correlation", "required": True}]


    def launch(self, datatype):
        """Construct data for visualization and launch it."""
        labels = self._get_associated_connectivity_labeling(datatype)
        matrix = datatype.get_data('array_data').mean(axis=0)[:, :, 0, 0]
        pars = self.compute_params(matrix, 'Correlation matrix plot', labels=labels)
        return self.build_display_result("matrix/svg_view", pars)