
import ai_search.main as ai

def update():
    import update
    return "updating..."
    
def request(text):
    # set the request
    ai.req = text
    ai.run()
    results = ai.result

    # print the results
    return results