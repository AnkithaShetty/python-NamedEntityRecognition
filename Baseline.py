def file_reader(file_path, list_lines ):
    print("Reading files into list of lines")
    file_stream = open(file_path, 'r')
    with file_stream as in_file:
        for lines in in_file:
            list_lines.append(lines.split())
    return list_lines


def word_dictionary_builder(list_lines):
    print(" Building word Dictionary for training data")
    word_dictionary = {}
    for i in range(0, len(list_lines) - 2, 3):
        word_tuple = list(zip(list_lines[i], list_lines[i + 1], list_lines[i + 2]))
        for word, pos, ner in word_tuple:
            if word in word_dictionary.keys():
                p, n, counter = word_dictionary[word]
                counter += 1
                word_dictionary[word] = (p, n, counter)
            else:
                word_dictionary[word] = (pos, ner, 0)
    return word_dictionary


def word_builder_for_test(test_lines, word_dictionary):
    print("Building list of tuples for test data")
    test_ner = []
    for i in range(0, len(test_lines) - 2, 3):
        word_tuple_test = list(zip(test_lines[i], test_lines[i + 1], test_lines[i + 2]))
        for word, pos, loc in word_tuple_test:
            if word in word_dictionary.keys():
                pos, ner, counter = word_dictionary[word]
                test_ner.extend([(word,ner,loc)])
    return test_ner


def main():
    file_path_train = "D:\PythonProjects\\NamedEntityRecognition\\trainingData\\train.txt"
    file_path_test = "D:\PythonProjects\\NamedEntityRecognition\\testData\\test.txt"

    list_lines_train = file_reader(file_path_train, [])
    word_dict_train = word_dictionary_builder(list_lines_train)

    list_lines_test = file_reader(file_path_test, [])
    word_tuples_test = word_builder_for_test(list_lines_test,word_dict_train)

    words_not_found = []
    ner_position_dict = {'ORG': [-1], 'MISC': [-1], 'PER': [-1], 'LOC': [-1]}

    for word, ner, loc in word_tuples_test:
        ner = ner[2:]
        if ner in ner_position_dict.keys():
            if ner_position_dict[ner]:
                ner_position_dict[ner].extend([loc])
        else:
            words_not_found.append(word)

    for key, val in ner_position_dict.items():
        integer_list_values = [int(v) for v in val]
        ner_position_dict[key] = sorted(integer_list_values)

    for k,v in ner_position_dict.items():
        ranges = sum((list(t) for t in zip(v, v[1:]) if t[0] + 1 != t[1]), [])
        iranges = iter(v[0:1] + ranges + v[-1:])
        ner_position_dict[k] = ' '.join([str(n) + '-' + str(next(iranges)) for n in iranges])

    import csv
    with open('namedEntityRecon.csv', 'w') as csvfile:
        header = ['Type', 'Prediction']
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for key, value in ner_position_dict.items():
            writer.writerow([key, value])


if __name__ == "__main__":
        main()

