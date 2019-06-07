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
.. moduleauthor:: Mihai Andrei <mihai.andrei@codemart.ro>
"""
import json
import uuid
import numpy
from tvb.datatypes.time_series import TimeSeriesRegion, TimeSeriesEEG
from tvb.adapters.uploaders.abcuploader import ABCUploader, ABCUploaderForm
from tvb.adapters.uploaders.mat.parser import read_nested_mat_file
from tvb.core.adapters.exceptions import ParseException, LaunchException
from tvb.core.entities.file.datatypes.time_series import TimeSeriesRegionH5, TimeSeriesEEGH5
from tvb.core.entities.model.datatypes.connectivity import ConnectivityIndex
from tvb.core.entities.model.datatypes.time_series import TimeSeriesRegionIndex, TimeSeriesEEGIndex
from tvb.core.entities.storage import transactional
from tvb.basic.arguments_serialisation import parse_slice
from tvb.core.neotraits._forms import UploadField, SimpleStrField, SimpleBoolField, SimpleIntField, DataTypeSelectField
from tvb.core.neotraits.db import prepare_array_shape_meta
from tvb.interfaces.neocom._h5loader import DirLoader

TS_REGION = "Region"
TS_EEG = "EEG"

class MatTimeSeriesImporterForm(ABCUploaderForm):

    def __init__(self, prefix='', project_id=None):
        super(MatTimeSeriesImporterForm, self).__init__(prefix, project_id)
        self.data_file = UploadField('.mat', self, name='data_file', required=True,
                                     label='Please select file to import')
        self.dataset_name = SimpleStrField(self, name='dataset_name', required=True, label='Matlab dataset name',
                                           doc='Name of the MATLAB dataset where data is stored')
        self.structure_path = SimpleStrField(self, name='structure_path', default='',
                                             label='For nested structures enter the field path (separated by .)')
        self.transpose = SimpleBoolField(self, name='transpose', default=False,
                                         label='Transpose the array. Expected shape is (time, channel)')
        self.slice = SimpleStrField(self, name='slice', default='',
                                    label='Slice of the array in numpy syntax. Expected shape is (time, channel)')
        self.sampling_rate = SimpleIntField(self, name='sampling_rate', default=100, label='sampling rate (Hz)')
        self.start_time = SimpleIntField(self, name='start_time', default=0, label='starting time (ms)', required=True)


class RegionMatTimeSeriesImporterForm(MatTimeSeriesImporterForm):

    def __init__(self, prefix='', project_id=None):
        super(RegionMatTimeSeriesImporterForm, self).__init__(prefix, project_id)
        self.region = DataTypeSelectField(ConnectivityIndex, self, name='tstype_parameters', required=True,
                                          label='Connectivity')


class MatTimeSeriesImporter(ABCUploader):
    """
    Import time series from a .mat file.
    """
    _ui_name = "Timeseries Region MAT"
    _ui_subsection = "mat_ts_importer"
    _ui_description = "Import time series from a .mat file."
    tstype = TS_REGION

    def get_form(self):
        if self.form is None:
            return RegionMatTimeSeriesImporterForm
        return self.form
    form = None

    def get_input_tree(self): return None

    def get_upload_input_tree(self): return None

    def set_form(self, form):
        self.form = form

    def get_output(self):
        return [TimeSeriesRegionIndex, TimeSeriesEEGIndex]

    def create_region_ts(self, data_shape, connectivity):
        if connectivity.number_of_regions != data_shape[1]:
            raise LaunchException("Data has %d channels but the connectivity has %d nodes"
                                  % (data_shape[1], connectivity.number_of_regions))
        ts_idx = TimeSeriesRegionIndex()
        ts_idx.connectivity = connectivity

        ts_h5_path = self.loader.path_for(TimeSeriesRegionH5, ts_idx.gid)
        ts_h5 = TimeSeriesRegionH5(ts_h5_path)
        ts_h5.connectivity.store(uuid.UUID(connectivity.gid))

        return TimeSeriesRegion(), ts_idx, ts_h5

    def create_eeg_ts(self, data_shape, sensors):
        if sensors.number_of_sensors != data_shape[1]:
            raise LaunchException("Data has %d channels but the sensors have %d"
                                  % (data_shape[1], sensors.number_of_sensors))

        ts_idx = TimeSeriesEEGIndex()
        ts_idx.sensors = sensors

        ts_h5_path = self.loader.path_for(TimeSeriesEEGH5, ts_idx.gid)
        ts_h5 = TimeSeriesEEGH5(ts_h5_path)
        ts_h5.sensors.store(uuid.UUID(sensors.gid))

        return TimeSeriesEEG(), ts_idx, ts_h5

    ts_builder = {TS_REGION: create_region_ts, TS_EEG: create_eeg_ts}

    @transactional
    def launch(self, data_file, dataset_name, structure_path='',
               transpose=False, slice=None, sampling_rate=1000,
               start_time=0, tstype_parameters=None):
        try:
            data = read_nested_mat_file(data_file, dataset_name, structure_path)

            if transpose:
                data = data.T
            if slice:
                data = data[parse_slice(slice)]

            self.loader = DirLoader(self.storage_path)

            ts, ts_idx, ts_h5 = self.ts_builder[self.tstype](self, data.shape, tstype_parameters)

            ts.start_time = start_time
            ts.sample_period = 1.0 / sampling_rate
            ts.sample_period_unit = 's'

            ts_h5.write_time_slice(numpy.r_[:data.shape[0]] * ts.sample_period)
            # we expect empirical data shape to be time, channel.
            # But tvb expects time, state, channel, mode. Introduce those dimensions
            ts_h5.write_data_slice(data[:, numpy.newaxis, :, numpy.newaxis])

            data_shape = ts_h5.read_data_shape()
            ts_h5.nr_dimensions.store(len(data_shape))
            ts_h5.gid.store(uuid.UUID(ts_idx.gid))
            ts_h5.sample_period.store(ts.sample_period)
            ts_h5.sample_period_unit.store(ts.sample_period_unit)
            ts_h5.sample_rate.store(sampling_rate)
            ts_h5.start_time.store(ts.start_time)
            ts_h5.labels_ordering.store(ts.labels_ordering)
            ts_h5.labels_dimensions.store(ts.labels_dimensions)
            ts_h5.title.store(ts.title)
            ts_h5.close()

            ts_idx.title = ts.title
            ts_idx.sample_period_unit = ts.sample_period_unit
            ts_idx.sample_period = ts.sample_period
            ts_idx.sample_rate = ts.sample_rate
            ts_idx.labels_ordering = json.dumps(ts.labels_ordering)
            ts_idx.data_ndim = len(data_shape)
            ts_idx.data_length_1d, ts_idx.data_length_2d, ts_idx.data_length_3d, ts_idx.data_length_4d = prepare_array_shape_meta(
                data_shape)

            return ts_idx
        except ParseException as ex:
            self.log.exception(ex)
            raise LaunchException(ex)
