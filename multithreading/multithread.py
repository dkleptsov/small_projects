# import threading
import concurrent.futures
import time

start = time.perf_counter()


def do_smth(sec):
    print(f"Sleep {sec} second(s)!")
    time.sleep(sec)
    return f"Done sleeping {sec} second(s)"

with concurrent.futures.ThreadPoolExecutor() as executor:
    secs = [5, 4, 3, 2, 1]
    results = executor.map(do_smth, secs)
    for result in results:
        print(result)



    # results = [executor.submit(do_smth, sec) for sec in secs]
    # for f in concurrent.futures.as_completed(results):
    #     print(f.result())


# threads = []
# for _ in range(10):
#     t = threading.Thread(target=do_smth, args = [1.5])
#     t.start()
#     threads.append(t)

# for thread in threads:
#     thread.join()

print(f"Finished in {time.perf_counter() - start} seconds!")