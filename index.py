import logging, os
from dotenv import load_dotenv
from pyzeebe import ZeebeWorker, Job
from libs.classifier import Classifier

load_dotenv() # Loading env vars
logging.basicConfig(format='%(levelname)s:%(message)s', 
    level=int(os.environ["LOGGING_LEVEL"]))

logging.info("Picking model: \"" + os.environ["MODEL"] + "\"")
classifier = Classifier.get_instance(os.environ["MODEL"])
logging.info("Classifier ready!")

def on_start(job: Job) -> Job:
    """
    on_start will be called before the task starts
    """ 
    logging.info("on_start: job " + str(job.key))
    logging.debug(job)
    if('sequence' not in job.variables):
        error_msg = f"Missing required variable 'sequence'"
        logging.error(error_msg)
        job.set_error_status(error_msg)
    if('candidate_labels' not in job.variables):
        error_msg2 = f"Missing required variable 'candidate_labels'"
        logging.error(error_msg2)
        job.set_error_status(error_msg2)    

    return job

def on_end(job: Job) -> Job:
    """
    on_end will be called after the task completed
    """     
    logging.info("on_end: job " + str(job.key))
    logging.debug(job)
    return job    

def on_error(exception: Exception, job: Job):
    """
    on_error will be called when the task fails
    """ 
    logging.error(exception)
    job.set_error_status(f"Failed to handle job {job}. Error: {str(exception)}")

# Create a zeebe worker
worker = ZeebeWorker(hostname=os.environ["HOSTNAME"], port=int(os.environ["PORT"]), 
    max_connection_retries=int(os.environ["MAX_CONNECTION_RETRIES"])) 
logging.info("Worker created!")

@worker.task(task_type=os.environ["TASK_NAME"], timeout=int(os.environ["TIMEOUT"]), 
    max_jobs_to_activate=int(os.environ["MAX_JOBS_TO_ACTIVATE"]), before=[on_start], 
    after=[on_end], exception_handler=[on_error])
def process_task(sequence: str, candidate_labels: list):
    logging.info("Processing task")
    return classifier.infer(sequence, candidate_labels)

# Now every time that a task with type example is called process_task will be called
worker.work() 