import os


class AppDirHandler:

    @staticmethod
    def create_app_dir():
        os.makedirs(os.path.expanduser("~/.ovh_auto_dns_update"))
        ip_file_path = os.path.expanduser("~/.ovh_auto_dns_update/prev-ip.txt")
        with open(ip_file_path, "w") as f:
            f.write("")

    @staticmethod
    def app_dir_exists():
        return os.path.exists(os.path.expanduser("~/.ovh_auto_dns_update"))

    @staticmethod
    def get_app_dir_path():
        return os.path.expanduser("~/.ovh_auto_dns_update")

    @staticmethod
    def get_prev_ip_file_path():
        return os.path.join(AppDirHandler.get_app_dir_path(), "prev-ip.txt")

    @staticmethod
    def get_prev_ip():
        with open(AppDirHandler.get_prev_ip_file_path(), "r") as f:
            return f.read()
