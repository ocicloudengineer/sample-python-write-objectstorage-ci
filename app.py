import time
import random
import logging
import os
import oci

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# OCI Configuration (Resource Principal)
try:
    signer = oci.auth.signers.get_resource_principals_signer()
    object_storage = oci.object_storage.ObjectStorageClient(config={}, signer=signer)
    OBJECT_STORAGE_NAMESPACE = "axtd5xmm9rsu"
    BUCKET_NAME = "bucket-logs-ci"
    OBJECT_NAME_PREFIX = "app-log-"
    print(f"OCI client with resource principals created successfully.")

except Exception as e:
    print(f"Error initializing OCI client with resource principals: {e}")
    object_storage = None

def write_to_object_storage(message, log_count):
    """Writes a message to an object storage bucket."""
    if object_storage is None:
        print("Object Storage client not initialized. Logs will not be written to object storage")
        return

    object_name = f"{OBJECT_NAME_PREFIX}{log_count}.log"
    try:
        object_storage.put_object(
            namespace_name=OBJECT_STORAGE_NAMESPACE,
            bucket_name=BUCKET_NAME,
            object_name=object_name,
            put_object_body=message.encode("utf-8"),
        )
        print(f"Log written to Object Storage: {object_name}")
    except Exception as e:
        print(f"Error writing log to Object Storage: {e}")

def process_data():
    """Simulates a data processing task."""
    log_count = 0
    write_to_object_storage("Starting data processing...", log_count)
    log_count +=1
    #logging.info("Starting data processing...")
    try:
        for i in range(5):
            logging.info(f"Processing item {i + 1}...")
            time.sleep(random.uniform(0.5, 2))  # Simulate variable processing time
            if random.random() < 0.1:  # Simulate occasional errors
                raise ValueError(f"Error processing item {i + 1}")
            logging.info(f"Item {i + 1} processed successfully.")
        logging.info("Data processing complete.")
        return True
    except ValueError as e:
        logging.error(f"Data processing failed: {e}")
        return False
    except Exception as e:
        logging.critical(f"Unexpected error: {e}")
        return False

def main():
    """Main application function."""
    print("Application started.")
    result = process_data()

    if result:
        print("Application completed successfully.")
    else:
        print("Application completed with errors.")

    print("Application exiting.")

if __name__ == "__main__":
    main()
