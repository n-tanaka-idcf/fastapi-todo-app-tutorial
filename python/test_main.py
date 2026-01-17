import runpy


def test_main_prints_hello(capsys):
    import main

    main.main()
    captured = capsys.readouterr()
    assert captured.out == "Hello from python!\n"


def test_running_as_script_prints_hello(capsys):
    runpy.run_path("main.py", run_name="__main__")

    captured = capsys.readouterr()
    assert captured.out == "Hello from python!\n"
