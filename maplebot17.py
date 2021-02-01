import random, datetime, sys
from pprint import pprint
from ananas import PineappleBot, hourly, reply, html_strip_tags, daily, interval

class MapleBot(PineappleBot):

	def start(self):
		with open('maple_behaviors','r') as behaviors:
			self.behaviors = behaviors.read().split("\n")
		with open('maple_responses','r') as responses:
			self.responses = responses.read().split("\n")
		print("Hello!")
		self.recents = {}
		self.max_recents = 3

	@hourly(minute=14)
	def post_behavior(self):
		behavior = "-mom" # initialize
		while "-mom" in behavior: # exclude certain behaviors
			behavior = random.choice(self.behaviors)
		print("Scheduled behavior: {}".format(behavior))
		self.mastodon.status_post("*{}*".format(behavior))
		self.clear_recents()

	@daily(hour=10, minute=8)
	def post_snek(self):
		print("Good morning!")
		self.mastodon.status_post("*goes around the house kissing everyone good morning*")
		self.clear_recents()

	@reply
	def post_response(self, mention, user):
		msg = html_strip_tags(mention["content"])
		rsp = random.choice(self.responses)
		tgt = user["acct"]
		if tgt in ["noelle@elekk.xyz","lamia@elekk.xyz"] and rsp.find("rides") >= 0:
  			rsp = rsp.replace(r"foot","tail")
		if tgt in ["noelle@elekk.xyz","lamia@elekk.xyz"] and rsp.find("leg") >= 0:
			rsp = rsp.replace(r"leg", "tail")
		irt = mention["id"]
		vis = mention["visibility"]
		print("Received toot from {}: {}".format(tgt, msg))
		try:
			tgt_rec = self.recents[tgt]
		except KeyError:
			tgt_rec = 0
		if "mom?" in msg or "moms?" in msg:
			self.mastodon.status_post("{} *holds up a picture of @noelle@elekk.xyz".format(tgt), in_reply_to_id = irt, visibility = vis)
		else:
			if tgt_rec < self.max_recents or vis == 'direct':
				print("Responding with {} visibility: {}".format(vis, rsp))
				self.mastodon.status_post("@{} *{}*".format(tgt, rsp),
									  in_reply_to_id = irt,
									  visibility = vis)
				if vis != 'direct':
					self.recents[tgt] = tgt_rec + 1
					print("self.recents updated: ", end="")
					pprint(self.recents)
			else:
				print("...but I've responded to {} too recently.".format(tgt))

	@interval(60)
	def clear_recents(self):
		import copy
		if len(self.recents.keys()) >= 1:
			try:
				self.recents = {}
				# ky = self.recents.keys()
				# for k in ky:
				# 	new_v = self.recents[k] - 1
				# 	if new_v == 0:
				# 		del self.recents[k]
				# 	else:
				# 		self.recents[k] = new_v
				# print("self.recents updated: ", end="")
				# pprint(self.recents)
			except:
				print(f"I ran into an error trying to clear self.recents: {str(sys.exc_info()[0])}")

