import time
import atexit
import json
import traceback
import uuid

L = {}
counter = 0

def get_stamp():
    return f"{ str(counter) }-{ str(uuid.uuid4()) }"

def debug_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            global counter
            global L
            stamp = get_stamp()
            L[stamp] = {}
            L[stamp]['function'] = f"{func.__name__}"
            L[stamp]['start_time'] = time.time()
            L[stamp]['calling_function'] = f'called by {func.__module__}'
            L[stamp]['arguments'] = f'args: {args}, kwargs: {kwargs}'
            result = func(*args, **kwargs)
            L[stamp]['execution_time'] = time.time() - L[stamp]['start_time']
            return result
        except Exception as E:
            stack_trace = traceback.format_exc()
            print(stack_trace)
            print(E)
            L[stamp]['exception'] = str(E)
            L[stamp]['trace'] = stack_trace
            save()
            #exit(1) #if the exception is caught here, it cannot be caught elsewhere.
            raise(E)
    return wrapper

def save(file_name="trace.json"):
    global L
    with open(file_name, "w") as out:
        out.write(json.dumps(L, indent=4, sort_keys=True))

atexit.register(save)