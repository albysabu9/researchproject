from django.db.models.signals import post_save
from django.dispatch import receiver
from apiApp import models
from apiApp.blockchain import Blockchain, BlockChainTypes
from apiApp.hyperledgersc import create_ledger

@receiver(post_save, sender=models.ProductModel)
def create_blockchain_entry(sender, instance, created,update_fields=None, **kwargs):
    if created:
        create_ledger(
            instance.p_owner.username, 
            "", 
            instance.p_price, 
            instance.p_name, 
            f"{instance.p_owner.username} created a new asset named {instance.p_name}"
        )
        block_chain_obj = Blockchain(product_id=instance.id, type=BlockChainTypes.CREATE.value)
        new_block = block_chain_obj.mine_block(instance.p_name)
        models.BlockChainModel.objects.create(product=instance, block=new_block, 
                                        type_of_block=BlockChainTypes.CREATE.value, 
                                        block_detail=\
                                        f"{instance.p_owner.username} created a new asset named {instance.p_name}")
        return True
    else:
        create_ledger(
            "", 
            instance.p_owner.username, 
            instance.p_price, 
            instance.p_name, 
            f"Owner accepted the request of user {instance.p_owner} for asset named {instance.p_name}"
        )
        if 'p_owner' in update_fields:
            block_chain_obj = Blockchain(product_id=instance.id, type=BlockChainTypes.EDIT.value)
            new_block = block_chain_obj.mine_block(instance.p_name)
            models.BlockChainModel.objects.create(product=instance, block=new_block, 
                                        type_of_block=BlockChainTypes.BID_ACCEPT.value, 
                                        block_detail=f"Owner  accepted the request of user {instance.p_owner} for asset named {instance.p_name}")
        else:
            create_ledger(
                instance.p_owner.username, 
                "", 
                instance.p_price, 
                instance.p_name, 
                f"Asset {instance.p_name} has been updated in the system"
            )
            block_chain_obj = Blockchain(product_id=instance.id, type=BlockChainTypes.EDIT.value)
            new_block = block_chain_obj.mine_block(instance.p_name)
            models.BlockChainModel.objects.create(product=instance, block=new_block, 
                                            type_of_block=BlockChainTypes.EDIT.value, 
                                            block_detail=f"Asset {instance.p_name} has been updated in the system")
        return True


@receiver(post_save, sender=models.BidModel)
def create_bid_blockchain_entry(sender, instance, created, **kwargs):
    if created:
        create_ledger(
            instance.user.username, 
            instance.product.p_owner.username, 
            1, 
            instance.product.p_name, 
            f"{instance.user.username} requested {instance.product.p_owner.username} for asset named {instance.product.p_name}"
        )
        block_chain_obj = Blockchain(product_id=instance.id, type=BlockChainTypes.CREATE.value)
        new_block = block_chain_obj.mine_block(f"{instance.product.p_owner.username}_{instance.product.p_name}")
        models.BlockChainModel.objects.create(product=instance.product, block=new_block, 
                                        type_of_block=BlockChainTypes.BID_ON.value, 
                                        block_detail=f"{instance.product.p_owner.username} raised a request on asset {instance.product.p_name} of amount {instance.price}")
        return True
    else:
        create_ledger(
            instance.product.p_owner.username, 
            instance.user.username, 
            1,  
            instance.product.p_name, 
            f"{instance.product.p_owner.username} accepted the request of user {instance.user.username} for asset {instance.product.p_name}"
        )
        block_chain_obj = Blockchain(product_id=instance.product, type=BlockChainTypes.EDIT.value)
        new_block = block_chain_obj.mine_block(instance.product.p_name)
        models.BlockChainModel.objects.create(product=instance, block=new_block, 
                                        type_of_block=BlockChainTypes.BID_ACCEPT.value, 
                                        block_detail=f"Owner accepted the request of user {instance.user.username} of amt {instance.product.p_name}")
        return True