from browselite.src.automation import AutomationManager, SearchServiceType


def browse(query, service_name:SearchServiceType):
    manager = AutomationManager()
    result = manager.execute_search(query=query, service_name=service_name)
    return result

