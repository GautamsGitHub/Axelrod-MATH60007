from distutils.util import strtobool
from collections import namedtuple
import operator


def passes_boolean_filter(strategy, value, classifier):
    if isinstance(value, str):
        filter_value = strtobool(value)
    else:
        filter_value = value

    return strategy.classifier[classifier] == filter_value


def passes_operator_filter(strategy, value, classifier, operator):
    if isinstance(value, str):
        filter_value = int(value)
    else:
        filter_value = value

    classifier_value = strategy.classifier[classifier]
    if (isinstance(classifier_value, str) and
            classifier_value.lower() == 'infinity'):
        classifier_value = float('inf')

    return operator(classifier_value, filter_value)


def passes_in_list_filter(strategy, value, classifier):
    return value in strategy.classifier[classifier]


def passes_filterset(strategy, filterset):
    """
    Determines whether a given strategy meets the criteria defined in a
    dictionary of filters.

    Parameters
    ----------
        strategy : a descendant class of axelrod.Player
        filterset : dict
            mapping filter name to criterion.
            e.g.
                {
                    'stochastic': True,
                    'min_memory_depth': 2
                }

    Returns
    -------
        boolean

        True if the given strategy meets all the supplied criteria in the
        filterset, otherwise false.

    """

    # A dictionary mapping filter name (from the supplied filterset) to
    # the relevant function and arguments for that filter.
    FilterFunction = namedtuple('FilterFunction', 'function kwargs')
    filter_functions = {
        'stochastic': FilterFunction(
            function=passes_boolean_filter,
            kwargs={'classifier': 'stochastic'}),
        'long_run_time': FilterFunction(
            function=passes_boolean_filter,
            kwargs={'classifier': 'long_run_time'}),
        'manipulates_state': FilterFunction(
            function=passes_boolean_filter,
            kwargs={'classifier': 'manipulates_state'}),
        'manipulates_source': FilterFunction(
            function=passes_boolean_filter,
            kwargs={'classifier': 'manipulates_source'}),
        'inspects_source': FilterFunction(
            function=passes_boolean_filter,
            kwargs={'classifier': 'inspects_source'}),
        'min_memory_depth': FilterFunction(
            function=passes_operator_filter,
            kwargs={'classifier': 'memory_depth', 'operator': operator.ge}),
        'max_memory_depth': FilterFunction(
            function=passes_operator_filter,
            kwargs={'classifier': 'memory_depth', 'operator': operator.le}),
        'makes_use_of': FilterFunction(
            function=passes_in_list_filter,
            kwargs={'classifier': 'makes_use_of'})
    }

    # A list of boolean values to record whether the strategy passed or failed
    # each of the filters in the supplied filterset.
    passes_filters = []

    for filter, filter_function in filter_functions.items():

        if filterset.get(filter, None) is not None:
            kwargs = filter_function.kwargs
            kwargs['strategy'] = strategy
            kwargs['value'] = filterset[filter]
            passes_filters.append(filter_function.function(**kwargs))

    # Only return True if the strategy passes all the supplied filters
    return all(passes_filters)
