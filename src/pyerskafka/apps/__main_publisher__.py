import click
import os
from time import sleep

import erskafka.ERSPublisher as erspub
from erskafka.ERSPublisher import ERSException, SeverityLevel  # import the custom exception and the SeverityLevel enum


def cli(kafka_address, kafka_port, number_of_messages, kafka_topic, session):
    # Assign the session to the relevant env var
    os.environ['DUNEDAQ_PARTITION']=session

    # Set up the bootstrap
    bootstrap = f"{kafka_address}:{kafka_port}"

    # Construct the publisher
    publisher = erspub.ERSPublisher(
        bootstrap = bootstrap,
        topic = kafka_topic,
        application_name = "pyerskafka_publisher_test",
        package_name = "pyerskafka",
    )

    for i in range(number_of_messages):
        message = f"Simple message with ID: {i}"
        result = publisher.publish(
            message,
            severity=SeverityLevel((i%5)+1).name
        )
        if result is None:
            raise ERSException("Publishing failed, exiting.")
        sleep(0.5)


    # Test 2: publish with Exception
    try:
        raise Exception("Custom ERS exception for testing publish_simple_message!")
    except Exception as e:
        print(f"Caught an ERSException: {e}")
        result = publisher.publish(e, severity=SeverityLevel.WARNING.name)
        print(f"Publishing exception message: {'successful' if result else 'failed'}")

    # Test 3: publish with CustomException
    try:
        raise CustomException("Custom ERS exception for testing publish_simple_message!")
    except Exception as e:
        print(f"Caught an ERSException: {e}")
        result = publisher.publish(e, severity=SeverityLevel.WARNING.name)
        print(f"Publishing exception message: {'successful' if result else 'failed'}")

    # Test 4: publish text with exception as cause
    for i in range(number_of_messages) :
        try:
            raise CustomException("I am an exception")
        except Exception as e:
            print(f"Caught an ERSException: {e}")
            severity = SeverityLevel((i%5)+1).name
            issue_chain = publisher.publish(f"Exception found, causing a severity of {severity}", severity=severity, cause=e)
            print(f"Publishing issue from create_issue with exception: {'successful' if result else 'failed'}")

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--kafka-address', type=click.STRING, default="monkafka.cern.ch", help="Address of the Kafka broker.")
@click.option('--kafka-port', type=click.INT, default=30092, help='Port of the Kafka broker.')
@click.option('--number-of-messages', type=click.INT, default=10, help='Number of messages to send.')
@click.option('--kafka-topic', type=click.STRING, default="ers_stream", help="Name of the Kafka topic.")
@click.option('--session', type=click.STRING, default="pyerskafka_app", help="Name of the session")
def main(kafka_address:str, kafka_port:int, number_of_messages:int, kafka_topic:str, session:str):
    """
    Publishes test messages to kafka with the configuration defined by the options
    """
    cli(kafka_address, kafka_port, number_of_messages, kafka_topic, session)

