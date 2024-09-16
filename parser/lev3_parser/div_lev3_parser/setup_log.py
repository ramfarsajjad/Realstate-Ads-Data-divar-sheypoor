import logging

def setup_logger(log_file, logger_name):
    # ساخت لاگر جدید با هندلر و فایل لاگ مشخص
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # ایجاد هندلر فایل
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # ایجاد هندلر کنسول
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # اضافه کردن هندلرها به لاگر
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger