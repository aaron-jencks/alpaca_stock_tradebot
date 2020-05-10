import unittest

import tradebot.messaging.message as msg


class MessagingTestCase(unittest.TestCase):
    def test_mailman(self):
        print('Testing mailman join capability')
        handler = msg.MessageHandler('handler')
        handler.join()
        self.assertTrue(msg.MessageHandler.mailman is None)

    def test_receiver(self):
        handler1 = msg.MessageHandler('handler1', ['test1'])
        handler2 = msg.MessageHandler('handler2', ['test2'])

        handler1.send(msg.Message('test2'))

        m = handler2.receive()
        self.assertTrue(m is not None, 'Handler can receive others\' messages')
        handler1.join()

    def test_global(self):
        handler1 = msg.MessageHandler('handler1')
        handler2 = msg.MessageHandler('handler2')

        handler1.send(msg.Message('all'))

        m = handler2.receive()
        self.assertTrue(m is not None, 'Handler can receive global messages')
        handler1.join()

    def test_addressed(self):
        handler1 = msg.MessageHandler('handler1')
        handler2 = msg.MessageHandler('handler2')

        handler1.send(msg.AddressedMessage('handler2', 'all'))

        m = handler2.receive()
        self.assertTrue(m is not None, 'Handler can receive addressed messages')
        handler1.join()


if __name__ == '__main__':
    unittest.main()
