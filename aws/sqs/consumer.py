import boto3
import os

queue_name = os.getenv("SQS_QUEUE_NAME", "test")
max_messages = os.getenv("SQS_QUEUE_MAX_MESSAGES", -1)

sqs = boto3.resource("sqs")
queue = sqs.get_queue_by_name(QueueName=queue_name)

def process_message(message_body):
    print(f"{message_body}")


def read():
    count = 0
    run_check = count < max_messages if max_messages > 0 else True
    while run_check:
        messages = queue.receive_messages()
        for message in messages:
            process_message(message.body)
            if max_messages > 0:
                count += 1


if __name__ == "__main__":
    read()
