import json
import os

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from libcoveweb2.process.base import ProcessDataTask


class TaskWithState(ProcessDataTask):
    """An abstract task that helps you save state from
    the processing step and add it to the context.

    It will cache one JSON blob for you, and add
    it to the view context when a user is looking at the results.
    (So make sure you choose keys in the JSON blob carefully
    so as not to clash with other view context variables!)

    Extend and provide your own state_filename and process_get_state.
    """

    #: Set state_filename to a unique name for each task.
    #:
    #: If you change this name the task will be rerun, so this is a good way to
    #: make sure all underlying data changes if a new version of this bit of cove
    #: is released.
    state_filename: str = "task_with_state.json"

    def process_get_state(self, process_data: dict):
        """Called to process data.

        Is only called if there is work to do,
        so does not need to worry about checking that.

        Should return a tuple.
        The first item is the results to save, as a dictionary.
        The second item is process_data, as a dictionary.

        Do NOT change process_data in this function!
        The fact it's returned is a mistake:
        https://github.com/OpenDataServices/lib-cove-web-2/issues/14
        """
        return {}, process_data

    def process(self, process_data: dict) -> dict:
        if self.does_state_exist():
            return process_data

        state, process_data_throw_away = self.process_get_state(process_data)

        default_storage.save(
            os.path.join(self.supplied_data.storage_dir(), self.state_filename),
            ContentFile(json.dumps(state, indent=4)),
        )

        return process_data

    def does_state_exist(self) -> bool:
        return default_storage.exists(
            os.path.join(self.supplied_data.storage_dir(), self.state_filename)
        )

    def is_processing_applicable(self) -> bool:
        return True

    def is_processing_needed(self) -> bool:
        return not self.does_state_exist()

    def get_context(self):
        if self.does_state_exist():
            with default_storage.open(
                os.path.join(self.supplied_data.storage_dir(), self.state_filename)
            ) as fp:
                return json.load(fp)
        else:
            return {}
