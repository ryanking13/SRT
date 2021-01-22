def pytest_addoption(parser):
    parser.addoption(
        "--full",
        action="store_true",
        default=None,
        help="Run full tests which includes dangerous tests such as reservation",
    )
