from typing import (
    Any, 
    Optional, 
    Callable, 
    Sequence, 
    Mapping,
)

def try2(
    main_func: Callable,
    main_args: Optional[Sequence | Any] = None,
    main_kwargs: Optional[Mapping] = None,
    default: Any = None
) -> Any:
    """
    wrapper for try-except so I can write them easily in one line

    Args:
        main_func (Callable): main function to try
        main_args (Optoinal[Sequence | Any]): *args that go into main_func
            Note: if you have just one argument, you can pass in one single argument
        main_kwargs (Optional[Mapping]): **kwargs that go into main)func
        default (Optional[Any]): value returned if exception found. defaults to None
    Returns:
        (Any) whatever main_func returns or return_value_on_exception
    """
    try:
        # handle fact that main_args can be a sequence or a singular value
        if main_args is None:
            main_args = []
        elif not isinstance(main_args, Sequence):
            main_args = [main_args]

        main_kwargs = main_kwargs or {}
        
        return main_func(*main_args, **main_kwargs)
    except Exception as e:
        return default