import abc


class WorkflowFactory(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def workflow(self):
        """Construct appropriate taskflow flow object.

        :returns: A flow.Flow subclass
        """
