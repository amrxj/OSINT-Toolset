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
        
domain_input = domain_lookup(input("Enter a domain you wish to verify: "))

print(domain_input)