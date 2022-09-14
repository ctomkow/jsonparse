# Craig Tomkow
#
# Dynamically parse JSON objects via two main methods...
#
# key: find all values of one key (stack based)
# key_chain: find all values of an ordered key chain (queue based)
# key_value: find all key:value pairs and return the parent set(s)

# python imports
from typing import Union


class Parser:
    """
    The Parser class.

    Methods:

    __init__(stack_trace, queue_trace):
        Returns the Parser object.

    key(data, key):
        Returns a list of values that have the corresponding key.

    key_chain(data, keys):
        Returns a list of values that have the corresponding key chain.

    key_value(data, key, value):
        Returns a list of set(s) that contain the key value pair.
    """

    def __init__(self,
                 stack_trace: bool = False,
                 queue_trace: bool = False) -> None:
        """
        Instantiates a Parser object used to access the search methods.

        Keyword arguments:

        stack_trace -- Set this to get a stdout printout of the stack as data
                       is parsed. This must be a boolean value. Default False.
        queue_trace -- Set this to get a stdout printout of the queue as data
                       is parsed. This must be a boolean value. Default False.
        """

        self.stack_trace = stack_trace
        self.queue_trace = queue_trace
        self.stack_ref = self._stack_init()
        self.queue_ref = self._queue_init()

    # depth first search for all keys using a STACK
    def key(self, data: Union[dict, list], key: str) -> list:
        """
        Search JSON data that consists of key:value pairs for all instances of
        provided key. The data can have complex nested dictionaries and lists.
        If duplicate keys exist in the data (at any layer) all matching key
        values will be returned. Data is parsed using a depth first search
        with a stack.

        Keyword arguments:

        data -- The python object representing JSON data with key:value pairs.
                This could be a dictionary or a list.
        key  -- The key that will be searched for in the JSON data.
                The key must be a string.
        """

        if not self._valid_key_input(data, key):
            raise

        self.stack_ref = self._stack_init()  # init a new queue every request
        self._stack_push(data)
        self._stack_trace()

        value_list = []

        while self._stack_size() >= 1:

            elem = self._stack_pop()

            if type(elem) is list:
                self._stack_push_list_elem(elem)
            elif type(elem) is dict:
                value = self._stack_all_key_values_in_dict(key, elem)
                if value:
                    for v in value:
                        value_list.append(v)
            else:  # according to RFC 7159, valid JSON can also contain a
                # string, number, 'false', 'null', 'true'
                pass  # discard these other values as they don't have a key

        return value_list

    # breadth first search for ordered series of keys using a QUEUE
    def key_chain(self, data: Union[dict, list], keys: list) -> list:
        """
        Search JSON data that consists of key:value pairs for the first
        instance of provided key chain. The data can have complex nested
        dictionaries and lists. If duplicate key chains exist in the data,
        all key chain values will be returned. The data is parsed using
        breadth first search using a queue.

        Keyword arguments:

        data -- The python object representing JSON data with key:value pairs.
                This could be a dictionary or a list.
        keys -- A list of keys that will be searched for in the JSON data.
                The first key will be depth 1, second key depth 2, and so on.
                The ordering of the keys matter.
                The keys must be strings within a list.
                A wildcard '*' key(s) can be used to match any.
        """

        if not self._valid_key_chain_input(data, keys):
            raise

        self.queue_ref = self._queue_init()  # init a new queue every request
        self._queue_push(data)
        self._queue_trace()

        while len(keys) >= 1:

            # if key is not found, return empty list
            if self._queue_size() == 0 and len(keys) >= 1:
                return []

            queue_size_snapshot = self._queue_size()
            key_found = False

            while queue_size_snapshot >= 1:

                elem = self._queue_pop()

                if type(elem) is list:
                    self._queue_push_list_elem(elem)
                elif type(elem) is dict:
                    if self._queue_all_key_values_in_dict(keys[0], elem):
                        key_found = True
                else:  # according to RFC 7159, valid JSON can also contain a
                    # string, number, 'false', 'null', 'true'
                    pass  # discard these other values as they don't have a key

                queue_size_snapshot -= 1

            if key_found:
                keys.pop(0)

        return self.queue_ref

    def key_value(self,
                  data: Union[dict, list],
                  key: str,
                  value: Union[str, int, float, bool]) -> list:
        """
        Search JSON data that consists of key:value pairs for all instances of
        provided key and value pair. The parent set that contains the key:value
        pair will be returned. The data can have complex nested
        dictionaries and lists. If duplicate key and value pairs exist in
        the data (at any layer) all matching key and value pair set(s)
        that contain the key:value pair will be returned. Data is parsed
        using a depth first search with a stack.

        Keyword arguments:

        data -- The python object representing JSON data with key:value pairs.
                This could be a dictionary or a list.
        key  -- The key that will be searched for in the JSON data.
                The key must be a string.
        value -- The value that will be searched for in the JSON data.
                 The value must be a string, integer, float, or boolean.
        """

        if not self._valid_key_value_input(data, key, value):
            raise

        self.stack_ref = self._stack_init()  # init a new queue every request
        self._stack_push(data)
        self._stack_trace()

        value_list = []

        while self._stack_size() >= 1:

            elem = self._stack_pop()

            if type(elem) is list:
                self._stack_push_list_elem(elem)
            elif type(elem) is dict:
                if self._stack_all_key_and_value_in_dict(key, value, elem):
                    value_list.append(elem)
            else:  # according to RFC 7159, valid JSON can also contain a
                # string, number, 'false', 'null', 'true'
                pass  # discard these other values as they don't have a key

        return value_list

    # STACK operations

    def _stack_init(self) -> list:

        stack = []
        return stack

    def _stack_push(self, elem: Union[dict, list]) -> None:

        self.stack_ref.append(elem)

    def _stack_pop(self) -> Union[dict, list]:

        try:
            return self.stack_ref.pop()
        except IndexError:
            raise

    def _stack_peak(self) -> Union[dict, list]:

        try:
            return self.stack_ref[-1:][0]
        except IndexError:
            raise

    def _stack_size(self) -> int:

        return len(self.stack_ref)

    def _stack_push_list_elem(self, elem: list) -> None:

        if type(elem) is not list:
            raise TypeError

        if len(elem) <= 0:  # don't want empty list on the stack
            pass
        else:
            for e in elem:
                self._stack_push(e)
                self._stack_trace()

    def _stack_all_key_values_in_dict(self, key: str, elem: dict) -> list:

        value_list = []

        if type(elem) is not dict:
            raise TypeError
        elif type(key) is not str:
            raise TypeError

        if len(elem) <= 0:  # don't want an empty dict on the stack
            pass
        else:
            for e in elem:
                if e == key:
                    value_list.append(elem[e])
                else:
                    self._stack_push(elem[e])
                    self._stack_trace()
        return value_list

    def _stack_all_key_and_value_in_dict(
            self,
            key: str,
            value: Union[str, int, float, bool],
            elem: dict) -> bool:

        if type(elem) is not dict:
            raise TypeError
        elif type(key) is not str:
            raise TypeError
        elif not isinstance(value, (str, int, float, bool)):
            raise TypeError

        if len(elem) <= 0:  # don't want an empty dict on the stack
            pass
        else:
            for e in elem:
                if e == key and elem[e] == value:
                    return True
                else:
                    self._stack_push(elem[e])
                    self._stack_trace()
        return False

    def _stack_trace(self) -> None:

        if self.stack_trace:
            print("STACK DEPTH: {}".format(self._stack_size()))
            try:
                print(self._stack_peak())
            except IndexError:
                raise

    # QUEUE operations

    def _queue_init(self) -> list:

        queue = []
        return queue

    def _queue_push(self, elem: Union[dict, list]) -> None:

        self.queue_ref.append(elem)

    def _queue_pop(self) -> Union[dict, list]:

        try:
            return self.queue_ref.pop(0)
        except IndexError:
            raise

    def _queue_peak(self) -> Union[dict, list]:

        try:
            return self.queue_ref[0]
        except IndexError:
            raise

    def _queue_size(self) -> int:

        return len(self.queue_ref)

    def _queue_push_list_elem(self, elem: list) -> None:

        if type(elem) is not list:
            raise TypeError

        if len(elem) <= 0:  # don't want empty list in the queue
            pass
        else:
            for e in elem:
                self._queue_push(e)
                self._queue_trace()

    def _queue_all_key_values_in_dict(self, key: str, elem: dict) -> bool:

        found = False
        if type(elem) is not dict:
            raise TypeError
        elif type(key) is not str:
            raise TypeError

        if len(elem) <= 0:  # don't want an empty dict in the queue
            pass
        else:
            for e in elem:
                if e == key or key == '*':  # only push on matching key values
                    self._queue_push(elem[e])
                    self._queue_trace()
                    found = True
                else:
                    pass
        if found:
            return True
        else:
            return False

    def _queue_trace(self) -> None:

        if self.queue_trace:
            print("QUEUE DEPTH: {}".format(self._queue_size()))
            try:
                print(self._queue_peak())
            except IndexError:
                raise

    # Input validation

    def _valid_key_input(
            self,
            data: Union[dict, list],
            key: str) -> bool:

        if not isinstance(data, (dict, list)):
            raise TypeError
        elif not isinstance(key, str):
            raise TypeError
        elif not key:  # if key is an empty string
            raise ValueError
        return True

    def _valid_key_chain_input(
            self,
            data: Union[dict, list],
            keys: list) -> bool:

        if not isinstance(data, (dict, list)):
            raise TypeError
        elif not isinstance(keys, list):
            raise TypeError

        for k in keys:
            if not k:  # if key is an empty string
                raise ValueError
            if not isinstance(k, str):  # if key is not a string
                raise TypeError

        return True

    def _valid_key_value_input(
            self,
            data: Union[dict, list],
            key: str,
            value: Union[str, int, float, bool]) -> bool:

        if not isinstance(data, (dict, list)):
            raise TypeError
        elif not isinstance(key, str):
            raise TypeError
        elif not key:  # if key is an empty string
            raise ValueError
        elif not isinstance(value, (str, int, float, bool)):
            raise TypeError
        return True
