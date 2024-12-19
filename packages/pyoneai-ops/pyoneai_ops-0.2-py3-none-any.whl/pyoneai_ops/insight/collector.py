__all__ = ("generate_predictions",)
from abc import ABC, abstractmethod
from typing import Generator, Iterable, Literal

import pandas as pd
import prometheus_client
from prometheus_client.core import CollectorRegistry, GaugeMetricFamily
from pyoneai import Session
from pyoneai.core import (
    Entity,
    Host,
    HostState,
    One,
    VirtualMachine,
    VirtualMachineState,
)

from .config import get_config

_SupportedEntityes = Literal["virtualmachine", "host", "cluster"]


class MetricsCollector(ABC):
    """
    Abstract base class for collecting metrics predictions.

    This class defines the interface for collecting metrics predictions
    for different entities such as virtual machines and hosts. It
    provides methods to generate predictions and collect them in a
    format suitable for Prometheus.

    Parameters
    ----------
    session : Session
        The session object containing connection objects to OpenNebula
        components.
    metric_name : str
        The name of the metric to collect predictions for.
    resolution : str
        The resolution of the predictions.
    steps : int, optional
        The number of prediction steps to retrieve. Must be a positive
        integer. Defaults to 1.

    Attributes
    ----------
    metric_name : str
        The name of the metric to collect predictions for.
    resolution : str
        The resolution of the predictions.
    session : Session
        The session object containing connection objects to OpenNebula.
    predictions_nbr : int
        The number of prediction steps to retrieve.
    one : One
        Entity used for accessing information from OpenNebula.

    Raises
    ------
    ValueError
        If `steps` is not a positive integer.
    """

    def __init__(
        self,
        session: Session,
        metric_name: str,
        resolution: str,
        steps: int = 1,
    ):
        if not isinstance(steps, int) or steps < 1:
            raise ValueError("'steps' must be a positive integer")
        self.metric_name = metric_name
        self.resolution = resolution
        self.session = session
        self.predictions_nbr = steps
        self.one = One(self.session)

    @property
    @abstractmethod
    def export_name(self) -> str:
        """
        Abstract property to define the export name for the metric.

        Returns
        -------
        str
            The export name for the metric.
        """
        raise NotImplementedError

    @abstractmethod
    def iter_over_entities(self) -> Iterable[Entity]:
        """
        Abstract method to iterate over entities for which predictions
        are generated.

        Returns
        -------
        Iterable[Entity]
            An iterable of entities.
        """
        raise NotImplementedError

    @abstractmethod
    def generate_predictions(self, entity: Entity) -> dict:
        """
        Abstract method to generate predictions for a given entity.

        Parameters
        ----------
        entity : Entity
            The entity for which predictions are generated.

        Returns
        -------
        dict
            A dictionary of prediction horizons and their corresponding
            values.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def labels(self) -> list[str]:
        """
        Abstract property for Prometheus metric labels.

        Returns
        -------
        list of str
            The Prometheus labels for the metric.
        """
        raise NotImplementedError

    def collect(self) -> Generator[GaugeMetricFamily, None, None]:
        """
        Collect and yield metrics as Prometheus GaugeMetricFamily.

        This method gathers the metrics predictions for each entity and
        yields them as Prometheus GaugeMetricFamily objects, which can
        be used for monitoring and alerting purposes.

        Yields
        ------
        Generator[GaugeMetricFamily, None, None]
            The collected metrics as a generator of GaugeMetricFamily
            objects.
        """
        gauge = GaugeMetricFamily(
            self.export_name, self.export_name, labels=self.labels
        )
        for entity in self.iter_over_entities():
            predictions = self.generate_predictions(entity)
            for horizon, value in predictions.items():
                gauge.add_metric([str(entity.id), horizon], str(value))
        yield gauge


class BaseCollector(MetricsCollector):
    """
    Base class for collecting metrics predictions with a defined period.

    This class extends `MetricsCollector` and provides a method to
    define the period for which predictions are generated.
    """

    @property
    def period(self) -> str:
        """
        Period for predictions based on resolution and steps.

        Returns
        -------
        str
            The period for predictions.
        """
        return slice(
            pd.Timedelta(self.resolution),
            pd.Timedelta(self.resolution) * self.predictions_nbr,
            pd.Timedelta(self.resolution),
        )

    def generate_predictions(self, entity: Entity) -> dict:
        """
        Generate predictions for a given entity.

        Parameters
        ----------
        entity : Entity
            The entity for which predictions are generated.

        Returns
        -------
        dict
            A dictionary of prediction horizons and their corresponding
            values.
        """
        MINUTE_CHAR = "m"
        prediction_horizons = [
            f"+{int((pd.Timedelta(self.resolution) * i).total_seconds() // 60)}{MINUTE_CHAR}"
            for i in range(1, self.predictions_nbr + 1)
        ]
        predictions_values = (
            entity.metrics[self.metric_name][self.period].to_array().flatten()
        )
        return {
            horizon: value
            for horizon, value in zip(prediction_horizons, predictions_values)
        }


class VirtualMachineCollector(BaseCollector):
    """
    Collector for virtual machine metrics predictions.

    This class extends `BaseCollector` and provides methods to collect
    metrics predictions for virtual machines.
    """

    @property
    def export_name(self) -> str:
        """
        Export name for virtual machine metrics.

        Returns
        -------
        str
            The export name for virtual machine metrics.
        """
        return f"opennebula_vm_{self.metric_name}"

    @property
    def labels(self) -> list[str]:
        """
        Prometheus labels for virtual machine metrics.

        Returns
        -------
        list of str
            The Prometheus labels for virtual machine metrics.
        """
        return ["one_vm_id", "forecast"]

    def iter_over_entities(self) -> Iterable[VirtualMachine]:
        """
        Iterate over active virtual machines for predictions.

        Returns
        -------
        Iterable[VirtualMachine]
            An iterable of active virtual machines.
        """
        return self.one.vms[
            self.one.vms.metrics["state"]["0"] == VirtualMachineState.ACTIVE
        ]


class HostCollector(BaseCollector):
    """
    Collector for host metrics predictions.

    This class extends `BaseCollector` and provides methods to collect
    metrics predictions for hosts.
    """

    @property
    def export_name(self) -> str:
        """
        Export name for host metrics.

        Returns
        -------
        str
            The export name for host metrics.
        """
        return f"opennebula_host_{self.metric_name}"

    @property
    def labels(self) -> list[str]:
        """
        Prometheus labels for host metrics.

        Returns
        -------
        list of str
            The Prometheus labels for host metrics.
        """
        return ["one_host_id", "forecast"]

    def iter_over_entities(self) -> Iterable[Host]:
        """
        Iterates over monitored hosts for predictions.

        Returns
        -------
        Iterable[Host]
            An iterable of monitored hosts.
        """
        return self.one.hosts[
            self.one.hosts.metrics["state"]["0"] == HostState.MONITORED
        ]


class Registry:
    """
    Registry for managing metrics collectors and generating predictions.

    This class manages the registration of metrics collectors for
    different entities and generates the latest predictions using
    Prometheus.

    Parameters
    ----------
    entity : _SupportedEntityes
        The type of entity for which predictions are generated.
    metric_names : list of str, optional
        The names of the metrics to collect predictions for. Defaults
        to None.
    resolution : str
        The resolution of the predictions.
    steps : int
        The number of prediction steps to retrieve.

    Attributes
    ----------
    registry : CollectorRegistry
        The Prometheus collector registry.
    session : Session
        The session object containing connection objects to OpenNebula
        components.
    """

    registry: CollectorRegistry
    collector_class = {
        "virtualmachine": VirtualMachineCollector,
        "host": HostCollector,
    }

    def __init__(
        self,
        entity: _SupportedEntityes,
        metric_names: list[str] | None,
        resolution: str,
        steps: int,
    ):

        self.registry = CollectorRegistry()
        self.session = Session(get_config().config_path)
        if metric_names is None:
            # TODO: to update when the issue
            # https://github.com/OpenNebula/one-aiops/issues/390 is resolved
            metric_names = list(self.session.config.registry[entity].keys())

        collector_cls = self.collector_class[entity]

        for name in metric_names:
            self.registry.register(
                collector_cls(self.session, name, resolution, steps)
            )

    @property
    def latest(self) -> bytes:
        """
        Generate the latest predictions in Prometheus format.

        Returns
        -------
        bytes
            The latest predictions from registered collectors in
            Prometheus serialized format.
        """
        return prometheus_client.generate_latest(self.registry)


def generate_predictions(
    entity: _SupportedEntityes,
    metric_names: list[str] | None,
    resolution: str,
    steps: int,
) -> bytes:
    """
    Generate the latest metrics predictions for a specified entity.

    This function creates a `Registry` instance for the given entity
    and metric names, and retrieves the latest predictions in
    Prometheus format.

    Parameters
    ----------
    entity : _SupportedEntityes
        The type of entity for which predictions are generated. Must be
        one of "virtualmachine", "host", or "cluster".
    metric_names : list of str, optional
        The names of the metrics to collect predictions for. If None,
        defaults to all available metrics for the entity.
    resolution : str
        The resolution of the predictions.
    steps : int
        The number of prediction steps to retrieve.

    Returns
    -------
    bytes
        The latest predictions from registered collectors in Prometheus
        serialized format.
    """
    return Registry(entity, metric_names, resolution, steps).latest
