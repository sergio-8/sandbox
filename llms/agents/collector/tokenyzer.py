import transformers
import warnings
warnings.filterwarnings('ignore')

from transformers import AutoTokenizer

sentence = "not sure what to write here but here we go"

tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

token_ids = tokenizer(sentence).input_ids

print(token_ids)

for id in token_ids:
    print(tokenizer.decode(id))


# A list of colors in RGB for representing the tokens
colors = [
    '102;194;165', '252;141;98', '141;160;203',
    '231;138;195', '166;216;84', '255;217;47'
]

def show_tokens(sentence: str, tokenizer_name: str):
    """ Show the tokens each separated by a different color """

    # Load the tokenizer and tokenize the input
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    token_ids = tokenizer(sentence).input_ids

    # Extract vocabulary length
    print(f"Vocab length: {len(tokenizer)}")

    # Print a colored list of tokens
    for idx, t in enumerate(token_ids):
        print(
            f'\x1b[0;30;48;2;{colors[idx % len(colors)]}m' +
            tokenizer.decode(t) +
            '\x1b[0m',
            end=' '
        )


text = """
English and CAPITALIZATION
🎵 鸟
show_tokens False None elif == >= else: two tabs:"    " Three tabs: "       "
12.0*50=600
"""

show_tokens(text, "bert-base-cased")

#show_tokens(text, "bert-base-uncased")

show_tokens(text, "Xenova/gpt-4")