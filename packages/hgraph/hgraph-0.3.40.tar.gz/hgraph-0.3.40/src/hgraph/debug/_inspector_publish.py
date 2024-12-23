import logging
import os
import time
from collections import defaultdict
from datetime import datetime

import perspective
import psutil

from hgraph import Node, Graph
from hgraph.debug._inspector_state import InspectorState
from hgraph.debug._inspector_util import format_value, format_modified, format_scheduled


logger = logging.getLogger(__name__)


def process_tick(state: InspectorState, node: Node):
    start = time.perf_counter_ns()

    if item_id := state.node_subscriptions.get(node.node_id):
        v = item_id.find_item_on_graph(node.graph)
        str_id = item_id.to_str()
        state.tick_data[str_id] = dict(
            id=str_id,
            value=format_value(v),
            modified=format_modified(v),
            scheduled=format_scheduled(v)
        )

    for item_id in state.node_item_subscriptions.get(node.node_id, ()):
        v = item_id.find_item_on_graph(node.graph)
        str_id = item_id.to_str()
        state.tick_data[str_id] = dict(
            id=str_id,
            value=format_value(v),
            modified=format_modified(v),
            scheduled=format_scheduled(v)
        )

    state.inspector_time += (time.perf_counter_ns() - start) / 1_000_000_000


def process_graph(state: InspectorState, graph: Graph, publish_interval: float):
    start = time.perf_counter_ns()

    root_graph = state.observer.get_graph_info(())

    if graph.graph_id == ():
        # publish node stats
        for node_id, item_id in state.node_subscriptions.items():
            gi = state.observer.get_graph_info(node_id[:-1])
            if gi is not None:
                node_ndx = item_id.node
                state.perf_data.append(
                    dict(
                        id=item_id.to_str(),
                        evals=gi.node_eval_counts[node_ndx],
                        time=gi.node_eval_times[node_ndx] / 1_000_000_000,
                        of_graph=gi.node_eval_times[node_ndx] / gi.eval_time if gi.eval_time else None,
                        of_total=gi.node_eval_times[node_ndx] / root_graph.eval_time if root_graph.eval_time else None,
                    )
                )

        state.total_data["time"].append(datetime.utcnow())
        state.total_data["evaluation_time"].append(root_graph.graph.evaluation_clock.evaluation_time)
        state.total_data["cycles"].append(root_graph.eval_count)
        state.total_data["cycle_time"].append(root_graph.cycle_time)
        state.total_data["graph_time"].append(root_graph.eval_time)

        start = check_requests_and_publish(state, start)
    else:
        # not a root graph
        gi = state.observer.get_graph_info(graph.graph_id)
        if item_id := state.graph_subscriptions.get(graph.graph_id):
            parent_time = state.observer.get_graph_info(graph.parent_node.graph.graph_id).eval_time
            state.perf_data.append(
                dict(
                    id=item_id.to_str(),
                    timestamp=graph.parent_node.last_evaluation_time if graph.parent_node else None,
                    evals=gi.eval_count,
                    time=gi.eval_time / 1_000_000_000,
                    of_graph=gi.eval_time / parent_time if parent_time else None,
                    of_total=gi.eval_time / root_graph.eval_time if root_graph.eval_time else None,
                )
            )

    state.inspector_time += (time.perf_counter_ns() - start) / 1_000_000_000


def check_requests_and_publish(state: InspectorState, start: int = None, stats_period=2.5):
    if start is None:
        start_ = time.perf_counter_ns()

    from hgraph.debug._inspector_handler import handle_requests
    if state.last_request_process_time is None or (datetime.utcnow() - state.last_request_process_time).total_seconds() > 0.1:
        publish_values = handle_requests(state)
        state.last_request_process_time = datetime.utcnow()

        publish = state.last_publish_time is None or (datetime.utcnow() - state.last_publish_time).total_seconds() > stats_period
        if publish_values or publish:
            if start is not None:
                state.inspector_time += (time.perf_counter_ns() - start) / 1_000_000_000
                start = time.perf_counter_ns()
            publish_tables(state, include_stats=publish)
            state.inspector_time = 0.0

    if start is None:
        state.inspector_time += (time.perf_counter_ns() - start_) / 1_000_000_000

    return start


def publish_tables(state: InspectorState, include_stats=True):
    state.manager.update_table(
        "inspector",
        [i for i in state.value_data if i["id"] not in state.value_removals],
        state.value_removals
    )
    state.value_data = []

    state.manager.update_table(
        "inspector",
        [i for i in state.perf_data if i["id"] not in state.value_removals]
    )
    state.perf_data = []

    state.manager.update_table(
        "inspector",
        [i for i in state.tick_data.values() if i["id"] not in state.value_removals]
    )
    state.tick_data = {}

    state.value_removals = set()

    data = state.total_data
    if data["time"]:
        total_time = (state.total_data["time"][-1] - state.total_data_prev.get("time", datetime.min)).total_seconds()
        total_graph_time = (data["graph_time"][-1] - state.total_data_prev.get("graph_time", 0)) / 1_000_000_000
        lags = [(data["time"][i] - data["evaluation_time"][i]).total_seconds() for i in range(len(data["time"]))]

        proc = psutil.Process(os.getpid())
        readings = dict(
            time=data["time"][-1],
            evaluation_time=data["evaluation_time"][-1],
            cycles=(data["cycles"][-1] - state.total_data_prev.get("cycles", 0)) / total_time,
            avg_cycle=sum(data["cycle_time"]) / (len(data["time"]) * 1_000_000_000),
            max_cycle=max(data["cycle_time"]) / 1_000_000_000,
            graph_time=total_graph_time,
            graph_load=total_graph_time / total_time,
            avg_lag=sum(lags) / len(data["time"]), max_lag=max(lags),
            inspection_time=state.inspector_time / total_graph_time,
            memory=proc.memory_info().rss / (1024 * 1024),
            virt_memory=proc.memory_info().vms / (1024 * 1024),
        )

        state.manager.update_table("graph_performance", [readings])
        logger.info(f"performance: {readings}")

        state.total_data_prev = {k: v[-1] for k, v in data.items()}
        state.total_data = defaultdict(list)

    state.last_publish_time = datetime.utcnow()
