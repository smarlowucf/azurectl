from account import Account

class StorageAccount(Account):
    def get_account_name(self):
        return self.read('storage_account_name')

    def get_account_key(self):
        return self.read('storage_account_key')
