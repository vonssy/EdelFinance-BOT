from web3 import Web3
from web3.exceptions import TransactionNotFound
from curl_cffi import requests
from http.cookies import SimpleCookie
from eth_account import Account
from eth_account.messages import encode_defunct
from eth_utils import to_hex
from datetime import datetime, timezone
from colorama import *
import asyncio, random, time, uuid, json, os, pytz

wib = pytz.timezone('Asia/Jakarta')

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
]

class EdelFinance:
    def __init__(self) -> None:
        self.API_1 = "https://auth.privy.io/api/v1"
        self.API_2 = "https://new-backend-713705987386.europe-north1.run.app"

        self.RPC_URL = "https://base-mainnet.g.alchemy.com/v2/8tLSlmm95fjoFgamNTWgX"
        self.EXPLORER = "https://basescan.org/tx/"

        self.TOKENS = {
            "EDEL": {
                "address": "0xFb31f85A8367210B2e4Ed2360D2dA9Dc2D2Ccc95",
            },
            "mockUSD1": {
                "address": "0xAA465B5B06687eDe703437A7bF42A52A356c6e6c",
            },
            "mockSPY": {
                "address": "0x07C6a25739Ffe02b1dae12502632126fFA7497c2",
            },
            "mockUSDC": {
                "address": "0x66E8D8E1ba5cfaDB32df6CC0B45eA05Cc3d7201E",
            },
            "mockMETA": {
                "address": "0x960e1155741108C85A9BB554F79165df939E66BB",
            },
            "mockQQQ": {
                "address": "0xA0Aa9Dd11c6a770cEbB4772728538648F2de0F82",
            },
            "mockTSLA": {
                "address": "0x119505B31d369d5cF27C149A0d132D8Cdd99Cf5e",
            },
            "mockGOOGL": {
                "address": "0x367A8A0A55f405AA6980e44f3920463ABC6BB132",
            },
            "mockAAPL": {
                "address": "0xFBEfaE5034AA4cc7f3E9ac17E56d761a1bF211D4",
            },
            "mockAMZN": {
                "address": "0xA4a87f3F6b8aef9029f77edb55542cc32b8944D8",
            },
            "mockCRCL": {
                "address": "0xc1f76f5F8cab297a096Aec245b28B70B8822Bfa4",
            },
            "mockNVDA": {
                "address": "0x60C80e0086B1cFb0D21c9764E36d5bf469f7F158",
            },
            "mockPLTR": {
                "address": "0x6401999437FB8d6af9Df5AdEFe10D87F2AF3EC7d",
            },
            "mockHOOD": {
                "address": "0x856736DFf1579DDE3E35B278432c857Cb55Bc407",
            }
        }

        self.SPIN_CONTRACT_ADDRESS = "0x6fe7938cDeA9B04315B48EF60e325e19790CF5f6"
        self.REFER_CONTRACT_ADDRESS = "0x1d1aFC2d015963017bED1De13e4ed6c3d3ED1618"
        self.LENDING_POOL_ADDRESS = "0x0B72c91279A61cFcEc3FCd1BF30C794c69236e6e"

        self.CONTRACT_ABI = [
            {
                "inputs": [
                    { "internalType": "address", "name": "owner", "type": "address" },
                    { "internalType": "address", "name": "spender", "type": "address" }
                ],
                "name": "allowance",
                "outputs": [
                    { "internalType": "uint256", "name": "", "type": "uint256" }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    { "internalType": "address", "name": "spender", "type": "address" },
                    { "internalType": "uint256", "name": "value", "type": "uint256" }
                ],
                "name": "approve",
                "outputs": [
                    { "internalType": "bool", "name": "", "type": "bool" }
                ],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    { "internalType": "address", "name": "account", "type": "address" }
                ],
                "name": "balanceOf",
                "outputs": [
                    { "internalType": "uint256", "name": "", "type": "uint256" }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [
                    { "internalType": "uint8", "name": "", "type": "uint8" }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    { "internalType": "address", "name": "", "type": "address" }
                ],
                "name": "freeSpins",
                "outputs": [
                    { "internalType": "uint256", "name": "", "type": "uint256" }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    { "internalType": "address", "name": "", "type": "address" }
                ],
                "name": "lastSpinPurchaseTimestamp",
                "outputs": [
                    { "internalType": "uint256", "name": "", "type": "uint256" }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    { "internalType": "address", "name": "", "type": "address" }
                ],
                "name": "paidSpins",
                "outputs": [
                    { "internalType": "uint256", "name": "", "type": "uint256" }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "edelPrice",
                "outputs": [
                    { "internalType": "uint256", "name": "", "type": "uint256" }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    { "internalType": "enum IEdelFaucet.PaymentToken", "name": "paymentMethod", "type": "uint8" }, 
                    { "internalType": "address", "name": "referral", "type": "address" }
                ],
                "name": "buySpin",
                "outputs": [],
                "stateMutability": "payable",
                "type": "function"
            },
            {
                "inputs": [
                    { "internalType": "address", "name": "reserve", "type": "address" }, 
                    { "internalType": "uint256", "name": "amount", "type": "uint256" }, 
                    { "internalType": "address", "name": "onBehalfOf", "type": "address" }, 
                    { "internalType": "uint16", "name": "referralCode", "type": "uint16" }
                ],
                "name": "deposit",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            }
        ]

        self.HEADERS_1 = {}
        self.HEADERS_2 = {}
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}
        self.cookie_headers = {}
        self.token = {}

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Edel Finance {Fore.BLUE + Style.BRIGHT}Auto BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    def load_accounts(self):
        filename = "accounts.txt"
        try:
            with open(filename, 'r') as file:
                accounts = [line.strip() for line in file if line.strip()]
            return accounts
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Failed To Load Accounts: {e}{Style.RESET_ALL}")
            return None
        
    def load_proxies(self):
        filename = "proxy.txt"
        try:
            if not os.path.exists(filename):
                self.log(f"{Fore.RED + Style.BRIGHT}File {filename} Not Found.{Style.RESET_ALL}")
                return
            with open(filename, 'r') as f:
                self.proxies = [line.strip() for line in f.read().splitlines() if line.strip()]
            
            if not self.proxies:
                self.log(f"{Fore.RED + Style.BRIGHT}No Proxies Found.{Style.RESET_ALL}")
                return

            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Proxies Total  : {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(self.proxies)}{Style.RESET_ALL}"
            )
        
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Failed To Load Proxies: {e}{Style.RESET_ALL}")
            self.proxies = []

    def check_proxy_schemes(self, proxies):
        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxies.startswith(scheme) for scheme in schemes):
            return proxies
        return f"http://{proxies}"

    def get_next_proxy_for_account(self, account):
        if account not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[account] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[account]

    def rotate_proxy_for_account(self, account):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
        self.account_proxies[account] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy
    
    def generate_address(self, account: str):
        try:
            account = Account.from_key(account)
            address = account.address

            return address
        except Exception as e:
            return None
        
    def generate_login_payload(self, account: str, address: str, nonce: str):
        try:
            issued_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
            message = f"testnet.edel.finance wants you to sign in with your Ethereum account:\n{address}\n\nBy signing, you are proving you own this wallet and logging in. This does not initiate a transaction or cost any fees.\n\nURI: https://testnet.edel.finance\nVersion: 1\nChain ID: 8453\nNonce: {nonce}\nIssued At: {issued_at}\nResources:\n- https://privy.io"
            encoded_message = encode_defunct(text=message)
            signed_message = Account.sign_message(encoded_message, private_key=account)
            signature = to_hex(signed_message.signature)

            payload = {
                "message": message,
                "signature": signature,
                "chainId": "eip155:8453",
                "walletClientType": "metamask",
                "connectorType": "injected",
                "mode": "login-or-sign-up"
            }

            return payload
        except Exception as e:
            raise Exception(f"Generate Login Payload Failed: {str(e)}")
        
    def generate_spin_payload(self, account: str, address: str, is_free_spin: bool):
        try:
            timestamp = int(time.time()) * 1000

            message = json.dumps({
                "account": address,
                "useFreeSpin": is_free_spin,
                "timestamp": timestamp
            }, separators=(",", ":"))

            encoded_message = encode_defunct(text=message)
            signed_message = Account.sign_message(encoded_message, private_key=account)
            signature = to_hex(signed_message.signature)

            payload = {
                "signature": signature,
                "walletAddress": address,
                "timestamp": timestamp,
                "useFreeSpin": is_free_spin
            }

            return payload
        except Exception as e:
            raise Exception(f"Generate Spin Payload Failed: {str(e)}")
        
    def mask_account(self, account):
        try:
            mask_account = account[:6] + '*' * 6 + account[-6:]
            return mask_account
        except Exception as e:
            return None
        
    async def get_web3_with_check(self, address: str, use_proxy: bool, retries=3, timeout=60):
        request_kwargs = {"timeout": timeout}

        proxy = self.get_next_proxy_for_account(address) if use_proxy else None

        if use_proxy and proxy:
            request_kwargs["proxies"] = {"http": proxy, "https": proxy}

        for attempt in range(retries):
            try:
                web3 = Web3(Web3.HTTPProvider(self.RPC_URL, request_kwargs=request_kwargs))
                web3.eth.get_block_number()
                return web3
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(3)
                    continue
                raise Exception(f"Failed to Connect to RPC: {str(e)}")
        
    async def last_purchase_time(self, address: str, use_proxy: bool):
        try:
            web3 = await self.get_web3_with_check(address, use_proxy)

            spin_address = web3.to_checksum_address(self.SPIN_CONTRACT_ADDRESS)
            token_contract = web3.eth.contract(address=spin_address, abi=self.CONTRACT_ABI)
            timestamp = token_contract.functions.lastSpinPurchaseTimestamp(address).call()

            return timestamp
        except Exception as e:
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Status   :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} Failed to Fetch Last Spin Purchase Timestamp {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Message  :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
            )
            return None
        
    async def get_free_spins(self, address: str, use_proxy: bool):
        try:
            web3 = await self.get_web3_with_check(address, use_proxy)

            spin_address = web3.to_checksum_address(self.SPIN_CONTRACT_ADDRESS)
            token_contract = web3.eth.contract(address=spin_address, abi=self.CONTRACT_ABI)
            free_spin = token_contract.functions.freeSpins(address).call()

            return free_spin
        except Exception as e:
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Status   :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} Failed to Fetch Available Free Spins {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Message  :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
            )
            return None
        
    async def get_paid_spins(self, address: str, use_proxy: bool):
        try:
            web3 = await self.get_web3_with_check(address, use_proxy)

            spin_address = web3.to_checksum_address(self.SPIN_CONTRACT_ADDRESS)
            token_contract = web3.eth.contract(address=spin_address, abi=self.CONTRACT_ABI)
            paid_spin = token_contract.functions.paidSpins(address).call()

            return paid_spin
        except Exception as e:
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Status   :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} Failed to Fetch Available Paid Spins {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Message  :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
            )
            return None
        
    async def get_spin_price(self, address: str, use_proxy: bool):
        try:
            web3 = await self.get_web3_with_check(address, use_proxy)

            spin_address = web3.to_checksum_address(self.SPIN_CONTRACT_ADDRESS)
            token_contract = web3.eth.contract(address=spin_address, abi=self.CONTRACT_ABI)
            spin_price = token_contract.functions.edelPrice().call()

            price = web3.from_wei(spin_price, "ether")

            return price
        except Exception as e:
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Status   :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} Failed to Fetch Spin Price {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Message  :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
            )
            return None
        
    async def get_token_balance(self, address: str, token_address: str, use_proxy: bool):
        try:
            web3 = await self.get_web3_with_check(address, use_proxy)

            contract_address = web3.to_checksum_address(token_address)
            token_contract = web3.eth.contract(address=contract_address, abi=self.CONTRACT_ABI)
            balance = token_contract.functions.balanceOf(address).call()
            decimals = token_contract.functions.decimals().call()

            token_balance = balance / (10 ** decimals)

            return token_balance
        except Exception as e:
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Status   :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} Failed to Fetch EDEL Token Balance {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Message  :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
            )
            return None
    
    async def send_raw_transaction_with_retries(self, account, web3, tx, retries=5):
        for attempt in range(retries):
            try:
                signed_tx = web3.eth.account.sign_transaction(tx, account)
                raw_tx = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
                tx_hash = web3.to_hex(raw_tx)
                return tx_hash
            except TransactionNotFound:
                pass
            except Exception as e:
                self.log(
                    f"{Fore.BLUE + Style.BRIGHT}   Message  :{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} [Attempt {attempt + 1}] Send TX Error: {str(e)} {Style.RESET_ALL}"
                )
            await asyncio.sleep(2 ** attempt)
        raise Exception("Transaction Hash Not Found After Maximum Retries")

    async def wait_for_receipt_with_retries(self, web3, tx_hash, retries=5):
        for attempt in range(retries):
            try:
                receipt = await asyncio.to_thread(web3.eth.wait_for_transaction_receipt, tx_hash, timeout=300)
                return receipt
            except TransactionNotFound:
                pass
            except Exception as e:
                self.log(
                    f"{Fore.BLUE + Style.BRIGHT}   Message  :{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} [Attempt {attempt + 1}] Wait for Receipt Error: {str(e)} {Style.RESET_ALL}"
                )
            await asyncio.sleep(2 ** attempt)
        raise Exception("Transaction Receipt Not Found After Maximum Retries")
    
    async def approving_token(self, account: str, address: str, asset_address: str, spender_address: str, amount_to_wei: int, use_proxy: bool):
        try:
            web3 = await self.get_web3_with_check(address, use_proxy)
    
            token_contract = web3.eth.contract(address=asset_address, abi=self.CONTRACT_ABI)

            allowance = token_contract.functions.allowance(address, spender_address).call()
            if allowance < amount_to_wei:
                approve_data = token_contract.functions.approve(spender_address, 2**256 - 1)
                estimated_gas = approve_data.estimate_gas({"from": address})

                max_priority_fee = web3.to_wei(0.01, "gwei")
                max_fee = max_priority_fee

                approve_tx = approve_data.build_transaction({
                    "from": address,
                    "gas": int(estimated_gas * 1.2),
                    "maxFeePerGas": int(max_fee),
                    "maxPriorityFeePerGas": int(max_priority_fee),
                    "nonce": web3.eth.get_transaction_count(address, "pending"),
                    "chainId": web3.eth.chain_id,
                })

                tx_hash = await self.send_raw_transaction_with_retries(account, web3, approve_tx)
                receipt = await self.wait_for_receipt_with_retries(web3, tx_hash)
                block_number = receipt.blockNumber

                self.log(
                    f"{Fore.BLUE+Style.BRIGHT}   Approve  :{Style.RESET_ALL}"
                    f"{Fore.GREEN+Style.BRIGHT} Success {Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.BLUE+Style.BRIGHT}   Block    :{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {block_number} {Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.BLUE+Style.BRIGHT}   Tx Hash  :{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {tx_hash} {Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.BLUE+Style.BRIGHT}   Explorer :{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {self.EXPLORER}{tx_hash} {Style.RESET_ALL}"
                )
                await asyncio.sleep(random.uniform(3.0, 5.0))

            return True
        except Exception as e:
            raise Exception(f"Approving Token Contract Failed: {str(e)}")
        
    async def perform_buy_spin(self, account: str, address: str, spin_price: int, use_proxy: bool):
        try:
            web3 = await self.get_web3_with_check(address, use_proxy)

            edel_address = web3.to_checksum_address(self.TOKENS["EDEL"]["address"])
            spin_address = web3.to_checksum_address(self.SPIN_CONTRACT_ADDRESS)
            refer_address = web3.to_checksum_address(self.REFER_CONTRACT_ADDRESS)

            amount_to_wei = web3.to_wei(spin_price, "ether")

            await self.approving_token(account, address, edel_address, spin_address, amount_to_wei, use_proxy)

            spin_contract = web3.eth.contract(address=spin_address, abi=self.CONTRACT_ABI)

            buy_spin_data = spin_contract.functions.buySpin(2, refer_address)
            estimated_gas = buy_spin_data.estimate_gas({"from": address, "value": 0})

            max_priority_fee = web3.to_wei(0.01, "gwei")
            max_fee = max_priority_fee

            buy_spin_tx = buy_spin_data.build_transaction({
                "from": web3.to_checksum_address(address),
                "value": 0,
                "gas": int(estimated_gas * 1.2),
                "maxFeePerGas": int(max_fee),
                "maxPriorityFeePerGas": int(max_priority_fee),
                "nonce": web3.eth.get_transaction_count(address, "pending"),
                "chainId": web3.eth.chain_id,
            })

            tx_hash = await self.send_raw_transaction_with_retries(account, web3, buy_spin_tx)
            receipt = await self.wait_for_receipt_with_retries(web3, tx_hash)
            block_number = receipt.blockNumber

            return {
                "tx_hash": tx_hash, 
                "block": block_number
            }
        except Exception as e:
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Status   :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} Failed to Perform On-Chain Transaction {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Message  :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
            )
            return None
        
    async def perform_supply_token(self, account: str, address: str, token_address: str, amount: float, use_proxy: bool):
        try:
            web3 = await self.get_web3_with_check(address, use_proxy)

            asset_address = web3.to_checksum_address(token_address)
            pool_address = web3.to_checksum_address(self.LENDING_POOL_ADDRESS)

            token_contract = web3.eth.contract(address=asset_address, abi=self.CONTRACT_ABI)
            decimals = token_contract.functions.decimals().call()

            amount_to_wei = int(amount * (10 ** decimals))

            await self.approving_token(account, address, asset_address, pool_address, amount_to_wei, use_proxy)

            token_contract = web3.eth.contract(address=pool_address, abi=self.CONTRACT_ABI)

            deposit_data = token_contract.functions.deposit(asset_address, amount_to_wei, address, 0)
            estimated_gas = deposit_data.estimate_gas({"from": address})

            max_priority_fee = web3.to_wei(0.01, "gwei")
            max_fee = max_priority_fee

            deposit_tx = deposit_data.build_transaction({
                "from": web3.to_checksum_address(address),
                "gas": int(estimated_gas * 1.2),
                "maxFeePerGas": int(max_fee),
                "maxPriorityFeePerGas": int(max_priority_fee),
                "nonce": web3.eth.get_transaction_count(address, "pending"),
                "chainId": web3.eth.chain_id,
            })

            tx_hash = await self.send_raw_transaction_with_retries(account, web3, deposit_tx)
            receipt = await self.wait_for_receipt_with_retries(web3, tx_hash)
            block_number = receipt.blockNumber

            return {
                "tx_hash": tx_hash, 
                "block": block_number
            }
        except Exception as e:
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Status   :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} Failed to Perform On-Chain Transaction {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Message  :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
            )
            return None

    async def process_perform_buy_spin(self, account: str, address: str, spin_price: int, use_proxy: bool):
        onchain = await self.perform_buy_spin(account, address, spin_price, use_proxy)
        if not onchain: return False

        block_number = onchain["block"]
        tx_hash = onchain["tx_hash"]
    
        self.log(
            f"{Fore.BLUE+Style.BRIGHT}   Status   :{Style.RESET_ALL}"
            f"{Fore.GREEN+Style.BRIGHT} Success {Style.RESET_ALL}"
        )
        self.log(
            f"{Fore.BLUE+Style.BRIGHT}   Block    :{Style.RESET_ALL}"
            f"{Fore.WHITE+Style.BRIGHT} {block_number} {Style.RESET_ALL}"
        )
        self.log(
            f"{Fore.BLUE+Style.BRIGHT}   Tx Hash  :{Style.RESET_ALL}"
            f"{Fore.WHITE+Style.BRIGHT} {tx_hash} {Style.RESET_ALL}"
        )
        self.log(
            f"{Fore.BLUE+Style.BRIGHT}   Explorer :{Style.RESET_ALL}"
            f"{Fore.WHITE+Style.BRIGHT} {self.EXPLORER}{tx_hash} {Style.RESET_ALL}"
        )

        return True

    async def process_perform_supply_token(self, account: str, address: str, token_address: str, amount: float, use_proxy: bool):
        onchain = await self.perform_supply_token(account, address, token_address, amount, use_proxy)
        if not onchain: return False

        block_number = onchain["block"]
        tx_hash = onchain["tx_hash"]
    
        self.log(
            f"{Fore.BLUE+Style.BRIGHT}   Status   :{Style.RESET_ALL}"
            f"{Fore.GREEN+Style.BRIGHT} Success {Style.RESET_ALL}"
        )
        self.log(
            f"{Fore.BLUE+Style.BRIGHT}   Block    :{Style.RESET_ALL}"
            f"{Fore.WHITE+Style.BRIGHT} {block_number} {Style.RESET_ALL}"
        )
        self.log(
            f"{Fore.BLUE+Style.BRIGHT}   Tx Hash  :{Style.RESET_ALL}"
            f"{Fore.WHITE+Style.BRIGHT} {tx_hash} {Style.RESET_ALL}"
        )
        self.log(
            f"{Fore.BLUE+Style.BRIGHT}   Explorer :{Style.RESET_ALL}"
            f"{Fore.WHITE+Style.BRIGHT} {self.EXPLORER}{tx_hash} {Style.RESET_ALL}"
        )

        return True

    def print_question(self):
        while True:
            try:
                print(f"{Fore.GREEN + Style.BRIGHT}Select Option:{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}1. Lucky Spin{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}2. Supply Token{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}3. Run All Features{Style.RESET_ALL}")
                option = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2/3] -> {Style.RESET_ALL}").strip())

                if option in [1, 2, 3]:
                    option_type = (
                        "Lucky Spin" if option == 1 else 
                        "Supply Token" if option == 2 else 
                        "Run All Features"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}{option_type} Selected.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1, 2, or 3.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1, 2, or 3).{Style.RESET_ALL}")

        if option in [2, 3]:
            while True:
                try:
                    print(f"{Fore.GREEN + Style.BRIGHT}Select Supply Option:{Style.RESET_ALL}")
                    print(f"{Fore.WHITE + Style.BRIGHT}1. Supply 25%{Style.RESET_ALL}")
                    print(f"{Fore.WHITE + Style.BRIGHT}2. Supply 50%{Style.RESET_ALL}")
                    print(f"{Fore.WHITE + Style.BRIGHT}3. Supply 75%{Style.RESET_ALL}")
                    print(f"{Fore.WHITE + Style.BRIGHT}4. Supply 100%{Style.RESET_ALL}")
                    supply_option = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2/3/4] -> {Style.RESET_ALL}").strip())

                    if supply_option in [1, 2, 3, 4]:
                        supply_option_type = (
                            "Supply 25%" if option == 1 else 
                            "Supply 50%" if option == 2 else 
                            "Supply 75%" if option == 3 else 
                            "Supply 100%"
                        )
                        print(f"{Fore.GREEN + Style.BRIGHT}{supply_option_type} Selected.{Style.RESET_ALL}")
                        self.supply_option = supply_option
                        break
                    else:
                        print(f"{Fore.RED + Style.BRIGHT}Please enter either 1, 2, 3, or 4.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1, 2, 3, or 4).{Style.RESET_ALL}")

        while True:
            try:
                print(f"{Fore.WHITE + Style.BRIGHT}1. Run With Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}2. Run Without Proxy{Style.RESET_ALL}")
                proxy_choice = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2] -> {Style.RESET_ALL}").strip())

                if proxy_choice in [1, 2]:
                    proxy_type = (
                        "With" if proxy_choice == 1 else 
                        "Without"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}Run {proxy_type} Proxy Selected.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1 or 2.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1 or 2).{Style.RESET_ALL}")

        rotate_proxy = False
        if proxy_choice == 1:
            while True:
                rotate_proxy = input(f"{Fore.BLUE + Style.BRIGHT}Rotate Invalid Proxy? [y/n] -> {Style.RESET_ALL}").strip()

                if rotate_proxy in ["y", "n"]:
                    rotate_proxy = rotate_proxy == "y"
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter 'y' or 'n'.{Style.RESET_ALL}")

        return option, proxy_choice, rotate_proxy
    
    def ensure_ok(self, response):
        if not response.ok:
            raise Exception(f"HTTP {response.status_code}:{response.text}")

    async def check_connection(self, address: str, use_proxy: bool):
        proxy_url = self.get_next_proxy_for_account(address) if use_proxy else None
        proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
        try:
            response = await asyncio.to_thread(requests.get, url="https://api.ipify.org?format=json", proxies=proxies, timeout=30, impersonate="chrome120")
            self.ensure_ok(response)
            return True
        except Exception as e:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}Status:{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} Connection Not 200 OK {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
            )
        
        return None

    async def siwe_init(self, address: str, use_proxy: bool, retries=5):
        url = f"{self.API_1}/siwe/init"
        data = json.dumps({"address": address})
        headers = {
            **self.HEADERS_1[address],
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        await asyncio.sleep(random.uniform(0.5, 1.0))
        for attempt in range(retries):
            proxy_url = self.get_next_proxy_for_account(address) if use_proxy else None
            proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, data=data, proxies=proxies, timeout=120, impersonate="chrome120")
                self.ensure_ok(response)
                raw_cookies = response.headers.get_list('Set-Cookie')
                if raw_cookies:
                    cookie = SimpleCookie()
                    cookie.load("\n".join(raw_cookies))
                    cookie_string = "; ".join([f"{key}={morsel.value}" for key, morsel in cookie.items()])
                    self.cookie_headers[address] = cookie_string

                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Status:{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Init Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )

        return None
    
    async def siwe_authenticate(self, account: str, address: str, nonce: str, use_proxy: bool, retries=5):
        url = f"{self.API_1}/siwe/authenticate"
        data = json.dumps(self.generate_login_payload(account, address, nonce))
        headers = {
            **self.HEADERS_1[address],
            "Content-Length": str(len(data)),
            "Content-Type": "application/json",
            "Cookie": self.cookie_headers[address]
        }
        await asyncio.sleep(random.uniform(0.5, 1.0))
        for attempt in range(retries):
            proxy_url = self.get_next_proxy_for_account(address) if use_proxy else None
            proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, data=data, proxies=proxies, timeout=120, impersonate="chrome120")
                self.ensure_ok(response)
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Status:{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Authenticate Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )

        return None
    
    async def lucky_spin(self, account: str, address: str, is_free_spin: bool, use_proxy: bool, retries=5):
        url = f"{self.API_2}/lucky-spin/spin"
        data = json.dumps(self.generate_spin_payload(account, address, is_free_spin))
        headers = {
            **self.HEADERS_2[address],
            "Authorization": f"Bearer {self.token[address]}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json",
            "Cookie": self.cookie_headers[address]
        }
        await asyncio.sleep(random.uniform(0.5, 1.0))
        for attempt in range(retries):
            proxy_url = self.get_next_proxy_for_account(address) if use_proxy else None
            proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, data=data, proxies=proxies, timeout=120, impersonate="chrome120")
                self.ensure_ok(response)
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.BLUE+Style.BRIGHT}     Spin     :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Failed {Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.BLUE+Style.BRIGHT}     Message  :{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )

        return None
    
    async def process_check_connection(self, address: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}Proxy :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {proxy} {Style.RESET_ALL}"
            )

            check = await self.check_connection(address, use_proxy)
            if check: return True

            if rotate_proxy:
                proxy = self.rotate_proxy_for_account(address)
                await asyncio.sleep(1)
                continue

            return False

    async def process_login(self, account: str, address: str, use_proxy: bool, rotate_proxy: bool):
        is_valid = await self.process_check_connection(address, use_proxy, rotate_proxy)
        if is_valid:
            init = await self.siwe_init(address, use_proxy)
            if not init: return False

            nonce = init.get("nonce")

            authenticate = await self.siwe_authenticate(account, address, nonce, use_proxy)
            if not authenticate: return False

            self.token[address] = authenticate["token"]

            self.log(
                f"{Fore.CYAN + Style.BRIGHT}Status:{Style.RESET_ALL}"
                f"{Fore.GREEN + Style.BRIGHT} Login Success {Style.RESET_ALL}"
            )

            return True

    async def process_option_1(self, account: str, address: str, use_proxy: bool):
        self.log(f"{Fore.CYAN + Style.BRIGHT}Spin  :{Style.RESET_ALL}")

        self.log(
            f"{Fore.MAGENTA+Style.BRIGHT} ● {Style.RESET_ALL}"
            f"{Fore.GREEN+Style.BRIGHT}Free Spins{Style.RESET_ALL}"
        )

        free_spins = await self.get_free_spins(address, use_proxy)
        if free_spins is not None:
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Available:{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {free_spins} Free Spins {Style.RESET_ALL}"
            )

            if free_spins > 0:
                for i in range(free_spins):
                    self.log(
                        f"{Fore.GREEN+Style.BRIGHT}   ● {Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT}{i+1}/{free_spins}{Style.RESET_ALL}"
                    )

                    spin = await self.lucky_spin(account, address, True, use_proxy)
                    if not spin: continue

                    if not spin.get("success"):
                        self.log(
                            f"{Fore.BLUE+Style.BRIGHT}     Spin     :{Style.RESET_ALL}"
                            f"{Fore.RED+Style.BRIGHT} Failed {Style.RESET_ALL}"
                        )
                        continue

                    tx_hash = spin.get("txnHash")

                    self.log(
                        f"{Fore.BLUE+Style.BRIGHT}     Spin     :{Style.RESET_ALL}"
                        f"{Fore.GREEN+Style.BRIGHT} Success {Style.RESET_ALL}"
                    )
                    self.log(
                        f"{Fore.BLUE+Style.BRIGHT}     Tx Hash  :{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {tx_hash} {Style.RESET_ALL}"
                    )
                    self.log(
                        f"{Fore.BLUE+Style.BRIGHT}     Explorer :{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {self.EXPLORER}{tx_hash} {Style.RESET_ALL}"
                    )

                    await asyncio.sleep(random.uniform(3.0, 5.0))

        self.log(
            f"{Fore.MAGENTA+Style.BRIGHT} ● {Style.RESET_ALL}"
            f"{Fore.GREEN+Style.BRIGHT}Paid Spins{Style.RESET_ALL}"
        )

        paid_spins = await self.get_paid_spins(address, use_proxy)
        if paid_spins is not None:
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Available:{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {paid_spins} Paid Spins {Style.RESET_ALL}"
            )

            if paid_spins == 0:
            
                last_purchase = await self.last_purchase_time(address, use_proxy)
                if last_purchase is None: return False

                timestamp = int(time.time())
                next_purchase = last_purchase + 24 * 60 * 60

                if timestamp <= next_purchase:
                    self.log(
                        f"{Fore.BLUE+Style.BRIGHT}   Status   :{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Not Time to Buy Spin {Style.RESET_ALL}"
                    )
                    return False
                
                spin_price = await self.get_spin_price(address, use_proxy)
                if spin_price is None: return False
                self.log(
                    f"{Fore.BLUE+Style.BRIGHT}   Price    :{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {spin_price} EDEL {Style.RESET_ALL}"
                )
                
                balance = await self.get_token_balance(address, self.TOKENS["EDEL"]["address"], use_proxy)
                if balance is None: return False

                self.log(
                    f"{Fore.BLUE+Style.BRIGHT}   Balance  :{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {balance} EDEL {Style.RESET_ALL}"
                )

                if balance < spin_price:
                    self.log(
                        f"{Fore.BLUE+Style.BRIGHT}   Status   :{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Insufficient EDEL Token Balance {Style.RESET_ALL}"
                    )
                    return False

                onchain = await self.process_perform_buy_spin(account, address, spin_price, use_proxy)
                if not onchain: return False

                paid_spins = 1

            for i in range(paid_spins):
                self.log(
                    f"{Fore.GREEN+Style.BRIGHT}   ● {Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT}{i+1}/{paid_spins}{Style.RESET_ALL}"
                )

                await asyncio.sleep(random.uniform(3.0, 5.0))

                spin = await self.lucky_spin(account, address, False, use_proxy)
                if not spin: continue

                if not spin.get("success"):
                    self.log(
                        f"{Fore.BLUE+Style.BRIGHT}     Spin     :{Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT} Failed {Style.RESET_ALL}"
                    )
                    continue

                tx_hash = spin.get("txnHash")

                self.log(
                    f"{Fore.BLUE+Style.BRIGHT}     Spin     :{Style.RESET_ALL}"
                    f"{Fore.GREEN+Style.BRIGHT} Success {Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.BLUE+Style.BRIGHT}     Tx Hash  :{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {tx_hash} {Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.BLUE+Style.BRIGHT}     Explorer :{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {self.EXPLORER}{tx_hash} {Style.RESET_ALL}"
                )

    async def process_option_2(self, account: str, address: str, use_proxy: bool):
        self.log(f"{Fore.CYAN + Style.BRIGHT}Supply:{Style.RESET_ALL}")

        for symbol, data in ((s, d) for s, d in self.TOKENS.items() if s != "EDEL"):
            
            await asyncio.sleep(random.uniform(3.0, 5.0))

            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT} ● {Style.RESET_ALL}"
                f"{Fore.GREEN+Style.BRIGHT}{symbol}{Style.RESET_ALL}"
            )
            
            balance = await self.get_token_balance(address, data['address'], use_proxy)
            if balance is None: continue

            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Balance  :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {balance} {symbol} {Style.RESET_ALL}"
            )

            if balance == 0:
                self.log(
                    f"{Fore.BLUE+Style.BRIGHT}   Status   :{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} Insufficient {symbol} Token Balance {Style.RESET_ALL}"
                )
                continue

            if self.supply_option == 1:
                amount = balance * 0.25
            elif self.supply_option == 2:
                amount = balance * 0.5
            elif self.supply_option == 3:
                amount = balance * 0.75
            elif self.supply_option == 4:
                amount = balance * 1

            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Amount   :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {amount} {symbol} {Style.RESET_ALL}"
            )

            await self.process_perform_supply_token(account, address, data['address'], amount, use_proxy)

    async def process_accounts(self, account: str, address: str, option: int, use_proxy: bool, rotate_proxy: bool):
        is_logined = await self.process_login(account, address, use_proxy, rotate_proxy)
        if is_logined:

            if option == 1:
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}Option:{Style.RESET_ALL}"
                    f"{Fore.BLUE + Style.BRIGHT} Lucky Spin {Style.RESET_ALL}"
                )
                await self.process_option_1(account, address, use_proxy)

            elif option == 2:
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}Option:{Style.RESET_ALL}"
                    f"{Fore.BLUE + Style.BRIGHT} Supply Token {Style.RESET_ALL}"
                )
                await self.process_option_2(account, address, use_proxy)

            elif option == 3:
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}Option:{Style.RESET_ALL}"
                    f"{Fore.BLUE + Style.BRIGHT} Run All Features {Style.RESET_ALL}"
                )
                await self.process_option_1(account, address, use_proxy)
                await self.process_option_2(account, address, use_proxy)

    async def main(self):
        try:
            accounts =self.load_accounts()
            if not accounts: return

            option, proxy_choice, rotate_proxy = self.print_question()

            while True:
                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(accounts)}{Style.RESET_ALL}"
                )

                use_proxy = True if proxy_choice == 1 else False
                if use_proxy: self.load_proxies()

                separator = "=" * 25
                for idx, account in enumerate(accounts, start=1):
                    if account:
                        address = self.generate_address(account)
                        self.log(
                            f"{Fore.CYAN + Style.BRIGHT}{separator}[{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {idx} {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {self.mask_account(address)} {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}]{separator}{Style.RESET_ALL}"
                        )

                        if not address:
                            self.log(
                                f"{Fore.CYAN + Style.BRIGHT}Status:{Style.RESET_ALL}"
                                f"{Fore.RED + Style.BRIGHT} Invalid Private Key or Library Version Not Supported {Style.RESET_ALL}"
                            )
                            continue

                        user_agent = random.choice(USER_AGENTS)

                        self.HEADERS_1[address] = {
                            "Accept": "application/json",
                            "Accept-Encoding": "gzip, deflate, br",
                            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
                            "Cache-Control": "no-cache",
                            "Origin": "https://testnet.edel.finance",
                            "Pragma": "no-cache",
                            "Privy-App-Id": "cmf5gt8yi019ljv0bn5k8xrdw",
                            "Privy-Ca-Id": str(uuid.uuid4()),
                            "Privy-Client": "react-auth:3.0.1",
                            "Referer": "https://testnet.edel.finance/",
                            "Sec-Fetch-Dest": "empty",
                            "Sec-Fetch-Mode": "cors",
                            "Sec-Fetch-Site": "cross-site",
                            "Sec-Fetch-Storage-Access": "active",
                            "User-Agent": user_agent
                        }

                        self.HEADERS_2[address] = {
                            "Accept": "*/*",
                            "Accept-Encoding": "gzip, deflate, br",
                            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
                            "Cache-Control": "no-cache",
                            "Origin": "https://testnet.edel.finance",
                            "Pragma": "no-cache",
                            "Referer": "https://testnet.edel.finance/",
                            "Sec-Fetch-Dest": "empty",
                            "Sec-Fetch-Mode": "cors",
                            "Sec-Fetch-Site": "cross-site",
                            "User-Agent": user_agent
                        }
                        
                        await self.process_accounts(account, address, option, use_proxy, rotate_proxy)

                self.log(f"{Fore.CYAN + Style.BRIGHT}={Style.RESET_ALL}"*72)
                seconds = 24 * 60 * 60
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.BLUE+Style.BRIGHT}All Accounts Have Been Processed.{Style.RESET_ALL}",
                        end="\r"
                    )
                    await asyncio.sleep(1)
                    seconds -= 1

        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")
            raise e

if __name__ == "__main__":
    try:
        bot = EdelFinance()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] Edel Finance - BOT{Style.RESET_ALL}                                       "                              
        )