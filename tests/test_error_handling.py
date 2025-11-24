"""Test error handling and custom exceptions."""
import asyncio
import pytest
from dexscreener import (
    APIError
)
from dexscreener import DexscreenerClient


@pytest.mark.asyncio
async def test_invalid_chain():
    """Test API error with invalid chain."""
    print("\n" + "="*60)
    print("TEST: Invalid Chain ID")
    print("="*60)
    
    client = DexscreenerClient()
    
    try:
        pair = await client.get_token_pair_async(
            "invalid_chain_that_does_not_exist",
            "0x1234567890123456789012345678901234567890"
        )
        print("❌ FAIL: No error raised - unexpected!")
    except APIError as e:
        print(f"✅ PASS: Caught APIError")
        print(f"   Status Code: {e.status_code}")
        print(f"   Message: {e.message}")
        print(f"   Response Data: {e.response_data}")
    except Exception as e:
        print(f"❌ FAIL: Unexpected error: {type(e).__name__}: {e}")


@pytest.mark.asyncio
async def test_invalid_address_format():
    """Test API error with invalid address format."""
    print("\n" + "="*60)
    print("TEST: Invalid Address Format")
    print("="*60)
    
    client = DexscreenerClient()
    
    try:
        pair = await client.get_token_pair_async("ethereum", "not_a_valid_address")
        print("❌ FAIL: No error raised - unexpected!")
    except APIError as e:
        print(f"✅ PASS: Caught APIError")
        print(f"   Status Code: {e.status_code}")
        print(f"   Message: {e.message}")
    except Exception as e:
        print(f"❌ FAIL: Unexpected error: {type(e).__name__}: {e}")


@pytest.mark.asyncio
async def test_nonexistent_pair():
    """Test with valid format but non-existent pair."""
    print("\n" + "="*60)
    print("TEST: Non-existent Pair")
    print("="*60)
    
    client = DexscreenerClient()
    
    try:
        # Valid format but likely doesn't exist
        pair = await client.get_token_pair_async(
            "ethereum",
            "0x0000000000000000000000000000000000000001"
        )
        if pair is None:
            print("✅ PASS: Returned None for non-existent pair")
        else:
            print(f"⚠️  WARNING: Found pair (might actually exist): {pair.pair_address}")
    except APIError as e:
        print(f"✅ PASS: Caught APIError (API returned error for non-existent)")
        print(f"   Status Code: {e.status_code}")
    except Exception as e:
        print(f"❌ FAIL: Unexpected error: {type(e).__name__}: {e}")


@pytest.mark.asyncio
async def test_too_many_addresses():
    """Test validation error with too many addresses."""
    print("\n" + "="*60)
    print("TEST: Too Many Addresses (>30)")
    print("="*60)
    
    client = DexscreenerClient()
    
    try:
        # Generate 31 fake addresses (limit is 30)
        fake_addresses = [f"0x{'1234567890'*4}{i:02d}" for i in range(31)]
        
        pairs = await client.get_token_pair_list_async("ethereum", fake_addresses)
        print("❌ FAIL: No error raised - unexpected!")
    except ValueError as e:
        print(f"✅ PASS: Caught ValueError for exceeding address limit")
        print(f"   Message: {e}")
    except Exception as e:
        print(f"❌ FAIL: Unexpected error: {type(e).__name__}: {e}")


@pytest.mark.asyncio
async def test_empty_search_query():
    """Test search with empty query."""
    print("\n" + "="*60)
    print("TEST: Empty Search Query")
    print("="*60)
    
    client = DexscreenerClient()
    
    try:
        results = await client.search_pairs_async("")
        print(f"✅ PASS: Empty search returned {len(results)} results")
    except APIError as e:
        print(f"✅ PASS: API rejected empty search")
        print(f"   Status Code: {e.status_code}")
    except Exception as e:
        print(f"❌ FAIL: Unexpected error: {type(e).__name__}: {e}")


@pytest.mark.asyncio
async def test_special_characters_in_search():
    """Test search with special characters."""
    print("\n" + "="*60)
    print("TEST: Special Characters in Search")
    print("="*60)
    
    client = DexscreenerClient()
    
    try:
        results = await client.search_pairs_async("!@#$%^&*()")
        print(f"✅ PASS: Special chars search returned {len(results)} results")
    except APIError as e:
        print(f"✅ PASS: API rejected special characters")
        print(f"   Status Code: {e.status_code}")
    except Exception as e:
        print(f"❌ FAIL: Unexpected error: {type(e).__name__}: {e}")


@pytest.mark.asyncio
async def test_sync_methods():
    """Test synchronous methods for errors."""
    print("\n" + "="*60)
    print("TEST: Synchronous Methods Error Handling")
    print("="*60)
    
    client = DexscreenerClient()
    
    try:
        pairs = client.get_token_pairs("invalid_address_format")
        print(f"⚠️  WARNING: Returned {len(pairs)} pairs (might be valid)")
    except APIError as e:
        print(f"✅ PASS: Sync method caught APIError")
        print(f"   Status Code: {e.status_code}")
    except Exception as e:
        print(f"❌ FAIL: Unexpected error: {type(e).__name__}: {e}")


@pytest.mark.asyncio
async def test_network_timeout():
    """Test timeout handling (this will take 30+ seconds if timeout works)."""
    print("\n" + "="*60)
    print("TEST: Network Timeout (may take 30s)")
    print("="*60)
    print("⏭️  SKIPPED: Would take too long")
    # Uncomment to actually test:
    # from dexscreener.http_client import HttpClient
    # client = HttpClient(60, 60, timeout=1)  # 1 second timeout
    # try:
    #     await client.request_async("GET", "dex/pairs/ethereum/0x...")
    # except TimeoutError as e:
    #     print(f"✅ PASS: Caught TimeoutError: {e}")


async def main():
    """Run all error handling tests."""
    print("\n" + "🧪 " * 30)
    print("COMPREHENSIVE ERROR HANDLING TEST SUITE")
    print("🧪 " * 30)
    
    await test_invalid_chain()
    await test_invalid_address_format()
    await test_nonexistent_pair()
    await test_too_many_addresses()
    await test_empty_search_query()
    await test_special_characters_in_search()
    await test_sync_methods()
    await test_network_timeout()
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETED")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())