

import pytest

from jsons.jsons import JsonSearch


class TestJsonParser:

    @pytest.fixture
    def stack_init(self):

        return JsonSearch()

    @pytest.fixture
    def push_one_str(self, stack_init):

        stack_init._stack_push('test-str-1')

    @pytest.fixture
    def push_one_list_one_str_elem(self, stack_init):

        stack_init._stack_push(['test-list-1'])

    @pytest.fixture
    def push_one_list_two_str_elem(self, stack_init):

        stack_init._stack_push(['test-list-1', 'test-list-2'])

    @pytest.fixture
    def push_one_dict_one_str_num_elem(self, stack_init):

        stack_init._stack_push({'dict1-key1': 1})

    @pytest.fixture
    def pop(self, stack_init):

        stack_init._stack_pop()

    def test_init_of_parser_stack(self, stack_init):

        assert stack_init.stack_ref == []

    def test_pushing_one_onto_stack(self, stack_init):

        stack_init._stack_push('test-str-1')
        assert len(stack_init.stack_ref) == 1

    def test_popping_one_off_empty_stack(self, stack_init):

        try:
            stack_init._stack_pop()
        except IndexError:
            assert True
        else:
            assert False

    def test_peak_top_of_stack_with_zero_elem(self, stack_init):

        try:
            stack_init._stack_peak()
        except IndexError:
            assert True
        else:
            assert False

    def test_peak_top_of_stack_with_one_string(self, stack_init, push_one_str):

        assert stack_init._stack_peak() == 'test-str-1'

    def test_stack_size_with_zero_elem(self, stack_init):

        assert stack_init._stack_size() == 0

    def test_stack_size_with_one_string(self, stack_init, push_one_str):

        assert stack_init._stack_size() == 1

    def test_list_parse_with_dict_as_elem(self, stack_init, push_one_dict_one_str_num_elem):

        try:
            stack_init._stack_push_list_elem(stack_init._stack_pop())
        except TypeError:
            assert True
        else:
            assert False

    def test_list_parse_with_zero_elem(self, stack_init):

        stack_init._stack_push_list_elem([])
        assert stack_init._stack_size() == 0

    def test_list_parse_with_one_list_one_str_elem(self, stack_init, push_one_list_one_str_elem):

        stack_init._stack_push_list_elem(stack_init._stack_pop())
        assert stack_init._stack_pop() == 'test-list-1'

    def test_list_parse_with_one_list_two_elem(self, stack_init, push_one_list_two_str_elem):

        stack_init._stack_push_list_elem(stack_init._stack_pop())
        assert stack_init._stack_pop() == 'test-list-2'
        assert stack_init._stack_pop() == 'test-list-1'

    def test_dict_parse_with_list_as_elem(self, stack_init, push_one_list_one_str_elem):

        try:
            stack_init._stack_all_key_values_in_dict(stack_init._stack_pop(), '')
        except TypeError:
            assert True
        else:
            assert False

    def test_dict_parse_with_num_as_key(self, stack_init, push_one_dict_one_str_num_elem):

        try:
            stack_init._stack_all_key_values_in_dict(stack_init._stack_pop(), 666)
        except TypeError:
            assert True
        else:
            assert False

    def test_dict_parse_with_dict_zero_elem_zero_key(self, stack_init):

        stack_init._stack_all_key_values_in_dict({}, '')
        assert stack_init._stack_size() == 0

    def test_dict_parse_with_one_dict_correct_key(self, stack_init, push_one_dict_one_str_num_elem):

        value_list = stack_init._stack_all_key_values_in_dict(stack_init._stack_pop(), 'dict1-key1')
        assert value_list.pop() == 1

    def test_dict_parse_with_one_dict_incorrect_key(self, stack_init, push_one_dict_one_str_num_elem):

        value_list = stack_init._stack_all_key_values_in_dict(stack_init._stack_pop(), 'wrong')
        assert len(value_list) == 0
