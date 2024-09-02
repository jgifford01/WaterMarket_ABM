from concurrent.futures import ProcessPoolExecutor, as_completed
import time
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(process)d - %(levelname)s - %(message)s')

def simple_task(n):
    logging.info(f"Starting task {n} in process {os.getpid()}")
    time.sleep(1)
    result = n * n
    logging.info(f"Completed task {n} with result {result}")
    return result

def parallel_processing():
    logging.info("Starting parallel processing...")
    start_time = time.time()
    with ProcessPoolExecutor() as executor:
        results = [executor.submit(simple_task, i) for i in range(5)]
        for future in as_completed(results):
            result = future.result()
            logging.info(f"Received result: {result}")
            print(f"Result: {result}")
    end_time = time.time()
    logging.info(f"Parallel processing took {end_time - start_time:.2f} seconds")

def single_threaded_processing():
    logging.info("Starting single-threaded processing...")
    start_time = time.time()
    results = [simple_task(i) for i in range(5)]
    for result in results:
        logging.info(f"Received result: {result}")
        print(f"Result: {result}")
    end_time = time.time()
    logging.info(f"Single-threaded processing took {end_time - start_time:.2f} seconds")

if __name__ == '__main__':
    logging.info("Starting comparison...")
    
    logging.info("Running parallel processing...")
    parallel_processing()
    
    logging.info("Running single-threaded processing...")
    single_threaded_processing()

    logging.info("Comparison complete.")

import os
print(f"Number of CPU cores: {os.cpu_count()}")