
import getopt
import sys
from serunner.task import SeRunner
from serunner.log import logger
def main():
    """
    python script.py -p ./test_case
    """

    args = list(sys.argv[1:])
    _short_to_long = {}
    options, args = getopt.getopt(sys.argv[1:], 'p:i:')
    try:
        for name, value in options:
            print (value,type(value))
            if name in ('p'):
                serunner = SeRunner(**{})
                serunner.run(value)
                logger.info("测试结果汇总如下'\t\n'{sum}".format(sum=serunner.summary))
    except Exception:
        logger.error("命令行参数有误")
        raise


if __name__ == '__main__':
    main()

