from omegaconf import OmegaConf
from .parser import ConfigParser 
from .sweeper import Sweeper
from .importer import import_class
from .launcher import Launcher

def main():
    parser = ConfigParser()
    conf = parser.parse()

    sweeper = Sweeper(conf)
    confs = sweeper.sweep()

    cls = import_class(conf.get('_cls_', None))

    dotlist = parser.parse_cli(return_dotlist=True)
    launcher = Launcher(cls, confs, ','.join(dotlist))
    launcher.launch()


if __name__ == '__main__':
    main()
