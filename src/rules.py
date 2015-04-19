VERBS = ["MD", "VB", "VBZ", "VBZhas", "VBZis", "VBD", "VBG", "VBN", "VBP"]

PAST    = ["VBD", "VBN", "VBZhas"]
PRESENT = ["VBZ", "VBP", "VBZis"]
FUTURE  = ["VBG"]

VERB_BIGRAM_RULES = [
	"VBD,VBG",
	"VBD,VBP",
	"MD,VBZis",
	"MD,VBZhas",
	"MD,VBD",
	"MD,VBN",
	"MD,VBG",
	"MD,VBP",
	"VBP,VBP",
	"MD,MD",
	"MD,VBZis",
	"MD,VBZhas",
	"VB,MD",
	"VB,VBZis",
	"VB,VBZhas",
	"VBD,MD",
	"VBZis,MD",
	"VBZhas,MD",
	"VBP,MD",
	"VBN,MD",
	"VBN,JJ",
	"VBZ,VB",
	"VBZis,VBZis",
	"VBZis,VB",
	"VBZis,VBP",
	"VBZis,VBD",
	"VBZhas,VBZhas",
	"VBZhas,VBZis",
	"VBZhas,VB",
	"VBZhas,VBP",
	"VBZhas,VBD",
	"VBZhas,VBG",
	"WDT,VBN"
]

VERB_TRIGRAM_RULES = [
	"MD,VB,VBD",
	"MD,VB,VBG",
	"MD,VB,VBP",
	"MD,VB,VBZ",
	"MD,VB,VB",
	"MD,VB,VBZis",
	"MD,VB,VBZhas",
	"MD,VBZhas,VBN",
	"MD,VBZhas,VB",
	"MD,VBZhas,VBD",
	"MD,VBZhas,VBN",
	"MD,VBZhas,VBP",
	"MD,VBZhas,VBZhas",
	"MD,VBZis,VBN",
	"MD,VBZis,VB",
	"MD,VBZis,VBD",
	"MD,VBZis,VBN",
	"MD,VBZis,VBP",
	"MD,VBZis,VBZis",
	"MD,VBN,VBN",
	"MD,VBN,VB",
	"MD,VBN,VBD",
	"MD,VBN,VBN",
	"MD,VBN,VBP",
	"MD,VBN,VBZis",
	"MD,VBN,VBZhas"
]

FUTURE_INDICATORS = [
	"will",
	"might",
	"may"
]

PAST_INDICATORS = [
	"was",
	"were"
]