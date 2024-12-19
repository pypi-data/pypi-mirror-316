import xml.etree.ElementTree as ET

import pytest
import yaml

from pyoneai import One, TimeIndex
from pyoneai.core import (
    HostState,
    Metric,
    VirtualMachineLCMState,
    VirtualMachineState,
)


class TestSKDIntegration:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.one = One()
        self.entity_dict = {
            "one": lambda **kwargs: self.one,
            "virtualmachine": lambda vm_id=None, **kwargs: self.one.vms[vm_id],
            "host": lambda host_id=None, **kwargs: self.one.hosts[host_id],
            "datastore": lambda ds_id=None, **kwargs: self.one.datastores[
                ds_id
            ],
        }
        self.pool_dict = {
            "virtualmachine": self.one.vms,
            "host": self.one.hosts,
            "datastore": self.one.datastores,
        }
        self.registry_data = self.read_registry()

    def read_registry(self):
        with open("/etc/one/aiops/registry.yaml", "r") as file:
            return yaml.safe_load(file)

    def test_metrics_available(
        self, entity, metric, time_range, expected_data, vm_id, host_id, ds_id
    ):
        parts = time_range.split(":")
        entity_ = self.entity_dict[entity](
            vm_id=vm_id, host_id=host_id, ds_id=ds_id
        )
        if parts.__len__() == 3:
            metrics = entity_.metrics[metric][parts[0] : parts[1] : parts[2]]
        else:
            metrics = entity_.metrics[metric][parts[0]]
        assert len(metrics) == expected_data
        assert (
            not metrics.to_dataframe().isna().any().any()
        ), f"Filed {metrics}"

    def test_pool_metrics(self, time_range, expected_data):
        parts = time_range.split(":")
        for entity_str, metrics in self.registry_data.items():
            if entity_str in ("default", "one") or metrics is None:
                continue
            pool_ = self.pool_dict[entity_str]
            if entity_str == "virtualmachine":
                pool_ = pool_[
                    (pool_.metrics["state"]["0"] == VirtualMachineState.ACTIVE)
                ]
            for metric in metrics:
                if len(parts) == 3:
                    metric_data = pool_.metrics[metric][
                        parts[0] : parts[1] : parts[2]
                    ]
                else:
                    metric_data = pool_.metrics[metric][parts[0]]
                for k, v in metric_data:
                    assert len(v) == expected_data, (
                        f"Failed {entity_str} - {metric} - {time_range}. "
                        f"Expected {expected_data}, got {len(v)}"
                    )
                assert len(metric_data) == len(pool_.ids), (
                    f"Failed {entity_str} - {metric} - {time_range}. "
                    f"Expected {len(pool_.ids)}, got {len(metric_data)}"
                )

    def test_metrics_values(
        self, one_data, host_data, vm_data, ds_data, vm_id, host_id, ds_id
    ):
        one_metrics = ["oned_state", "scheduler_state", "flow_state"]
        for idx, metric in enumerate(one_metrics):
            metrics = self.one.metrics[metric]["0"].item()
            assert metrics == one_data[idx], (
                f"Failed 'One' - '{metric}' metric "
                f"Expected {one_data[idx]}, got {metrics}"
            )
        host_metrics = ["cpu_maximum_ratio", "cpu_ratio", "state"]
        for idx, metric in enumerate(host_metrics):
            metrics = self.one.hosts[host_id].metrics[metric]["0"].item()
            assert metrics == host_data[idx], (
                f"Failed 'Virtual Machine' - '{metric}' metric "
                f"Expected {host_data[idx]}, got {metrics}"
            )
        vm_metrics = ["lcm_state", "cpu_ratio", "cpu_vcpus", "mem_total_bytes"]
        for idx, metric in enumerate(vm_metrics):
            metrics = self.one.vms[vm_id].metrics[metric]["0"].item()
            assert metrics == vm_data[idx], (
                f"Failed 'Host' - '{metric}' metric "
                f"Expected {vm_data[idx]}, got {metrics}"
            )
        ds_metrics = ["total_bytes"]
        for idx, metric in enumerate(ds_metrics):
            metrics = self.one.datastores[ds_id].metrics[metric]["0"].item()
            metrics = metrics / (1024 * 1024)
            assert metrics == ds_data[idx], (
                f"Failed  'Datastore' - '{metric}' metric "
                f"Expected {ds_data[idx]}, got {metrics}"
            )

    def test_multivariate(self, vm_id, host_id, ds_id):
        time_ranges = [
            TimeIndex(slice("-3m", "0m", "1m")),
            TimeIndex(slice("-3m", "-1m", "1m")),
            TimeIndex(slice("+1m", "+3m", "1m")),
            TimeIndex(slice("0m", "+3m", "1m")),
            TimeIndex("0m"),
            TimeIndex("-1m"),
            TimeIndex("+1m"),
        ]
        for entity, metrics_list in self.registry_data.items():
            if entity == "default" or metrics_list is None:
                continue
            entity_ = self.entity_dict[entity](
                vm_id=vm_id, host_id=host_id, ds_id=ds_id
            )
            for idx, time_range in enumerate(time_ranges):
                current_metrics = entity_.metrics[metrics_list.keys()][
                    time_range
                ]
                df = current_metrics.to_dataframe()
                assert df.shape[1] == len(metrics_list), (
                    f"Failed {entity}, time range[{idx}] {time_range.values} "
                    f"Expected {len(metrics_list)}, got {df.shape[1]}"
                )
                null_values = df[df.isnull().any(axis=1)]
                if not null_values.empty:
                    null_columns = null_values.columns[
                        null_values.isnull().any()
                    ]
                    failed_data = null_values[null_columns]
                    fail_message = (
                        f"Failed {entity}, time range[{idx}] {time_range.values}\n"
                        f"Expected no null values. Found nulls in columns:\n"
                        f"{failed_data}\n"
                    )
                    raise AssertionError(fail_message)

    def test_latest_metrics(self, vm_id, host_id, ds_id):
        for entity_str, metrics in self.registry_data.items():
            # TODO: remove "one" when One has LatestMetricValues
            if entity_str in ("default", "one") or metrics is None:
                continue
            entity_ = self.entity_dict[entity_str](
                vm_id=vm_id, host_id=host_id, ds_id=ds_id
            )
            for metric_name in metrics:
                assert entity_.metrics[metric_name]["0"].item() == getattr(
                    entity_, metric_name
                ), f"Failed {entity_str} - {metric_name}"

    def test_pool_metric_object(self, vm_id, vm2_id):
        vm_metrics = self.registry_data["virtualmachine"].keys()
        pool_ = self.one.vms[
            (self.one.vms.metrics["state"]["0"] == VirtualMachineState.ACTIVE)
        ]
        metrics_dict = pool_.metrics[vm_metrics]["0"]
        assert len(metrics_dict.metrics.items()) == len(pool_.ids)

        entity_df = metrics_dict[vm_id].to_dataframe()
        assert entity_df.shape[0] == 1
        assert entity_df.shape[1] == len(vm_metrics)

        metric_df = metrics_dict[["cpu_usage", "state"]][vm_id].to_dataframe()
        assert metric_df.shape[0] == 1
        assert metric_df.shape[1] == 2

        combine = metrics_dict[[vm_id, vm2_id], ["cpu_usage", "state"]]
        assert len(combine.metrics) == 2
        assert combine.ids == {vm_id, vm2_id}

        combine_df = combine[vm2_id].to_dataframe()
        assert not combine_df.isnull().any().any()
        assert combine_df.index.is_monotonic_increasing

    def test_pool_filter(self, vm_id, host_id, host2_id, ds_id):
        pool_ = self.one.vms[
            (self.one.vms.metrics["state"]["0"] == VirtualMachineState.ACTIVE)
            & (self.one.vms.metrics["cpu_vcpus"]["0"] == 1)
            & (self.one.vms.metrics["host_id"]["0"] == host_id)
            & (
                self.one.vms.metrics["lcm_state"]["0"]
                == VirtualMachineLCMState.RUNNING
            )
        ]
        assert len(pool_.ids) == 1
        assert pool_.ids == {vm_id}

        pool_ = self.one.hosts[
            (self.one.hosts.metrics["state"]["0"] == HostState.MONITORED)
            & (self.one.hosts.metrics["cpu_ratio"]["0"] > 0)
            & (self.one.hosts.metrics["cpu_usage_ratio"]["0"] > 0)
            & (self.one.hosts.metrics["mem_usage_bytes"]["0"] > 0)
        ]
        assert len(pool_.ids) == 2
        assert pool_.ids == {host_id, host2_id}

        pool_ = self.one.datastores[
            (self.one.datastores.metrics["total_bytes"]["0"] > 0)
            & (self.one.datastores.metrics["free_bytes"]["0"] > 0)
            & (self.one.datastores.metrics["used_bytes"]["0"] > 0)
        ]
        assert len(pool_.ids) > 0
        assert ds_id in pool_.ids

    def test_vm_migration(self, vm_id, time_range, expected_data):
        parts = time_range.split(":")
        if parts.__len__() == 3:
            metrics = self.one.vms[vm_id].metrics["cpu_usage"][
                parts[0] : parts[1] : parts[2]
            ]
        else:
            metrics = self.one.vms[vm_id].metrics["cpu_usage"][parts[0]]
        assert expected_data == len(metrics)

    def test_vm_timestamps(self, vm_id):
        metrics = self.one.vms[vm_id].metrics["cpu_usage"]["-5m":"5m":"1m"]
        assert metrics.time_index.is_monotonic_increasing, "Not ordered"

    def test_vm_state(self, vm_id, state, expected_data):
        state_map = {
            "ACTIVE": VirtualMachineState.ACTIVE,
            "STOPPED": VirtualMachineState.STOPPED,
            "PENDING": VirtualMachineState.PENDING,
        }
        vm_list = self.one.vms[
            self.one.vms.metrics["state"]["0"] == state_map[state]
        ]
        assert len(vm_list._ids) == expected_data
        assert vm_id in vm_list._ids

    def test_metric_details(self, vm_id, host_id, ds_id):
        one_metric = self.one.metrics["oned_state"]["0"]
        host_metric = self.one.hosts[host_id].metrics["cpu_usage"]["0"]
        vm_metric = self.one.vms[vm_id].metrics["cpu_usage"]["0"]
        ds_metric = self.one.datastores[ds_id].metrics["total_bytes"]["0"]

        # Test DataFrame
        for metric, entity in zip(
            [one_metric, host_metric, vm_metric, ds_metric],
            ["one", "host", "vm", "datastore"],
        ):
            df = metric.to_dataframe()
            assert not df.empty
            assert df.shape[0] > 0
            assert df.shape[1] == 1
            assert df.index.is_monotonic_increasing

        # Test multivariate
        multivariate_vm_metric = Metric.multivariate(
            [
                self.one.vms[vm_id].metrics["cpu_usage"]["0"],
                self.one.vms[vm_id].metrics["state"]["0"],
            ]
        )
        multivariate_df = multivariate_vm_metric.to_dataframe()
        assert multivariate_df.shape[1] == 2
        null_values = multivariate_df[multivariate_df.isnull().any(axis=1)]
        if not null_values.empty:
            null_columns = null_values.columns[null_values.isnull().any()]
            failed_data = null_values[null_columns]
            fail_message = (
                f"Expected no null values. Found nulls in columns:\n"
                f"{failed_data}\n"
            )
            raise AssertionError(fail_message)

        # Test univariate
        univariate_metrics = multivariate_vm_metric.univariate()
        assert len(univariate_metrics) == 2
        for univ_metric, original_metric in zip(
            univariate_metrics, ["cpu_usage", "state"]
        ):
            df_univ = univ_metric.to_dataframe()
            assert df_univ.shape[1] == 1
            null_values = df_univ[df_univ.isnull().any(axis=1)]
            if not null_values.empty:
                null_columns = null_values.columns[null_values.isnull().any()]
                failed_data = null_values[null_columns]
                fail_message = (
                    f"Expected no null values. Found nulls in columns:\n"
                    f"{failed_data}\n"
                )
                raise AssertionError(fail_message)

    def test_metric_operations(self, vm_id):
        cpu_usage = self.one.vms[vm_id].metrics["cpu_usage"]["0"]

        # Test arithmetic operation
        multiplied_usage = 2 * cpu_usage
        multi_df = multiplied_usage.to_dataframe()
        assert multi_df.shape[1] == 1
        assert multi_df.index.equals(cpu_usage.to_dataframe().index)
        assert (multi_df.values == 2 * cpu_usage.to_dataframe().values).all()

        # Test comparison between two metrics
        comparison_metrics = multiplied_usage >= cpu_usage
        comparison_df = comparison_metrics.to_dataframe()
        assert comparison_df.shape[1] == 1
        assert comparison_df.index.equals(cpu_usage.to_dataframe().index)
        assert comparison_df.values.all()

    def test_sdk_info(
        self, host_data, vm_data, ds_data, vm_id, host_id, ds_id
    ):
        vm_sdk_info = ET.fromstring(self.one.vms[vm_id].get_info())
        vm_sdk_data = self.one.vms[vm_id].get_data()
        assert vm_sdk_data["LCM_STATE"] == str(vm_data[0])
        assert vm_sdk_info.find(".//LCM_STATE").text == str(vm_data[0])
        assert vm_sdk_data["TEMPLATE"]["CPU"] == str(vm_data[1])
        assert vm_sdk_info.find(".//TEMPLATE/CPU").text == str(vm_data[1])
        assert vm_sdk_data["TEMPLATE"]["VCPU"] == str(vm_data[2])
        assert vm_sdk_info.find(".//TEMPLATE/VCPU").text == str(vm_data[2])
        assert vm_sdk_data["TEMPLATE"]["MEMORY"] == str(
            int(vm_data[3] / (1024 * 1024))
        )
        assert vm_sdk_info.find(".//TEMPLATE/MEMORY").text == str(
            int(vm_data[3] / (1024 * 1024))
        )

        host_sdk_info = ET.fromstring(self.one.hosts[host_id].get_info())
        host_sdk_data = self.one.hosts[host_id].get_data()
        assert host_sdk_data["HOST_SHARE"]["TOTAL_CPU"] == str(
            int(host_data[0] * 100)
        )
        assert host_sdk_info.find(".//HOST_SHARE/TOTAL_CPU").text == str(
            int(host_data[0] * 100)
        )
        assert host_sdk_data["HOST_SHARE"]["CPU_USAGE"] == str(
            int(host_data[1] * 100)
        )
        assert host_sdk_info.find(".//HOST_SHARE/CPU_USAGE").text == str(
            int(host_data[1] * 100)
        )
        assert host_sdk_data["STATE"] == str(host_data[2])
        assert host_sdk_info.find(".//STATE").text == str(host_data[2])

        ds_sdk_info = ET.fromstring(self.one.datastores[ds_id].get_info())
        ds_sdk_data = self.one.datastores[ds_id].get_data()
        assert ds_sdk_data["TOTAL_MB"] == str(ds_data[0])
        assert ds_sdk_info.find(".//TOTAL_MB").text == str(ds_data[0])
