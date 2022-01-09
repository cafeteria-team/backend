from django.db import transaction
from .models import Store


class StoreManager:
    @transaction.atomic
    def create_store(self, store, user_id):
        new_store = Store()
        new_store.user_id = user_id
        new_store.addr = store["addr"]
        new_store.zip_code = store["zip_code"]
        new_store.detail_addr = store["detail_addr"]
        new_store.busi_num = store["busi_num"]
        new_store.save()

        return new_store
