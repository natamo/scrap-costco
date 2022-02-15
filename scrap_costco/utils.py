import scrap_costco.constants as cnst


def get_logger(logger_name: str):
    from sbk_utils.logger import LoggerFactory
    from sbk_scraping.utils import load_config_file
    dict_config = load_config_file(cnst.LOGGER_FILE_NAME)

    return LoggerFactory(
        logger_name=logger_name,
        config=dict_config
    ).build()
