from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from trips.api.serializers import ReadOnlyTripSerializer, TripSerializer 

import asyncio


class TaxiConsumer(AsyncJsonWebsocketConsumer):

	def __init__(self, scope):
		super().__init__(scope)

		#keep track of the usr's trips
		self.trips = set()

	async def connect(self):
		user = self.scope['user']
		if user.is_anonymous:
			await self.close()
		else:
			await self.accept()

	async def receive_json(self, content, **kwargs):
		message_type = content.get('type')
		if message_type == 'create.trip':
			await self.create_trip(content)

	async def echo_message(self, event):
		await self.send_json(event)

	async def create_trip(self, event):
		trip = await self._create_trip(event.get('data'))
		trip_id = f'{trip.id}'
		trip_data = ReadOnlyTripSerializer(trip).data
		
		# add trip to set
		self.trips.add(trip_id)

		# add this channel to the new trips groups
		await self.channel_layer.group_add(
			group=trip_id,
			channel=self.channel_name
		)


		await self.send_json({
			'type': 'create.trip',
			'data': trip_data
		})

	async def diconnect(self, code):
		# remove this channel from every trip's group
		channel_groups = [
			self.channel_layer.group_discard(
				group=trip,
				channel=self.channel_name
			)
			for trip in self.trips
		]
		asyncio.gather(*channel_groups)

		# remove all reference to trips
		self.trips.clear()

		await super().disconnect(code)

	@database_sync_to_async
	def _create_trip(self, content):
		serializer = TripSerializer(data=content)
		serializer.is_valid(raise_exception = True)
		trip = serializer.create(serializer.validated_data)
		return trip 
