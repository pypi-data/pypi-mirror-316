import unittest
import random
import string

from atmst.all import MemoryBlockStore, NodeStore, NodeWrangler, mst_diff, very_slow_mst_diff
from atmst.mst.node import MSTNode
from cbrrr import CID


class MSTDiffTestCase(unittest.TestCase):
	def setUp(self):
		dummy_value = CID.cidv1_dag_cbor_sha256_32_from(b"value")

		bs = MemoryBlockStore()
		self.ns = NodeStore(bs)
		wrangler = NodeWrangler(self.ns)
		root = self.ns.get_node(None).cid

		random.seed(4) # chosen by fair dice roll
		self.included_rpaths = []
		for _ in range(1000):
			random_rpath = "".join([random.choice(string.ascii_lowercase + string.digits) for _ in range(10)])
			self.included_rpaths.append(random_rpath)
			root = wrangler.put_record(root, random_rpath, dummy_value)

	def test_inclusion_proof(self):
		pass

if __name__ == "__main__":
	unittest.main(module="tests.test_mst_proofs")
