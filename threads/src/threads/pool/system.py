#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Colony Framework. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import copy
import threading

import colony.base.system
import colony.libs.structures_util

DEFAULT_NUMBER_THREADS = 5
""" The default number of threads to be created """

DEFAULT_MAXIMUM_NUMBER_THREADS = 15
""" The default maximum number of threads to be created """

CONSTANT_SCHEDULING_ALGORITHM = 1
""" The constant size scheduling algorithm value """

DYNAMIC_SCHEDULING_ALGORITHM = 2
""" The dynamic size scheduling algorithm value """

START_THREAD_TASK_TYPE = "start_thread"
""" The start thread task type """

STOP_THREAD_TASK_TYPE = "stop_thread"
""" The stop thread task type """

START_TASK_TASK_TYPE = "start_task"
""" The start task task type """

STOP_TASK_TASK_TYPE = "stop_task"
""" The stop task task type """

PAUSE_TASK_TASK_TYPE = "pause_task"
""" The pause task task type """

RESUME_TASK_TASK_TYPE = "resume_task"
""" The resume task task type """

TASK_RUNNING_STATUS = 1
""" The task running status value """

TASK_STOPPED_STATUS = 2
""" The task stopped status value """

TASK_PAUSED_STATUS = 3
""" The task paused status value """

SCHEDULING_ALGORITHM_NAME_MAP = {
    CONSTANT_SCHEDULING_ALGORITHM : "constant",
    DYNAMIC_SCHEDULING_ALGORITHM : "dynamic"
}
""" The scheduling algorithm name map """

class ThreadPool(colony.base.system.System):
    """
    The thread pool class.
    """

    thread_pools_list = []
    """ The list of currently enabled thread pools """

    def __init__(self, plugin):
        colony.base.system.System.__init__(self, plugin)
        self.thread_pools_list = []

    def unload(self):
        """
        Unloads the thread pool, stopping all the available thread pools.
        """

        # iterates over all the thread pools
        for thread_pool in self.thread_pools_list:
            # stops the thread pool
            thread_pool.stop_pool()

    def create_new_thread_pool(self, name, description, number_threads = DEFAULT_NUMBER_THREADS, scheduling_algorithm = CONSTANT_SCHEDULING_ALGORITHM, maximum_number_threads = DEFAULT_MAXIMUM_NUMBER_THREADS):
        """
        Creates a new thread pool with the given name, description
        and number of threads.

        @type name: String
        @param name: The thread pool name.
        @type description: String
        @param description: The thread pool description.
        @type number_threads: int
        @param number_threads: The thread pool number of threads.
        @type scheduling_algorithm: int
        @param scheduling_algorithm: The thread pool scheduling algorithm.
        @type maximum_number_threads: int
        @param maximum_number_threads: The thread pool maximum number of threads.
        @rtype: ThreadPoolImplementation
        @return: The created thread pool.
        """

        # retrieves the logger
        logger = self.plugin.logger

        # creates a new thread pool
        thread_pool = ThreadPoolImplementation(name, description, number_threads, scheduling_algorithm, maximum_number_threads, logger)

        # adds the new thread pool to the list of thread pools
        self.thread_pools_list.append(thread_pool)

        # returns the new thread pool
        return thread_pool

    def get_thread_task_descriptor_class(self):
        """
        Retrieves the thread task descriptor class.

        @rtype: Class
        @return: The thread task descriptor class.
        """

        return TaskDescriptor

    def get_system_information(self):
        """
        Retrieves the system information map, containing structured
        information to be visible using presentation viewers.

        @rtype: Dictionary
        @return: The system information map.
        """

        # creates the map to hold the system information (ordered  map)
        thread_pool_information = colony.libs.structures_util.OrderedMap()

        # iterates over all the thread pools
        for thread_pool in self.thread_pools_list:
            # retrieves the thread pool values
            thread_pool_name = thread_pool.name
            thread_pool_number_threads = thread_pool.number_threads
            thread_pool_scheduling_algorithm = thread_pool.scheduling_algorithm
            thread_pool_maximum_number_threads = thread_pool.maximum_number_threads
            thread_pool_current_threads = thread_pool.current_number_threads
            thread_pool_busy_threads = thread_pool.busy_threads

            # retrieves the thread pool scheduling algorithm name
            thread_pool_scheduling_algorithm_name = SCHEDULING_ALGORITHM_NAME_MAP[thread_pool_scheduling_algorithm]

            # creates the thread pool thread string
            thread_pool_thread_string = "%d / %d / %d / %d" % (thread_pool_busy_threads, thread_pool_current_threads, thread_pool_number_threads, thread_pool_maximum_number_threads)

            # sets the instance value for the thread pool information
            thread_pool_information[thread_pool_name] = (
                thread_pool_thread_string,
                thread_pool_scheduling_algorithm_name
            )

        # defines the thread pool item columns
        thread_pool_item_columns = [
            {
                "type" : "name",
                "value" : "Pool Name"
            },
            {
                "type" : "value",
                "value" : "BUS / CUR / MIN / MAX"
            },
            {
                "type" : "value",
                "value" : "Algorithm"
            }
        ]

        # creates the thread pool item
        thread_pool_item = {}

        # sets the thread pool item values
        thread_pool_item["type"] = "map"
        thread_pool_item["columns"] = thread_pool_item_columns
        thread_pool_item["values"] = thread_pool_information

        # creates the system information (item)
        system_information = {}

        # sets the system information (item) values
        system_information["name"] = "Thread Pool Manager"
        system_information["items"] = [thread_pool_item]

        # returns the system information
        return system_information

class ThreadPoolImplementation:
    """
    The thread pool implementation class.
    """

    name = "none"
    """ The thread pool name """

    description = "none"
    """ The thread pool description """

    number_threads = DEFAULT_NUMBER_THREADS
    """ The thread pool number of threads """

    scheduling_algorithm = CONSTANT_SCHEDULING_ALGORITHM
    """ The thread pool scheduling algorithm """

    maximum_number_threads = DEFAULT_MAXIMUM_NUMBER_THREADS
    """ The thread pool maximum number of threads """

    logger = None
    """ The logger used """

    worker_threads_list = []
    """ The thread pool list of worker threads """

    task_queue = []
    """ The thread pool task queue """

    task_descriptor_running_queue = []
    """ The thread pool running task descriptor queue """

    task_condition = None
    """ The thread pool task condition """

    current_number_threads = 0
    """ The thread pool current number of threads """

    busy_threads = 0
    """ The thread pool number of busy threads """

    thread_size_modification_semaphore = None
    """ The thread pool thread size modification semaphore """

    def __init__(self, name = "none", description = "none", number_threads = DEFAULT_NUMBER_THREADS, scheduling_algorithm = CONSTANT_SCHEDULING_ALGORITHM, maximum_number_threads = DEFAULT_MAXIMUM_NUMBER_THREADS, logger = None):
        """
        Constructor of the class.

        @type name: String
        @param name: The thread pool name.
        @type description: String
        @param description: The thread pool description.
        @type number_threads: int
        @param number_threads: The thread pool number of threads.
        @type scheduling_algorithm: int
        @param scheduling_algorithm: The thread pool scheduling algorithm.
        @type maximum_number_threads: int
        @param maximum_number_threads: The thread pool maximum number of threads.
        @type logger: Log
        @param logger: The logger used.
        """

        self.name = name
        self.description = description
        self.number_threads = number_threads
        self.scheduling_algorithm = scheduling_algorithm
        self.maximum_number_threads = maximum_number_threads
        self.logger = logger

        self.worker_threads_list = []
        self.task_queue = []
        self.task_descriptor_running_queue = []

        self.task_condition = threading.Condition()

        self.current_number_threads = 0
        self.busy_threads = 0

        self.thread_size_modification_semaphore = threading.Semaphore()

    def start_pool(self):
        """
        Starts the thread pool launching and starting all the threads.
        """

        # iterates over the number of threads for the thread pool
        for _n_thread in range(self.number_threads):
            # creates a worker thread for the thread pool
            self.create_worker_thread()

    def stop_pool(self):
        """
        Stops the thread pool exiting all the threads.
        """

        # creates a worker thread task to stop the thread
        worker_thread_task = WorkerThreadTask(STOP_THREAD_TASK_TYPE)

        # inserts the worker thread task into the task queue
        self.insert_worker_thread_task_all(worker_thread_task)

        # iterates over all the threads to join them
        for thread in self.worker_threads_list:
            # joins the thread
            thread.join()

    def stop_pool_tasks(self):
        """
        Stops the thread tasks pool removing all the tasks.
        """

        # creates a copy of the task queue (to remove worker thread task)
        task_queue_copy = copy.copy(self.task_queue)

        # iterates over all the tasks in the task queue
        for task in task_queue_copy:
            # removes the task from the task queue
            self.remove_worker_thread_task(task)

        # creates a copy of the task descriptor running queue (to stop the task)
        task_descriptor_running_queue_copy = copy.copy(self.task_descriptor_running_queue)

        # iterates over all the task descriptors running in the task descriptor running queue
        for task_descriptor_running in task_descriptor_running_queue_copy:
            # stops the running task descriptor
            task_descriptor_running.stop_task([])

    def create_worker_thread(self):
        """
        Creates a worker thread for the thread pool
        """

        # constructs a new worker thread
        worker_thread = WorkerThread(self)

        # start the worker thread
        worker_thread.start()

        # inserts the thread into the current list of threads
        self.worker_threads_list.append(worker_thread)

        # increments the current number of threads
        self.current_number_threads += 1

    def destroy_worker_thread(self):
        """
        Destroys a worker thread for the thread pool.
        """

        # creates a worker thread task to stop a thread
        worker_thread_task = WorkerThreadTask(STOP_THREAD_TASK_TYPE, ())

        # inserts the worker thread task into the task queue
        self.insert_worker_thread_task(worker_thread_task, False)

    def notify_thread_destroyed(self, worker_thread):
        """
        Notifies the thread pool about the thread destruction.

        @type worker_thread: WorkerThread
        @param worker_thread: The worker thread to be notified about destruction.
        """

        # in case the worker thread exists in the current list of threads
        if worker_thread in self.worker_threads_list:
            # removes the worker thread from the current list of threads
            self.worker_threads_list.remove(worker_thread)

        # increments the current number of threads
        self.current_number_threads -= 1

    def refresh_thread_pool_size(self, increment_size = True):
        """
        Refreshes the thread pool size, growing it if necessary.

        @type increment_size: bool
        @param increment_size: The increment of decrement thread pool size value.
        """

        # in case the current scheduling algorithm is dynamic scheduling
        if self.scheduling_algorithm == DYNAMIC_SCHEDULING_ALGORITHM:
            # in case increment size is active
            if increment_size:
                # retrieves the length of the task queue
                task_queue_length = len(self.task_queue)

                # calculates the required number of threads
                required_threads = self.busy_threads + task_queue_length

                # in case the number of current threads is less or equal
                # than the the number of required threads
                if self.current_number_threads <= required_threads:
                    # in case the current number of threads is less
                    # than the maximum number of threads
                    if self.current_number_threads < self.maximum_number_threads:
                        # prints a debug message about the thread pool grow
                        self.logger.debug("Thread pool (%s) grown" % self.name)

                        # creates a new worker thread
                        self.create_worker_thread()
            else:
                # in case the current number of threads is greater that the default number
                if self.current_number_threads > self.number_threads:
                    # retrieves the length of the task queue
                    task_queue_length = len(self.task_queue)

                    # calculates the required number of threads
                    required_threads = self.busy_threads + task_queue_length

                    # in case the current number of threads is greater than the number
                    # of required threads
                    if self.current_number_threads > required_threads:
                        # prints a debug message about the thread pool shrink
                        self.logger.debug("Thread pool (%s) shrinked" % self.name)

                        # retrieves the task queue size
                        task_queue_size = len(self.task_queue)

                        # retrieves the difference between the current number of threads
                        # and the busy threads (non busy threads) plus the size of the task queue
                        difference_threads = self.current_number_threads - self.busy_threads - task_queue_size

                        # retrieves the difference between the current number of threads and the default number of threads
                        difference_current_threads_and_number_threads = self.current_number_threads - self.number_threads

                        # in case the first difference is bigger than the second
                        if difference_threads > difference_current_threads_and_number_threads:
                            number_threads_destroy = difference_current_threads_and_number_threads
                        else:
                            number_threads_destroy = difference_threads

                        # destroys the defined number of threads
                        for _n_thread_destroy in range(number_threads_destroy):
                            # destroys a worker thread
                            self.destroy_worker_thread()

    def insert_task(self, task_descriptor, start_method_args = []):
        """
        Inserts a new task into the thread pool.

        @type task_descriptor: TaskDescriptor
        @param task_descriptor: The descriptor of the task to be inserted.
        @type start_method_args: List
        @param start_method_args: The start method arguments.
        """

        # creates a worker thread task to start a task and inserts the
        # task descriptor and arguments as arguments
        worker_thread_task = WorkerThreadTask(
            START_TASK_TASK_TYPE,
            (task_descriptor, start_method_args)
        )

        # inserts the worker thread task into the task queue
        self.insert_worker_thread_task(worker_thread_task)

    def remove_task(self, task_descriptor, stop_method_args = []):
        """
        Removes a task from the thread pool.

        @type task_descriptor: TaskDescriptor
        @param task_descriptor: The descriptor of the task to be removed.
        @type stop_method_args: List
        @param stop_method_args: The stop method arguments.
        """

        # creates a worker thread task to stop a task and inserts the
        # task descriptor and arguments as arguments
        worker_thread_task = WorkerThreadTask(
            STOP_TASK_TASK_TYPE,
            (task_descriptor, stop_method_args)
        )

        # inserts the worker thread task into the task queue
        self.insert_worker_thread_task(worker_thread_task)

    def pause_task(self, task_descriptor, pause_method_args = []):
        """
        Pauses a task from the thread pool.

        @type task_descriptor: TaskDescriptor
        @param task_descriptor: The descriptor of the task to be paused.
        @type pause_method_args: List
        @param pause_method_args: The pause method arguments.
        """

        # creates a worker thread task to pause a task and inserts the
        # task descriptor and arguments as arguments
        worker_thread_task = WorkerThreadTask(
            PAUSE_TASK_TASK_TYPE,
            (task_descriptor, pause_method_args)
        )

        # inserts the worker thread task into the task queue
        self.insert_worker_thread_task(worker_thread_task)

    def resume_task(self, task_descriptor, resume_method_args = []):
        """
        Resumes a task from the thread pool.

        @type task_descriptor: TaskDescriptor
        @param task_descriptor: The descriptor of the task to be resumed.
        @type resume_method_args: List
        @param resume_method_args: The resume method arguments.
        """

        # creates a worker thread task to pause a task and inserts the
        # task descriptor and arguments as arguments
        worker_thread_task = WorkerThreadTask(
            RESUME_TASK_TASK_TYPE,
            (task_descriptor, resume_method_args)
        )

        # inserts the worker thread task into the task queue
        self.insert_worker_thread_task(worker_thread_task)

    def cancel_task(self, task_descriptor, stop_method_args = []):
        """
        Cancels a task from the thread pool.

        @type task_descriptor: TaskDescriptor
        @param task_descriptor: The descriptor of the task to be canceled.
        @type stop_method_args: List
        @param stop_method_args: The stop method arguments.
        """

        # creates a worker thread task to stop a task and inserts the task descriptor and arguments as arguments
        worker_thread_task = WorkerThreadTask(
            STOP_TASK_TASK_TYPE,
            (task_descriptor, stop_method_args)
        )

        # inserts the worker thread task into the task queue
        self.insert_worker_thread_task(worker_thread_task)

    def insert_worker_thread_task(self, worker_thread_task, insert_at_end = True):
        """
        Inserts a worker thread task into the task queue.

        @type worker_thread_task: WorkerThreadTask
        @param worker_thread_task: The worker thread task to
        inserted in the task queue.
        @type insert_at_end: bool
        @param insert_at_end: If the worker thread task is to be
        inserted at the end of the queue or not.
        """

        # refreshes the thread pool size
        self.refresh_thread_pool_size()

        self.task_condition.acquire()
        if insert_at_end:
            self.task_queue.append(worker_thread_task)
        else:
            self.task_queue.insert(0, worker_thread_task)
        self.task_condition.notify()
        self.task_condition.release()

    def insert_worker_thread_task_all(self, worker_thread_task, insert_at_end = True):
        """
        Inserts n worker thread tasks into the task queue (the
        same amount as the current number of active threads
        in the pool).

        @type worker_thread_task: WorkerThreadTask
        @param worker_thread_task: The worker thread task to
        inserted in the task queue.
        @type insert_at_end: bool
        @param insert_at_end: If the worker thread task is to be
        inserted at the end of the queue or not.
        """

        # iterates over the number of currently available threads
        for _n_thread in range(self.number_threads):
            self.task_condition.acquire()
            if insert_at_end:
                self.task_queue.append(worker_thread_task)
            else:
                self.task_queue.insert(0, worker_thread_task)
            self.task_condition.notify()
            self.task_condition.release()

    def remove_worker_thread_task(self, worker_thread_task):
        """
        Removes a worker thread task from the task queue.

        @type worker_thread_task: WorkerThreadTask
        @param worker_thread_task: The worker thread task to removed
        from the task queue.
        """

        # refreshes the thread pool size
        self.refresh_thread_pool_size()

        self.task_condition.acquire()
        if worker_thread_task in self.task_queue:
            self.task_queue.remove(worker_thread_task)
        self.task_condition.notify()
        self.task_condition.release()

class WorkerThread(threading.Thread):
    """
    The worker thread class.
    """

    thread_pool = None
    """ The thread pool associated with this worker tread """

    def __init__(self, thread_pool):
        """
        Constructor of the class

        @type thread_pool: ThreadPoolImplementation
        @param thread_pool: The thread pool to be associated with
        this worker tread.
        """

        threading.Thread.__init__(self)

        self.thread_pool = thread_pool

        self.daemon = True

    def run(self):
        """
        Starts the run of the thread.
        """

        # retrieves the thread pool
        thread_pool = self.thread_pool

        # retrieves the task queue from the thread pool
        task_queue = thread_pool.task_queue

        # retrieves the task descriptor running queue from the thread pool
        task_descriptor_running_queue = thread_pool.task_descriptor_running_queue

        # retrieves the task condition from the thread pool
        task_condition = thread_pool.task_condition

        # iterates continuously
        while True:
            # acquires the task condition
            task_condition.acquire()

            # iterates while the task queue is empty
            while not len(task_queue):
                # waits for the task condition
                task_condition.wait()

            # increments the number of busy threads
            thread_pool.busy_threads += 1

            # retrieves the worker thread task to process
            worker_thread_task = task_queue.pop(0)

            # releases the task condition
            task_condition.release()

            # retrieves the worker thread task type
            worker_thread_task_type = worker_thread_task.task_type

            # retrieves the worker thread task arguments
            worker_thread_task_arguments = worker_thread_task.task_arguments

            # in case the worker thread task type is start thread
            if worker_thread_task_type == START_THREAD_TASK_TYPE:
                pass
            # in case the worker thread task type is stop thread
            elif worker_thread_task_type == STOP_THREAD_TASK_TYPE:
                # decrements the number of busy threads
                thread_pool.busy_threads -= 1

                # notifies the thread pool about thread destruction
                thread_pool.notify_thread_destroyed(self)

                # returns the thread (finishing it)
                return
            # in case the worker thread task type is start task
            elif worker_thread_task_type == START_TASK_TASK_TYPE:
                # retrieves the task descriptor and the start method arguments
                task_descriptor, start_method_args = worker_thread_task_arguments

                # sets the worker thread for the task descriptor
                task_descriptor.set_worker_thread(self)

                # adds the task descriptor to the queue of running tasks descriptors
                task_descriptor_running_queue.append(task_descriptor)

                # starts the task represented by the task descriptor
                task_descriptor.start_task(start_method_args)

                # removes the task descriptor from the queue of running tasks descriptors
                task_descriptor_running_queue.remove(task_descriptor)
            # in case the worker thread task type is stop task
            elif worker_thread_task_type == STOP_TASK_TASK_TYPE:
                # retrieves the task descriptor and the stop method arguments
                task_descriptor, stop_method_args = worker_thread_task_arguments

                # stops the task represented by the task descriptor
                task_descriptor.stop_task(stop_method_args)
            # in case the worker thread task type is pause task
            elif worker_thread_task_type == PAUSE_TASK_TASK_TYPE:
                # retrieves the task descriptor and the pause method arguments
                task_descriptor, pause_method_args = worker_thread_task_arguments

                # pauses the task represented by the task descriptor
                task_descriptor.pause_task(pause_method_args)
            # in case the worker thread task type is resume task
            elif worker_thread_task_type == RESUME_TASK_TASK_TYPE:
                # retrieves the task descriptor and the resume method arguments
                task_descriptor, resume_method_args = worker_thread_task_arguments

                # resumes the task represented by the task descriptor
                task_descriptor.resume_task(resume_method_args)

            # decrements the number of busy threads
            thread_pool.busy_threads -= 1

            # refreshes the thread pool size shrinking it if necessary
            thread_pool.refresh_thread_pool_size(False)

class WorkerThreadTask:
    """
    The worker thread task class.
    """

    task_type = None
    """ The type of the work thread task """

    task_arguments = None
    """ The arguments of the work thread task """

    def __init__(self, task_type, task_arguments = None):
        """
        Constructor of the class

        @type task_type: String
        @param task_type: The type of the work thread task.
        @type task_arguments: List
        @param task_arguments: The arguments of the work thread task.
        """

        self.task_type = task_type
        self.task_arguments = task_arguments

class TaskDescriptor:
    """
    Class that describes a single task for a thread pool.
    """

    name = "none"
    """ The name of task """

    description = "none"
    """ The description of the task """

    start_method = None
    """ The start method of the task """

    stop_method = None
    """ The stop method of the task """

    pause_method = None
    """ The pause method of the task """

    resume_method = None
    """ The resume method of the task """

    worker_thread = None
    """ The worker thread for the task """

    status = TASK_STOPPED_STATUS
    """ The current status of the task """

    def __init__(self, name = "none", description = "none", start_method = None, stop_method = None, pause_method = None, resume_method = None):
        """
        Constructor of the class

        @type name: String
        @param name: The name of task.
        @type description: String
        @param description: The description of the task.
        @type start_method: Method
        @param start_method: The start method of the task.
        @type start_method: Method
        @param start_method: The stop method of the task.
        @type pause_method: Method
        @param pause_method: The pause method of the task.
        @type resume_method: Method
        @param resume_method: The resume method of the task.
        """

        self.name = name
        self.description = description
        self.start_method = start_method
        self.stop_method = stop_method
        self.pause_method = pause_method
        self.resume_method = resume_method

        self.status = TASK_STOPPED_STATUS

    def start_task(self, start_method_args):
        """
        Starts the task represented by this task descriptor.

        @type start_method_args: List
        @param start_method_args: The arguments for the start method.
        """

        # in case the task descriptor contains a valid start method
        if self.start_method:
            # calls the start method of the task descriptor
            self.start_method(*start_method_args)

        self.status = TASK_RUNNING_STATUS

    def stop_task(self, stop_method_args):
        """
        Stops the task represented by this task descriptor.

        @type stop_method_args: List
        @param stop_method_args: The arguments for the stop method.
        """

        # in case the task descriptor contains a valid stop method
        if self.stop_method:
            # calls the stop method of the task descriptor
            self.stop_method(*stop_method_args)

        self.status = TASK_STOPPED_STATUS

    def pause_task(self, pause_method_args):
        """
        Pauses the task represented by this task descriptor.

        @type pause_method_args: List
        @param pause_method_args: The arguments for the pause method.
        """

        # in case the task descriptor contains a valid pause method
        if self.pause_method:
            # calls the pause method of the task descriptor
            self.pause_method(*pause_method_args)

        self.status = TASK_PAUSED_STATUS

    def resume_task(self, resume_method_args):
        """
        Resumes the task represented by this task descriptor.

        @type resume_method_args: List
        @param resume_method_args: The arguments for the resume method.
        """

        # in case the task descriptor contains a valid resume method
        if self.resume_method:
            # calls the resume method of the task descriptor
            self.resume_method(*resume_method_args)

        self.status = TASK_RUNNING_STATUS

    def get_worker_thread(self):
        """
        Retrieves the worker thread for the task descriptor.

        @rtype: WorkerThread
        @return: The worker thread for the task.
        """

        return self.worker_thread

    def set_worker_thread(self, worker_thread):
        """
        Sets the worker thread for the task descriptor.

        @type worker_thread: WorkerThread
        @param worker_thread: The worker thread for the task.
        """

        self.worker_thread = worker_thread

    def get_status(self):
        """
        Retrieves the current task status for the task descriptor.

        @rtype: int
        @return: The current task status for the task descriptor.
        """

        return self.status

    def set_status(self, status):
        """
        Sets the current task status for the task descriptor.

        @type status: int
        @param status: The current task status for the task descriptor.
        """

        self.status = status
