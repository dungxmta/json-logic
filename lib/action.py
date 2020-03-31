import time


def ignore(data):
    print("... -> ignore")
    time.sleep(0.1)
    return


def query(data):
    print("... -> query")
    time.sleep(0.2)
    # results = [1,2]
    results = [1]
    return results


def insert(data):
    print("... -> insert")
    time.sleep(0.5)
    return


def update(data):
    print("... -> update")
    time.sleep(0.5)
    return
