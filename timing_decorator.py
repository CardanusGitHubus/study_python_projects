import time


class Benchmark:
    def __init__(self, number_of_runs=5):
        self.number_of_runs = number_of_runs

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, type, value, traceback):
        self.end = time.time()
        time_ = self.end - self.start
        print(f'Time of performing of function is {time_}')

    def __call__(self, function):
        def wrap(*args, **kwargs):
            avg_time = 0
            for i in range(self.number_of_runs):
                start = time.time()
                function(*args, **kwargs)  # callable function
                end = time.time()
                avg_time += (end - start)
            avg_time /= self.number_of_runs
            print(f'Average time of function {function} is {avg_time} for {self.number_of_runs} runs')

        return wrap


@Benchmark()  # можно передать аргумент number_of_runs, по умолчанию он равен 5
def fibonacci():
    seq = [1]
    f_i2 = 0
    f_i1 = 1
    _sum = 0
    for i in range(2, 100000):
        f_curr = f_i1 + f_i2
        f_i2 = f_i1
        f_i1 = f_curr
        seq.append(f_i2)
    return seq


fibonacci()


# with Benchmark() as b:  # закомментировать декоратор и вызов функции fibonacci
#     fibonacci()
