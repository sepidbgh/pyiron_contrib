# Copyright (c) Max-Planck-Institut für Eisenforschung GmbH - Computational Materials Design (CM) Department

"""
Job class to calculate the stacking fault energy using the ANNNI model.
"""

__author__ = "Marvin Poul"
__copyright__ = "Copyright 2021, Max-Planck-Institut für Eisenforschung GmbH " \
                "- Computational Materials Design (CM) Department"
__version__ = "0.1"
__maintainer__ = "Marvin Poul"
__email__ = "poul@mpie.de"
__status__ = "development"
__date__ = "Jun 14, 2021"


from pyiron_base import GenericMaster, DataContainer

class StackingFaultANNNI(GenericMaster):

    def __init__(self, project=None, job_name=None):
        super().__init__(project=project, job_name=job_name)
        self.input = DataContainer(table_name="parameters")
        self.input.container = None

    @property
    def container(self):
        return self.input.container

    @container.setter
    def container(self, container):
        self.input.container = container

    def validate_ready_to_run(self):
        if self.input.container is None:
            raise ValueError("No structure container set!")
        if self.ref_job is None:
            raise ValueError("No reference job set!")
        self.ref_job.validate_ready_to_run()
        copy = self.ref_job.copy_to(
                project=self.project_hdf5,
                new_job_name=f"{self.name}_calculator",
                new_database_entry=True
        )
        self.append(copy)


    def run_static(self):
        self.status.running = True



        self.status.collect = True
        self.run()

    def collect_output(self):
        self.to_hdf()

    def write_input(self):
        pass

    def to_hdf(self, hdf=None, group_name=None):
        super().to_hdf(hdf=hdf, group_name=group_name)
        self.input.to_hdf(hdf=self.project_hdf5)

    def from_hdf(self, hdf=None, group_name=None):
        super().from_hdf(hdf=hdf, group_name=group_name)
        self.input.from_hdf(hdf=self.project_hdf5)
