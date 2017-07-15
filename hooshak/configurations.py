
settings = pymlconf.DeferredConfigManager()

BUILTIN_CONFIGURATION = """
debug: true
"""

settings.load(builtin=BUILTIN_CONFIGURATION)
