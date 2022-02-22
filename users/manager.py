class UserMananger:
    def type_check_busi_num(busi_num):
        try:
            busi_num = int(busi_num)
            return True
        except:
            return False
