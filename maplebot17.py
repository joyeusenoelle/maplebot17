import random
import datetime
from ananas import PineappleBot, hourly, reply, html_strip_tags, daily, interval

class MapleBot(PineappleBot):

	def start(self):
		with open('maple_behaviors','r') as behaviors:
			self.behaviors = behaviors.read().split("\n")
		with open('maple_responses','r') as responses:
			self.responses = responses.read().split("\n")
		print("Hello!")
		self.recents = []

	@hourly(minute=12)
	def post_behavior(self):
		behavior = random.choice(self.behaviors)
		print("Scheduled behavior: {}".format(behavior))
		self.mastodon.status_post("*{}*".format(behavior))
		self.clear_recents()

	@daily(hour=13, minute=16)
	def post_maple(self):
		print("Good morning Maple")
		self.mastodon.status_post("@squirrel@computerfairi.es *kisses Maple-mom good morning*")
		self.clear_recents()

	@daily(hour=17, minute=21)
	def post_birb(self):
		print("Good morning Laser")
		self.mastodon.status_post("@laserscheme@computerfairi.es *kisses Bird-mom good morning*")
		self.clear_recents()

	@daily(hour=7, minute=8)
	def post_snek(self):
		print("Good morning Ellie")
		self.mastodon.status_post("@noelle@elekk.xyz *kisses Snake-mom good morning*")
		self.clear_recents()

	@reply
	def post_response(self, mention, user):
		msg = html_strip_tags(mention["content"])
		rsp = random.choice(self.responses)
		tgt = user["acct"]
		irt = mention["id"]
		vis = mention["visibility"]
		print("Received toot from {}: {}".format(tgt, msg))
		if tgt not in self.recents or vis == 'direct':
			print("Responding with {} visibility: {}".format(vis, rsp))
			self.mastodon.status_post("@{} *{}*".format(tgt, rsp),
								  in_reply_to_id = irt,
								  visibility = vis)
			if vis != 'direct':
				self.recents.append(tgt)
				print("self.recents updated. Now [{}].".format(", ".join(self.recents)))
		else:
			print("...but I've responded to {} too recently.".format(tgt))

	@interval(180)
	def clear_recents(self):
		try:
			old_recents = []
			for item in self.recents:
				old_recents.append(item)
			self.recents = []
			if self.recents != old_recents:
				print("self.recents cleared. Now [{}].".format(", ".join(self.recents)))
			else:
				#print("self.recents was empty, so I don't have to clear it.")
				pass
		except:
			print("I ran into an error trying to clear self.recents.")

