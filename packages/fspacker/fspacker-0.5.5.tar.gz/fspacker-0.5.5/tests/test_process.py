class TestProcess:
    def test_base_examples(self, base_examples, run_proc):
        assert run_proc(base_examples)

    def test_gui_examples(self, gui_examples, run_proc):
        assert run_proc(gui_examples)

    def test_math_examples(self, math_examples, run_proc):
        assert run_proc(math_examples)
