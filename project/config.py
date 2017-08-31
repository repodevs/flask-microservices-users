
class BaseConfig:
    """Base Configuration"""
    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    """Development Configuration"""
    DEBUG = True


class TestingConfig(BaseConfig):
    """Testing Configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(BaseConfig):
    """Production Configuration"""
    DEBUG = False
