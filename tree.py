from node import *

NODE_WORDS = {}


def get(key, data):
    index = data.index(key) + len(key) + 1
    value = data[index : index + data[index:].index("$")]
    if key == "connections":
        value = value.split(", ")
    return None if (value == "_" or value == ["_"]) else value


def create_node(chunks, node_key):
    data = chunks[node_key]
    if data["connections"] == None:
        return Node(data["words"], data["response"], None)

    connections = []
    for x in data["connections"]:
        connections.append(create_node(chunks, x))
    return Node(data["words"], data["response"], connections)


def build_tree():
    with open("Dependencies/Tree.txt", "r") as f:
        data = f.read()
        chunks = {}
        while data != "":
            block = {}
            start_index = data.index("[") + 1
            end_index = data.index("]")

            key = get("node", data[start_index:end_index])
            block["response"] = get("response", data[start_index:end_index])
            block["words"] = get("words", data[start_index:end_index])
            block["connections"] = get("connections", data[start_index:end_index])

            priority = get("priority", data[start_index:end_index])
            for word in block["words"].split():
                NODE_WORDS[word] = priority
            data = data[end_index + 1 :]
            chunks[key] = block
    return create_node(chunks, "root")


def process_input(root, input):
    for word in input:
        for element in root.get_connections().keys():
            if word in element:
                root = root.get_connections()[element]
    return root.get_response()
