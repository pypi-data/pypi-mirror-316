__all__ = ("api_v1",)
from typing import Annotated, Optional

from fastapi import APIRouter, Query
from fastapi.responses import PlainTextResponse

from .collector import generate_predictions

api_v1 = APIRouter()


@api_v1.get("/virtualmachine/metrics", response_class=PlainTextResponse)
async def vm_metrics_endpoint(
    name: Annotated[list[str] | None, Query()] = None,
    steps: Optional[int] = 1,
    resolution: Optional[str] = "1m",
):
    """
    Retrieve predicted metrics for all active virtual machines.

    This endpoint fetches the latest predicted metrics for all active
    virtual machines.
    The predictions can be filtered by metric names, number of steps,
    and resolution.

    Parameters
    ----------
    name : list of str, optional
        A list of metric names to filter the predictions. Defaults to
        None.
    steps : int, optional
        The number of prediction steps to retrieve. Defaults to 1.
    resolution : str, optional
        The resolution of the predictions. Defaults to "1m".

    Returns
    -------
    PlainTextResponse
        The latest predicted metrics for the virtual machine.
    """
    latest_value = generate_predictions(
        entity="virtualmachine",
        metric_names=name,
        resolution=resolution,
        steps=steps,
    )
    return latest_value


@api_v1.get("/host/metrics", response_class=PlainTextResponse)
async def host_metrics_endpoint(
    name: Annotated[list[str] | None, Query()] = None,
    steps: Optional[int] = 1,
    resolution: Optional[str] = "1m",
):
    """
    Retrieve predicted metrics for all monitored hosts.

    This endpoint fetches the latest predicted metrics for all 
    monitored hosts.
    The predictions can be filtered by metric names, number of steps,
    and resolution.

    Parameters
    ----------
    name : list of str, optional
        A list of metric names to filter the predictions. Defaults to None.
    steps : int, optional
        The number of prediction steps to retrieve. Defaults to 1.
    resolution : str, optional
        The resolution of the predictions. Defaults to "1m".

    Returns
    -------
    PlainTextResponse
        The latest predicted metrics for the host.
    """
    latest_value = generate_predictions(
        entity="host", metric_names=name, resolution=resolution, steps=steps
    )
    return latest_value
