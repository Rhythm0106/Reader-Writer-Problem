import threading
import time

class ReaderWriter:
    def __init__(self):
        self.rw_mutex = threading.Semaphore(1)  # Semaphore for writer access
        self.mutex = threading.Semaphore(1)     # Semaphore for mutual exclusion
        self.read_count = 0                     # Number of readers currently in critical section
        self.buffer = []                       
        self.user_input = ""
        self.input_lock = threading.Lock()      # Lock for user input synchronization
        self.finish_event = threading.Event()   # Event to finish current process
        self.completed_task = False             # Flag to track task completion

    def writer(self):
        while True:
            self.finish_event.wait()  # Wait until finish event is set
            self.input_lock.acquire()
            if self.user_input == "writer":
                print("Writer Entered")
                print("Other Reader and Writer are waiting ")
                self.rw_mutex.acquire()
                self.rw_mutex.release()
            self.input_lock.release()
            self.finish_event.clear()  # Clear finish event to allow next process
            time.sleep(1.0)  # Polling interval

    def reader(self):
        while True:
            self.finish_event.wait()  # Wait until finish event is set
            self.input_lock.acquire()
            if self.user_input == "reader":
                print("Reader entered")
                print("Writer is waiting")
                print("Other Reader can read this file.")
                self.mutex.acquire()
                self.read_count += 1
                if self.read_count == 1:
                    self.rw_mutex.acquire()  # First reader locks out writers
                self.mutex.release()
                # Reading operation (e.g., consuming an item from the buffer)
                time.sleep(1)  # Simulate reading time
                self.mutex.acquire()
                self.read_count -= 1
                if self.read_count == 0:
                    self.rw_mutex.release()  # Last reader releases writer lock
                self.mutex.release()
            self.input_lock.release()
            self.finish_event.clear()  # Clear finish event to allow next process
            time.sleep(1.0)  # Polling interval

    def get_user_input(self):
        input_count = 0  # Counter for user input prompts
        while True:
            if input_count < 2:
                user_input = input("Enter 'reader' to act as a reader or 'writer' to act as a writer: ")
            else:
                while True:
                    user_input = input("Enter 'completed' if the task is completed or 'not completed' otherwise: ")
                    if user_input == "completed":
                        print("Now readers or writers can enter.")
                        input_count = 0  # Reset input count for the next loop
                        break
                    elif user_input == "not completed":
                        print("Writer is still waiting...")
                        input_count = 0  # Reset input count for the next loop
                        continue
                    else:
                        print("Invalid input. Please enter 'completed' or 'not completed'.")
            if user_input == "reader" or user_input == "writer":
                self.input_lock.acquire()
                self.user_input = user_input
                self.input_lock.release()
                self.finish_event.set()  # Set finish event to start processing
                if input_count >= 2:
                    print("Waiting for the next input...")
                input_count += 1

if __name__ == "__main__":
    rw = ReaderWriter()

    # Create thread for getting user input
    input_thread = threading.Thread(target=rw.get_user_input)
    input_thread.start()

    # Create threads for writer and readers
    writer_thread = threading.Thread(target=rw.writer)
    writer_thread.start()

    reader_thread = threading.Thread(target=rw.reader)
    reader_thread.start()

    # Join threads to main thread
    input_thread.join()
    writer_thread.join()
    reader_thread.join()
