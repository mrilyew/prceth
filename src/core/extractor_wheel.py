from resources.globals import importlib, traceback, logger

def extractor_wheel(args, entity_dir, extractor_name):
    module = importlib.import_module(f'extractors.{extractor_name}')
    instance = getattr(module, extractor_name)(temp_dir=entity_dir)

    try:
        results = instance.execute(args=args)
        results["extractor_name"] = extractor_name

        return instance, results
    except Exception as e:
        traceback.print_exc()
        logger.logException(e)
        instance.cleanup_fail()
