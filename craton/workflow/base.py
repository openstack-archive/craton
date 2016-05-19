import abc

import six


@six.add_metaclass(abc.ABCMeta)
class WorkflowFactory(object):

    @abc.abstractmethod
    def workflow(self):
        """Construct appropriate taskflow flow object.

        :returns: A flow.Flow subclass
        """
