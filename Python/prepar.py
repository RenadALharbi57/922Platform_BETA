
import emoji  # Import the emoji library
import re  # Import regular expression module for text processing
from nltk.tokenize import word_tokenize  # Import word tokenizer from NLTK
from nltk.corpus import stopwords  # Import stopwords from NLTK
from pandas import DataFrame  # Import DataFrame from pandas for handling data
from nltk.stem import ISRIStemmer  # Import stemmer from NLTK for Arabic text normalization
from nltk.stem import SnowballStemmer  # Import Snowball stemmer from NLTK
import pandas as pd # Import pandas for data manipulation
import nltk
nltk.download('punkt')
nltk.download('stopwords')



# تعريف دالة normalize لتوحيد النصوص العربية
def normalize(Ticket):
    Ticket = re.sub("[إأٱآا]", "ا", Ticket)
    Ticket = re.sub("ى", "ي", Ticket)
    Ticket = re.sub("_", " ", Ticket)
    Ticket = re.sub("#", " ", Ticket)
    Ticket = re.sub("ؤ", "و", Ticket)
    Ticket = re.sub("ة", "ه", Ticket)
    noise = re.compile(""" ّ    | # Tashdid
                            َ    | # Fatha
                            ً    | # Tanwin Fath
                            ُ    | # Damma
                            ٌ    | # Tanwin Damm
                            ِ    | # Kasra
                            ٍ    | # Tanwin Kasr
                            ْ    | # Sukun
                            ـ     # Tatwil/Kashida
                        """, re.VERBOSE)
    Ticket = re.sub(noise, '', Ticket)
    return Ticket

# إزالة الكلمات التوقف (Stopwords)
def stopwordremoval(Ticket):
    stop = stopwords.words("arabic")
    needed_words = []
    words = word_tokenize(Ticket)
    for w in words:
        if len(w) >= 2 and w not in stop:
            needed_words.append(w)
    filterd_sent = " ".join(needed_words)
    return filterd_sent

# إزالة الرموز التعبيرية
def give_emoji_free_Ticket(Ticket):
    Ticket_with_emojis_converted = emoji.demojize(Ticket)
    clean_Ticket = re.sub(r':[a-zA-Z_]+:', '', Ticket_with_emojis_converted)
    return clean_Ticket

# إزالة الأحرف غير العربية
def removenonarabic(Ticket):
    cleaned_Ticket = re.sub(r'[^\u0600-\u06FF\s]', '', Ticket)
    return cleaned_Ticket.strip()

# إزالة الرموز والأرقام
def remove_symbols(Ticket):
    cleaned_Ticket = re.sub(r'[^\w\s\u0600-\u06FF]', '', Ticket)
    cleaned_Ticket = re.sub(r'[٪،?%,٠١٢٣٤٥٦٧٨٩؟]', '', cleaned_Ticket)
    return cleaned_Ticket.strip()

# إزالة التكرارات
def remove_repeating_char(Ticket):
    cleaned_Ticket = re.sub(r'\b(\w+)\s+\1\b', r'\1', Ticket)
    return re.sub(r'(.)\1{2,}', r'\1\1', cleaned_Ticket)

def remove_spaces_arabic(Ticket):
    # Define a regular expression pattern to match spaces in Arabic text
    pattern = r'\s+'
    
    cleaned_Ticket = re.sub(pattern, ' ', Ticket)
    return cleaned_Ticket

def remove_numbers(Ticket):
    cleaned_Ticket = re.sub(r'\d+', '', Ticket)
    return cleaned_Ticket
