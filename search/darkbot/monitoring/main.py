from search.darkbot.monitoring import monitor
import logging

logger = logging.getLogger(__name__)

def main(type="email"):
    '''
    The main controller of asset monitoring process creates an instance of given type and start monitoring

    :param type: The asset type you want to monitor
    :type type: str
    '''
    logger.debug("In main of monitoring")
    logger.debug("The arg pass to main = "+type)
    m = monitor.Monitor(type=type)
    m.startMonitoring()