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
.. moduleauthor:: Gabriel Florea <gabriel.florea@codemart.ro>
.. moduleauthor:: Lia Domide <lia.domide@codemart.ro>
.. moduleauthor:: Bogdan Neacsa <bogdan.neacsa@codemart.ro>
"""

import os
import shutil
import uuid
from tempfile import gettempdir
from zipfile import ZipFile, ZIP_DEFLATED
from tvb.adapters.uploaders.abcuploader import ABCUploader
from tvb.adapters.uploaders.cff import load
from tvb.adapters.uploaders.networkx_connectivity.parser import NetworkxParser
from tvb.adapters.uploaders.gifti.parser import GIFTIParser
from tvb.basic.logger.builder import get_logger
from tvb.adapters.uploaders.networkx_importer import NetworkxCFFCommonImporterForm
from tvb.core.adapters.exceptions import LaunchException, ParseException
from tvb.core.entities.file.datatypes.connectivity_h5 import ConnectivityH5
from tvb.core.entities.model.datatypes.connectivity import ConnectivityIndex
from tvb.core.entities.storage import dao, transactional
from tvb.datatypes.connectivity import Connectivity
from tvb.core.neotraits._forms import UploadField, SimpleBoolField
from tvb.interfaces.neocom._h5loader import DirLoader


class CFFImporterForm(NetworkxCFFCommonImporterForm):

    def __init__(self, prefix='', project_id=None):
        super(CFFImporterForm, self).__init__(prefix, project_id, label_prefix='CNetwork: ')
        self.cff = UploadField('.cff', self, name='cff', required=True, label='CFF archive',
                               doc='Connectome File Format archive expected')


class CFF_Importer(ABCUploader):
    """
    Upload Connectivity Matrix from a CFF archive.
    """

    _ui_name = "CFF"
    _ui_subsection = "cff_importer"
    _ui_description = "Import from CFF archive one or multiple datatypes."
    logger = get_logger(__name__)

    form = None

    def get_input_tree(self): return None

    def get_upload_input_tree(self): return None

    def get_form(self):
        if self.form is None:
            return CFFImporterForm
        return self.form

    def set_form(self, form):
        self.form = form

    def get_output(self):
        return [Connectivity]


    @transactional
    def launch(self, cff, should_center=False, **kwargs):
        """
        Process the uploaded CFF and convert read data into our internal DataTypes.
        :param cff: CFF uploaded file to process.
        """
        if cff is None:
            raise LaunchException("Please select CFF file which contains data to import")

        conn_obj = load(cff)
        network = conn_obj.get_connectome_network()
        warning_message = ""
        results = []
        loader = DirLoader(self.storage_path)

        if network:
            partial = self._parse_connectome_network(network, warning_message, **kwargs)
            for conn in partial:
                conn_idx = ConnectivityIndex()
                conn_idx.fill_from_has_traits(conn)

                conn_h5_path = loader.path_for(ConnectivityH5, conn_idx.gid)
                with ConnectivityH5(conn_h5_path) as conn_h5:
                    conn_h5.store(conn)
                    conn_h5.gid.store(uuid.UUID(conn_idx.gid))
                results.append(conn_idx)


        self._cleanup_after_cfflib(conn_obj)

        current_op = dao.get_operation_by_id(self.operation_id)
        current_op.user_group = conn_obj.get_connectome_meta().title
        if warning_message:
            current_op.additional_info = warning_message
        dao.store_entity(current_op)

        return results



    def _parse_connectome_network(self, connectome_network, warning_message, **kwargs):
        """
        Parse data from a NetworkX object and save it in Connectivity DataTypes.
        """
        connectivities = []
        parser = NetworkxParser(**kwargs)

        for net in connectome_network:
            try:
                net.load()
                connectivity = parser.parse(net.data)
                connectivity.user_tag_1 = str(connectivity.weights.shape[0]) + " regions"
                connectivities.append(connectivity)

            except ParseException:
                self.logger.exception("Could not process Connectivity")
                warning_message += "Problem when importing Connectivities!! \n"

        return connectivities


    def _is_hemisphere_file(self, file_name):
        """
        :param file_name: File Name to analyze
        :return: expected pair file name (replace left <--> right) or None is the file can not be parsed
        """
        if file_name:

            if file_name.count('lh') == 1:
                return file_name.replace('lh', 'rh')

            if file_name.count('left') == 1:
                return file_name.replace('left', 'right')

            if file_name.count('rh') == 1:
                return file_name.replace('rh', 'lh')

            if file_name.count('right') == 1:
                return file_name.replace('right', 'left')

        return None


    def _cleanup_after_cfflib(self, conn_obj):
        """
        CFF doesn't delete temporary folders created, so we need to track and delete them manually!!
        """
        temp_files = []
        root_folder = gettempdir()

        for ele in conn_obj.get_all():
            if hasattr(ele, 'tmpsrc') and os.path.exists(ele.tmpsrc):
                full_path = ele.tmpsrc
                while os.path.split(full_path)[0] != root_folder and os.path.split(full_path)[0] != os.sep:
                    full_path = os.path.split(full_path)[0]
                #Get the root parent from the $gettempdir()$
                temp_files.append(full_path)

        conn_obj.close_all()
        conn_obj._zipfile.close()

        for ele in temp_files:
            try:
                if os.path.isdir(ele):
                    shutil.rmtree(ele)
                elif os.path.isfile(ele):
                    os.remove(ele)
            except OSError:
                self.logger.exception("Could not cleanup temporary files after import...")