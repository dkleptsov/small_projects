import concurrent.futures
# import multiprocessing
import time


def do_smth(sec):
    print(f"Sleeping {sec} second...")
    time.sleep(sec)
    return f"Done Sleeping {sec}..."


def main():
    start = time.perf_counter()
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(do_smth, reversed(range(7)))
        [print(x) for x in results]

        # results = [executor.submit(do_smth, x) for x in reversed(range(7))]
        # for r in concurrent.futures.as_completed(results):
        #     print(r.result())

        # f1 = executor.submit(do_smth, 1)
        # print(f1.result())

    print(f"Finished in {time.perf_counter() - start:.2f} seconds!")

    # p1 = multiprocessing.Process(target=do_smth, args=(2, "uuu"),
    # kwargs={"y":"ddd", "vv":"nnn"})
    # p2 = multiprocessing.Process(target=do_smth, args=[3, "fff","ccc"])
    # p1.start()
    # p2.start()
    # p1.join()
    # p2.join()


if __name__ == "__main__":
    main()