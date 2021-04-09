from etl.GSheetsEtl import GSheetsEtl
def etl():
    print ('etl process started.')
    etl_instance= GSheetsEtl("https://foo_bar.com","c:/Users","GSheets","C:/Users/my.gdb")
    etl_instance.process()
