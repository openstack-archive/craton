..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==============================
 Workflow Engine
==============================

https://blueprints.launchpad.net/craton/+spec/craton-workflow-engine

Workflows are integral part of Craton. A workflow in Craton is a representation
of task or a set of tasks that can be executed as a job. A job is simply a task or
a set of tasks that gets executed. Task(s) is pre-defined and run by an operator
of openstack cloud on a given set of inventory. Tasks can be combined together to
form a workflow but can also be executed as a single task workflow. Workflow engine
also ensures users have proper permission to run a given task. Admin users can make
a task public or make it available to a given role.

Problem description
===================

Implementation of workflow engine is a key feature provided by Craton.
Currently we do not have this feature so this spec is a proposal to
add this feature.

Example case:
Given a condition where operator needs to do a disruptive maintenance on a host,
a craton workflow could be written to do the following in an automated fashion:

1. Disable compute in nova
2. Live-migrate all vm's from the host to another
3. Run some pre-patch/reboot checks
5. Disable monitoring
4. Patch the host
5. Reboot the host
6. Run post patch/reboot checks
7. Enable monitoring
8. Enable compute

This is one example where each step is a registered task, a workflow is formed
by combining these tasks into a job and executing that job in the form of a
workflow.

Each task could be separately run as a job as well. In such a case, the workflow
on a given inventory is simply a job consisting of one task.

Audits are another example where we need to execute some plugin for information
gathering. The process behind audit job is exactly the same as the process
behind a remediation job.

Proposed change
===============

This spec proposes that we implement workflow engine that uses containers,
Docker in this case, as the underlying technology. We will use Docker based
clustering and orchrestration engine (either Swarm or Kubernetes) to sandbox
each task execution.

The process will look like so:

#. User -> Create Individual tasks.
#. User -> Creates Workflow. Workflow is a combination of tasks.
#. User -> Executes a workflow on some inventory as a job.

User -> API -> Execute WF -> Wofkflow [Docker Swarm] -> [ Execute Task 1 in container]
                                                         \ if successful
                                                        [ Execute Task 2 in container]
                                                         \ if successful
                                                        [ Execute Task N in container]

One important aspect of achieving this process is to define what a task
is and where it lives. A task (a plugin or script written in a programming
or scripting language) in order to be executed on a given host(s) needs to
be in the executing environment (in this case a docker container). We assume
that tasks are written by the operator for different use cases and are
registered againt craton api. Creating a task though the api will include
defining where a task lives. We will start by supporting tasks defined in
github and local storage, such that when the task is created, we create
a docker image and sync it to the cluster for task execution. The task
only becomes available for execution once the image is synced to the
cluster.


In github or in local dir:

 /craton_task1
  __init__.py
  task1.py
  task_uti.py
  requirements.txt
  Dockerfile

When the task is created in Craton though the api (using cli), we build the docker
image and sync it to all the swarm cluster nodes. Users can see that the task is
ready to be used in a workflow when the status filed in task is Ready.
This means the images was successfully build and is ready to be consumed.
Users can locally test this in their laptop before creating the task.

$ craton task-show 12345
---------------------------------------------------------------------
| id    | name  | location                         | ..... | Status |
---------------------------------------------------------------------
| 12345 | task1 | github.com/sulochan/craton_tasks | ..... | Ready  |
---------------------------------------------------------------------

Once the task is ready, it can be a part of a workflow Definition.
When a user executes a workflow, the task container is run with the
inventory data payload and any other payload defined in the workflow
variables. This basically translates to

docker run -t task1:latest python /craton/task1.py '{"a":"b" ...}'

What command is called on the particular task is defined during task creation.
The dockerfile is responsible to putting things and installing the correct
modules required by the task. For example for task1 the dockerfile looks like so:

$ cat Dockerfile
from alpine:latest
RUN apk add --no-cache bash linux-headers build-base git python3 python3-dev
ADD https://bootstrap.pypa.io/get-pip.py /root/get-pip.py
RUN python3.5 /root/get-pip.py
Add . /craton
RUN pip install -r /craton/requirements.txt

Hence, the calling command become /craton/task1.py '{"a":"b" ...}'
where the variables part is passed during the execution of the task by
craton workflow engine.

If the task is successful, the next task (if one exists) is called and so on.

Alternatives
------------
There are a few alternatives to this:

1. Use celery for task execution. All the tasks will be present in all the
nodes at all the time and we dont have to wory about building container images
and so on.

2. Use Taskflow for task execution. Similar to celery we wont have to worry
about building containers and tasks live in code tree.

Data model impact
-----------------
This will introduce three new data tables.
1. Task
2. Workflow
3. Jobs

REST API impact
---------------
New calls will be made available through the REST API as so:
- GET/POST     /tasks
- GET/POST/PUT /workflow
- GET/POST     /jobs

Security impact
---------------
Since we are executing tasks on host machines there are considerable
security implications.
1. All tasks executed should be sandboxed in a way that only the owner
   of the task executes the said task and no other task in this environment.
2. All tasks created should have proper access control.
3. Task should be approved prior to be available for execution.
4. Ensure tasks can only be executed on inventory that is owned by the
   tenant executing the task.

Notifications impact
--------------------
Craton does not yet have notifications.

Other end user impact
---------------------
New functionality to end user means new commands and api calls will
be available through python-cratonclient.

Performance Impact
------------------
There should not be any performance impact on the service created by this code
although it will frequently be called.

Other deployer impact
---------------------
None

Developer impact
----------------
None


Implementation
==============

Assignee(s)
-----------
Primary assignee:
- sulo

Other contributors:
- None

Work Items
----------
Work items can be summarized but not limited to:

- Add data model for workflow engine
- Add api functionality for managing (create/update/delete) tasks,
  workflows, and jobs.
- Add functionality to integrate with docker swarm or k8s.
- Add functionality to execute workflow.
- Add functionality to manage per container logs for tasks.


Dependencies
============
- Secrets Management
- Access Control


Testing
=======
This should be tested though unit and functional tests.


Documentation Impact
====================
This will impact our API reference documentation


References
==========
None
