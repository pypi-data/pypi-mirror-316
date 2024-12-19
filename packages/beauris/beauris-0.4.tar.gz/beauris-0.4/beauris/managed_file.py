import logging
import os

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class ManagedFile():

    def __init__(self, type, path=None, name="", version=None, revision=None, locked_path=None, locked_revision=None, metadata={}, publish=True, **kwargs):

        self.type = type

        # These ones are optional
        self.path = path
        self.name = name
        self.version = version
        if revision:
            self.revision = int(revision)
        else:
            self.revision = 0

        self.locked_path = locked_path
        if locked_revision:
            self.locked_revision = int(locked_revision)
        else:
            self.locked_revision = None

        # Only used when we have just locked data for real, but not yet deployed
        # => We load the newly locked yml content here (to get the real path),
        #    while keeping the old locked yml data (to remember which data was changed)
        self.future_locked_path = None

        self.metadata = metadata

        self.publish = publish

    def to_yml(self):

        raise NotImplementedError()

    def get_publish_path(self, base_work_dir, base_publish_dir):

        raise NotImplementedError()

    def get_metadata(self):

        # Set some default metadata, overwrite with stored ones (if any)
        metadata = {
            'version': self.version,
            'revision': self.get_revision(),
            'type': self.type,
            'filename': os.path.basename(self.path)
        }
        metadata.update(self.metadata)

        return metadata

    def merge_with_locked(self, locked_yml, future=False):

        if self.is_same_file(locked_yml):
            if future:
                self.future_locked_path = locked_yml["locked_path"]
            else:
                self.locked_path = locked_yml["locked_path"]
                self.locked_revision = int(locked_yml["revision"])

    def is_same_file(self, other):

        same = True

        if 'path' in other:
            same = same and self.path == other['path']

        if 'type' in other:
            same = same and self.type == other['type']

        if 'version' in other:
            same = same and self.version == other['version']

        return same

    def has_changed_since_last_lock(self):

        # revision is a number (0 by default) and can be updated:
        #  - manually in organism yml file for input file
        #  - automatically when a derived file is updated (force run or updated dep)
        # locked_revision can be an integer (file has already been locked once), or None
        return self.get_revision() != self.locked_revision

    def file_exists(self, locked=False):

        """
        If locked is True, we look at a locked path
        """

        # Check if we have an existing locked file
        if locked:
            return self.get_locked_path() and os.path.exists(self.get_locked_path())

        # Check if we have an existing non-locked file
        return self.path and os.path.exists(self.path)

        return False

    def get_usable_path(self, force_work_dir=False):

        if self.future_locked_path:
            return self.future_locked_path
        elif not self.has_changed_since_last_lock() and self.locked_path and os.path.exists(self.locked_path):
            return self.locked_path
        else:
            return self.path

    def get_locked_path(self):

        if self.future_locked_path:
            return self.future_locked_path

        return self.locked_path

    def get_revision(self):

        return self.revision

    def needs_to_run(self):

        return False

    def has_locked_path(self):
        return self.get_locked_path() and os.path.exists(self.get_locked_path())


class InputFile(ManagedFile):

    def __init__(self, type, path=None, url=None, name="", version=None, revision=None, locked_path=None, locked_revision=None, metadata={}, publish=True, no_lock=False, check_files_exist=True, hash_type=None, hash_value=None):

        ManagedFile.__init__(self, type, path=path, name=name, version=version, revision=revision, locked_path=locked_path, locked_revision=locked_revision, metadata=metadata, publish=publish, no_lock=no_lock)

        self.url = url
        self.path = path

        self.hash_type = hash_type
        self.hash_value = hash_value

        # A path where groomed data is saved (after download and/org unzipping)
        # Not defined means there's no groomed data, just use the input path
        self.greeted_path = None

        # Additional checks for InputFile
        if not self.path and not self.url:
            raise Exception("Trying to build an InputFile object without a 'path' or an 'url', that's forbidden.")

        if check_files_exist:
            if not os.path.exists(self.path):
                # TODO in theory the file could have disappeared, as long as it's locked we should be happy
                raise Exception("Could not find input file {}".format(path))

        if not self.is_remote() and not os.path.abspath(self.path):
            raise Exception("Input file path {} should be absolute".format(path))

        if not self.name:
            raise Exception("Trying to build an InputFile object without a 'name', that's forbidden.")

        if self.version is None:
            raise Exception("Trying to build an InputFile object without a 'version', that's forbidden.")

        # Hack to prevent locking huge file, use with extra caution (used for huge bam tracks)
        self.no_lock = no_lock

    @classmethod
    def from_yml(cls, yml_data, name, version, no_lock=False, check_files_exist=True):

        params = {
            "type": yml_data["type"],
            "path": yml_data["path"] if "path" in yml_data else None,
            "url": yml_data["url"] if "url" in yml_data else None,
            "name": name,
            "version": version,
            "revision": yml_data["revision"] if "revision" in yml_data else None,
            "no_lock": no_lock,
            "check_files_exist": check_files_exist,
            "hash_type": yml_data["hash"]["type"] if "hash" in yml_data else None,
            "hash_value": yml_data["hash"]["value"] if "hash" in yml_data else None,
        }

        file = cls(**params)

        return file

    def to_yml(self):

        yml = {
            "path": self.path,
            "type": self.type,
        }

        if self.locked_path:
            yml['locked_path'] = self.locked_path

        yml['revision'] = self.get_revision()

        return yml

    def get_publish_path(self, base_work_dir, base_publish_dir, entity):

        return os.path.join(entity.get_work_dir().replace(base_work_dir, base_publish_dir), entity.slug(), self.name, os.path.basename(self.path))

    def is_remote(self):
        return self.url and not self.path

    def get_usable_path(self, force_work_dir=False):

        if self.future_locked_path:
            return self.future_locked_path
        elif not self.has_changed_since_last_lock() and self.locked_path and os.path.exists(self.locked_path):
            return self.locked_path
        elif self.greeted_path:
            return self.greeted_path
        else:
            return self.path


class DerivedFile(ManagedFile):

    # TODO sniff tool_version automatically instead of hard coding
    def __init__(self, type, path=None, name="", version=None, revision=None, locked_path=None, locked_revision=None, metadata={}, depends_on=[], task=None, tool_version="", publish=True, optional=True):

        ManagedFile.__init__(self, type, path=path, name=name, version=version, revision=revision, locked_path=locked_path, locked_revision=locked_revision, metadata=metadata, publish=publish)

        # It's ok if the file does not exits yet
        if not os.path.abspath(self.path):
            raise Exception("Input file path {} should be absolute".format(path))

        self.task = task
        self.tool_version = tool_version

        # A list of other ManagedFiles that this derived file depends on
        self.depends_on = depends_on

        # DerivedFiles can have a 'path' attribute (when created from a newly created file in work dir)
        # or potentially not (when loaded only from a lock file, but that never happens as of writing this)

        # DerivedFiles don't have a 'version' attribute (no sense to have one), but they have a 'tool_version' = the version of the tool that produced it

        # Will be True if this file has changed and its revision has been bumped
        self.dirty = False

        # Revision can be None
        # Getting a revision for a DerivedFile is not really expected in normal life
        self.revision = revision

        # Some tools can return optional files. We want to manage them, but not raise an error when they are missing
        self.optional = optional

    @classmethod
    def from_yml(cls, yml_data):

        params = {
            "type": yml_data["type"],
            "path": yml_data["path"] if "path" in yml_data else None,
            "name": yml_data["name"] if "name" in yml_data else None,
            "tool_version": yml_data["tool_version"] if "tool_version" in yml_data else None,
            "revision": yml_data["revision"] if "revision" in yml_data else None,
        }

        file = cls(**params)

        return file

    def to_yml(self):

        yml = {
            "type": self.type,
        }

        yml['locked_path'] = self.locked_path if self.locked_path else ""

        if self.get_tool_version():
            yml['tool_version'] = self.get_tool_version()

        yml['revision'] = self.get_revision()

        if self.name:
            yml['name'] = self.name

        if self.task:
            yml['task_id'] = self.task.name

        # TODO add generation date
        # TODO add status (online/archived/...)
        # TODO add more type info (tsv is not enough: interproscan/eggnog/...)
        # TODO adapt schema accordingly

        return yml

    def get_metadata(self):

        # Set some default metadata, overwrite with stored ones (if any)
        metadata = {
            'tool_version': self.get_tool_version(),
            'revision': self.get_revision(),
            'type': self.type,
            'filename': os.path.basename(self.locked_path) if self.locked_path else os.path.basename(self.path),
            'name': self.name if self.name else "",
            'task_id': self.task.name if self.task else ""
        }
        metadata.update(self.metadata)

        return metadata

    def merge_with_locked(self, locked_yml, future=False):

        if self.is_same_file(locked_yml):
            if future:
                self.future_locked_path = locked_yml["locked_path"]
            else:
                self.locked_path = locked_yml["locked_path"]
                self.locked_revision = int(locked_yml["revision"])
                if 'tool_version' in locked_yml:
                    self.tool_version = locked_yml["tool_version"]

    def set_dirty(self):

        self.dirty = True

    def is_dirty(self):

        return self.dirty or self.needs_to_run()

    def needs_to_run(self):

        return self.task and self.task.needs_to_run()

    def get_revision(self):

        if self.locked_revision is None:
            return 0

        if self.is_dirty():
            return self.locked_revision + 1

        return self.locked_revision

    def get_tool_version(self):

        if self.task is not None:
            task_output = self.task.get_derived_output_by_name(self.name)

            if task_output is not None and task_output.tool_version and self.is_dirty():
                return task_output.tool_version

        if self.tool_version:
            return self.tool_version

        return ""

    def has_changed_since_last_lock(self):

        if ManagedFile.has_changed_since_last_lock(self):
            return True

        if self.is_dirty():
            return True

        # Check derived dependencies recursively too
        # in case file X depends on file Y which depends on file Z which has changed
        for res_dep in self.depends_on:
            if res_dep.has_changed_since_last_lock():
                return True

        return False

    def get_usable_path(self, force_work_dir=False):

        if self.future_locked_path:
            return self.future_locked_path
        elif not force_work_dir and self.locked_path and os.path.exists(self.locked_path):
            return self.locked_path
        else:
            return self.path

    def get_publish_path(self, base_work_dir, base_publish_dir, entity):

        return os.path.join(entity.get_work_dir().replace(base_work_dir, base_publish_dir), entity.slug(), self.name, os.path.basename(self.path))
