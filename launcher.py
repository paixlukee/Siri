from siri import Siri
import asyncio

def run_bot():
	loop = asyncio.get_event_loop() 
	bot = Siri()
	bot.run()
	
if __name__ == '__main__':
	run_bot()