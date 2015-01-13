from account import Account

class ServiceAccount(Account):
    def get_account_subscription_id(self):
        return self.read('subscription_id')

    def get_account_subscription_cert(self):
        return self.read('subscription_cert')
