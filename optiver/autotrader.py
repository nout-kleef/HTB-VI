import socket
import select
from MarketState import MarketState
from secrets import USERNAME, PASSWORD 

REMOTE_IP = "35.179.45.135"
UDP_ANY_IP = ""

# -------------------------------------
# EML code (EML is execution market link)
# -------------------------------------

EML_UDP_PORT_LOCAL = 8078
EML_UDP_PORT_REMOTE = 8001

eml_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
eml_sock.bind((UDP_ANY_IP, EML_UDP_PORT_LOCAL))


# -------------------------------------
# IML code (IML is information market link)
# -------------------------------------

IML_UDP_PORT_LOCAL = 7078
IML_UDP_PORT_REMOTE = 7001
IML_INIT_MESSAGE = "TYPE=SUBSCRIPTION_REQUEST"

iml_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
iml_sock.bind((UDP_ANY_IP, IML_UDP_PORT_LOCAL))


# -------------------------------------
# Auto trader
# -------------------------------------

def start_autotrader():
    subscribe()
    event_listener()


def subscribe():
    iml_sock.sendto(IML_INIT_MESSAGE.encode(),
                    (REMOTE_IP, IML_UDP_PORT_REMOTE))

def event_listener():
    """
    Wait for messages from the exchange and
    call handle_message on each of them.
    """
    marketStateESX = MarketState('ESX', 'ESX-FUTURE')
    marketStateSP = MarketState('SP', 'SP-FUTURE')
    while True:
        ready_socks, _, _ = select.select([iml_sock, eml_sock], [], [])
        for socket in ready_socks:
            data, addr = socket.recvfrom(1024)
            message = data.decode('utf-8')
            handle_message(message, marketStateESX, marketStateSP)

def place_order_if_eligible_sell(market, bid_price, volume):
    if market.isEligibleForTradeSell(bid_price):                                              
        send_order(feedcode,"SELL",bid_price,volume) 
        print("Selling {0} at: {1}, Volume: {2}".format(market.stock, bid_price, volume))                    

def place_order_if_eligble_buy(market, ask_price, volume):
    if market.isEligibleForTradeBuy(ask_price):
        send_order(market.feedcode,"BUY",ask_price,volume) 
        print("Buying {0} at: {1}, Volume: {2}".format(market.stock, ask_price, volume))                
    
"""
Adds entry to market. 
Calls place_order_if_eligible_sell
Calls place_order_if_eligble_buy
"""
def handle_server_message_for_marketState(market, bid_price, ask_price):
    add_entry_to_market(market)
    place_order_if_eligible_sell(market, bid_price, 0)
    place_order_if_eligble_buy(market, ask_price, 0)

def add_entry_to_market(market):      
    market.addEntry(bid_price, ask_price)
                                       
"""
Handles an entry message from the server [Either type: PRICE or TRADE]
Receives message and a reference to marketStateESX and marketStateSP
On message received from server its adding the entry to the appropriate market and checks if eiligble to open position.
If yes, it opens a position using open_position().
"""
def handle_message(message, marketStateESX, marketStateSP):
    comps = message.split("|")
    
    if len(comps) == 0:
        print(f"Invalid message received: {message}")
        return

    type = comps[0]

    if type == "TYPE=PRICE":

        feedcode = comps[1].split("=")[1]
        bid_price = float(comps[2].split("=")[1])
        bid_volume = int(comps[3].split("=")[1])
        ask_price = float(comps[4].split("=")[1])
        ask_volume = int(comps[5].split("=")[1])
        
        if feedcode == "SP-FUTURE":
            handle_server_message_for_marketState(marketStateSP, bid_price, ask_price)            

        if feedcode == "ESX-FUTURE":
            handle_server_message_for_marketState(marketStateESX, bid_price, ask_price)                    

        print(
            f"[PRICE] product: {feedcode} bid: {bid_volume}@{bid_price} ask: {ask_volume}@{ask_price}")

    if type == "TYPE=TRADE":

        feedcode = comps[1].split("=")[1]
        side = comps[2].split("=")[1]
        traded_price = float(comps[3].split("=")[1])
        traded_volume = int(comps[4].split("=")[1])

        print(
            f"[TRADE] product: {feedcode} side: {side} price: {traded_price} volume: {traded_volume}")

    if type == "TYPE=ORDER_ACK":

        if comps[1].split("=")[0] == "ERROR":
            error_message = comps[1].split("=")[1]
            print(f"Order was rejected because of error {error_message}.")
            return

        feedcode = comps[1].split("=")[1]
        traded_price = float(comps[2].split("=")[1])

        # This is only 0 if price is not there, and volume became 0 instead.
        # Possible cause: someone else got the trade instead of you.
        if traded_price == 0:
            print(f"Unable to get trade on: {feedcode}")
            return

        traded_volume = int(comps[3].split("=")[1])

        print(
            f"[ORDER_ACK] feedcode: {feedcode}, price: {traded_price}, volume: {traded_volume}")


def send_order(target_feedcode, action, target_price, volume):
    """
    Send an order to the exchange.
    :param target_feedcode: The feedcode, either "SP-FUTURE" or "ESX-FUTURE"
    :param action: "BUY" or "SELL"
    :param target_price: Price you want to trade at
    :param volume: Volume you want to trade at. Please start with 10 and go from there. Don't go crazy!
    :return:
    Example:
    If you want to buy  100 SP-FUTURES at a price of 3000:
    - send_order("SP-FUTURE", "BUY", 3000, 100)
    """
    order_message = f"TYPE=ORDER|USERNAME={USERNAME}|PASSWORD={PASSWORD}|FEEDCODE={target_feedcode}|ACTION={action}|PRICE={target_price}|VOLUME={volume}"
    print(f"[SENDING ORDER] {order_message}")
    eml_sock.sendto(order_message.encode(), (REMOTE_IP, EML_UDP_PORT_REMOTE))


# -------------------------------------
# Main
# -------------------------------------

if __name__ == "__main__":
    start_autotrader()
