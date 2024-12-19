from main import Dhesend
from type import SendEmailPayload, WebhookEvent

def test_email(dhesend: Dhesend):
    """Test sending and retrieving emails."""
    params: SendEmailPayload = {
        "from_": "test@example.com",
        "to": ["some@example.com"],
        "subject": "Testing subject..."
    }
    
    res = dhesend.Email.send(params)
    if res["error"]:
        print(f"Error sending email: {res['error']}")
        return
    
    print(f"Successfully sent email: {res['data']}")
    
    res1 = dhesend.Email.get(res["data"]["id"])
    if res1["error"]:
        print(f"Error fetching email: {res1['error']}")
        return
    
    print(f"Successfully fetched email: {res1['data']}")

def test_domain(dhesend: Dhesend):
    """Test domain creation, listing, and deletion."""
    res = dhesend.Domain.create("google.com")
    if res["error"]:
        print(f"Error creating domain: {res['error']}")
        return
    
    print(f"Successfully created domain: {res['data']}")
    
    res1 = dhesend.Domain.list()
    if res1["error"]:
        print(f"Error listing domains: {res1['error']}")
        return
    
    print(f"Successfully listed domains: {res1['data']}")
    
    res2 = dhesend.Domain.delete(res["data"]["name"])
    if res2["error"]:
        print(f"Error deleting domain: {res2['error']}")
        return
    
    print(f"Successfully deleted domain: {res2['data']}")

def test_apikey(dhesend: Dhesend):
    """Test API key creation, listing, and deletion."""
    res = dhesend.Apikey.create("Messenger API Key")
    if res["error"]:
        print(f"Error creating API key: {res['error']}")
        return
    
    print(f"Successfully created API key: {res['data']}")
    
    res1 = dhesend.Apikey.list()
    if res1["error"]:
        print(f"Error listing API keys: {res1['error']}")
    else:
        print(f"Successfully listed API keys: {res1['data']}")
    
    res2 = dhesend.Apikey.delete(res["data"]["token"])
    if res2["error"]:
        print(f"Error deleting API key: {res2['error']}")
        return
    
    print(f"Successfully deleted API key: {res2['data']}")

def test_webhook(dhesend: Dhesend):
    """Test webhook creation, status updates, and deletion."""
    res = dhesend.Webhook.create(
        "https://1234.com", 
        [WebhookEvent.EMAIL_BOUNCED.value, WebhookEvent.EMAIL_COMPLAINT.value]
    )
    if res["error"]:
        print(f"Error creating webhook: {res['error']}")
        return
    
    print(f"Successfully created webhook: {res['data']}")

    res1 = dhesend.Webhook.refresh_secret(res["data"]["id"])
    if res1["error"]:
        print(f"Error refreshing webhook secret: {res1['error']}")
        return
    
    print(f"Successfully refreshed webhook secret: {res1['data']}")
    
    res2 = dhesend.Webhook.update_status(res["data"]["id"], "disabled")
    if res2["error"]:
        print(f"Error updating webhook status: {res2['error']}")
        return
    
    print(f"Successfully updated webhook status: {res2['data']}")
    
    res3 = dhesend.Webhook.list()
    if res3["error"]:
        print(f"Error listing webhooks: {res3['error']}")
        return
    
    print(f"Successfully listed webhooks: {res3['data']}")
    
    res4 = dhesend.Webhook.delete(res["data"]["id"])
    if res4["error"]:
        print(f"Error deleting webhook: {res4['error']}")
        return
    
    print(f"Successfully deleted webhook: {res4['data']}")

def start_test():
    dhesend = Dhesend("sdfhjksdfhksdhfksdfh")    
    print("\nStarting webhook tests...")
    test_webhook(dhesend)

if __name__ == "__main__":
    start_test()
