import logging
from os import listdir

from .config import Config
from .data_locker import DataLockers
from .deployers import Deployers
from .job_runner import Runners
from .organism import Organism
from .raw_data_greeters import RawDataGreeters
from .util import Util

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class Beauris():

    def __init__(self, root_work_dir=None, config_file=None):

        self.config = Config(root_work_dir, config_file)

        self.runners = Runners(self.config.job_specs)

        self.data_lockers = DataLockers()

        self.deployers = Deployers(self.config)

        self.raw_data_greeters = RawDataGreeters()

        labels = Util.mr_labels

        if 'logging-debug' in labels:
            # Override root logger
            logging.basicConfig(level=logging.DEBUG, force=True)

    def load_organism(self, yml_path, test_data=False, locked_dir=None, future_locked_dir=None, check_files_exist=True):

        self.config.check_files_exist = check_files_exist

        return Organism(self.config, yml_path, test_data=test_data, locked_dir=locked_dir, future_locked_dir=future_locked_dir, default_services=self.config.deploy_services)

    def get_runner(self, method, entity, task_id, workdir="", server="", access_mode="public"):

        return self.runners.get(method, entity, task_id, workdir, server, access_mode)

    def get_data_locker(self, override_conf={}):

        method = self.config.raw['data_locker']['method']

        locker_conf = self.config.raw['data_locker']['options']

        # This is used mainly for tests
        locker_conf.update(override_conf)

        return self.data_lockers.get(method, locker_conf)

    def get_deployer(self, service, server, entity):

        return self.deployers.get(service, server, entity)

    def load_organisms(self, yml_dir, test_data=False, locked_dir=None, future_locked_dir=None, check_files_exist=False,):
        organisms = []

        for f in listdir(yml_dir):
            if (f.lower().endswith('.yml')):
                path = "{}/{}".format(yml_dir, f)
                organisms.append(self.load_organism(path, test_data=test_data, locked_dir=locked_dir, future_locked_dir=future_locked_dir, check_files_exist=check_files_exist))

        return organisms

    def load_organisms_by_tags(self, yml_dir, test_data=False, locked_dir=None, future_locked_dir=None, check_files_exist=False, with_tags={}):
        tagged_organisms = []
        organisms = self.load_organisms(yml_dir, test_data=test_data, locked_dir=locked_dir, future_locked_dir=future_locked_dir, check_files_exist=check_files_exist)

        for org in organisms:
            if all(tag in org.get_tags() for tag in with_tags):
                tagged_organisms.append(org)

        return tagged_organisms
