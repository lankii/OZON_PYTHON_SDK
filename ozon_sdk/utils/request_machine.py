from ..request.abstract import Request
from typing import List
import concurrent.futures


class RequestMachine:

    def __init__(self, requests: List[Request], max_threads: int):
        """
        :param requests: SdkRequest objects list
        :param max_threads: How many threads we can use.
        """
        self.requests = requests
        self.max_threads = max_threads

    @staticmethod
    def __get_request_result(request: Request):
        return request.get_result()

    @staticmethod
    def array_division(array: list, division_by: int) -> list:
        """ Function divides one large list to few small lists of 'division_by' in each """
        count = len(array) // division_by + 1
        final_list = []
        start: int = 0
        finish: int = 1
        while finish <= count:
            final_list.append(array[start * division_by: finish * division_by])
            start += 1
            finish += 1
        return final_list

    def get_results(self, skip_fail_request: bool = False, replace_fail_data_to=None):
        """
        This SDK can return Exception after response if status_code != 200; with another reasons too.
        You can skipping this Exceptions. you should set 'skip_fail_request' to True
        and set variable 'replace_fail_data_to' for replace it instead failure data.
        :param skip_fail_request: bool
        :param replace_fail_data_to: JSON serializable object
        :return:
        """
        results = []
        futures = []
        request_arrays = self.array_division(self.requests, self.max_threads)
        for array in request_arrays:
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
                for request in array:
                    futures.append(executor.submit(self.__get_request_result, request=request))
                for future in concurrent.futures.as_completed(futures):
                    try:
                        results.append(future.result())
                    except Exception as e:
                        if skip_fail_request and replace_fail_data_to:
                            results.append(replace_fail_data_to)
                        else:
                            raise e
        return results
