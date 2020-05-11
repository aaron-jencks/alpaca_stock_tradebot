import unittest

import tradebot.tests.cli as cli
import tradebot.tests.messaging_test as msg
import tradebot.tests.qsm as qsm
import tradebot.tests.state_saving as ss


def suite():
    st = unittest.TestSuite()
    st.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cli.CLITest))
    st.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(msg.MessagingTestCase))
    st.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(qsm.QSMTestCase))
    st.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(ss.StateTestCase))
    return st


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
