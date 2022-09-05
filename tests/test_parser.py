

import pytest

from jsonparse.parser import Parser


class TestParser:

    @pytest.fixture
    def parser_init(self):

        return Parser(stack_trace=True, queue_trace=True)

    @pytest.fixture
    def push_stack_one_str(self, parser_init):

        parser_init._stack_push('test-str-1')

    @pytest.fixture
    def push_stack_one_list_one_str_elem(self, parser_init):

        parser_init._stack_push(['test-list-1'])

    @pytest.fixture
    def push_stack_one_list_two_str_elem(self, parser_init):

        parser_init._stack_push(['test-list-1', 'test-list-2'])

    @pytest.fixture
    def push_stack_one_dict_one_str_num_elem(self, parser_init):

        parser_init._stack_push({'dict1-key1': 1})

    @pytest.fixture
    def pop_stack(self, parser_init):

        parser_init._stack_pop()

    # _stack_init
    def test_init_of_parser_stack(self, parser_init):

        assert parser_init.stack_ref == []

    # _stack_push
    def test_pushing_one_onto_empty_stack(self, parser_init):

        parser_init._stack_push('test-str-1')
        assert len(parser_init.stack_ref) == 1

    # _stack_pop
    def test_popping_one_off_empty_stack(self, parser_init):

        try:
            parser_init._stack_pop()
        except IndexError:
            assert True
        else:
            assert False
    
    def test_popping_one_off_stack_of_one(self, parser_init, push_stack_one_str):

        parser_init._stack_pop()
        assert parser_init.stack_ref == []

    # _stack_peak
    def test_peak_top_of_stack_with_zero_elem(self, parser_init):

        try:
            parser_init._stack_peak()
        except IndexError:
            assert True
        else:
            assert False

    def test_peak_top_of_stack_with_one_string(self, parser_init, push_stack_one_str):

        assert parser_init._stack_peak() == 'test-str-1'

    # _stack_size
    def test_stack_size_with_zero_elem(self, parser_init):

        assert parser_init._stack_size() == 0

    def test_stack_size_with_one_string(self, parser_init, push_stack_one_str):

        assert parser_init._stack_size() == 1

    # _stack_push_list_elem
    def test_list_parse_with_dict_as_elem(self, parser_init, push_stack_one_dict_one_str_num_elem):

        try:
            parser_init._stack_push_list_elem(parser_init._stack_pop())
        except TypeError:
            assert True
        else:
            assert False

    def test_list_parse_with_zero_elem(self, parser_init):

        parser_init._stack_push_list_elem([])
        assert parser_init._stack_size() == 0

    def test_list_parse_with_one_list_one_str_elem(self, parser_init, push_stack_one_list_one_str_elem):

        parser_init._stack_push_list_elem(parser_init._stack_pop())
        assert parser_init._stack_pop() == 'test-list-1'

    def test_list_parse_with_one_list_two_elem(self, parser_init, push_stack_one_list_two_str_elem):

        parser_init._stack_push_list_elem(parser_init._stack_pop())
        assert parser_init._stack_pop() == 'test-list-2'
        assert parser_init._stack_pop() == 'test-list-1'

    #_stack_all_key_values_in_dict
    def test_dict_parse_with_list_as_elem(self, parser_init, push_stack_one_list_one_str_elem):

        try:
            parser_init._stack_all_key_values_in_dict('', parser_init._stack_pop())
        except TypeError:
            assert True
        else:
            assert False

    def test_dict_parse_with_num_as_key(self, parser_init, push_stack_one_dict_one_str_num_elem):

        try:
            parser_init._stack_all_key_values_in_dict(123, parser_init._stack_pop())
        except TypeError:
            assert True
        else:
            assert False

    def test_dict_parse_with_dict_zero_elem_zero_key(self, parser_init):

        parser_init._stack_all_key_values_in_dict('', {})
        assert parser_init._stack_size() == 0

    def test_dict_parse_with_one_dict_correct_key(self, parser_init, push_stack_one_dict_one_str_num_elem):

        value_list = parser_init._stack_all_key_values_in_dict('dict1-key1', parser_init._stack_pop())
        assert value_list.pop() == 1

    def test_dict_parse_with_one_dict_incorrect_key(self, parser_init, push_stack_one_dict_one_str_num_elem):

        value_list = parser_init._stack_all_key_values_in_dict('wrong', parser_init._stack_pop())
        assert len(value_list) == 0

    # _stack_trace
    def test_stack_trace_empty_stack(self, parser_init):

        try:
            parser_init._stack_trace()
        except IndexError:
            assert True
        else:
            assert False
    
    def test_stack_trace_non_empty_stack(self, parser_init, push_stack_one_str):

        parser_init._stack_trace()

    # _queue_init
    def test_init_of_parser_queue(self, parser_init):

        assert parser_init.queue_ref == []
    
    # _queue_push
    def test_pushing_one_onto_empty_queue(self, parser_init):

        parser_init._queue_push('test-str-1')
        assert len(parser_init.queue_ref) == 1
