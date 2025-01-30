from pyee import AsyncIOEventEmitter
import logging

# Initialize the event emitter
event_emitter = AsyncIOEventEmitter()

# Logger for event system
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Example Event: Item Created
@event_emitter.on("item_created")
async def handle_item_created(item_data):
    """
    Handles item creation events.
    """
    logger.info(f"Item created: {item_data['_id']} - {item_data['name']}")

    #TODO - If I had more time I would send to external API's or
    # Some AWS cloud infrastructure for event processing

def emit_item_created_event(item):
    """
    Emits an 'item_created' event.
    """
    event_emitter.emit("item_created", item)
