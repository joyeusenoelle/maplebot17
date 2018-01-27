import random
from ananas import PineappleBot, hourly, reply, html_strip_tags, daily

class MapleBot(PineappleBot):

	def start(self):
		with open('maple_behaviors','r') as behaviors:
			self.behaviors = behaviors.read().split("\n")
		with open('maple_responses','r') as responses:
			self.responses = responses.read().split("\n")
		print("Hello!")

	@hourly(minute=12)
	@hourly(minute=47)
	def post_behavior(self):
		behavior = random.choice(self.behaviors)
		print("Scheduled behavior: {}".format(behavior))
		self.mastodon.status_post("*{}*".format(behavior))

	@daily(hour=15, minute=12)
	def post_maple(self):
		print("Good morning Maple")
		self.mastodon.status_post("@squirrel@computerfairi.es *kisses Maple-mom good morning")

	@reply
	def post_response(self, mention, user):
		msg = html_strip_tags(mention["content"])
		rsp = random.choice(self.responses)
		tgt = user["acct"]
		irt = mention["id"]
		vis = mention["visibility"]
		print("Received toot from {}: {}".format(tgt, msg))
		print("Responding with {} visibility: {}".format(vis, rsp))
		self.mastodon.status_post("@{} *{}*".format(tgt, rsp),
								  in_reply_to_id = irt,
								  visibility = vis)