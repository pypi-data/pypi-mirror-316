import unittest
from computenestcli.base_log import load_process_config, setup_logging


class TestLoggingConfig(unittest.TestCase):

    def test_load_process_config(self):
        config = load_process_config()
        # 判断包含BuildService
        self.assertIn('BuildService', config)
        print(config)


if __name__ == '__main__':
    unittest.main()
