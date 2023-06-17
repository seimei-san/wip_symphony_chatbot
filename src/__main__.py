#!/usr/bin/env python3
import asyncio
import logging.config
from pathlib import Path
import json


from symphony.bdk.core.activity.command import CommandContext
from symphony.bdk.core.config.loader import BdkConfigLoader
from symphony.bdk.core.service.datafeed.real_time_event_listener import RealTimeEventListener
from symphony.bdk.core.symphony_bdk import SymphonyBdk
from symphony.bdk.gen.agent_model.v4_initiator import V4Initiator
from symphony.bdk.gen.agent_model.v4_message_sent import V4MessageSent

from .activities import EchoCommandActivity, GreetUserJoinedActivity
from .gif_activities import GifSlashCommand, GifFormReplyActivity

from src import wip

# Configure logging
current_dir = Path(__file__).parent.parent
logging_conf = Path.joinpath(current_dir, 'resources', 'logging.conf')
logging.config.fileConfig(logging_conf, disable_existing_loggers=False)




async def run():
    config = BdkConfigLoader.load_from_file(Path.joinpath(current_dir, 'resources', 'config.yaml'))

    async with SymphonyBdk(config) as bdk:
        datafeed_loop = bdk.datafeed()
        datafeed_loop.subscribe(MessageListener())

        activities = bdk.activities()
        activities.register(EchoCommandActivity(bdk.messages()))
        activities.register(GreetUserJoinedActivity(bdk.messages(), bdk.users()))
        activities.register(GifSlashCommand(bdk.messages()))
        activities.register(GifFormReplyActivity(bdk.messages()))

        @activities.slash("/hello")
        async def hello(context: CommandContext):
            name = context.initiator.user.display_name
            response = f"<messageML>Hello {name}, hope you return render_template('index.html')are doing well!</messageML>"
            await bdk.messages().send_message(context.stream_id, response)

        # Start the datafeed read loop
        await datafeed_loop.start()


class MessageListener(RealTimeEventListener):
    async def on_message_sent(self, initiator: V4Initiator, event: V4MessageSent):
        logging.debug("Message received from %s: %s",
            initiator.user.display_name, initiator.user.user_id, event.message.stream.stream_id, event.message.message_id, event.message.message, event.message.timestamp)
        wip.wip_api_post(initiator.user.display_name, initiator.user.user_id, event.message.stream.stream_id, "", event.message.message_id, event.message.timestamp, event.message.message)


# Start the main asyncio run
try:
    logging.info("Running bot application...")
    asyncio.run(run())
except KeyboardInterrupt:
    logging.info("Ending bot application")
