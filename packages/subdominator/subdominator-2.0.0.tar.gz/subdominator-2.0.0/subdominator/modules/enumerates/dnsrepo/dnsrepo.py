from colorama import Fore, Style
import aiohttp
import sys
import re

bold = Style.BRIGHT
blue = Fore.BLUE
red = Fore.RED
white = Fore.WHITE
reset = Style.RESET_ALL

async def dnsrepo(domain, session, args):
    try:
        url = url = f"https://dnsrepo.noc.org/?domain={domain}"
        proxy= args.proxy if args.proxy else None
        async with session.get(url, timeout=args.timeout, proxy=proxy, ssl=False) as response:
            if response.status!=200:
                return
            data = await response.text()
            filterdomain = re.escape(domain)
            pattern = r'(?i)(?:https?://)?([a-zA-Z0-9*_.-]+\.' + filterdomain + r')'
            subdomains = re.findall(pattern, data)
            return subdomains
        
    except aiohttp.ServerConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Dnsrepo, due to Serverside Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Dnsrepo, due to Serverside Error", file=sys.stderr)
    except TimeoutError as e:
        if args.show_timeout_info:
            if not args.no_color: 
                print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Dnsrepo, due to Timeout Error", file=sys.stderr)    
            else:
                print(f"[INFO]: Timeout reached for Dnsrepo, due to Timeout Error", file=sys.stderr)
                
    except KeyboardInterrupt as e:
        quit()
        
    except aiohttp.ClientConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Dnsrepo, due to ClientSide connection Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Dnsrepo, due to Clientside connection Error", file=sys.stderr)
                    
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured at dnsrepo: {e}, {type(e)}{reset}", file=sys.stderr)