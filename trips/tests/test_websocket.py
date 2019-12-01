from django.contrib.auth import get_user_model 
from django.contrib.auth.models import Group 
from django.test import Client 
from  channels.db import database_sync_to_async 
from channels.layers import get_channel_layer 
from channels.testing import WebsocketCommunicator 
import pytest
from taxi.routing import application 
from trips.models import Trip 


TEST_CHANNEL_LAYERS = {
	'default': {
		'BACKEND': 'channels.layers.InMemoryChannelLayer'
	},
}

@database_sync_to_async
def create_user(
	*,
	username = 'rider@example.com',
	password = 'pAss0rd!',
	group = 'rider'):
	# create user
	user = get_user_model().objects.create_user(
			username = username,
			password = password
		)
	# create user group
	user_group, _ = Group.objects.get_or_create(name=group)
	user.groups.add(user_group)
	user.save()
	return user

# a new function to create trip in the database 
@database_sync_to_async
def create_trip(**kwargs):
	return Trip.objects.create(**kwargs)

@pytest.mark.asyncio
@pytest.mark.django_db(transaction = True)
class TestWebsockets:
	async def test_authorized_user_can_connect(self, settings):
		#use in memory channels layers for testing
		settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
		# force authentication to get session ID
		
		user = await create_user(
			username = 'rider@example.com',
			group = 'rider')
		communicator =await auth_connect(user)		
		await communicator.disconnect()


	async def test_rider_can_create_trips(self, settings):		

		settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
		# force authentication to get session ID
		
		user = await create_user(
			username = 'rider@example.com',
			group = 'rider'
		)
		communicator = await connect_and_create_trip(user=user)		
		
		# Send JSON message to server
		# await communicator.send_json_to({
		# 		'type': 'create.trip',
		# 		'data': {
		# 			'pick_up_address': 'A',
		# 			'drop_off_address': 'B',
		# 			'rider': user.id,
		# 		}
		# 	})
		#receive JSON message from server
		response = await communicator.receive_json_from()
		data = response.get('data')

		#confirm data
		assert data['id'] is not None
		assert 'A' == data['pick_up_address']
		assert 'B' == data['drop_off_address']
		assert Trip.REQUESTED == data['status']
		assert data['driver'] is None
		assert user.username == data['rider'].get('username')


		await communicator.disconnect()


	async def test_rider_is_added_to_trip_group_on_create(self, settings):
		settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
		# force authentication to get session ID
		
		user = await create_user(		
			username='rider@example.com',
			group='rider'
		)

		# connect and send JSON message to server
		communicator = await connect_and_create_trip(user=user)		
		
		#receive JSON message from server
		# rider should be added to new trip's group
		response = await communicator.receive_json_from()
		data = response.get('data')

		trip_id = data['id']
		message = {
			'type': 'echo.message',
			'data': 'This is a test message'
		}

		# Send JSON message to new trips group
		channel_layer = get_channel_layer()
		await channel_layer.group_send(trip_id, message=message)

		# Receive JSON message from server
		response = await communicator.receive_json_from()

		#confirm data
		assert message == response


		await communicator.disconnect()

	async def test_rider_is_added_to_trip_groups_on_connect(self, settings):
		settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
		# force authentication to get session ID
		
		user = await create_user(		
			username='rider@example.com',
			group='rider'
		)

		# create trips and link to rider
		trip = await create_trip(
			pick_up_address = 'A',
			drop_off_address = 'B',
			rider = user
		)

		# connect to server
		# Trips for riser should be retrieved
		# Rider should be added to trip's group
		communicator = await auth_connect(user)
		message = {
			'type': 'echo.message',
			'data': 'this is a test message'
		}
		

				

		# Send JSON message to new trips group
		channel_layer = get_channel_layer()
		await channel_layer.group_send(f'{trip.id}', message=message)

		# Receive JSON message from server
		response = await communicator.receive_json_from()

		#confirm data
		assert message == response


		await communicator.disconnect()


	async def test_driver_can_update_trips(self, settings):		

		settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
				
		# create trips and link to rider
		trip = await create_trip(
			pick_up_address = 'A',
			drop_off_address = 'B',
		)

		user = await create_user(
			username = 'driver@example.com',
			group = 'driver'
		)

		#send JSON message to server
		communicator = await connect_and_update_trip(
			user = user,
			trip = trip,
			status = Trip.IN_PROGRESS
		)		
		
		
		#receive JSON message from server
		response = await communicator.receive_json_from()
		data = response.get('data')

		#confirm data
		assert str(trip.id) == data['id']
		assert 'A' == data['pick_up_address']
		assert 'B' == data['drop_off_address']
		assert Trip.IN_PROGRESS == data['status']		
		assert user.username == data['driver'].get('username')
		assert data['rider'] is None


		await communicator.disconnect()

	async def test_driver_is_added_to_trip_groups_on_update(self, settings):
		settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
				
		# create trips and link to rider
		trip = await create_trip(
			pick_up_address = 'A',
			drop_off_address = 'B',
		)

		user = await create_user(
			username = 'driver@example.com',
			group = 'driver'
		)

		#send JSON message to server
		communicator = await connect_and_update_trip(
			user = user,
			trip = trip,
			status = Trip.IN_PROGRESS
		)		
		
		
		#receive JSON message from server
		response = await communicator.receive_json_from()
		data = response.get('data')


	
		# connect to server
		# Trips for riser should be retrieved
		# Rider should be added to trip's group
		trip_id = data['id']
		message = {
			'type': 'echo.message',
			'data': 'this is a test message'
		}
		

				

		# Send JSON message to new trips group
		channel_layer = get_channel_layer()
		await channel_layer.group_send(trip_id, message=message)

		# Receive JSON message from server
		response = await communicator.receive_json_from()

		#confirm data
		assert message == response


		await communicator.disconnect()

	async def test_driver_is_alerted_on_trip_create(self, settings):
		settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS

		# listen to the drivers group test channel
		channel_layer = get_channel_layer()
		await channel_layer.group_add(
			group = 'drivers',
			channel = 'test_channel'
		)
				
		
		user = await create_user(
			username = 'rider@example.com',
			group = 'rider'
		)

		#send JSON message to server
		communicator = await connect_and_create_trip(user = user)		
		
		
		#receive JSON message from server
		response = await channel_layer.receive('test_channel')
		data = response.get('data')	
	
				

		#confirm data
		assert data['id'] is not None
		assert user.username == data['rider'].get('username')


		await communicator.disconnect()

	async def test_rider_is_alerted_on_trip_update(self, settings):
		settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
				
		# create trips and link to rider
		trip = await create_trip(
			pick_up_address = 'A',
			drop_off_address = 'B',
		)

		# listen to the trip group test channel
		channel_layer = get_channel_layer()
		await channel_layer.group_add(
			group = f'{trip.id}',
			channel = 'test_channel'
		)

		user = await create_user(
			username = 'driver@example.com',
			group = 'driver'
		)

		#send JSON message to server
		communicator = await connect_and_update_trip(
			user = user,
			trip = trip,
			status = Trip.IN_PROGRESS
		)		
		
		
		#receive JSON message from server on test channel

		response = await channel_layer.receive('test_channel')		
		data = response.get('data')




		#confirm data
		assert f'{trip.id}' == data['id']
		assert user.username == data['driver'].get('username')
		await communicator.disconnect()



async def auth_connect(user):
	# force authentication to get session ID
	client = Client()
	client.force_login(user=user)

	# pass session ID in headers to authenticate
	communicator = WebsocketCommunicator(
		application = application,
		path = '/taxi/',
		headers = [(
			b'cookie',
			f'sessionid={client.cookies["sessionid"].value}'.encode('ascii')
			)]
		)
	connected, _ = await communicator.connect()
	assert connected is True
	return communicator

async def connect_and_create_trip(*,
			user,
			pick_up_address = 'A',
			drop_off_address = 'B'
		):
	communicator = await auth_connect(user)
	await communicator.send_json_to({
		'type': 'create.trip',
		'data': {
			'pick_up_address': pick_up_address,
			'drop_off_address': drop_off_address,
			'rider': user.id,
		}

	})
	return communicator

async def connect_and_update_trip(*, user, trip, status):
	communicator = await auth_connect(user)
	await communicator.send_json_to({
		'type': 'update.trip',
		'data': {
			'id': f'{trip.id}',
			'pick_up_address': trip.pick_up_address,
			'drop_off_address': trip.drop_off_address,
			'status': status, 
			'driver': user.id,
		}

	})
	return communicator
