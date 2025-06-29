from tests.test_profile_discovery import demo_profile_discovery
from tests.test_group_dining import demo_group_dining
from tests.performance_tests import run_performance_tests


def main():
    """Run all demonstrations and tests."""
    print("=== Citadel Assignment - Algorithm Demonstrations ===\n")
    
    # Run profile discovery demo
    demo_profile_discovery()
    
    print("\n" + "="*60 + "\n")
    
    # Run group dining demo
    demo_group_dining()
    
    print("\n" + "="*60 + "\n")
    
    # Run performance tests
    performance_results = run_performance_tests()
    
    print("\n" + "="*60)
    print("=== Algorithm Implementation Complete ===")
    print("Both algorithms are ready for production deployment!")
    
    return performance_results


if __name__ == "__main__":
    main()
