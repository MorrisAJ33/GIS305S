from GSheetsEtl import GSheetsEtl

if __name__ == "__main__":
    etl_instance = GSheetsEtl("https://foo_bar.com","c:/Users","GSheets","C:/Users/my.gdb")

    etl_instance.process()