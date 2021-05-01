from etl.GSheetsEtl import GSheetsEtl
#script to activate help documentation
my_etl = GSheetsEtl({})

print(my_etl.__doc__)

help(my_etl)