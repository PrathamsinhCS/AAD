from flask import Flask, render_template, request

app = Flask(__name__)

class HuffmanNode:
    def __init__(self, symbol, frequency):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

def construct_huffman_tree(frequency_map):
    from heapq import heappush, heappop
    priority_queue = []
    for symbol, freq in frequency_map.items():
        heappush(priority_queue, HuffmanNode(symbol, freq))
    while len(priority_queue) > 1:
        node1 = heappop(priority_queue)
        node2 = heappop(priority_queue)
        combined = HuffmanNode(None, node1.frequency + node2.frequency)
        combined.left = node1
        combined.right = node2
        heappush(priority_queue, combined)
    return heappop(priority_queue)

def generate_huffman_codes(root, current_code="", mapping={}):
    if root is None:
        return
    if root.symbol is not None:
        mapping[root.symbol] = current_code
    generate_huffman_codes(root.left, current_code + "0", mapping)
    generate_huffman_codes(root.right, current_code + "1", mapping)
    return mapping

def huffman_encode(input_text, mapping):
    return ''.join(mapping[symbol] for symbol in input_text)

def huffman_decode(binary_code, root):
    result = ""
    node = root
    for bit in binary_code:
        node = node.left if bit == "0" else node.right
        if node.symbol:
            result += node.symbol
            node = root
    return result

@app.route('/process_huffman', methods=['POST'])
def process_huffman():
    symbol_frequency = {'A': 0.5, 'B': 0.35, 'C': 0.5, 'D': 0.1, 'E': 0.4, '-': 0.2}
    tree = construct_huffman_tree(symbol_frequency)
    mappings = generate_huffman_codes(tree)
    encode_input = request.form['text_to_encode']
    decode_input = request.form['text_to_decode']
    encoded = huffman_encode(encode_input, mappings)
    decoded = huffman_decode(decode_input, tree)
    return render_template('index.html', encoded_result=encoded, decoded_result=decoded, huffman_mappings=mappings)

if __name__ == '__main__':
    app.run(debug=True)
