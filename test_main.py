import unittest

import tradebot.tests.cli as cli
import tradebot.tests.messaging_test as msg


def suite():
    st = unittest.TestSuite()
    st.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cli.CLITest))
    st.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(msg.MessagingTestCase))
    return st


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
