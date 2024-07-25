import whois
import validators

def domain_lookup(dom):
    if validators.domain(dom):

        try:
            dom_info = whois.whois(dom)
            return dom_info
        
        except:
            return f"{dom} isn't registered or legit"
        
    else:
            return f"Enter a proper domain"
        
domain_input = input("Enter a domain you wish to verify: ")
result = domain_lookup(domain_input)
print(result)