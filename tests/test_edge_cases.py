"""Test edge cases and boundary conditions."""
import asyncio
import pytest
from dexscreener import DexscreenerClient, APIError
from dexscreener.exceptions import APIError


@pytest.mark.asyncio
async def test_exactly_30_addresses():
    """Test with exactly 30 addresses (the limit)."""
    print("\n" + "="*60)
    print("TEST: Exactly 30 Addresses (Boundary)")
    print("="*60)
    
    client = DexscreenerClient()
    
    try:
        # Generate exactly 30 addresses
        addresses = [f"0x{'1234567890'*4}{i:02d}" for i in range(30)]
        
        pairs = await client.get_token_pair_list_async("ethereum", addresses)
        print(f"✅ PASS: Accepted 30 addresses, returned {len(pairs)} pairs")
    except ValueError as e:
        print(f"❌ FAIL: Should accept 30 addresses: {e}")
    except APIError as e:
        print(f"⚠️  API Error (addresses might be invalid): {e.status_code}")
    except Exception as e:
        print(f"❌ FAIL: Unexpected error: {type(e).__name__}: {e}")


@pytest.mark.asyncio
async def test_single_address():
    """Test with single address."""
    print("\n" + "="*60)
    print("TEST: Single Address in List")
    print("="*60)
    
    client = DexscreenerClient()
    
    try:
        # Use a known token address (WETH on Ethereum)
        pairs = await client.get_token_pair_list_async(
            "ethereum",
            ["0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"]
        )
        print(f"✅ PASS: Single address returned {len(pairs)} pairs")
    except Exception as e:
        print(f"❌ FAIL: {type(e).__name__}: {e}")


@pytest.mark.asyncio
async def test_empty_address_list():
    """Test with empty address list."""
    print("\n" + "="*60)
    print("TEST: Empty Address List")
    print("="*60)
    
    client = DexscreenerClient()
    
    try:
        pairs = await client.get_token_pair_list_async("ethereum", [])
        print(f"✅ PASS: Empty list returned {len(pairs)} pairs")
    except ValueError as e:
        print(f"✅ PASS: Rejected empty list: {e}")
    except APIError as e:
        print(f"✅ PASS: API rejected empty list: {e.status_code}")
    except Exception as e:
        print(f"❌ FAIL: Unexpected error: {type(e).__name__}: {e}")


@pytest.mark.asyncio
async def test_duplicate_addresses():
    """Test with duplicate addresses."""
    print("\n" + "="*60)
    print("TEST: Duplicate Addresses")
    print("="*60)
    
    client = DexscreenerClient()
    
    try:
        # Same address multiple times
        weth = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
        pairs = await client.get_token_pair_list_async(
            "ethereum",
            [weth, weth, weth]
        )
        print(f"✅ PASS: Duplicate addresses returned {len(pairs)} pairs")
    except Exception as e:
        print(f"⚠️  {type(e).__name__}: {e}")


@pytest.mark.asyncio
async def test_mixed_case_addresses():
    """Test with mixed case addresses."""
    print("\n" + "="*60)
    print("TEST: Mixed Case Addresses")
    print("="*60)
    
    client = DexscreenerClient()
    
    try:
        # Mixed case (checksummed) address
        pairs = await client.get_token_pairs_async(
            "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"  # Mixed case
        )
        print(f"✅ PASS: Mixed case address returned {len(pairs)} pairs")
    except Exception as e:
        print(f"❌ FAIL: {type(e).__name__}: {e}")


@pytest.mark.asyncio
async def test_lowercase_addresses():
    """Test with lowercase addresses."""
    print("\n" + "="*60)
    print("TEST: Lowercase Addresses")
    print("="*60)
    
    client = DexscreenerClient()
    
    try:
        # All lowercase
        pairs = await client.get_token_pairs_async(
            "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"  # Lowercase
        )
        print(f"✅ PASS: Lowercase address returned {len(pairs)} pairs")
    except Exception as e:
        print(f"❌ FAIL: {type(e).__name__}: {e}")


@pytest.mark.asyncio
async def test_very_long_search_query():
    """Test with very long search query."""
    print("\n" + "="*60)
    print("TEST: Very Long Search Query")
    print("="*60)
    
    client = DexscreenerClient()
    
    try:
        long_query = "A" * 1000  # 1000 character query
        results = await client.search_pairs_async(long_query)
        print(f"✅ PASS: Long query returned {len(results)} results")
    except APIError as e:
        print(f"✅ PASS: API rejected long query: {e.status_code}")
    except Exception as e:
        print(f"❌ FAIL: {type(e).__name__}: {e}")


@pytest.mark.asyncio
async def test_unicode_in_search():
    """Test with unicode characters in search."""
    print("\n" + "="*60)
    print("TEST: Unicode in Search Query")
    print("="*60)
    
    client = DexscreenerClient()
    
    try:
        results = await client.search_pairs_async("Bitcoin🚀💎")
        print(f"✅ PASS: Unicode query returned {len(results)} results")
    except APIError as e:
        print(f"✅ PASS: API handled unicode: {e.status_code}")
    except Exception as e:
        print(f"❌ FAIL: {type(e).__name__}: {e}")


async def main():
    """Run all edge case tests."""
    print("\n" + "🔬 " * 30)
    print("EDGE CASE TEST SUITE")
    print("🔬 " * 30)
    
    await test_exactly_30_addresses()
    await test_single_address()
    await test_empty_address_list()
    await test_duplicate_addresses()
    await test_mixed_case_addresses()
    await test_lowercase_addresses()
    await test_very_long_search_query()
    await test_unicode_in_search()
    
    print("\n" + "="*60)
    print("ALL EDGE CASE TESTS COMPLETED")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())