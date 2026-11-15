from pathlib import Path
import os
import re

# Small fallback only, used if no external lexicon file is present.
FALLBACK_WORDS = """
AAH AB ABLE ABOUT ABOVE ACE ACID ACT ADD AGE AGENT AGILE AIR ALL ALSO AM
AN AND ANT ANY APPLE ARE ARM ART AS ASK AT ATE BAD BAG BAR BAT BAY BE BED
BEE BEEN BEER BIG BIT BITE BLACK BLUE BOAT BODY BOX BOY BOOK BOTH BOX
CAB CAD CAN CAP CAR CARE CAT CATS COT COW CUE CUT DAD DAY DEAR DECK DID
DIG DIM DIN DO DOG DOT DRY DUE EAR EARN EARTH EAT EEL EGG EGO ELK END
ERA ERR EVEN EWE EYE FAN FAR FAT FED FEE FEW FIG FIT FIX FLY FOR FOX FUN
GAP GAS GET GIN GOD GOT GUM GUN GUY HAD HAM HAS HAT HAY HEN HER HET HIM
HIP HIS HIT HOG HOT HOW HUE HUG I IAN ICE ICK IDEA ILL IN INK INN ION
JAB JAM JAR JAW JAY JET JIG JOG JOY JUG JUT KAY KEY KID KIN KIT
LAB LAD LAG LAP LAW LAY LED LEG LET LID LIE LIP LIT LOG LOT LOW LUG
MAD MAN MAP MAT MAY MEN MET MID MIX MOB MOD MOP MOW MUD MUG
NAG NAP NET NEW NIB NIL NIP NOD NOR NOT NOW NUN NUT
OAK OAR OAT ODD OFF OFT OIL OLD ONE OPT OR OUR OUT OVA OWE OWL OWN
PAD PAL PAN PAP PAR PAT PAW PAY PEA PEE PEG PEN PET PIE PIG PIN PIT
POD POP POT POW PRO PRY PUB PUG PUN PUP PUT
QUA QUE
RAG RAM RAN RAP RAT RAW RAY RED REF RIB RID RIG RIM RIP ROB ROD ROT ROW
RUB RUE RUG RUM RUN RUT
SAC SAD SAG SAP SAT SAW SAY SEA SEE SET SEW SHE SHY SIN SIP SIR SIT SIX
SKI SKY SLY SOB SOD SON SOP SOT SOW SOY SPA SPY SUB SUE SUM SUN SUP
TAB TAG TAN TAP TAR TAX TEA TED TEN THE TIE TIN TIP TOE TON TOO TOP
TOW TOY TRY TUB TUG TWO
USE VAN VAT VET VEX VIA VIE VOW
WAD WAG WAR WAS WAX WAY WEB WED WET WHO WHY WIN WIT WOK WON WOO WOW
YAK YAM YAP YAW YEA YEN YES YET YOU YOW
ZAG ZAP ZED ZEE ZEN ZIP ZIT ZOO
""".split()

class Dictionary:
    def __init__(self, words):
        cleaned = set()
        for item in words:
            # Handles one-word-per-line files and common whitespace-separated lists.
            tokens = re.findall(r"[A-Za-z]{2,}", str(item).upper())
            cleaned.update(tokens)
        self.words = cleaned

    @classmethod
    def from_file(cls, path):
        path = Path(path)
        text = path.read_text(encoding="utf-8-sig", errors="ignore")
        return cls(text.splitlines())

    def __contains__(self, word):
        return word.upper() in self.words

    def __iter__(self):
        return iter(self.words)

    def __len__(self):
        return len(self.words)

def find_wordlist():
    explicit = os.getenv("SCRABBLE_WORDLIST")
    if explicit and Path(explicit).is_file():
        return Path(explicit)
    data = Path("data")
    candidates = [data / "words.txt"]
    candidates += sorted(data.glob("*.txt"))
    for candidate in candidates:
        if candidate.is_file() and candidate.name.lower() not in {"readme.txt"}:
            return candidate
    return None

def load_dictionary():
    path = find_wordlist()
    if path:
        return Dictionary.from_file(path), str(path)
    return Dictionary(FALLBACK_WORDS), "built-in demo word list"
