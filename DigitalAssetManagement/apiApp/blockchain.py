from django.shortcuts import render
import datetime
import hashlib
import json
from django.http import JsonResponse
from apiApp import models
from enum import Enum


class BlockChainTypes(Enum):
    CREATE = 'ASSET CREATE'
    EDIT = 'ASSET EDITTED'
    BID_ON = 'REQUESTED ON THE ASSET'
    BID_ACCEPT = 'REQUEST ACCEPTED'


class Blockchain:
    def __init__(self, product_id, type) -> None:
        self.product_id = product_id
        self.type = type

    def _create_block_structure(self, nonce=1, previous_hash=None, data=None):
        block = {
                 'timestamp': str(datetime.datetime.now()),
                 'nonce': nonce,
                 'data':data,
                 'previous_hash': previous_hash
                 }
        return block

    def _get_recent_block(self):
        try:
            return models.BlockChainModel.objects.filter(product=self.product_id).order_by('-time_stamp').first().block
        except Exception as e:
            return "genesis_block"


    def _hash(self, block):
        str_obj = json.dumps(block, sort_keys=True)
        block_str = str_obj.encode()
        raw_hash = hashlib.sha256(block_str)
        hex_hash = raw_hash.hexdigest()
        return hex_hash
    
    # Mining a new block
    def mine_block(self, data):
        previous_block = self._get_recent_block()
        new_block = self._create_block_structure(previous_hash=previous_block, data=data)
        return self._hash(new_block)


