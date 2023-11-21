import tree
import voice

root = tree.build_tree()


def sort(array):
    if len(array) <= 1:
        return array

    mid = len(array) // 2
    left = sort(array[:mid])
    right = sort(array[mid:])

    return_array = []
    left_index = 0
    right_index = 0
    while left_index < len(left) and right_index < len(right):
        if tree.NODE_WORDS[left[left_index]] < tree.NODE_WORDS[right[right_index]]:
            return_array.append(left[left_index])
            left_index += 1
        else:
            return_array.append(right[right_index])
            right_index += 1

    return_array += right[right_index:]
    return_array += left[left_index:]

    return return_array


def create_input(query):
    raw_words = query.split()
    sanitized_words = []
    for word in raw_words:
        if "'" in word:
            word = word[: word.index("'")]
        if word in tree.NODE_WORDS.keys():
            sanitized_words.append(word)
    response = tree.process_input(root, sort(sanitized_words))
    if response == "Exit Code 0":
        voice.speak("Goodbye " + voice.title)
        exit()
    else:
        voice.speak(response)


voice.speak("Hello " + voice.title)
while True:
    create_input(voice.takeCommand())
