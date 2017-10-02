def file_reader(file_path, list_lines ):
    print("Reading file into list of lines")
    file_stream = open(file_path, 'r')
    with file_stream as in_file:
        for lines in in_file:
            list_lines.append(lines.split())
    return list_lines


def word_dictionary_builder(list_lines, data):
    print(" Building word Dictionary for " + data + " data")
    word_dictionary = {}
    for i in range(0, len(list_lines) - 2, 3):
        word_tuple = list(zip(list_lines[i], list_lines[i + 1], list_lines[i + 2]))
        for word, pos, ner in word_tuple:
           word_dictionary[word] = (pos, ner)
    return word_dictionary

def main():
    file_path_train = "D:\PythonProjects\\NamedEntityRecognition\\trainingData\\train.txt"
    file_path_test = "D:\PythonProjects\\NamedEntityRecognition\\testData\\test.txt"

    list_lines_train = file_reader(file_path_train, [])
    word_dict_train = word_dictionary_builder(list_lines_train, "Training")

    list_lines_test = file_reader(file_path_test, [])
    word_dict_test = word_dictionary_builder(list_lines_test, "Test")
    #print(list_lines_test)
    print(word_dict_train.keys())
    print(word_dict_test.keys())
    keys_not_found = []
    ner_position_dict = {'ORG':[-1], 'MISC':[-1], 'PER':[-1], 'LOC':[-1]}
    for key in word_dict_test.keys():
        if key in word_dict_train.keys():
            pos1, ner = word_dict_train[key]
            pos2, location = word_dict_test[key]
            ner = ner[2:]
            if ner in ner_position_dict.keys():
                if ner_position_dict[ner]:
                    ner_position_dict[ner].extend([location])
        else:
            keys_not_found.append(key)
    print(len(keys_not_found))

    for key, val in ner_position_dict.items():
        integer_list_values = [int(v) for v in val]
        ner_position_dict[key] =sorted(integer_list_values)

    for k,v in ner_position_dict.items():
        ranges = sum((list(t) for t in zip(v, v[1:]) if t[0] + 1 != t[1]), [])
        iranges = iter(v[0:1] + ranges + v[-1:])
        ner_position_dict[k] = ' '.join([str(n) + '-' + str(next(iranges)) for n in iranges])

    #print(ner_position_dict)
    import csv
    with open('namedEntityRecon.csv', 'w') as csvfile:
        header = ['Type', 'Prediction']
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for key, value in ner_position_dict.items():
            writer.writerow([key, value])


if __name__ == "__main__":
        main()

#2831
#3026