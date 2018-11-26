from configobj import ConfigObj

c = ConfigObj("config.ini", encoding='UTF8')

print(c)