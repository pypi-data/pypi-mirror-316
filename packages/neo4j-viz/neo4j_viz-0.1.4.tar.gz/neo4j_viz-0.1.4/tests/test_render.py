from pathlib import Path
from typing import Any

import pytest
from selenium import webdriver

from neo4j_viz import Node, Relationship, VisualizationGraph
from neo4j_viz.options import Layout

render_cases = {
    "default": {},
    "force layout": {"layout": Layout.FORCE_DIRECTED},
    "grid layout": {"layout": Layout.GRID},
}


@pytest.mark.parametrize("render_option", render_cases.values(), ids=render_cases.keys())
def test_basic_render(render_option: dict[str, Any], tmp_path: Path) -> None:
    nodes = [
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:0", caption="Person"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:6", caption="Product"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:11", caption="Product"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:12", caption="Product"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:1", caption="Person"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:7", caption="Product"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:8", caption="Product"),
    ]
    relationships = [
        Relationship(
            source="4:d09f48a4-5fca-421d-921d-a30a896c604d:0",
            target="4:d09f48a4-5fca-421d-921d-a30a896c604d:6",
            caption="BUYS",
        ),
        Relationship(
            source="4:d09f48a4-5fca-421d-921d-a30a896c604d:0",
            target="4:d09f48a4-5fca-421d-921d-a30a896c604d:11",
            caption="BUYS",
        ),
    ]

    VG = VisualizationGraph(nodes=nodes, relationships=relationships)

    html = VG.render(**render_option)

    file_path = tmp_path / "basic_render.html"

    with open(file_path, "w+") as the_file:
        the_file.write(html.data)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # avoid browser window popping up
    driver = webdriver.Chrome(options=chrome_options)
    # wait for page to render
    driver.implicitly_wait(3)

    driver.get(f"file://{file_path}")

    logs = driver.get_log("browser")  # type: ignore[no-untyped-call]

    severe_logs = [log for log in logs if log["level"] == "SEVERE"]

    assert not severe_logs, f"Severe logs found: {severe_logs}, all logs: {logs}"
