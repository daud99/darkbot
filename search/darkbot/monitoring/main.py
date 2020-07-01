from search.darkbot.monitoring import monitor

def main(type="email"):
    m = monitor.Monitor(type=type)
    m.startMonitoring()