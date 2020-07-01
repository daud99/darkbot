from search.darkbot.monitoring import monitor

def main():
    m = monitor.Monitor(type="email")
    m.startMonitoring()