import time
from contextlib import contextmanager

from synth_sdk.tracing.abstractions import Event
from synth_sdk.tracing.decorators import _local, clear_current_event, set_current_event
from synth_sdk.tracing.events.store import event_store
from synth_sdk.tracing.local import instance_system_id_var, system_id_var


@contextmanager
def event_scope(event_type: str):
    """
    Context manager for creating and managing events.

    Usage:
        with event_scope("my_event_type"):
            # do stuff
    """
    # Check if we're in an async context
    try:
        import asyncio

        asyncio.get_running_loop()
        is_async = True
    except RuntimeError:
        is_async = False

    # Get instance_system_id from appropriate source
    instance_system_id = (
        instance_system_id_var.get()
        if is_async
        else getattr(_local, "instance_system_id", None)
    )
    system_id = (
        system_id_var.get()
        if is_async
        else getattr(_local, "system_id", None)
    )

    event = Event(
        instance_system_id=instance_system_id,
        event_type=event_type,
        opened=time.time(),
        closed=None,
        partition_index=0,
        agent_compute_steps=[],
        environment_compute_steps=[],
    )
    set_current_event(event)

    try:
        yield event
    finally:
        event.closed = time.time()
        clear_current_event(event_type)
        # Store the event if instance_system_id is available
        if instance_system_id:
            event_store.add_event(instance_system_id, system_id, event)
