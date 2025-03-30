import hashlib
import json
from time import time
from typing import List, Dict

class Block:
    def __init__(self, index: int, credentials: List[Dict], timestamp: float, previous_hash: str):
        self.index = index
        self.credentials = credentials
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        block_string = json.dumps(self.__dict__, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class AcademicBlockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.pending_credentials = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], time(), "0")
        self.chain.append(genesis_block)

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def add_credential(self, student_id: str, institution: str, degree: str, year: str):
        self.pending_credentials.append({
            'student_id': student_id,
            'institution': institution,
            'degree': degree,
            'year': year,
            'timestamp': time()
        })

    def mine_pending_credentials(self):
        block = Block(
            index=len(self.chain),
            credentials=self.pending_credentials,
            timestamp=time(),
            previous_hash=self.last_block.hash
        )
        self.chain.append(block)
        self.pending_credentials = []

    def verify_credential(self, student_id: str, institution: str, degree: str, year: str) -> bool:
        for block in self.chain:
            for credential in block.credentials:
                if (credential['student_id'] == student_id and
                    credential['institution'] == institution and
                    credential['degree'] == degree and
                    credential['year'] == year):
                    return True
        return False
