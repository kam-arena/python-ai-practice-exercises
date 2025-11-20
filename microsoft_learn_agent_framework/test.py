print("✓ Attempting to import AzureAIClient...\n")


# Method 1: Direct import
try:
    from agent_framework.azure import AzureAIClient
    print("✓ Method 1: Direct import successful")
except ImportError as e:
    print(f"✗ Method 1 failed: {e}")
   
    # Method 2: Module import
    try:
        import agent_framework.azure as azure_module
        AzureAIClient = azure_module.AzureAIClient
        print("✓ Method 2: Module import successful")
    except Exception as e2:
        print(f"✗ Method 2 failed: {e2}")
       
        # Method 3: Get class directly
        try:
            #from agent_framework.azure import AzureAIClient
            print("✓ Method 3: Submodule import successful")
        except Exception as e3:
            print(f"✗ Method 3 failed: {e3}")
            print("\nListing available classes:")
            import agent_framework.azure as az
            for name in dir(az):
                if 'Client' in name:
                    print(f"  - {name}: {type(getattr(az, name))}")
 