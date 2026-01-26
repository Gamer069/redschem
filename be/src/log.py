import sys

from loguru import logger

from tqdm import tqdm


def init_loguru(use_tqdm: bool = False):
	"""Init loguru logger, optionally redirect INFO/DEBUG to tqdm.write."""
	logger.remove()

	LOG_FORMAT = (
		"<green>{time:HH:mm:ss}</green> | "
		"<level>{level}</level> | "
		"<cyan>{{{name}:{line}</cyan>}} "
		"<level>{message}</level>"
	)

	stdout_sink = (lambda msg: tqdm.write(msg, end='')) if use_tqdm else sys.stdout
	stderr_sink = (lambda msg: tqdm.write(msg, end='')) if use_tqdm else sys.stderr

	logger.add(
		sink=stdout_sink,
		format=LOG_FORMAT,
		level="DEBUG",
		colorize=True,
		filter=lambda record: record["level"].no < 30  # Only DEBUG (10) and INFO (20)
	)

	logger.add(
		sink=stderr_sink,
		format=LOG_FORMAT,
		colorize=True,
		level="WARNING"  # WARNING (30), ERROR (40), CRITICAL (50)
	)

	logger.add(
		sink="logs/bot_{time:YYYY-MM-DD}.log",
		format=LOG_FORMAT,
		colorize=True,
		level="DEBUG",
		rotation="00:00",
		retention="7 days"
	)
