from omegaconf import OmegaConf
from .parser import ConfigParser 
from .sweeper import Sweeper
from .importer import ClassImporter
from .launcher import Launcher

def main():
    parser = ConfigParser()
    conf = parser.parse()

    sweeper = Sweeper(conf)
    confs = sweeper.sweep()

    importer = ClassImporter(conf.get('_cls_', None))
    cls = importer.import_class()

    dotlist = parser.parse_cli(return_dotlist=True)
    launcher = Launcher(cls, confs, ','.join(dotlist))
    launcher.launch()


if __name__ == '__main__':
    main()
