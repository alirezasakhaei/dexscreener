import asyncio
from dexscreener import DexscreenerClient


async def main():
    client = DexscreenerClient()
    
    print("=" * 60)
    print("Testing Dexscreener API Client")
    print("=" * 60)
    
    # Test 1: Get latest token profiles
    try:
        print("\n1. Testing get_latest_token_profiles()...")
        token_profiles = client.get_latest_token_profiles()
        print(f"   ✅ Success! Found {len(token_profiles)} token profiles")
        if token_profiles:
            print(f"   First token: {token_profiles[0].chain_id} - {token_profiles[0].token_address}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Get boosted tokens
    try:
        print("\n2. Testing get_latest_boosted_tokens()...")
        boosted_tokens = client.get_latest_boosted_tokens()
        print(f"   ✅ Success! Found {len(boosted_tokens)} boosted tokens")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Search pairs
    try:
        print("\n3. Testing search_pairs_async('WBTC')...")
        search = await client.search_pairs_async("WBTC")
        print(f"   ✅ Success! Found {len(search)} pairs")
        if search:
            pair = search[0]
            print(f"   First pair: {pair.base_token.symbol}/{pair.quote_token.symbol}")
            print(f"   Price USD: ${pair.price_usd}")
            print(f"   Chain: {pair.chain_id}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Get specific token pair
    try:
        print("\n4. Testing get_token_pair_async()...")
        pair = await client.get_token_pair_async(
            "ethereum",
            "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640"  # USDC/WETH on Uniswap V3
        )
        if pair:
            print(f"   ✅ Success! {pair.base_token.symbol}/{pair.quote_token.symbol}")
            print(f"   Price: ${pair.price_usd}")
            print(f"   24h Volume: ${pair.volume.h24}")
        else:
            print(f"   ⚠️  No pair found")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("Testing complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())