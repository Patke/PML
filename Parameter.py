#Parameter fuer spamfilter.py
dir_separator="\\"
dir_root="."+dir_separator
dir_results="dir.filter.results"+dir_separator
dir_input="dir.mail.input"+dir_separator
dir_nospam="dir.nospam"+dir_separator
dir_spam="dir.spam"+dir_separator
dir_output="dir.mail.output"+dir_separator
dir_temp="dir.temp"+dir_separator
filename_blacklist="blacklist"
filename_whitelist="whitelist"
filename_results="spamfilter.results"
filename_logfile="spamfilter.log"
priorityorder=["whitelist", "blacklist", "naive_bayes"]
nb_spam_class="spam", "undetermined", "nospam"
nb_spam_level= 0.67               #nb_level greater_or_equal is spam
nb_nospam_level= 0.33             #nb_level loweror equal is nospam
                                 #in between is undetermined
char_replaces = {"\n": " ", "_": " ", ".": " ", "\t": " ", "[": " ", "]": " ", "  ": " ", ":": " ", ",": " ", "/": " ", "(": " ", ")": " ", ">": " ", "<": " ", ";": " "}
