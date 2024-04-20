from configparser import ConfigParser
from discogsparser import parser


parser = parser.DiscogsAPI()
cfg = ConfigParser()
cfg.read("config.conf")
print(parser.search_release("risk of rain 2")[0])