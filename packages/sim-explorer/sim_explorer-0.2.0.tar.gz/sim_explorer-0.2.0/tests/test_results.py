from datetime import datetime
from pathlib import Path

from sim_explorer.case import Cases, Results


def test_init():
    # init through existing results file
    file = Path(__file__).parent / "data" / "BouncingBall3D" / "test_results"
    print("FILE", file)
    res = Results(file=file)
    # assert res.res.jspath("$.header.file", Path, True).exists()
    print("DATE", res.res.jspath("$.header.dateTime", datetime, True).isoformat())
    assert res.res.jspath("$.header.dateTime", datetime, True).isoformat() == "1924-01-14T00:00:00"
    assert res.res.jspath("$.header.casesDate", datetime, True).isoformat() == "1924-01-13T00:00:00"
    # init making a new file
    cases = Cases(Path(__file__).parent / "data" / "BouncingBall3D" / "BouncingBall3D.cases")
    case = cases.case_by_name("base")
    res = Results(case=case)
    # assert res.res.jspath("$.header.file", Path, True).exists()
    assert isinstance(res.res.jspath("$.header.dateTime", datetime, True).isoformat(), str)
    assert isinstance(res.res.jspath("$.header.casesDate", datetime, True).isoformat(), str)


def test_add():
    cases = Cases(Path(__file__).parent / "data" / "BouncingBall3D" / "BouncingBall3D.cases")
    case = cases.case_by_name("base")
    res = Results(case=case)
    res._header_transform(tostring=True)
    res.add(time=0.0, comp=0, typ=0, refs=[6], values=(9.81,))
    # print( res.res.write( pretty_print=True))
    assert res.res.jspath("$['0.0'].bb.g") == 9.81


def test_plot_time_series(show):
    file = Path(__file__).parent / "data" / "BouncingBall3D" / "test_results"
    assert file.exists(), f"File {file} not found"
    res = Results(file=file)
    if show:
        res.plot_time_series(comp_var=["bb.x[2]", "bb.v[2]"], title="Test plot")


def test_inspect():
    file = Path(__file__).parent / "data" / "BouncingBall3D" / "test_case"
    res = Results(file=file)
    cont = res.inspect()
    assert cont["bb.e"]["len"] == 1, "Not a scalar??"
    assert cont["bb.e"]["range"][1] == 0.01, "Not at time 0.01??"
    assert cont["bb.e"]["info"]["description"] == "Coefficient of restitution"
    assert list(cont.keys()) == ["bb.e", "bb.g", "bb.x", "bb.v", "bb.x_b[0]"]
    assert cont["bb.x"]["len"] == 300
    assert cont["bb.x"]["range"] == [0.01, 3.0]
    assert cont["bb.x"]["info"]["description"] == "3D Position of the ball in meters"
    assert cont["bb.x"]["info"]["variables"] == (0, 1, 2), "ValueReferences"


def test_retrieve():
    file = Path(__file__).parent / "data" / "BouncingBall3D" / "test_results"
    res = Results(file=file)
    data = res.retrieve((("bb", "g"), ("bb", "e")))
    assert data == [[0.01, 9.81, 0.5]]
    data = res.retrieve((("bb", "x"), ("bb", "v")))
    assert len(data) == 300
    assert data[0] == [0.01, [0.01, 0.0, 39.35076771653544], [1.0, 0.0, -0.0981]]


if __name__ == "__main__":
    # retcode = pytest.main(["-rA", "-v", __file__, "--show", "True"])
    # assert retcode == 0, f"Non-zero return code {retcode}"
    import os

    os.chdir(Path(__file__).parent.absolute() / "test_working_directory")
    # test_retrieve()
    # test_init()
    # test_add()
    test_plot_time_series(show=True)
    # test_inspect()
