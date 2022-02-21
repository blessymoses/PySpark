"""Configuring log4j with PySpark
1. Create a log4j configuration file
2. Configure spark JVM to pickup the log4j configuration file
3. Get spark's log4j instance and use it
"""
from pyspark.sql import *

if __name__ == "__main__":
    print("Starting main...")
