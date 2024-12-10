import sys, base64, unittest
from blockchain_parser.block import Block

class TestBlock(unittest.TestCase):
    def test_block(self):
        transaction_hex = '''
        010000006fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d6
        190000000000982051fd1e4ba744bbbe680e1fee14677ba1a3c3540bf7b1
        cdb606e857233e0e61bc6649ffff001d01e3629901010000000100000000
        00000000000000000000000000000000000000000000000000000000ffff
        ffff0704ffff001d0104ffffffff0100f2052a0100000043410496b538e8
        53519c726a2c91e61ec11600ae1390813a627c66fb8be7947be63c52da75
        89379515d4e0a604f8141781e62294721166bf621e73a82cbf2342c858ee
        ac00000000'''.replace('\n', '').replace(' ', '').strip()
        # transaction_hex = sys.argv[1]
        block = Block(base64.b16decode(transaction_hex.upper().encode()))
        t = block.transactions[0].inputs[0].script.operations
        print(t)

if __name__ == '__main__':
    unittest.main()
